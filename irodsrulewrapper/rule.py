from dhpythonirodsutils import validators, exceptions
from irods.exception import (
    DataObjectDoesNotExist,
    CollectionDoesNotExist,
    CAT_NO_ROWS_FOUND,
    CAT_INVALID_CLIENT_USER,
    QueryException,
)
from irods.query import SpecificQuery

from irodsrulewrapper.rule_managers.collections import CollectionRuleManager
from irodsrulewrapper.rule_managers.groups import GroupRuleManager
from irodsrulewrapper.rule_managers.ingest import IngestRuleManager
from irodsrulewrapper.rule_managers.projects import ProjectRuleManager
from irodsrulewrapper.rule_managers.resources import ResourceRuleManager
from irodsrulewrapper.rule_managers.users import UserRuleManager
from .utils import *


class RuleManager(
    CollectionRuleManager, ProjectRuleManager, UserRuleManager, GroupRuleManager, ResourceRuleManager, IngestRuleManager
):
    def __init__(self, client_user=None, config=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, config, admin_mode)

    def check_irods_connection(self):
        """
        Check if an iRODS connection can be established

        Returns
        -------
        bool
            boolean
        """
        try:
            self.session.pool.get_connection()
        except CAT_INVALID_CLIENT_USER:
            return False
        else:
            return True

    def get_temp_password(self, username, sessions_cleanup=True):
        """
        Get a temporary password for a user. Must be called with an admin account.

        Parameters
        ----------
        username : str
            The client username
        sessions_cleanup: bool
            If true, the session will be closed after retrieving the values.

        Returns
        -------
        str
            The temporary password
        """
        pwd = self.session.users.temp_password_for_user(username)
        if sessions_cleanup:
            self.session.cleanup()
        return pwd

    def generate_temporary_password(self, irods_user_name, irods_id):
        """
        Get a temporary password for a user and delete all existing ones.
        Must be called with an admin account.
        Parameters
        ----------
        irods_user_name : str
            The client username
        irods_id : str
            The irods id for the user
        sessions_cleanup: bool
            If true, the session will be closed after retrieving the values.

        Returns
        -------
        json dict :
            temporary_password : str
                The temporary password
            valid_until : int
                Unix timestamp until which the temporary password is valid

        Example output: {"temporary_password": "ba66856", "valid_until": 1666606633}
        """
        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        if self.session.users.get(irods_user_name).type != 'rodsuser':
            raise RuleInputValidationError("invalid irods user type for *irods_user_name: expected a rodsuser")

        if self.get_irods_user_id_by_username(irods_user_name) != irods_id:
            raise RuleInputValidationError("invalid match between *irods_user_name and *irods_id: expected a match")

        number_of_temp_passwords = self.count_user_temporary_passwords(irods_id)
        if int(number_of_temp_passwords) > 0:
            self.remove_user_temporary_passwords(irods_id)
        pwd = self.get_temp_password(irods_user_name, sessions_cleanup=False)
        ts = self.get_user_temporary_password_creation_timestamp(irods_id)
        if not ts:
            raise QueryException
        # Add the temporary password lifetime (90 days) to the creation timestamp to get it validity date
        ts = int(ts) + 7776000
        return {"temporary_password": pwd, "valid_until": ts}

    def remove_user_temporary_passwords(self, irods_id):

        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        try:
            query = SpecificQuery(self.session, alias="delete_password", args=[irods_id])
            result = query.execute()
            if result and result[0] != 0:
                raise QueryException  # TODO maybe also log an error for elastalert??
        except CAT_NO_ROWS_FOUND:
            return

    def count_user_temporary_passwords(self, irods_id):

        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        try:
            query = SpecificQuery(self.session, alias="count_password", args=[irods_id])
            for result in query:
                return result[0]
        except CAT_NO_ROWS_FOUND:
            return 0

    def get_user_temporary_password_creation_timestamp(self, irods_id):

        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        try:
            query = SpecificQuery(self.session, alias="get_create_ts_password", args=[irods_id])
            for result in query:
                return result[0]
        except CAT_NO_ROWS_FOUND:
            return 0

    def get_irods_user_id_by_username(self, user_name):
        user_id = self.session.users.get(user_name).id
        return user_id

    def download_file(self, path):
        """
        Returns the file buffer of the path given, if the file exists

        Parameters
        ----------
        path : str
            The full path to the file
            e.g. "P000000012/C000000001/metadata.xml"
        """
        file = None
        file_information = None
        path_prefix = "/nlmumc/projects/"
        full_path = path_prefix + path

        try:
            validators.validate_file_path(full_path)
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError:
            return file, file_information

        try:
            file_information = self.session.data_objects.get(full_path)
            file = self.session.data_objects.open(full_path, "r")
        except (CollectionDoesNotExist, DataObjectDoesNotExist) as error:
            print('File download request of "' + path + '" failed, file does not exist')
            print(error)

        return file, file_information


class RuleJSONManager(RuleManager):
    """
    RuleJSONManager inherit all RuleManager's rule methods. And set parse_to_dto as False.
    Executing a rule with RuleJSONManager, will return a JSON instead of a DTO

    """

    def __init__(self, client_user=None, config=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, config, admin_mode)
        self.parse_to_dto = False
