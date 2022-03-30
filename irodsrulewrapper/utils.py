import logging

from dhpythonirodsutils import loggers

from irods.session import iRODSSession

import os
import pika
import pytz
import datetime
import ssl

logger = logging.getLogger(__name__)


def convert_to_current_timezone(date, date_format="%Y-%m-%d %H:%M:%S"):
    old_timezone = pytz.timezone("UTC")
    new_timezone = pytz.timezone("Europe/Amsterdam")
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return old_timezone.localize(date).astimezone(new_timezone).strftime(date_format)


class BaseRuleManager:
    def __init__(self, client_user=None, config=None, admin_mode=False):
        self.session = []
        self.parse_to_dto = True
        if not client_user and not admin_mode:
            raise Exception("No user to initialize RuleManager provided")
        self.ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None
        )

        self.ssl_settings = {
            "irods_client_server_negotiation": "request_server_negotiation",
            "irods_encryption_algorithm": "AES-256-CBC",
            "irods_encryption_key_size": 32,
            "irods_encryption_num_hash_rounds": 16,
            "irods_encryption_salt_size": 8,
            "ssl_context": self.ssl_context,
        }

        if config is None:
            self.init_with_environ_conf(client_user, admin_mode)
        else:
            self.init_with_variable_config(client_user, config, admin_mode)

    def __del__(self):
        # __del__() is a finalizer that is called when the object is garbage
        # collected. And this happens *after* all the references to the object
        # have been deleted. This is what CPython does, however it is not
        # guranteed behavior by Python. Ideally we do the cleanup() after using
        # this object to execute a rule/s. Perhaps with a try/finally.
        self.session.cleanup()

    def init_with_environ_conf(self, client_user, admin_mode):
        self.ssl_settings["irods_client_server_policy"] = os.environ["IRODS_CLIENT_SERVER_POLICY"]
        if admin_mode:
            self.session = iRODSSession(
                host=os.environ["IRODS_HOST"],
                port=1247,
                user=os.environ["IRODS_USER"],
                password=os.environ["IRODS_PASS"],
                zone="nlmumc",
                **self.ssl_settings
            )
        else:
            self.session = iRODSSession(
                host=os.environ["IRODS_HOST"],
                port=1247,
                user=os.environ["IRODS_USER"],
                password=os.environ["IRODS_PASS"],
                zone="nlmumc",
                client_user=client_user,
                **self.ssl_settings
            )

    def init_with_variable_config(self, client_user, config, admin_mode):
        self.ssl_settings["irods_client_server_policy"] = config["IRODS_CLIENT_SERVER_POLICY"]
        if admin_mode:
            self.session = iRODSSession(
                host=config["IRODS_HOST"],
                port=1247,
                user=config["IRODS_USER"],
                password=config["IRODS_PASS"],
                zone="nlmumc",
                **self.ssl_settings
            )
        else:
            self.session = iRODSSession(
                host=config["IRODS_HOST"],
                port=1247,
                user=config["IRODS_USER"],
                password=config["IRODS_PASS"],
                zone="nlmumc",
                client_user=client_user,
                **self.ssl_settings
            )


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


def log_audit_trail_message(user_id: int, event: str):
    """
    Log an entry with AUDIT_TRAIL tag and user ID

    Parameters
    ----------
    user_id: int
        The user identifier number
    event: str
        The event you want to be logged

    """
    logger.warning(loggers.format_audit_trail_message(user_id, event))
