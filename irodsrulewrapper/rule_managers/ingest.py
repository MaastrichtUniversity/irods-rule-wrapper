from irodsrulewrapper.decorator import rule_call
from irodsrulewrapper.utils import BaseRuleManager, RuleInfo, RuleInputValidationError
from irodsrulewrapper.dto.metadata_xml import MetadataXML
from irodsrulewrapper.dto.drop_zones import DropZones, DropZone
from irodsrulewrapper.dto.token import Token

import logging


class IngestRuleManager(BaseRuleManager):
    def __init__(self, client_user=None, admin_mode=False):
        BaseRuleManager.__init__(self, client_user, admin_mode=admin_mode)

    @rule_call
    def get_active_drop_zones(self, report):
        """
        Get the list of active drop zones

        Parameters
        ----------
        report : str
            'true'/'false' excepted values; If true, show extra values: startDate, endDate & userName

        Returns
        -------
        DropZones
            dto.DropZones object
        """
        if report != "false" and report != "true":
            raise RuleInputValidationError("invalid value for *report: expected 'true' or 'false'")

        return RuleInfo(name="listActiveDropZones", get_result=True, session=self.session, dto=DropZones)

    @rule_call
    def get_active_drop_zone(self, token, check_ingest_resource_status):
        """
        Get the list of active drop zones

        Parameters
        ----------
        token : str
            The dropzone token
        check_ingest_resource_status : str
            'true'/'false' excepted values; If true, show the project resource status

        Returns
        -------
        DropZone
            dto.DropZone object
        """
        if type(token) != str:
            raise RuleInputValidationError("invalid type for *token: expected a string")

        if check_ingest_resource_status != "false" and check_ingest_resource_status != "true":
            raise RuleInputValidationError(
                "invalid value for *check_ingest_resource_status: expected 'true' or 'false'"
            )

        return RuleInfo(name="get_active_drop_zone", get_result=True, session=self.session, dto=DropZone)

    @rule_call
    def start_ingest(self, user, token):
        input_params = {"*user": '"{}"'.format(user), "*token": '"{}"'.format(token)}

        rule_body = """
            execute_rule{
                startIngest;
            }
            """

        return RuleInfo(
            name="startIngest",
            get_result=False,
            session=self.session,
            dto=None,
            input_params=input_params,
            rule_body=rule_body,
        )

    @rule_call
    def create_ingest(self, user, token, project, title):

        input_params = {
            "*user": '"{}"'.format(user),
            "*token": '"{}"'.format(token),
            "*project": '"{}"'.format(project),
            "*title": '"{}"'.format(title),
        }

        rule_body = """
        execute_rule{
            createIngest;
        }
        """

        return RuleInfo(
            name="createIngest",
            get_result=False,
            session=self.session,
            dto=None,
            input_params=input_params,
            rule_body=rule_body,
        )

    def ingest(self, user, token):
        logger = logging.getLogger(__name__)
        try:
            self.set_total_size_dropzone(token)
        except Exception as e:
            logger.warning("set_total_size_dropzone failed with error: {}".format(e))
        self.start_ingest(user, token)

    def create_drop_zone(self, data):
        token = self.generate_token().token
        self.create_ingest(data["user"], token, data["project"], data["title"])
        data["token"] = token
        self.save_metadata_xml(data)
        return token

    def read_metadata_xml_from_dropzone(self, token):
        xml_path = "/nlmumc/ingest/zones/" + token + "/" + "metadata.xml"
        return MetadataXML.read_metadata_xml(self.session, xml_path, token)

    def save_metadata_xml(self, data):
        xml = MetadataXML.create_from_dict(data)
        xml.write_metadata_xml(self.session)

    @rule_call
    def edit_drop_zone(self, token, project, title):
        """
        Edits the dropzone's project and title AVUs

        Parameters
        ----------
        token : str
            the token of the DZ to modify
        project : str
            the new project number (ex. P000000001)
        title : str
            the new title (ex. bar)

        """

        input_params = {
            "*token": '"{}"'.format(token),
            "*project": '"{}"'.format(project),
            "*title": '"{}"'.format(title),
        }

        rule_body = """
               execute_rule{
                   editIngest;
               }
               """

        return RuleInfo(
            name="editIngest",
            get_result=False,
            session=self.session,
            dto=None,
            input_params=input_params,
            rule_body=rule_body,
        )

    @rule_call
    def generate_token(self):
        """
        Gets a unused (dropzone) token generated by iRODS

        Returns
        -------
        Token
            The token generated by iRODS

        """

        return RuleInfo(name="generate_token", get_result=True, session=self.session, dto=Token)

    @rule_call
    def set_total_size_dropzone(self, token):
        """
        Set an attribute value to the input user

        Parameters
        ----------
        token : str
            The dropzone token to be ingested

        """
        if type(token) != str:
            raise RuleInputValidationError("invalid type for *token: expected a string")

        return RuleInfo(name="set_dropzone_total_size_avu", get_result=False, session=self.session, dto=None)
