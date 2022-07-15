from dhpythonirodsutils.enums import ProjectAVUs
from dhpythonirodsutils import validators, exceptions

from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.dto.boolean import Boolean
from irodsrulewrapper.dto.contributing_project import ContributingProject
from irodsrulewrapper.dto.contributing_projects import ContributingProjects
from irodsrulewrapper.dto.create_project import CreateProject
from irodsrulewrapper.dto.managing_projects import ManagingProjects
from irodsrulewrapper.dto.migration_cards import MigrationCards
from irodsrulewrapper.dto.project_contributors import ProjectContributors
from irodsrulewrapper.dto.project_contributors_metadata import ProjectContributorsMetadata
from irodsrulewrapper.dto.projects_minimal import ProjectsMinimal
from irodsrulewrapper.dto.projects import Projects, Project
from irodsrulewrapper.dto.projects_cost import ProjectsCost
from irodsrulewrapper.dto.projects_overview import ProjectsOverview
from irodsrulewrapper.utils import (
    BaseRuleManager,
    RuleInfo,
    RuleInputValidationError,
)


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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010") from err
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *show_service_accounts: expected 'true' or 'false'"
            ) from err

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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project's path format: e.g P000000010") from err
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *showServiceAccounts: expected 'true' or 'false'"
            ) from err

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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *show_service_accounts: expected 'true' or 'false'"
            ) from err

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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010") from err

        if not isinstance(users, str):
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
        if mode not in ["default", "recursive"]:
            raise RuleInputValidationError("invalid value for *mode: expected 'default' or 'recursive'")
        if access_level not in ["own", "write", "read", "null", "admin:own", "admin:write", "admin:read", "admin:null"]:
            raise RuleInputValidationError("invalid value for *access_level: expected 'read', 'write', 'own, 'null'")
        if not isinstance(user, str):
            raise RuleInputValidationError("invalid type for *user: expected a string")
        if not isinstance(path, str):
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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *show_service_accounts: expected 'true' or 'false'"
            ) from err

        return RuleInfo(name="list_projects", get_result=True, session=self.session, dto=Projects)

    @rule_call
    def get_projects_minimal(self):
        """
        Get the list of projects with minimal information (id & title).

        Returns
        -------
        ProjectsMinimal
            dto.ProjectsMinimal object
        """
        return RuleInfo(name="list_projects_minimal", get_result=True, session=self.session, dto=ProjectsMinimal)

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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010") from err

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

        if not isinstance(ingest_resource, str):
            raise RuleInputValidationError(f"invalid type for *{ProjectAVUs.INGEST_RESOURCE.value}: expected a string")

        if not isinstance(resource, str):
            raise RuleInputValidationError(f"invalid type for *{ProjectAVUs.RESOURCE.value}: expected a string")

        if not isinstance(title, str):
            raise RuleInputValidationError(f"invalid type for *{ProjectAVUs.TITLE.value}: expected a string")

        if not isinstance(principal_investigator, str):
            raise RuleInputValidationError("invalid type for *principalInvestigator: expected a string")

        if not isinstance(data_steward, str):
            raise RuleInputValidationError(f"invalid type for *{ProjectAVUs.DATA_STEWARD.value}: expected a string")

        if not isinstance(responsible_cost_center, str):
            raise RuleInputValidationError(
                f"invalid type for *{ProjectAVUs.RESPONSIBLE_COST_CENTER.value}: expected a string"
            )

        if not isinstance(extra_parameters, dict):
            raise RuleInputValidationError("invalid type for *extraParameters: expected a dict")

        if ProjectAVUs.AUTHORIZATION_PERIOD_END_DATE.value in extra_parameters:
            # TODO check data format
            if not isinstance(extra_parameters[ProjectAVUs.AUTHORIZATION_PERIOD_END_DATE.value], str):
                raise RuleInputValidationError(
                    f"invalid type for *{ProjectAVUs.AUTHORIZATION_PERIOD_END_DATE.value}: expected a string"
                )

        if ProjectAVUs.DATA_RETENTION_PERIOD_END_DATE.value in extra_parameters:
            # TODO check data format
            if not isinstance(extra_parameters[ProjectAVUs.DATA_RETENTION_PERIOD_END_DATE.value], str):
                raise RuleInputValidationError(
                    f"invalid type for *{ProjectAVUs.DATA_RETENTION_PERIOD_END_DATE.value}: expected a string"
                )

        if ProjectAVUs.STORAGE_QUOTA_GB.value in extra_parameters:
            if not isinstance(extra_parameters[ProjectAVUs.STORAGE_QUOTA_GB.value], int):
                raise RuleInputValidationError(
                    f"invalid type for *{ProjectAVUs.STORAGE_QUOTA_GB.value}: expected an integer"
                )

        if ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters[ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value])
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    f"invalid value for *{ProjectAVUs.ENABLE_OPEN_ACCESS_EXPORT.value}: expected 'true' or 'false'"
                ) from err

        if ProjectAVUs.ENABLE_ARCHIVE.value in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters[ProjectAVUs.ENABLE_ARCHIVE.value])
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    f"invalid value for *{ProjectAVUs.ENABLE_ARCHIVE.value}: expected 'true' or 'false'"
                ) from err

        if ProjectAVUs.ENABLE_UNARCHIVE.value in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters[ProjectAVUs.ENABLE_UNARCHIVE.value])
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    f"invalid value for *{ProjectAVUs.ENABLE_UNARCHIVE.value}: expected 'true' or 'false'"
                ) from err

        if ProjectAVUs.ENABLE_DROPZONE_SHARING.value in extra_parameters:
            try:
                validators.validate_string_boolean(extra_parameters[ProjectAVUs.ENABLE_DROPZONE_SHARING.value])
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    f"invalid value for *{ProjectAVUs.ENABLE_DROPZONE_SHARING.value}: expected 'true' or 'false'"
                ) from err

        if ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value in extra_parameters:
            if not isinstance(extra_parameters[ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value], str):
                raise RuleInputValidationError(
                    f"invalid type for *{ProjectAVUs.COLLECTION_METADATA_SCHEMAS.value}: expected a string"
                )

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
            * inherited='true' cumulates authorizations to designate the role.
                i.e. A contributor has 'OWN' or 'WRITE' access
            * inherited='false' only shows explicit contributors.
                i.e. A contributor only has 'WRITE' access
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        ProjectContributors
            dto.ProjectContributors object
        """
        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project's id format: eg. P000000010") from err
        try:
            validators.validate_string_boolean(inherited)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'") from err
        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *show_service_accounts: expected 'true' or 'false'"
            ) from err

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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id; eg. P000000001") from err

        try:
            validators.validate_string_boolean(show_service_accounts)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError(
                "invalid value for *show_service_accounts: expected 'true' or 'false'"
            ) from err

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
            * inherited='true' cumulates authorizations to designate the role.
                i.e. A contributor has 'OWN' or 'WRITE' access
            * inherited='false' only shows explicit contributors.
                i.e. A contributor only has 'WRITE' access

        Returns
        -------
        dict
            JSON rule output
        """

        try:
            validators.validate_project_id(project_id)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id; eg. P000000001") from err
        try:
            validators.validate_string_boolean(inherited)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'") from err

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
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid project id; eg. P000000001") from err

        return RuleInfo(
            name="get_project_contributors_metadata",
            get_result=True,
            session=self.session,
            dto=ProjectContributorsMetadata,
        )

    @rule_call
    def list_contributing_projects_by_attribute(self, attribute):
        """
        Query the list of projects where the client user is at least a contributor and the action feature is enable for
        the project.

        Parameters
        ----------
        attribute: str
            The attribute value of a project feature AVU. e.g: 'enableArchive', 'enableUnarchive',
            'enableOpenAccessExport', 'enableContributorEditMetadata'

        Returns
        -------
        dict
            Per project, it returns the project: ID, path, and title
        """
        if not isinstance(attribute, str):
            raise RuleInputValidationError("invalid type for *action: expected a string")

        try:
            validators.validate_project_collections_action_avu(attribute)
        except exceptions.ValidationError as err:
            raise RuleInputValidationError("invalid value for *attribute; e.g: 'enableArchive'") from err

        return RuleInfo(
            name="list_contributing_projects_by_attribute",
            get_result=True,
            session=self.session,
            dto=ProjectsMinimal,
        )
