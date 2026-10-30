"""
This module provides rules helpers classes and functions.

Classes:
    BaseRuleManager
    RuleInputValidationError
    RuleInfo

Functions:
    convert_to_current_timezone
    publish_message
    log_error_message
    log_warning_message
    log_audit_trail_message
"""
import datetime
import logging
import os
import ssl
from contextlib import contextmanager
from contextvars import ContextVar

import pytz
from dhpythonirodsutils import loggers
from irods.session import iRODSSession

logger = logging.getLogger(__name__)
_session_scope = ContextVar("irods_session_scope", default=None)
_scope_pool = ContextVar("irods_session_scope_pool", default=None)


@contextmanager
def irods_session_scope(pool=None):
    """Reuse sessions within this context; optionally borrow from a pool.

    Managers borrow the scoped sessions: their cleanup calls and finalizers
    defer cleanup until scope exit. Without a pool, sessions close on exit.
    Outside a scope managers retain their normal ownership. Nested scopes
    own independent sets of sessions.
    """
    sessions = {}
    token = _session_scope.set(sessions)
    pool_token = _scope_pool.set(pool)
    failed = True
    try:
        yield
        failed = False
    finally:
        _session_scope.reset(token)
        _scope_pool.reset(pool_token)
        for session in sessions.values():
            try:
                if pool is None:
                    session.cleanup()
                else:
                    pool.release(session, discard=failed)
            except Exception:  # Clean up the other sessions and preserve request errors.
                logger.exception("Failed to clean up a scoped iRODS session")


def convert_to_current_timezone(date, date_format="%Y-%m-%d %H:%M:%S"):
    old_timezone = pytz.timezone("UTC")
    new_timezone = pytz.timezone("Europe/Amsterdam")
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return old_timezone.localize(date).astimezone(new_timezone).strftime(date_format)


def format_rule_argument(argument):
    """
    Format a rule argument to prevent single or double quote issues
    Parameters
    ----------
    argument : string
        Argument that needs to be formatted
    """
    if '"' in argument and "'" in argument:
        argument = argument.replace('"', '\\"')
        value = f'"{argument}"'
    elif '"' in argument:
        value = f"'{argument}'"
    elif "'" in argument:
        value = f'"{argument}"'
    else:
        value = f'"{argument}"'

    return value


class BaseRuleManager:
    """
    This (abstract) class has the basic methods to set up an iRODS (SSL) connection.
    The class is inherited by the classes in the sub-package irodsrulewrapper.rule_managers.
    """

    # ssl_context & ssl_settings left as class variables to help with mocking during testing
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
    ssl_settings = {
        "irods_client_server_negotiation": "request_server_negotiation",
        "irods_encryption_algorithm": "AES-256-CBC",
        "irods_encryption_key_size": 32,
        "irods_encryption_num_hash_rounds": 16,
        "irods_encryption_salt_size": 8,
        "ssl_context": ssl_context,
    }

    def __init__(self, client_user=None, config=None, admin_mode=False):
        self.session = None
        self._owns_session = True
        self.parse_to_dto = True
        if not client_user and not admin_mode:
            raise Exception("No user to initialize RuleManager provided")

        self.init_irods_session(client_user, admin_mode, with_config=config)

    def __del__(self):
        # Standalone managers retain finalizer cleanup; scoped sessions live
        # until scope exit, regardless of when their managers are collected.
        self.cleanup()

    def cleanup(self):
        """Close an owned session; borrowed sessions are closed by their scope."""
        if self.session and self._owns_session:
            self.session.cleanup()

    def init_irods_session(self, client_user, admin_mode, with_config=None):
        irods_session_settings = {
            "host": with_config["IRODS_HOST"] if with_config else os.environ["IRODS_HOST"],
            "user": with_config["IRODS_USER"] if with_config else os.environ["IRODS_USER"],
            "password": with_config["IRODS_PASS"] if with_config else os.environ["IRODS_PASS"],
            "port": 1247,
            "zone": "nlmumc",
            "irods_client_server_policy": os.environ["IRODS_CLIENT_SERVER_POLICY"],
            **self.ssl_settings,
        }

        if not admin_mode:
            irods_session_settings["client_user"] = str(getattr(client_user, "username", client_user))

        sessions = _session_scope.get()
        self._owns_session = sessions is None
        if self._owns_session:
            self.session = iRODSSession(**irods_session_settings)
        else:
            key = (bool(admin_mode), tuple(sorted(irods_session_settings.items())))
            if key not in sessions:
                pool = _scope_pool.get()
                if pool is None:
                    sessions[key] = iRODSSession(**irods_session_settings)
                else:
                    sessions[key] = pool.borrow(key, lambda: iRODSSession(auto_cleanup=False, **irods_session_settings))
            self.session = sessions[key]


class RuleInputValidationError(Exception):
    """Exception raised for errors during the rule's validation of the input parameters.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "RuleInputValidationError, {0}".format(self.message)


class RuleInfo:
    """
    This class represents the extra information required by the @rule_call decorator to execute an iRODS rule.
    Its objects are instantiated inside a rule wrapped method inside a RuleManager.
    """

    def __init__(self, name, get_result, session, dto, input_params=None, rule_body=None, parse_to_dto=True):
        self.name = name
        self.get_result = get_result
        self.session = session
        self.dto = dto
        self.input_params = input_params
        self.rule_body = rule_body
        self.parse_to_dto = parse_to_dto


def log_error_message(user, message):
    logger.error(loggers.format_error_message(user, message))


def log_warning_message(user, message):
    logger.warning(loggers.format_warning_message(user, message))


def log_audit_trail_message(user_id: int, topic: str, event: str):
    """
    Log an entry with AUDIT_TRAIL tag and user ID

    Parameters
    ----------
    user_id: int
        The user identifier number
    topic: str
        The General topic for this log
    event: str
        The event you want to be logged

    """
    logger.warning(loggers.format_audit_trail_message(user_id, topic, event))
