from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.project_contributors_metadata import ProjectContributorsMetadata
from irodsrulewrapper.utils import (
    BaseRuleManager,
    RuleInfo,
    RuleInputValidationError,
)
from irodsrulewrapper.dto.projects import Projects, Project
from irodsrulewrapper.dto.projects_overview import ProjectsOverview
from irodsrulewrapper.dto.managing_projects import ManagingProjects
from irodsrulewrapper.dto.contributing_projects import ContributingProjects
from irodsrulewrapper.dto.projects_cost import ProjectsCost
from irodsrulewrapper.dto.create_project import CreateProject
from irodsrulewrapper.dto.migration_cards import MigrationCards
from irodsrulewrapper.dto.project_contributors import ProjectContributors
from irodsrulewrapper.dto.contributing_project import ContributingProject
from irodsrulewrapper.dto.boolean import Boolean

from dhpythonirodsutils import validators, exceptions


class ProjectRuleManager(BaseRuleManager):
    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, admin_mode=admin_mode)

    @rule_call
    def get_project_details(self, project_path, show_service_accounts):
        """
        Get the list of projects

        Parameters
        ----------
        project_path : str
            The project's absolute path; eg. /nlmumc/projects/P000000010
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------

        dict || Project
            JSON || dto.Project object
        """
        try:
            validators.validate_project_path(project_path)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *show_service_accounts: expected 'true' or 'false'")

        return RuleInfo(
            name="get_project_details",
            get_result=True,
            session=self.session,
            dto=Project,
            parse_to_dto=self.parse_to_dto,
        )

    @rule_call
    def get_project_acl_for_manager(self, project_id, show_service_accounts):
        """
        Query the list of ACL for a project for the client user

        Parameters
        ----------
        project_id : str
            The project's id; e.g P000000010
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        ManagingProjects
            The list of usernames for managers, contributors and viewers.
            Returns an empty list if the user is not a manager.
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project's path format: e.g P000000010")
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *showServiceAccounts: expected 'true' or 'false'")

        return RuleInfo(
            name="get_project_acl_for_manager",
            get_result=True,
            session=self.session,
            dto=ManagingProjects,
            parse_to_dto=self.parse_to_dto,
        )

    @rule_call
    def get_contributing_projects(self, show_service_accounts):
        """
        Query the list of ACL for a project for the client user.
        Returns an empty list if the user is not a contributor.

        Parameters
        ----------
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        ContributingProjects
            dto.ContributingProjects object
        """
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *show_service_accounts: expected 'true' or 'false'")

        return RuleInfo(
            name="list_contributing_projects", get_result=True, session=self.session, dto=ContributingProjects
        )

    @rule_call
    def change_project_permissions(self, project_id, users):
        """
        Change immediately the ACL on the project level.
        Then in the delay queue, change recursively all the collections under the project.

        Parameters
        ----------
        project_id : str
            The project's id; e.g P000000010
        users: str
            The input string to modify the ACL.
            It should follow the following format: 'username:access_level"
            e.g "p.vanschayck@maastrichtuniversity.nl:read m.coonen@maastrichtuniversity.nl:write"
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        if type(users) != str:
            raise RuleInputValidationError("invalid type for *users: expected a string")

        return RuleInfo(name="changeProjectPermissions", get_result=False, session=self.session, dto=None)

    @rule_call
    def set_acl(self, mode, access_level, user, path):
        """
        Set the ACL of a given collection

        Parameters
        ----------
        mode : str
            'default', 'recursive' excepted values
        access_level : str
            access level: 'own', 'write', 'read'
        user : str
            The username
        path : str
            The absolute path of the collection
        """
        if mode != "default" and mode != "recursive":
            raise RuleInputValidationError("invalid value for *mode: expected 'default' or 'recursive'")
        if access_level not in ["own", "write", "read", "null", "admin:own", "admin:write", "admin:read", "admin:null"]:
            raise RuleInputValidationError("invalid value for *access_level: expected 'read', 'write', 'own, 'null'")
        if type(user) != str:
            raise RuleInputValidationError("invalid type for *user: expected a string")
        if type(path) != str:
            raise RuleInputValidationError("invalid type for *path: expected a string")

        return RuleInfo(name="set_acl", get_result=False, session=self.session, dto=None)

    @rule_call
    def check_edit_metadata_permission(self, path):
        """
        Return boolean if the current user is allowed to edit metadata for a given project
        path : str
            The absolute path of the project
        """
        return RuleInfo(name="check_edit_metadata_permission", get_result=True, session=self.session, dto=Boolean)

    @rule_call
    def get_projects_finance(self):
        """
        Get the list of projects financial information

        Returns
        -------
        ProjectsCost
            The list of projects financial information

        """

        return RuleInfo(name="get_projects_finance", get_result=True, session=self.session, dto=ProjectsCost)

    @rule_call
    def get_projects(self, show_service_accounts):
        """
        Get the list of projects

        Parameters
        ----------
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        Projects
            dto.Projects object
        """
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *show_service_accounts: expected 'true' or 'false'")

        return RuleInfo(name="list_projects", get_result=True, session=self.session, dto=Projects)

    @rule_call
    def get_project_migration_status(self, project_path):
        """
        Get the list of project's collections

        Parameters
        ----------
        project_path : str
            The project's absolute path; eg. /nlmumc/projects/P000000010

        Returns
        -------
        MigrationCards
            dto.MigrationCards object
        """
        try:
            validators.validate_project_path(project_path)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        return RuleInfo(name="get_project_migration_status", get_result=True, session=self.session, dto=MigrationCards)

    @rule_call
    def create_new_project(
        self,
        ingest_resource,
        resource,
        title,
        principal_investigator,
        data_steward,
        responsible_cost_center,
        extra_parameters,
    ):
        """
        Create a new iRODS project

        Parameters
        ----------
        ingest_resource : str
            The ingest resource to use during the ingestion
        resource : str
            The destination resource to store future collection
        title : str
            The project title
        principal_investigator : str
            The principal investigator(OBI:0000103) for the project
        data_steward : str
            The data steward for the project
        responsible_cost_center : str
            The budget number
        extra_parameters: dict
            Json formatted list of extra parameters.
            Currently supported are:
                authorizationPeriodEndDate : str
                    Date
                dataRetentionPeriodEndDate : str
                    Date
                storageQuotaGb  : str
                    The storage quota in Gb
                enableOpenAccessExport : str
                    'true'/'false' expected values
                enableArchive : str
                    'true'/'false' expected values
                enableUnarchive : str
                    'true'/'false' expected values
                enableDropzoneSharing : str
                    'true'/'false' expected values
                collectionMetadataSchemas : str
                    csv string that contains the list of schema names

        Returns
        -------
        CreateProject
            dto.CreateProject object
        """

        if type(ingest_resource) != str:
            raise RuleInputValidationError("invalid type for *ingestResource: expected a string")

        if type(resource) != str:
            raise RuleInputValidationError("invalid type for *resource: expected a string")

        if type(title) != str:
            raise RuleInputValidationError("invalid type for *title: expected a string")

        if type(principal_investigator) != str:
            raise RuleInputValidationError("invalid type for *principalInvestigator: expected a string")

        if type(data_steward) != str:
            raise RuleInputValidationError("invalid type for *dataSteward: expected a string")

        if type(responsible_cost_center) != str:
            raise RuleInputValidationError("invalid type for *responsibleCostCenter: expected a string")

        if not isinstance(extra_parameters, dict):
            raise RuleInputValidationError("invalid type for *extraParameters: expected a string")

        if "authorizationPeriodEndDate" in extra_parameters:
            # TODO check data format
            if type(extra_parameters["authorizationPeriodEndDate"]) != str:
                raise RuleInputValidationError("invalid type for *authorizationPeriodEndDate: expected a string")

        if "dataRetentionPeriodEndDate" in extra_parameters:
            # TODO check data format
            if type(extra_parameters["dataRetentionPeriodEndDate"]) != str:
                raise RuleInputValidationError("invalid type for *dataRetentionPeriodEndDate: expected a string")

        if "storageQuotaGb" in extra_parameters:
            if type(extra_parameters["storageQuotaGb"]) != int:
                raise RuleInputValidationError("invalid type for *storageQuotaGb: expected an integer")

        if "enableOpenAccessExport" in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters["enableOpenAccessExport"])
            except exceptions.ValidationError:
                raise RuleInputValidationError("invalid value for *enableOpenAccessExport: expected 'true' or 'false'")

        if "enableArchive" in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters["enableArchive"])
            except exceptions.ValidationError:
                raise RuleInputValidationError("invalid value for *enableArchive: expected 'true' or 'false'")

        if "enableUnarchive" in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters["enableUnarchive"])
            except exceptions.ValidationError:
                raise RuleInputValidationError("invalid value for *enableUnarchive: expected 'true' or 'false'")

        if "enableDropzoneSharing" in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters["enableDropzoneSharing"])
            except exceptions.ValidationError:
                raise RuleInputValidationError("invalid value for *enableDropzoneSharing: expected 'true' or 'false'")

        if "collectionMetadataSchemas" in extra_parameters:
            if not isinstance(extra_parameters["collectionMetadataSchemas"], str):
                raise RuleInputValidationError("invalid type for *collectionMetadataSchemas: expected a string")

        return RuleInfo(name="create_new_project", get_result=True, session=self.session, dto=CreateProject)

    @rule_call
    def get_project_contributors(self, project_id, inherited, show_service_accounts):
        """
        Get the contributors of the projects

        Parameters
        ----------
        project_id : str
            The project's id path; eg. 000000010
        inherited : str
            Role inheritance
            * inherited='true' cumulates authorizations to designate the role. i.e. A contributor has OWN or WRITE access
            * inherited='false' only shows explicit contributors. i.e. A contributor only has WRITE access
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        ProjectContributors
            dto.ProjectContributors object
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")
        try:
            validators.validate_string_boolean(inherited)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'")
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *show_service_accounts: expected 'true' or 'false'")

        return RuleInfo(
            name="list_project_contributors", get_result=True, session=self.session, dto=ProjectContributors
        )

    @rule_call
    def get_contributing_project(self, project_id, show_service_accounts):
        """
        Get project ACL if the user is a contributor. Otherwise, it returns None

        Parameters
        ----------
        project_id : str
            The project's id path; eg. P000000010
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        ContributingProject
            dto.ContributingProject object
        """

        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *show_service_accounts: expected 'true' or 'false'")

        return RuleInfo(name="get_contributing_project", get_result=True, session=self.session, dto=ContributingProject)

    @rule_call
    def get_projects_overview(self):
        """
        Get the list of projects

        Returns
        -------
        Projects
            dto.ProjectsOverview object
        """

        return RuleInfo(name="optimized_list_projects", get_result=True, session=self.session, dto=ProjectsOverview)

    @rule_call
    def list_projects_by_user(self):
        """
        Get the list of projects that each user has access into.


        Returns
        -------
        dict
            JSON rule output
        """

        return RuleInfo(
            name="listProjectsByUser", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )

    @rule_call
    def details_project(self, project_id, inherited):
        """
        Native iRODS language rule detailsProject.
        Get the project AVUs and its collections details in one rule.

        Parameters
        ----------
        project_id : str
            The project's id path; eg. P000000010.
        inherited : str
            Role inheritance
            * inherited='true' cumulates authorizations to designate the role. i.e. A contributor has OWN or WRITE access
            * inherited='false' only shows explicit contributors. i.e. A contributor only has WRITE access

        Returns
        -------
        dict
            JSON rule output
        """

        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project id; eg. P000000001")
        try:
            validators.validate_string_boolean(inherited)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'")

        return RuleInfo(
            name="detailsProject", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )

    @rule_call
    def get_project_contributors_metadata(self, project_id):
        """
        Get the contributors(PI, data-steward, etc) metadata of the given project.

        Parameters
        ----------
        project_id : str
            The project's id path; eg. P000000010.

        Returns
        -------
        ProjectContributorsMetadata
            The contributors(PI, data-steward, etc) metadata.

        """

        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError:
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        return RuleInfo(
            name="get_project_contributors_metadata",
            get_result=True,
            session=self.session,
            dto=ProjectContributorsMetadata,
        )
