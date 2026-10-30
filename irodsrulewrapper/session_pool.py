"""Exclusive, worker-local borrowing of authenticated iRODS sessions."""

import atexit
import logging
import os
import threading
import time
import weakref
from collections import OrderedDict

from irods.api_number import api_number
from irods.message import iRODSMessage

logger = logging.getLogger(__name__)
_pools = weakref.WeakSet()


def _disconnect(connection, local_only=False):
    # Keep the socket reference: PRC clears it even when disconnect() fails.
    sock = connection.socket
    try:
        if not local_only:
            connection.disconnect()
    except Exception:
        logger.exception("Failed to disconnect a pooled iRODS connection")
    finally:
        try:
            if sock is not None:
                sock.close()
        except Exception:
            logger.exception("Failed to close a pooled iRODS socket")
        connection.socket = None
        connection._disconnected = True


class _SessionEntry:
    def __init__(self, key, session):
        self.key = key
        self.session = session
        self.client_pool = session.pool
        self.timeout = session.connection_timeout
        self.num_threads = session.numThreads
        self.discarded_connections = set()
        self.broken = False
        self.closed = False
        self.idle_since = None
        self.original_release = self.client_pool.release_connection

        def release_connection(connection, destroy=False):
            # PRC can report transport failure here even when a view catches it.
            if destroy:
                self.broken = True
                self.discarded_connections.add(connection)
            return self.original_release(connection, destroy)

        self.client_pool.release_connection = release_connection

    def reusable(self):
        session = self.session
        return (
            not self.broken
            and session.pool is self.client_pool
            and not self.client_pool.active
            and bool(self.client_pool.idle)
            and session.connection_timeout == self.timeout
            and session.numThreads == self.num_threads
            and not session.ticket__
            and not session.ticket_applied
            and all(
                connection.socket is not None
                and connection.socket.fileno() >= 0
                and not connection._disconnected
                for connection in self.client_pool.idle
            )
        )

    def trim_connections(self):
        pool = self.client_pool
        keep = pool._conn if pool._conn in pool.idle else next(iter(pool.idle))
        for connection in pool.idle - {keep}:
            _disconnect(connection)
            self.original_release(connection, destroy=True)

    def close(self, local_only=False):
        if self.closed:
            return
        self.closed = True
        # cleanup() normally reconfigures the PRC session. Retired sessions
        # must stay retired, and one failed disconnect must not skip the rest.
        self.session.do_configure = {}
        pools = {self.client_pool, self.session.pool}
        for pool in pools:
            for connection in pool.active | pool.idle | self.discarded_connections:
                _disconnect(connection, local_only=local_only)
            pool.active.clear()
            pool.idle.clear()
            pool._conn = None
        self.discarded_connections.clear()
        self.client_pool.release_connection = self.original_release
        if not local_only:
            try:
                self.session.cleanup()
            except Exception:
                logger.exception("Failed to clean up a pooled iRODS session")


class IRODSSessionPool:
    """Bound idle sessions, never lend a session to two scopes at once.

    Active requests do not wait for capacity. Only idle sessions count toward
    max_idle; surplus sessions are closed on return. Expiry is activity-driven.
    """

    def __init__(self, max_idle=32, idle_timeout=60):
        if max_idle < 0 or idle_timeout <= 0:
            raise ValueError("Invalid iRODS session pool limits")
        self.max_idle = max_idle
        self.idle_timeout = idle_timeout
        self._pid = os.getpid()
        self._lock = threading.Lock()
        self._entries = {}
        self._idle = OrderedDict()
        self._closed = False
        _pools.add(self)

    def _ensure_process(self):
        if self._pid != os.getpid():
            entries = list(self._entries.values())
            # Never acquire an inherited lock, or send a disconnect through a
            # socket that is still in use by the parent process.
            self._lock = threading.Lock()
            self._entries = {}
            self._idle = OrderedDict()
            self._pid = os.getpid()
            for entry in entries:
                entry.close(local_only=True)

    def _expire(self):
        """Remove expired entries under the bookkeeping lock."""
        expired = []
        now = time.monotonic()
        while self._idle:
            session, entry = next(iter(self._idle.items()))
            if now - entry.idle_since < self.idle_timeout:
                break
            self._idle.pop(session)
            self._entries.pop(session)
            expired.append(entry)
        return expired

    def _discard(self, entry):
        with self._lock:
            self._entries.pop(entry.session, None)
            self._idle.pop(entry.session, None)
        entry.close()

    def _prepare(self, entry, check_connection):
        try:
            # Also primes PRC's thread/greenlet-local connection reference,
            # avoiding an extra checkout in its data-object version lookup.
            with entry.client_pool.get_connection() as connection:
                if check_connection:
                    connection.send(iRODSMessage("RODS_API_REQ", int_info=api_number["GET_MISC_SVR_INFO_AN"]))
                    connection.recv()
            with self._lock:
                if self._closed:
                    raise RuntimeError("The iRODS session pool is closed")
        except BaseException:
            self._discard(entry)
            raise
        return entry.session

    def borrow(self, key, session_factory):
        """Borrow by the complete identity/settings key; never log that key."""
        self._ensure_process()
        entry = None
        with self._lock:
            if self._closed:
                raise RuntimeError("The iRODS session pool is closed")
            expired = self._expire()
            for session, candidate in reversed(self._idle.items()):
                if candidate.key == key:
                    entry = self._idle.pop(session)
                    break
        for old_entry in expired:
            old_entry.close()
        if entry is not None:
            try:
                return self._prepare(entry, check_connection=True)
            except Exception:
                # Only the read-only preflight failed. Application operations
                # have not begun, so one fresh authenticated session is safe.
                pass
        with self._lock:
            if self._closed:
                raise RuntimeError("The iRODS session pool is closed")
        entry = _SessionEntry(key, session_factory())
        with self._lock:
            self._entries[entry.session] = entry
        return self._prepare(entry, check_connection=False)

    def release(self, session, discard=False):
        """Return a lease, retaining only clean sessions with no open handles."""
        self._ensure_process()
        with self._lock:
            entry = self._entries.get(session)
            if entry is None or session in self._idle:
                return
        try:
            reusable = not discard and entry.reusable()
            if reusable:
                entry.trim_connections()
        except BaseException:
            self._discard(entry)
            raise
        with self._lock:
            retired = self._expire()
            if reusable and not self._closed:
                entry.idle_since = time.monotonic()
                self._idle[session] = entry
            else:
                self._entries.pop(session)
                retired.append(entry)
            while len(self._idle) > self.max_idle:
                old_session, old_entry = self._idle.popitem(last=False)
                self._entries.pop(old_session)
                retired.append(old_entry)
        for old_entry in retired:
            old_entry.close()

    def close(self):
        """Close idle sessions now; outstanding leases close when returned."""
        self._ensure_process()
        with self._lock:
            self._closed = True
            idle = list(self._idle.values())
            self._idle.clear()
            for entry in idle:
                self._entries.pop(entry.session)
        for entry in idle:
            entry.close()


_worker_pool = None
_worker_pid = os.getpid()
_worker_lock = threading.Lock()


def get_irods_session_pool():
    """Create the HTTP pool lazily, after worker startup and gevent patching."""
    global _worker_pool, _worker_pid, _worker_lock
    if _worker_pid != os.getpid():
        _worker_lock = threading.Lock()
        _worker_pid = os.getpid()
    with _worker_lock:
        if _worker_pool is None:
            _worker_pool = IRODSSessionPool()
        pool = _worker_pool
    pool._ensure_process()
    return pool


def close_irods_session_pool():
    """Release this worker's retained HTTP sessions, if initialized."""
    if _worker_pool is not None:
        _worker_pool.close()


def _after_fork():
    global _worker_pid, _worker_lock
    _worker_pid = os.getpid()
    _worker_lock = threading.Lock()
    for pool in list(_pools):
        pool._ensure_process()


os.register_at_fork(after_in_child=_after_fork)
atexit.register(close_irods_session_pool)
