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

import pika
import pytz
from dhpythonirodsutils import loggers
from irods.session import iRODSSession

logger = logging.getLogger(__name__)


def convert_to_current_timezone(date, date_format="%Y-%m-%d %H:%M:%S"):
    old_timezone = pytz.timezone("UTC")
    new_timezone = pytz.timezone("Europe/Amsterdam")
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return old_timezone.localize(date).astimezone(new_timezone).strftime(date_format)


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
        self.parse_to_dto = True
        if not client_user and not admin_mode:
            raise Exception("No user to initialize RuleManager provided")

        self.init_irods_session(client_user, admin_mode, with_config=config)

    def __del__(self):
        # __del__() is a finalizer that is called when the object is garbage
        # collected. And this happens *after* all the references to the object
        # have been deleted. This is what CPython does, however it is not
        # guaranteed behavior by Python. Ideally we do the cleanup() after using
        # this object to execute a rule/s. Perhaps with a try/finally.
        if self.session:
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
            irods_session_settings["client_user"] = client_user

        self.session = iRODSSession(**irods_session_settings)


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


def publish_message(exchange, routing_key, message):
    credentials = pika.PlainCredentials(os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASS"])
    parameters = pika.ConnectionParameters(
        host=os.environ["RABBITMQ_HOST"],
        port=5672,
        virtual_host="/",
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    connection.close()


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
