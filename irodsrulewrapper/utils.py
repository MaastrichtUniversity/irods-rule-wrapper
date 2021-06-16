import logging

from irods.session import iRODSSession

import re
import os


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


def is_safe_full_path(full_path):
    split_path = full_path.split('/')
    # basedir => "/nlmumc/projects/P[0-9]{9}/C[0-9]{9}"
    basedir = '/' + split_path[1] + '/' + split_path[2] + '/' + split_path[3] + '/' + split_path[4]
    return is_safe_path(basedir, full_path)


# https://security.openstack.org/guidelines/dg_using-file-paths.html
def is_safe_path(basedir, path):
    match_path = os.path.abspath(path)
    return basedir == os.path.commonpath((basedir, match_path))


class BaseRuleManager:
    def __init__(self, client_user=None, config=None):
        self.env_settings = {}
        self.session = []
        if config is None:
            self.init_with_environ_conf(client_user)
        else:
            self.init_with_variable_config(client_user, config)

    def init_with_environ_conf(self, client_user):
        if client_user is None:
            self.session = iRODSSession(host=os.environ['IRODS_HOST'], port=1247, user=os.environ['IRODS_USER'],
                                        password=os.environ['IRODS_PASS'], zone='nlmumc')
        else:
            self.session = iRODSSession(host=os.environ['IRODS_HOST'], port=1247, user=os.environ['IRODS_USER'],
                                        password=os.environ['IRODS_PASS'], zone='nlmumc', client_user=client_user)
        # Getting the RabbitMQ settings from the environment variables
        # and storing them in the Rule Manager class, accessible anywhere
        self.env_settings = {
            "rabbitmq_host": os.environ['RABBITMQ_HOST'],
            "rabbitmq_port": os.environ['RABBITMQ_PORT'],
            "rabbitmq_user": os.environ['RABBITMQ_USER'],
            "rabbitmq_pass": os.environ['RABBITMQ_PASS']
        }

    def init_with_variable_config(self, client_user, config):
        if client_user is None:
            self.session = iRODSSession(host=config['IRODS_HOST'], port=1247, user=config['IRODS_USER'],
                                        password=config['IRODS_PASS'], zone='nlmumc')
        else:
            self.session = iRODSSession(host=config['IRODS_HOST'], port=1247, user=config['IRODS_USER'],
                                        password=config['IRODS_PASS'], zone='nlmumc', client_user=client_user)
        if 'RABBITMQ_HOST' not in config:
            logging.warning("no rabbit mq config provided, dataverse features will not work.")
            return
        self.env_settings = {
            "rabbitmq_host": config['RABBITMQ_HOST'],
            "rabbitmq_port": config['RABBITMQ_PORT'],
            "rabbitmq_user": config['RABBITMQ_USER'],
            "rabbitmq_pass": config['RABBITMQ_PASS']
        }


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
    def __init__(self, name, get_result, session, dto, input_params=None, rule_body=None):
        self.name = name
        self.get_result = get_result
        self.session = session
        self.dto = dto
        self.input_params = input_params
        self.rule_body = rule_body
