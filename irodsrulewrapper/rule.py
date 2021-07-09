from irods.exception import CAT_INVALID_CLIENT_USER
from irods.exception import DataObjectDoesNotExist, CollectionDoesNotExist, NoResultFound, CAT_NO_ACCESS_PERMISSION
from irods.data_object import irods_basename
from irods.models import Collection as iRODSCollection
from irods.models import DataObject

from irodsrulewrapper.rule_managers.collections import CollectionRuleManager
from irodsrulewrapper.rule_managers.projects import ProjectRuleManager
from irodsrulewrapper.rule_managers.users import UserRuleManager
from irodsrulewrapper.rule_managers.groups import GroupRuleManager
from irodsrulewrapper.rule_managers.resources import ResourceRuleManager
from irodsrulewrapper.rule_managers.ingest import IngestRuleManager

from .utils import *


class RuleManager(CollectionRuleManager, ProjectRuleManager, UserRuleManager,
                  GroupRuleManager, ResourceRuleManager, IngestRuleManager):
    def __init__(self, client_user=None, config=None):
        BaseRuleManager.__init__(self, client_user, config)

    def __del__(self):
        # __del__ is a destructor method which is called as soon as all references of the object are deleted.
        # i.e when an object is garbage collected.
        # Session cleanup is not called after each rule execution anymore.
        # So it needs to happen here.
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

    def get_collection_tree(self, base, path, sessions_cleanup=True):
        """
        Lists the folders and files attributes at the input 'path'

        Parameters
        ----------
        base : str
            The base path to validate ; eg. P000000001/C000000001
        path : str
            The collection's id; eg. P000000001/C000000001/SubFolder1/Experiment1/
        sessions_cleanup: bool
            If true, the session will be closed after retrieving the values.

        Returns
        -------
        dict
            The folders and files attributes at the requested path
        """
        output = []
        base_path = "/nlmumc/projects/" + base
        absolute_path = "/nlmumc/projects/" + path
        collection = self.session.collections.get(absolute_path)

        if not is_safe_path(base_path, absolute_path):
            raise CAT_NO_ACCESS_PERMISSION

        for coll in collection.subcollections:
            # query extra collection info: ctime
            query = self.session.query(iRODSCollection).filter(iRODSCollection.id == coll.id)
            try:
                result = query.one()
            except NoResultFound:
                raise CollectionDoesNotExist()

            name = irods_basename(result[iRODSCollection.name])
            ctime = result[iRODSCollection.create_time]
            relative_path = path + "/" + name

            folder_node = {
                'name': name,
                'path': relative_path,
                'type': 'folder',
                'size': "--",
                'rescname': "--",
                'ctime': ctime.strftime('%Y-%m-%d %H:%M:%S')
            }

            output.append(folder_node)

        for data in collection.data_objects:
            # query extra data info: ctime
            query = self.session.query(DataObject).filter(DataObject.id == data.id)
            try:
                result = query.first()
            except NoResultFound:
                raise DataObjectDoesNotExist()

            ctime = result[DataObject.create_time]
            relative_path = path + "/" + data.name

            data_node = {
                'name': data.name,
                'path': relative_path,
                'type': 'file',
                'size': data.size,
                'rescname': data.resource_name,
                'offlineResource': data.resource_name == 'arcRescSURF01',
                'ctime': ctime.strftime('%Y-%m-%d %H:%M:%S')
            }

            output.append(data_node)

        if sessions_cleanup:
            self.session.cleanup()

        return output

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
        path_prefix = '/nlmumc/projects/'
        full_path = path_prefix + path

        if check_file_path_format(full_path) is False or is_safe_full_path(full_path) is False:
            return file, file_information

        try:
            file_information = self.session.data_objects.get(full_path)
            file = self.session.data_objects.open(full_path, 'r')
        except (CollectionDoesNotExist, DataObjectDoesNotExist) as error:
            print('File download request of "' + path + '" failed, file does not exist')
            print(error)

        return file, file_information


class RuleJSONManager(RuleManager):
    """
    RuleJSONManager inherit all RuleManager's rule methods. And set dto_parsing as False.
    Executing a rule with RuleJSONManager, will return a JSON instead of a DTO

    """
    def __init__(self, client_user=None, config=None):
        BaseRuleManager.__init__(self, client_user, config)
        self.dto_parsing = False
