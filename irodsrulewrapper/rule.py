"""This module contains the user-client Rule managers classes: RuleManager & RuleJSONManager."""
from typing import TypedDict

from dhpythonirodsutils import validators, exceptions
from irods.data_object import iRODSDataObject
from irods.exception import CAT_INVALID_CLIENT_USER, CAT_NO_ROWS_FOUND, QueryException
from irods.exception import DataObjectDoesNotExist, CollectionDoesNotExist
from irods.query import SpecificQuery

from irodsrulewrapper.decorator import retry_api_call, MAX_RETRY_API_CALL
from irodsrulewrapper.rule_managers.collections import CollectionRuleManager
from irodsrulewrapper.rule_managers.groups import GroupRuleManager
from irodsrulewrapper.rule_managers.ingest import IngestRuleManager
from irodsrulewrapper.rule_managers.projects import ProjectRuleManager
from irodsrulewrapper.rule_managers.resources import ResourceRuleManager
from irodsrulewrapper.rule_managers.users import UserRuleManager
from irodsrulewrapper.utils import BaseRuleManager, RuleInputValidationError, log_error_message


class TemporaryPasswordTTL(TypedDict):
    """
    Attributes:
    ---------
        temporary_password : str
            The temporary password
        valid_until : int
            Unix's timestamp until which the temporary password is valid
    """

    temporary_password: str
    valid_until: int


class RuleManager(
    CollectionRuleManager, ProjectRuleManager, UserRuleManager, GroupRuleManager, ResourceRuleManager, IngestRuleManager
):
    """
    This class provides instances to easily:
        * set up a new iRODS connection an admin or a proxied user
        * execute a predefined server-side rule and parse the rule output as a DTO
        * execute iRODS API features (get user temporary password, download files ...)
    """

    def __init__(self, client_user=None, config=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, config, admin_mode)

    def cleanup(self):
        if self.session:
            self.session.cleanup()

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

    def generate_temporary_password(self, irods_user_name: str, irods_id: int) -> TemporaryPasswordTTL:
        """
        Get a temporary password for a user and delete all existing ones.
        Must be called with an admin account.

        Examples
        output: {"temporary_password": "ba66856", "valid_until": 1666606633}

        Raises
        ------
        RuleInputValidationError
        QueryException

        Parameters
        ----------
        irods_user_name : str
            The client username
        irods_id : int
            The irods id for the user

        Returns
        -------
        TemporaryPasswordTTL
            The password and the Time to live (TTL)
        """
        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        if self.session.users.get(irods_user_name).type != "rodsuser":
            raise RuleInputValidationError("invalid irods user type for *irods_user_name: expected a rodsuser")

        if self.get_irods_user_id_by_username(irods_user_name) != irods_id:
            raise RuleInputValidationError("invalid match between *irods_user_name and *irods_id: expected a match")

        number_of_temp_passwords = self.count_user_temporary_passwords(irods_id)
        if int(number_of_temp_passwords) > 0:
            self.remove_user_temporary_passwords(irods_id)
        pwd = self.get_temp_password(irods_user_name, sessions_cleanup=False)
        creation_time_stamp = self.get_user_temporary_password_creation_timestamp(irods_id)
        temporary_password_lifetime = int(self.get_temporary_password_lifetime())
        if not creation_time_stamp:
            raise QueryException
        # Add the temporary password lifetime (from irods server) to the creation timestamp to get it validity date
        time_stamp = creation_time_stamp + temporary_password_lifetime
        return {"temporary_password": pwd, "valid_until": time_stamp}

    def remove_user_temporary_passwords(self, irods_id: int):
        """
        Removes all existing temporary passwords

        Raises
        ------
        RuleInputValidationError
        QueryException

        Parameters
        ----------
        irods_id : int
            The irods id for the user
        """
        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        try:
            query = SpecificQuery(self.session, alias="delete_password", args=[irods_id])
            result = query.execute()
            if result and result[0] != 0:
                log_error_message(irods_id, "Failed to remove temporary password")
                raise QueryException
        except CAT_NO_ROWS_FOUND:
            return

    def count_user_temporary_passwords(self, irods_id: int) -> int:
        """
        Count the number of temporary passwords for a user

        Raises
        ------
        RuleInputValidationError

        Parameters
        ----------
        irods_id : int
            The irods id for the user

        Returns
        -------
        int:
            the number of temporary passwords for a user
        """
        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        try:
            query = SpecificQuery(self.session, alias="count_password", args=[irods_id])
            for result in query:
                return int(result[0])
        except CAT_NO_ROWS_FOUND:
            return 0

    def get_user_temporary_password_creation_timestamp(self, irods_id: int) -> int | None:
        """
        Get the timestamp of creation for the temporary password for a specific user

        Raises
        ------
        RuleInputValidationError

        Parameters
        ----------
        irods_id : int
            The irods id for the user

        Returns
        -------
        int | None:
            Epoch timestamp for the creation of the temporary password
        """
        if not isinstance(irods_id, int):
            raise RuleInputValidationError("invalid type for *irods_id: expected a integer")

        try:
            query = SpecificQuery(self.session, alias="get_create_ts_password", args=[irods_id])
            for result in query:
                return int(result[0])
        except CAT_NO_ROWS_FOUND:
            return None

    def get_irods_user_id_by_username(self, user_name: str) -> int:
        """
        Get the irods user id for a give irods username

        Raises
        ------
        UserDoesNotExist

        Parameters
        ----------
        user_name : str
            The irods user_name

        Returns
        -------
        int:
            irods user id
        """
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

    @retry_api_call
    def does_collection_exist(self, full_path):
        """
        Check if the input path matches an existing iRODS collection/directory.

        Parameters
        ----------
        full_path: str
            The absolute collection path to check in iRODS

        Returns
        -------
        bool
            True, if the path matches an existing iRODS collection/directory

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        return self.session.collections.exists(full_path)

    @retry_api_call
    def does_data_object_exist(self, full_path):
        """
        Check if the input path matches an existing iRODS data object/file.

        Parameters
        ----------
        full_path: str
            The absolute data object path to check in iRODS

        Returns
        -------
        bool
            True, if the path matches an existing iRODS data object/file.

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        return self.session.data_objects.exists(full_path)

    @retry_api_call
    def move_collection(self, source_path, destination_path):
        """
        Move the iRODS collection from the source path to the destination path.

        Parameters
        ----------
        source_path: str
            The absolute path to locate the collection in iRODS
        destination_path: str
            The absolute path to move the existing collection to its new destination path in iRODS

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(source_path)
            validators.validate_full_path_safety(destination_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        self.session.collections.move(source_path, destination_path)

    @retry_api_call
    def move_data_object(self, source_path, destination_path):
        """
        Move the iRODS data object from the source path to the destination path.

        Parameters
        ----------
        source_path: str
            The absolute path to locate the collection in iRODS
        destination_path: str
            The absolute path to move the existing data object to its new destination path in iRODS

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(source_path)
            validators.validate_full_path_safety(destination_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        self.session.data_objects.move(source_path, destination_path)

    @retry_api_call
    def remove_collection(self, full_path, force):
        """
        Remove an existing iRODS collection/directory.

        Parameters
        ----------
        full_path: str
            The absolute path to the collection to delete in iRODS
        force: bool
            If true, Immediate removal of the collection without putting them in trash

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        if not isinstance(force, bool):
            raise RuleInputValidationError("invalid type for *force: expected a bool")

        self.session.collections.remove(full_path, force=force)

    @retry_api_call
    def remove_data_object(self, full_path, force):
        """
        Remove an existing iRODS data object/file.

        Parameters
        ----------
        full_path: str
            The absolute path to the data object to delete in iRODS
        force: bool
            If true, Immediate removal of the data-objects without putting them in trash

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        if not isinstance(force, bool):
            raise RuleInputValidationError("invalid type for *force: expected a bool")

        self.session.data_objects.unlink(full_path, force=force)

    @retry_api_call
    def create_collection(self, full_path):
        """
        Create a new collection at the inout location.

        Parameters
        ----------
        full_path: str
            The absolute path to the collection to create in iRODS

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        # On folder upload with multiple sub-folders, CollectionDoesNotExist can be triggered
        # Add retry mechanism, to fix the concurrent collection creation
        for retry_index in range(MAX_RETRY_API_CALL):
            try:
                self.session.collections.create(full_path)
            except CollectionDoesNotExist as error:
                if retry_index < MAX_RETRY_API_CALL - 1:
                    continue
                raise CollectionDoesNotExist(full_path) from error

    @retry_api_call
    def create_data_object(self, full_path):
        """
        Create a new empty data object at the inout location.

        Parameters
        ----------
        full_path: str
            The absolute path to the data object to create in iRODS

        Raises
        ------
        NetworkException
        RuleInputValidationError
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        self.session.data_objects.create(full_path)

    @retry_api_call
    def get_data_object(self, full_path):
        """
        Query the iRODS data object properties.

        Parameters
        ----------
        full_path: str
            The absolute path to the data object to retrieve in iRODS

        Raises
        ------
        NetworkException
        RuleInputValidationError

        Returns
        -------
        iRODSDataObject
            Requested data object properties
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        return self.session.data_objects.get(full_path)

    @retry_api_call
    def open_data_object(self, full_path, mode):
        """
        Query the iRODS data object properties.

        Parameters
        ----------
        full_path: str
            The absolute path to the data object to retrieve in iRODS
        mode: str
            The mode while opening a file: read, write or append
            'r': (self.O_RDONLY, False),
            'r+': (self.O_RDWR, False),
            'w': (self.O_WRONLY | createFlag | self.O_TRUNC, False),
            'w+': (self.O_RDWR | createFlag | self.O_TRUNC, False),
            'a': (self.O_WRONLY | createFlag, True),
            'a+': (self.O_RDWR | createFlag, True)

        Raises
        ------
        NetworkException
        RuleInputValidationError

        Returns
        -------
        io.BufferedRandom
            Data object buffer
        """
        try:
            validators.validate_full_path_safety(full_path)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("Invalid path provided") from err

        if mode not in ["r", "r+", "w", "w+", "a", "a+"]:
            raise RuleInputValidationError("Invalid data object open mode provided")

        return self.session.data_objects.open(full_path, mode)


class RuleJSONManager(RuleManager):
    """
    RuleJSONManager inherit all RuleManager's rule methods. And set parse_to_dto as False.
    Executing a rule with RuleJSONManager, will return a JSON instead of a DTO.
    """

    def __init__(self, client_user=None, config=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, config, admin_mode)
        self.parse_to_dto = False
