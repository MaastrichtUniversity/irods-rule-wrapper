"""Pool tests using PRC's real session/pool lifecycle and a fake transport."""

import os
from pathlib import Path
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from irods.connection import Connection
from irods.exception import NetworkException
from irods.pool import Pool as ClientPool
from irods.session import iRODSSession

from irodsrulewrapper import session_pool, utils
from irodsrulewrapper.rule import RuleManager
from irodsrulewrapper.session_pool import IRODSSessionPool


class FakeSocket:
    def __init__(self, timeout):
        self.timeout = timeout
        self.closed = False
        self.sent = []
        self.send_error = None

    def sendall(self, data):
        if self.send_error:
            raise self.send_error
        self.sent.append(data)

    def fileno(self):
        return -1 if self.closed else 42

    def close(self):
        self.closed = True

    def shutdown(self, how):
        pass

    def gettimeout(self):
        return self.timeout

    def settimeout(self, timeout):
        self.timeout = timeout


class FakeConnection(Connection):
    def __init__(self, pool, account):
        self.pool = pool
        self.account = account
        self.socket = FakeSocket(pool.connection_timeout)
        self._disconnected = False
        self._server_version = SimpleNamespace(relVersion="rods4.3.4")
        self.recv_error = None

    def recv(self, **kwargs):
        if self.recv_error:
            self.release(True)
            raise self.recv_error
        return SimpleNamespace(int_info=0)


class SessionPoolTests(unittest.TestCase):
    def setUp(self):
        env = {
            "IRODS_HOST": "example.invalid",
            "IRODS_USER": "proxy",
            "IRODS_PASS": "test-password",
            "IRODS_CLIENT_SERVER_POLICY": "CS_NEG_REQUIRE",
        }
        self.enterContext(patch.dict(os.environ, env))
        self.connect = self.enterContext(patch("irods.pool.Connection", side_effect=FakeConnection))
        self.sessions = []

        def make_session(**settings):
            session = iRODSSession(**settings)
            session.cleanup = Mock(wraps=session.cleanup)
            self.sessions.append(session)
            return session

        self.factory = self.enterContext(patch.object(utils, "iRODSSession", side_effect=make_session))
        self.pool = IRODSSessionPool()
        self.addCleanup(self.pool.close)

    def borrow(self, user="alice", **kwargs):
        with utils.irods_session_scope(pool=self.pool):
            return utils.BaseRuleManager(user, **kwargs).session

    def test_reuses_session_within_and_between_scopes(self):
        with utils.irods_session_scope(pool=self.pool):
            manager = utils.BaseRuleManager("alice")
            session = manager.session
            self.assertIs(session, utils.BaseRuleManager(SimpleNamespace(username="alice")).session)
            manager.cleanup()
            session.cleanup.assert_not_called()
        self.assertIs(self.borrow(), session)
        self.assertEqual(self.connect.call_count, 1)
        self.assertEqual(len(session.pool.idle), 1)
        self.assertFalse(session.pool.active)
        connection = next(iter(session.pool.idle))
        self.assertEqual(len(connection.socket.sent), 1)  # Read-only preflight.

    def test_isolates_users_admin_and_proxy_credentials(self):
        alice = self.borrow()
        self.assertIsNot(alice, self.borrow("bob"))
        self.assertIsNot(alice, self.borrow(admin_mode=True))
        # Even the admin's own name in normal mode is a separate identity.
        self.assertIsNot(self.borrow("proxy"), self.borrow(admin_mode=True))
        for name, value in [("IRODS_USER", "other-proxy"), ("IRODS_PASS", "other-password")]:
            with self.subTest(setting=name), patch.dict(os.environ, {name: value}):
                self.assertIsNot(alice, self.borrow())
        self.assertIs(alice, self.borrow())

    def test_isolates_connection_and_tls_settings(self):
        session = self.borrow()
        for name, value in [("IRODS_HOST", "other.invalid"), ("IRODS_CLIENT_SERVER_POLICY", "CS_NEG_REFUSE")]:
            with self.subTest(setting=name), patch.dict(os.environ, {name: value}):
                self.assertIsNot(session, self.borrow())
        for name, value in [
            ("irods_encryption_key_size", 16), ("ssl_context", object()), ("port", 1248), ("zone", "other-zone")
        ]:
            settings = dict(utils.BaseRuleManager.ssl_settings, **{name: value})
            with self.subTest(setting=name), patch.object(utils.BaseRuleManager, "ssl_settings", settings):
                self.assertIsNot(session, self.borrow())
        config = {"IRODS_HOST": "configured.invalid", "IRODS_USER": "proxy", "IRODS_PASS": "test-password"}
        self.assertIsNot(session, self.borrow(config=config))

    def test_standalone_and_unpooled_scopes_keep_ownership(self):
        manager = utils.BaseRuleManager("alice")
        manager.cleanup()
        manager.session.cleanup.assert_called_once()
        with utils.irods_session_scope():
            first = utils.BaseRuleManager("alice")
            self.assertIs(first.session, utils.BaseRuleManager("alice").session)
            first.cleanup()
            first.session.cleanup.assert_not_called()
        first.session.cleanup.assert_called_once()
        with utils.irods_session_scope():
            self.assertIsNot(first.session, utils.BaseRuleManager("alice").session)

    def test_nested_scopes_have_independent_leases_and_restore_context(self):
        with utils.irods_session_scope(pool=self.pool):
            outer = utils.BaseRuleManager("alice").session
            with utils.irods_session_scope(pool=self.pool):
                inner = utils.BaseRuleManager("alice").session
                self.assertIsNot(inner, outer)
            with utils.irods_session_scope():
                unpooled = utils.BaseRuleManager("alice").session
                self.assertIsNot(unpooled, outer)
            unpooled.cleanup.assert_called_once()
            self.assertIs(outer, utils.BaseRuleManager("alice").session)
        self.assertIsNone(utils._session_scope.get())
        self.assertIsNone(utils._scope_pool.get())

    def test_concurrent_requests_have_exclusive_leases_without_waiting(self):
        self.pool.max_idle = 1
        warm = self.borrow()
        barrier = threading.Barrier(3, timeout=5)
        finished = threading.Event()

        def request():
            with utils.irods_session_scope(pool=self.pool):
                session = utils.BaseRuleManager("alice").session
                barrier.wait()
                self.assertTrue(finished.wait(5))
                self.assertIs(session, utils.BaseRuleManager("alice").session)
                return session

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(request) for _ in range(2)]
            try:
                barrier.wait()
                self.assertEqual(self.connect.call_count, 2)
            finally:
                finished.set()
            sessions = [future.result(timeout=5) for future in futures]
        self.assertIsNot(sessions[0], sessions[1])
        self.assertIn(warm, sessions)
        self.assertEqual(sum(session.cleanup.call_count for session in sessions), 1)

    def test_checkout_primes_client_state_in_another_thread(self):
        session = self.borrow()

        def request():
            with utils.irods_session_scope(pool=self.pool):
                borrowed = utils.BaseRuleManager("alice").session
                self.assertIs(borrowed.pool._conn, next(iter(borrowed.pool.idle)))
                self.assertEqual(borrowed.data_objects.server_version, (4, 3, 4))
                self.assertFalse(borrowed.pool.active)
                return borrowed

        with ThreadPoolExecutor(max_workers=1) as executor:
            self.assertIs(executor.submit(request).result(timeout=5), session)
        self.assertEqual(self.connect.call_count, 1)

    def test_gevent_requests_have_independent_scopes(self):
        code = """
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.event import Event
from test_session_pool import SessionPoolTests, utils
case = SessionPoolTests()
case.setUp()
sessions = []
ready = Event()
def request():
    with utils.irods_session_scope(pool=case.pool):
        session = utils.BaseRuleManager('alice').session
        sessions.append(session)
        if len(sessions) == 2:
            ready.set()
        assert ready.wait(timeout=3)
        gevent.sleep(0)
        assert utils.BaseRuleManager('alice').session is session
        assert session.pool._conn in session.pool.idle
try:
    jobs = [gevent.spawn(request) for _ in range(2)]
    gevent.joinall(jobs, timeout=5, raise_error=True)
    assert all(job.ready() for job in jobs)
    assert len(sessions) == 2 and sessions[0] is not sessions[1]
    assert case.connect.call_count == 2
finally:
    case.doCleanups()
"""
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=Path(__file__).parent, capture_output=True, text=True, timeout=15
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_idle_expiry_uses_return_time_and_expires_at_boundary(self):
        with patch.object(session_pool.time, "monotonic", return_value=0):
            first = self.borrow()
        with patch.object(session_pool.time, "monotonic", return_value=59):
            self.assertIs(self.borrow(), first)
        with patch.object(session_pool.time, "monotonic", return_value=118):
            self.assertIs(self.borrow(), first)
        with patch.object(session_pool.time, "monotonic", return_value=178):
            self.assertIsNot(self.borrow(), first)
        first.cleanup.assert_called_once()

    def test_expiry_sweeps_other_identities_on_borrow_and_return(self):
        with patch.object(session_pool.time, "monotonic", return_value=0):
            old = self.borrow()
        with patch.object(session_pool.time, "monotonic", return_value=60):
            self.borrow("bob")
        old.cleanup.assert_called_once()
        with patch.object(session_pool.time, "monotonic", return_value=61) as clock:
            with utils.irods_session_scope(pool=self.pool):
                utils.BaseRuleManager("carol")
                clock.return_value = 121
        self.sessions[1].cleanup.assert_called_once()

    def test_eviction_is_global_and_least_recently_used(self):
        self.pool.max_idle = 2
        alice = self.borrow()
        bob = self.borrow("bob")
        self.assertIs(self.borrow(), alice)
        carol = self.borrow("carol")
        bob.cleanup.assert_called_once()
        alice.cleanup.assert_not_called()
        carol.cleanup.assert_not_called()
        self.assertIs(self.borrow(), alice)

    def test_zero_capacity_closes_every_returned_session(self):
        self.pool.max_idle = 0
        first = self.borrow()
        self.assertIsNot(self.borrow(), first)
        first.cleanup.assert_called_once()

    def test_surplus_client_connections_are_closed_without_poisoning_session(self):
        with utils.irods_session_scope(pool=self.pool):
            session = utils.BaseRuleManager("alice").session
            first = session.pool.get_connection()
            second = session.pool.get_connection()
            first.release()
            second.release()
        self.assertEqual(len(session.pool.idle), 1)
        self.assertIs(session.pool._conn, second)
        self.assertTrue(first._disconnected)
        self.assertIs(self.borrow(), session)

    def test_broken_health_check_replaces_session_before_application_work(self):
        session = self.borrow()
        connection = next(iter(session.pool.idle))
        sock = connection.socket
        connection.recv_error = NetworkException("stale connection")
        replacement = self.borrow()
        self.assertIsNot(replacement, session)
        self.assertEqual(self.connect.call_count, 2)
        session.cleanup.assert_called_once()
        self.assertTrue(sock.closed)

    def test_failed_replacement_authentication_propagates_and_is_cleaned_up(self):
        session = self.borrow()
        next(iter(session.pool.idle)).recv_error = NetworkException("stale connection")
        self.connect.side_effect = NetworkException("authentication failed")
        with self.assertRaisesRegex(NetworkException, "authentication failed"):
            self.borrow()
        self.assertEqual(self.connect.call_count, 2)
        for created in self.sessions:
            created.cleanup.assert_called_once()

    def test_fresh_authentication_failure_does_not_retry(self):
        self.connect.side_effect = NetworkException("authentication failed")
        with self.assertRaises(NetworkException):
            self.borrow()
        self.assertEqual(self.connect.call_count, 1)
        self.sessions[0].cleanup.assert_called_once()

    def test_handled_transport_failure_discards_entire_session(self):
        with utils.irods_session_scope(pool=self.pool):
            session = utils.BaseRuleManager("alice").session
            with session.pool.get_connection() as connection:
                connection.recv_error = NetworkException("ambiguous write failure")
                with self.assertRaises(NetworkException):
                    connection.recv()
            # A read-only retry may have created another healthy connection;
            # that must not hide the earlier transport failure from the pool.
            with session.pool.get_connection():
                pass
        session.cleanup.assert_called_once()
        self.assertIsNot(self.borrow(), session)

    def test_failed_send_closes_the_socket_even_if_disconnect_also_fails(self):
        with self.assertLogs(level="ERROR"):
            with utils.irods_session_scope(pool=self.pool):
                session = utils.BaseRuleManager("alice").session
                connection = session.pool.get_connection()
                sock = connection.socket
                sock.send_error = OSError("connection reset")
                with self.assertRaises(NetworkException):
                    connection.send(Mock(pack=Mock(return_value=b"request")))
        self.assertTrue(sock.closed)
        session.cleanup.assert_called_once()

    def test_locally_closed_socket_is_not_retained(self):
        with utils.irods_session_scope(pool=self.pool):
            session = utils.BaseRuleManager("alice").session
            next(iter(session.pool.idle)).socket.close()
        session.cleanup.assert_called_once()
        self.assertIsNot(self.borrow(), session)

    def test_escaped_exception_discards_all_request_sessions(self):
        with self.assertRaisesRegex(RuntimeError, "request failed"):
            with utils.irods_session_scope(pool=self.pool):
                utils.BaseRuleManager("alice")
                utils.BaseRuleManager(admin_mode=True)
                raise RuntimeError("request failed")
        for session in self.sessions:
            session.cleanup.assert_called_once()
        self.assertIsNone(utils._session_scope.get())

    def test_open_handles_and_changed_session_state_prevent_retention(self):
        for change in [
            lambda s: s.pool.get_connection(),
            lambda s: setattr(s, "connection_timeout", 5),
            lambda s: setattr(s, "numThreads", 2),
            lambda s: setattr(s, "ticket__", "temporary-ticket"),
            lambda s: s.ticket_applied.update({next(iter(s.pool.idle)): True}),
            lambda s: setattr(s, "pool", ClientPool(s.pool.account, session=s)),
        ]:
            with self.subTest(change=change):
                with utils.irods_session_scope(pool=self.pool):
                    session = utils.BaseRuleManager("alice").session
                    change(session)
                session.cleanup.assert_called_once()

    def test_cleanup_failures_do_not_skip_other_connections_or_sessions(self):
        with self.assertLogs(session_pool.logger, level="ERROR"):
            with utils.irods_session_scope(pool=self.pool):
                session = utils.BaseRuleManager("alice").session
                connection = session.pool.get_connection()
                sock = connection.socket
                healthy_socket = session.pool.get_connection().socket
                connection.disconnect = Mock(side_effect=OSError("disconnect failed"))
                session.cleanup.side_effect = RuntimeError("cleanup failed")
                self.addCleanup(setattr, session.cleanup, "side_effect", None)
                other = utils.BaseRuleManager("bob").session
            self.pool.close()
        self.assertTrue(sock.closed)
        self.assertTrue(healthy_socket.closed)
        other.cleanup.assert_called_once()

    def test_shutdown_is_idempotent_and_retires_outstanding_leases(self):
        idle = self.borrow("bob")
        with utils.irods_session_scope(pool=self.pool):
            borrowed = utils.BaseRuleManager("alice").session
            self.pool.close()
            self.pool.close()
            idle.cleanup.assert_called_once()
            borrowed.cleanup.assert_not_called()
        borrowed.cleanup.assert_called_once()
        with self.assertRaisesRegex(RuntimeError, "closed"):
            self.borrow()

    def test_shutdown_during_authentication_does_not_lend_session(self):
        def authenticate(pool, account):
            self.pool.close()
            return FakeConnection(pool, account)

        self.connect.side_effect = authenticate
        with self.assertRaisesRegex(RuntimeError, "closed"):
            self.borrow()
        self.sessions[0].cleanup.assert_called_once()

    def test_shutdown_during_health_check_does_not_create_a_replacement(self):
        session = self.borrow()
        connection = next(iter(session.pool.idle))
        connection.recv = Mock(side_effect=self.pool.close)
        with self.assertRaisesRegex(RuntimeError, "closed"):
            self.borrow()
        self.assertEqual(self.connect.call_count, 1)
        session.cleanup.assert_called_once()

    def test_fork_discards_inherited_sockets_without_protocol_disconnect(self):
        session = self.borrow()
        connection = next(iter(session.pool.idle))
        sock = connection.socket
        self.pool._lock.acquire()  # Simulate a lock held by a vanished thread.
        with patch.object(session_pool.os, "getpid", return_value=os.getpid() + 1):
            child = self.borrow()
        self.assertIsNot(child, session)
        self.assertTrue(sock.closed)
        self.assertEqual(sock.sent, [])
        self.assertFalse(session.pool.active | session.pool.idle)
        self.assertEqual(session.do_configure, {})

    def test_after_fork_hook_closes_child_copies_before_they_can_be_used(self):
        session = self.borrow()
        connection = next(iter(session.pool.idle))
        sock = connection.socket
        parent_lock = self.pool._lock
        parent_lock.acquire()
        pid = os.fork()
        if pid == 0:
            valid = sock.closed and not sock.sent and connection.socket is None
            os._exit(0 if valid else 1)
        parent_lock.release()
        _, status = os.waitpid(pid, 0)
        self.assertEqual(status, 0)
        self.assertFalse(sock.closed)
        self.assertIs(self.borrow(), session)

    def test_worker_singleton_is_lazy_and_cleanup_is_idempotent(self):
        with patch.object(session_pool, "_worker_pool", None):
            with patch.object(session_pool, "IRODSSessionPool", wraps=IRODSSessionPool) as constructor:
                session_pool.close_irods_session_pool()
                constructor.assert_not_called()
                pool = session_pool.get_irods_session_pool()
                self.assertIs(pool, session_pool.get_irods_session_pool())
                constructor.assert_called_once_with()
                session_pool.close_irods_session_pool()
                session_pool.close_irods_session_pool()


class WriteFailureTests(unittest.TestCase):
    def test_mutating_calls_are_not_replayed_after_network_failure(self):
        source = "/nlmumc/projects/P000000001/C000000001/a"
        destination = "/nlmumc/projects/P000000001/C000000001/b"
        cases = [
            ("move_collection", "collections", "move", (source, destination)),
            ("move_data_object", "data_objects", "move", (source, destination)),
            ("remove_collection", "collections", "remove", (source, True)),
            ("remove_data_object", "data_objects", "unlink", (source, True)),
            ("create_collection", "collections", "create", (source,)),
            ("create_data_object", "data_objects", "create", (source,)),
        ]
        cases.extend(("open_data_object", "data_objects", "open", (source, mode)) for mode in ["r", "w", "a", "r+"])
        for method, api_manager, api_method, args in cases:
            with self.subTest(method=method, args=args):
                manager = RuleManager.__new__(RuleManager)
                manager._owns_session = False
                manager.session = Mock()
                operation = getattr(getattr(manager.session, api_manager), api_method)
                operation.side_effect = NetworkException("response lost")
                with self.assertRaises(NetworkException):
                    getattr(manager, method)(*args)
                operation.assert_called_once()

    def test_read_only_network_retries_are_preserved(self):
        manager = RuleManager.__new__(RuleManager)
        manager._owns_session = False
        manager.session = Mock()
        manager.session.collections.exists.side_effect = [NetworkException("read failed"), True]
        self.assertTrue(manager.does_collection_exist("/nlmumc/projects/P000000001/C000000001/a"))
        self.assertEqual(manager.session.collections.exists.call_count, 2)


if __name__ == "__main__":
    unittest.main()
