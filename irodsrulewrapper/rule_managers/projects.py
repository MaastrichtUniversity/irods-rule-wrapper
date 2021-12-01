from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import (
    check_project_path_format,
    check_project_id_format,
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
        if not check_project_path_format(project_path):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")
        if show_service_accounts != "false" and show_service_accounts != "true":
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
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project's path format: e.g P000000010")
        if show_service_accounts != "false" and show_service_accounts != "true":
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
        if show_service_accounts != "false" and show_service_accounts != "true":
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
        if not check_project_id_format(project_id):
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
        if access_level != "own" and access_level != "write" and access_level != "read":
            raise RuleInputValidationError("invalid value for *access_level: expected 'default' or 'recursive'")
        if type(user) != str:
            raise RuleInputValidationError("invalid type for *user: expected a string")
        if type(path) != str:
            raise RuleInputValidationError("invalid type for *path: expected a string")

        return RuleInfo(name="set_acl", get_result=False, session=self.session, dto=None)

    @rule_call
    def metadata_edit_allowed(self, path):
        """
        Return boolean if the current user is allowed to edit metadata for a given project
        path : str
            The absolute path of the project
        """
        return RuleInfo(name="metadata_edit_allowed", get_result=True, session=self.session, dto=Boolean)

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
        if show_service_accounts != "false" and show_service_accounts != "true":
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
        if not check_project_path_format(project_path):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")

        return RuleInfo(name="get_project_migration_status", get_result=True, session=self.session, dto=MigrationCards)

    @rule_call
    def create_new_project(
        self,
        authorizationPeriodEndDate,
        dataRetentionPeriodEndDate,
        ingestResource,
        resource,
        storageQuotaGb,
        title,
        principalInvestigator,
        dataSteward,
        respCostCenter,
        openAccess,
        tapeArchive,
        tapeUnarchive,
        metadata_schemas,
    ):
        """
        Create a new iRODS project

        Parameters
        ----------
        authorizationPeriodEndDate : str
            The username
        dataRetentionPeriodEndDate : str
            The username
        ingestResource : str
            The ingest resource to use during the ingestion
        resource : str
            The destination resource to store future collection
        storageQuotaGb  : str
            The storage quota in Gb
        title : str
            The project title
        principalInvestigator : str
            The principal investigator(OBI:0000103) for the project
        dataSteward : str
            The data steward for the project
        respCostCenter : str
            The budget number
        openAccess : str
            'true'/'false' excepted values
        tapeArchive : str
            'true'/'false' excepted values
        tapeUnarchive : str
            'true'/'false' excepted values
        metadata_schemas : str
            csv string that contains the list of schema names

        Returns
        -------
        CreateProject
            dto.CreateProject object
        """
        # TODO check data format
        if type(authorizationPeriodEndDate) != str:
            raise RuleInputValidationError("invalid type for *authorizationPeriodEndDate: expected a string")

        # TODO check data format
        if type(dataRetentionPeriodEndDate) != str:
            raise RuleInputValidationError("invalid type for *dataRetentionPeriodEndDate: expected a string")

        if type(ingestResource) != str:
            raise RuleInputValidationError("invalid type for *ingestResource: expected a string")

        if type(resource) != str:
            raise RuleInputValidationError("invalid type for *resource: expected a string")

        if type(storageQuotaGb) != int:
            raise RuleInputValidationError("invalid type for *storageQuotaGb: expected an integer")

        if type(title) != str:
            raise RuleInputValidationError("invalid type for *title: expected a string")

        if type(principalInvestigator) != str:
            raise RuleInputValidationError("invalid type for *principalInvestigator: expected a string")

        if type(dataSteward) != str:
            raise RuleInputValidationError("invalid type for *dataSteward: expected a string")

        if type(respCostCenter) != str:
            raise RuleInputValidationError("invalid type for *respCostCenter: expected a string")

        if openAccess != "false" and openAccess != "true":
            raise RuleInputValidationError("invalid value for *openAccess: expected 'true' or 'false'")

        if tapeArchive != "false" and tapeArchive != "true":
            raise RuleInputValidationError("invalid value for *tapeArchive: expected 'true' or 'false'")

        if tapeUnarchive != "false" and tapeUnarchive != "true":
            raise RuleInputValidationError("invalid value for *tapeUnarchive: expected 'true' or 'false'")

        if not isinstance(metadata_schemas, str):
            raise RuleInputValidationError("invalid type for *metadata_schemas: expected a string")

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
        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project's path format: eg. /nlmumc/projects/P000000010")
        if inherited != "false" and inherited != "true":
            raise RuleInputValidationError("invalid value for *inherited: expected 'true' or 'false'")
        if show_service_accounts != "false" and show_service_accounts != "true":
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
            The project's id path; eg. 000000010
        show_service_accounts: str
            'true'/'false' expected; If true, hide the service accounts in the result

        Returns
        -------
        ContributingProject
            dto.ContributingProject object
        """

        if not check_project_id_format(project_id):
            raise RuleInputValidationError("invalid project id; eg. P000000001")

        if show_service_accounts != "false" and show_service_accounts != "true":
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
    def details_project(self, project, inherited):
        """
        Native iRODS language rule detailsProject.
        Get the project AVUs and its collections details in one rule.

        Returns
        -------
        dict
            JSON rule output
        """

        return RuleInfo(
            name="detailsProject", get_result=True, session=self.session, dto=None, parse_to_dto=self.parse_to_dto
        )
