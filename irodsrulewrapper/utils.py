import logging

from irods.session import iRODSSession

import re
import os
import pika
import ssl


def check_project_id_format(project):
    if re.search("^P[0-9]{9}$", project) is not None:
        return True
    else:
        return False


def check_project_path_format(project):
    if re.search("^/nlmumc/projects/P[0-9]{9}$", project) is not None:
        return True
    else:
        return False


def check_collection_id_format(collection):
    if re.search("^C[0-9]{9}$", collection) is not None:
        return True
    else:
        return False


def check_project_collection_path_format(path):
    if re.search("^/nlmumc/projects/P[0-9]{9}/C[0-9]{9}$", path) is not None:
        return True
    else:
        return False


def check_file_path_format(path):
    if re.search("^/nlmumc/projects/P[0-9]{9}/C[0-9]{9}/", path) is not None:
        return True
    else:
        return False


def get_project_from_collection_path(path):
    m = re.search(r"^(/nlmumc/projects/)?(?P<project>P[0-9]{9})/C[0-9]{9}/?", path)
    if m is not None:
        return "/nlmumc/projects/" + m.group("project")
    else:
        return None


def is_safe_full_path(full_path):
    split_path = full_path.split("/")
    # basedir => "/nlmumc/projects/P[0-9]{9}/C[0-9]{9}"
    basedir = "/" + split_path[1] + "/" + split_path[2] + "/" + split_path[3] + "/" + split_path[4]
    return is_safe_path(basedir, full_path)


# https://security.openstack.org/guidelines/dg_using-file-paths.html
def is_safe_path(basedir, path):
    match_path = os.path.abspath(path)
    return basedir == os.path.commonpath((basedir, match_path))


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
            "irods_client_server_policy": os.environ["IRODS_CLIENT_SERVER_POLICY"],
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

    def init_with_environ_conf(self, client_user, admin_mode):
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
        heartbeat_interval=600,
        blocked_connection_timeout=300,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    connection.close()
