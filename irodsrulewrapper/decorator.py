"""
This module contains the decorator function to execute iRODS rule
"""
import json
import os
from distutils.util import strtobool
from typing import Callable

from irods.rule import Rule


def rule_call(func: Callable):
    """
    This function extends another function, by parsing its input function arguments and its output RuleInfo, to execute
    it as an iRODS rule.

    Extending the input function:
        * execute the input function body (must contain input validation)
        * parse the output RuleInfo
        * prepare the rule object and then execute it
        * either parse the rule result as a DTO or pass the result JSON object
        * return the result to the caller.

    Examples
    --------
        @rule_call
        def get_groups(self, show_service_accounts):
            try:
                validators.validate_string_boolean(show_service_accounts)
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    "invalid value for *showServiceAccounts: expected 'true' or 'false'"
                ) from err

            return RuleInfo(name="get_groups", get_result=True, session=self.session, dto=Groups)

    is equivalent to:

        def get_groups(self, show_service_accounts):
            try:
                validators.validate_string_boolean(show_service_accounts)
            except exceptions.ValidationError as err:
                raise RuleInputValidationError(
                    "invalid value for *showServiceAccounts: expected 'true' or 'false'"
                ) from err

            rule_info = RuleInfo(name="get_groups", get_result=True, session=self.session, dto=Groups)
            rule_body = create_rule_body(show_service_accounts, rule_info=rule_info)
            input_params = create_rule_input(show_service_accounts, rule_info=rule_info)
            result = execute_rule(rule_body, input_params, rule_info)

            return result

    the caller just need to execute:
        result = RuleManager("user").get_groups("false")

    Parameters
    ----------
    func: Callable
        The function to decorate to be executed as a rule

    Returns
    -------
    Any
        The rule result as the mentioned DTO or a JSON
    """

    def create_rule_body(*args, **kwargs):
        """
        Create a rule body from a template with the list of arguments (*args)
            and the list of keyword/named arguments (**kwargs)
        Example:
            create_rule_body("P000000010", "C000000001",
                                rule_info.name="test_arg", rule_info.get_result=True)
        will return
            rule_body='''
            execute_rule{
                test_arg(*arg1, *arg2, *result);
            }
            '''
        """
        rule_info = kwargs["rule_info"]
        arguments_string = ""
        for argument_index in range(2, len(args) + 1):
            arguments_string += "*arg" + str(argument_index) + ","

        if rule_info.get_result:
            arguments_string = arguments_string + "*result"
        else:
            arguments_string = arguments_string[:-1]

        rule_body = f"""
        execute_rule{{
        {rule_info.name}({arguments_string});
        }}
        """
        return rule_body

    def create_rule_input(*args, **kwargs):
        """
        Create a list of input parameter from the list of arguments (*args)
            and the list of keyword/named arguments (**kwargs)
        Example:
            create_rule_input("P000000010", "C000000001",
                                rule_info.name="test_arg", rule_info.get_result=True)
        will return
            {
                "*arg1": '"P000000010"',
                "*arg2": '"C000000001"',
                "*result": '""'
            }
            '''
        """
        rule_info = kwargs["rule_info"]
        if rule_info.get_result:
            input_params = {"*result": '""'}
        else:
            input_params = {}
        for argument_index in range(2, len(args) + 1):
            key = "*arg" + str(argument_index)
            value = f'"{args[argument_index - 1]}"'
            input_params[key] = value
        return input_params

    def execute_rule(rule_body, input_params, rule_info):
        myrule = Rule(rule_info.session, body=rule_body, params=input_params, output="*result")
        result = myrule.execute()
        if rule_info.get_result:
            buf = result.MsParam_PI[0].inOutStruct.myStr
            buf_json = json.loads(buf)
            # Check if it will return the JSON rule's output or the DTO
            if rule_info.parse_to_dto:
                return rule_info.dto.create_from_rule_result(buf_json)

            return buf_json

        return None

    def wrapper_decorator(*args):
        rule_info = func(*args)

        if not rule_info.parse_to_dto and rule_info.get_result and strtobool(os.environ["MOCK_RULE_WRAPPER"]):
            return {}
        elif rule_info.get_result and strtobool(os.environ["MOCK_RULE_WRAPPER"]):
            try:
                return rule_info.dto.create_from_mock_json()
            except AttributeError:
                return rule_info.dto.create_from_mock_result()
        elif not rule_info.get_result and strtobool(os.environ["MOCK_RULE_WRAPPER"]):
            return

        if rule_info.rule_body is None:
            rule_body = create_rule_body(*args, rule_info=rule_info)
        else:
            rule_body = rule_info.rule_body

        if rule_info.input_params is None:
            input_params = create_rule_input(*args, rule_info=rule_info)
        else:
            input_params = rule_info.input_params

        result = execute_rule(rule_body, input_params, rule_info)
        return result

    return wrapper_decorator


def api_call(mock):
    def get_mock_result(func: Callable):
        def mock_api_call(*args, **kwargs):
            if strtobool(os.environ["MOCK_RULE_WRAPPER"]):
                print("mock")
                result = mock
            else:
                print("func")
                result = func(*args, **kwargs)

            return result

        return mock_api_call

    return get_mock_result


INSTANCE_JSON = json.loads(
    """
{
    "7_Contributor": [
        {
            "contributorIdentifierScheme": {
                "rdfs:label": "ORCiD",
                "@id": "https://orcid.org/"
            },
            "contributorAffiliation": {},
            "contributorFullName": {
                "@value": "Luis Sanchez"
            },
            "contributorIdentifier": {
                "@value": null
            },
            "contributorFamilyName": {
                "@value": "Sanchez"
            },
            "@context": {
                "contributorIdentifierScheme": "https://schema.metadatacenter.org/properties/264bff35-9c7e-4a84-a722-712217dfa232",
                "contributorAffiliation": "https://schema.metadatacenter.org/properties/73214405-3002-4fde-8f6c-b012faf907ec",
                "contributorFullName": "https://schema.metadatacenter.org/properties/272d6c5e-467c-4c01-a513-23b8df92585d",
                "contributorIdentifier": "https://schema.metadatacenter.org/properties/4636604a-6a42-4257-8a34-b8c68627cf32",
                "contributorFamilyName": "https://schema.metadatacenter.org/properties/510d9317-3658-429b-b773-8f9c0d288668",
                "contributorType": "https://schema.metadatacenter.org/properties/4d0bd488-6d4a-4388-bfa9-3cbb1d941afb",
                "contributorGivenName": "https://schema.metadatacenter.org/properties/1b2e719d-c7cc-4db0-b6f8-22ccdf43a387",
                "contributorEmail": "https://schema.metadatacenter.org/properties/72eb0553-76b7-4ef2-898f-694aa015cdd4"
            },
            "contributorType": {
                "rdfs:label": "project manager",
                "@id": "http://purl.org/zonmw/generic/10082"
            },
            "contributorGivenName": {
                "@value": "Luis"
            },
            "contributorEmail": {
                "@value": "l.sanchez@maastrichtuniversity.nl"
            },
            "@id": "https://repo.metadatacenter.org/template-elements/1d979a88-1028-421d-a124-11b5011f278a"
        }
    ],
    "schema:isBasedOn": "https://hdl.handle.net/21.T12996/P000000041C000000002schema.1",
    "2_Creator": {
        "creatorIdentifier": {
            "@value": "0000-0000-0000-0000"
        },
        "creatorIdentifierSchemeIRI": {
            "rdfs:label": "ORCiD",
            "@id": "https://orcid.org/"
        },
        "creatorGivenName": {
            "@value": "Laurent"
        },
        "creatorAffiliation": {},
        "creatorIdentifierScheme": {
            "rdfs:label": "ORCiD",
            "@id": "https://orcid.org/"
        },
        "creatorFamilyName": {
            "@value": "Winckers"
        },
        "@context": {
            "creatorIdentifier": "https://schema.metadatacenter.org/properties/18e308f9-0286-4d53-9acf-45b64cf13409",
            "creatorIdentifierSchemeIRI": "https://schema.metadatacenter.org/properties/47dbf3ad-a626-47f9-814c-df36df9959bc",
            "creatorGivenName": "https://schema.metadatacenter.org/properties/70630a4c-d76f-46b2-902c-916203a981a1",
            "creatorAffiliation": "https://schema.metadatacenter.org/properties/11ea34dd-138e-4901-8565-c56e8cf980ca",
            "creatorIdentifierScheme": "https://schema.metadatacenter.org/properties/2a4230e0-9dc4-4477-bea8-a718e32106af",
            "creatorFamilyName": "https://schema.metadatacenter.org/properties/356309ef-b052-41ad-97b6-a30f76ba6df4",
            "creatorFullName": "https://schema.metadatacenter.org/properties/34cd0986-098c-4c76-830c-300966ad422a"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/d2e97c7c-90b7-44c4-8d4b-2c43d46c98a9",
        "creatorFullName": {
            "@value": "Laurent Winckers"
        }
    },
    "schema:name": "DataHub General Schema",
    "10_ResourceType": {
        "@context": {
            "resourceTypeDetail": "https://schema.metadatacenter.org/properties/26faf602-2fd3-4e22-818b-32949c82b746",
            "resourceTypeGeneral": "https://schema.metadatacenter.org/properties/42039c05-9fe3-4e8a-b9f6-f97affc62d3c"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/34e8196b-c93f-4a04-a691-42d50da0aebf",
        "resourceTypeDetail": {
            "@value": "Collection"
        },
        "resourceTypeGeneral": {
            "rdfs:label": "Collection",
            "@id": "http://vocab.fairdatacollective.org/gdmt/Collection"
        }
    },
    "1_Identifier": {
        "datasetIdentifier": {
            "@value": "https://hdl.handle.net/21.T12996/P000000041C000000002.1"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/1a0ab675-8fc9-40bf-a3eb-a6e39d626e5a",
        "datasetIdentifierType": {
            "rdfs:label": "Handle",
            "@id": "http://vocab.fairdatacollective.org/gdmt/Handle"
        },
        "@context": {
            "datasetIdentifier": "http://purl.org/dc/terms/identifier",
            "datasetIdentifierType": "http://purl.org/spar/datacite/usesIdentifierScheme"
        }
    },
    "12_RelatedIdentifier": [
        {
            "relationType": {},
            "relatedResourceIdentifierType": {},
            "@id": "https://repo.metadatacenter.org/template-elements/c13bdf4e-46a5-4364-925a-c33d33c13256",
            "relatedResourceIdentifier": {
                "@value": null
            },
            "@context": {
                "relationType": "http://rs.tdwg.org/dwc/terms/relationshipOfResource",
                "relatedResourceIdentifierType": "http://schema.org/propertyID",
                "relatedResourceIdentifier": "http://purl.org/dc/terms/identifier"
            }
        }
    ],
    "pav:lastUpdatedOn": "2022-07-26T11:34:22",
    "4_Publisher": {
        "Publisher": {
            "@value": "DataHub"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/331f86b7-17c5-4c1c-8be1-41d1c9e084a0",
        "@context": {
            "Publisher": "https://schema.metadatacenter.org/properties/2c80f739-e2c4-425e-9bf0-fa20fffe29ba"
        }
    },
    "3_Title": {
        "@context": {
            "title": "https://schema.metadatacenter.org/properties/4ffd7c46-1df8-4885-ade4-50d542d5b81e"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/83367232-64e2-4117-9797-98f0d2694698",
        "title": {
            "@value": "test ingest to ceph over webdav"
        }
    },
    "7_ContactPerson": [
        {
            "contactFullName": {
                "@value": "Laurent Winckers"
            },
            "contactAffiliation": {},
            "contactNameIdentifier": {
                "@value": null
            },
            "contactEmail": {
                "@value": "laurent.winckers@maastrichtuniversity.nl"
            },
            "contactNameIdentifierScheme": {},
            "contactFamilyName": {
                "@value": "Winckers"
            },
            "contactGivenName": {
                "@value": "Laurent"
            },
            "contactType": {
                "rdfs:label": "contact person",
                "@id": "http://purl.org/zonmw/generic/10089"
            },
            "@context": {
                "contactFullName": "https://schema.metadatacenter.org/properties/9cc96e17-345e-43c1-955d-9777ef8136aa",
                "contactAffiliation": "https://schema.metadatacenter.org/properties/488e6114-b24f-4bf6-83b0-45a33abdabf6",
                "contactNameIdentifier": "https://schema.metadatacenter.org/properties/953598f5-f9f7-4276-899f-09851b9501d1",
                "contactEmail": "https://schema.metadatacenter.org/properties/72eb0553-76b7-4ef2-898f-694aa015cdd4",
                "contactNameIdentifierScheme": "https://schema.metadatacenter.org/properties/d680d7f5-ac6d-4fac-a245-37ca8e41a2f9",
                "contactFamilyName": "https://schema.metadatacenter.org/properties/510d9317-3658-429b-b773-8f9c0d288668",
                "contactGivenName": "https://schema.metadatacenter.org/properties/1b2e719d-c7cc-4db0-b6f8-22ccdf43a387",
                "contactType": "https://schema.metadatacenter.org/properties/4d0bd488-6d4a-4388-bfa9-3cbb1d941afb"
            },
            "@id": "https://repo.metadatacenter.org/template-elements/a5b4ede8-f284-4991-b2c0-2273b925b2ca"
        }
    ],
    "schema:description": "This is the basic DataHub General Schema",
    "17_Description": {
        "descriptionType": {
            "@value": "Abstract"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/1595a50e-f0c0-47c6-804e-fff5ac7a7531",
        "Description": {
            "@value": "Hitting ingest during upload to webdav"
        },
        "@context": {
            "descriptionType": "http://purl.org/spar/datacite/hasDescriptionType",
            "Description": "http://purl.org/dc/terms/description"
        }
    },
    "pav:createdOn": "2022-07-26T11:34:22",
    "datasetPagebreak": {},
    "pav:createdBy": "https://mdr.datahubmaastricht.nl/user/lwinckers",
    "oslc:modifiedBy": "https://mdr.datahubmaastricht.nl/user/lwinckers",
    "@context": {
        "schema:isBasedOn": {
            "@type": "@id"
        },
        "pav:createdOn": {
            "@type": "xsd:dateTime"
        },
        "oslc:modifiedBy": {
            "@type": "@id"
        },
        "pav:derivedFrom": {
            "@type": "@id"
        },
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "6_Subject": "https://schema.metadatacenter.org/properties/d8dc1860-b3a5-4547-ad22-0e003dc2e5fc",
        "7_Contributor": "https://schema.metadatacenter.org/properties/45bffde9-fe61-4479-a70d-953e3aa4a9c9",
        "2_Creator": "https://schema.metadatacenter.org/properties/6297f721-5a92-4014-9a7d-2eeb9afbe11b",
        "oslc": "http://open-services.net/ns/core#",
        "pav": "http://purl.org/pav/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "4_Publisher": "https://schema.metadatacenter.org/properties/68a521c1-69af-49e5-95a0-9890642da26d",
        "pav:createdBy": {
            "@type": "@id"
        },
        "8_Date": "https://schema.metadatacenter.org/properties/29cd27ea-b7b6-47b7-a82d-ab48ae34396d",
        "rdfs:label": {
            "@type": "xsd:string"
        },
        "schema:name": {
            "@type": "xsd:string"
        },
        "3_Title": "http://purl.org/dc/terms/title",
        "7_ContactPerson": "https://schema.metadatacenter.org/properties/9ae72767-4449-4018-9cf0-6da73604d0cc",
        "schema:description": {
            "@type": "xsd:string"
        },
        "skos:notation": {
            "@type": "xsd:string"
        },
        "1_Identifier": "https://schema.metadatacenter.org/properties/b260286d-3da0-4f53-a40d-eb769c24da8f",
        "12_RelatedIdentifier": "https://schema.metadatacenter.org/properties/65f55a39-f020-45d6-a071-c8388a12a25f",
        "17_Description": "https://schema.metadatacenter.org/properties/28d418d7-bfe7-44fb-968f-6e3ae9b68501",
        "10_ResourceType": "https://schema.metadatacenter.org/properties/8f154e9c-501a-4b80-b148-a74f250edc69",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "schema": "http://schema.org/",
        "pav:lastUpdatedOn": {
            "@type": "xsd:dateTime"
        }
    },
    "@id": "https://hdl.handle.net/21.T12996/P000000041C000000002instance.1",
    "6_Subject": [
        {
            "@context": {
                "subjectSchemeIRI": "http://vocab.fairdatacollective.org/gdmt/hasSubjectSchemeIRI",
                "valueURI": "https://schema.metadatacenter.org/properties/af9c45ec-d971-4056-a6c2-5ce930b9b181",
                "Subject": "https://schema.metadatacenter.org/properties/71f1a80c-d59e-4d92-a084-4f22f219cb6e"
            },
            "subjectSchemeIRI": {
                "@value": null
            },
            "valueURI": {},
            "@id": "https://repo.metadatacenter.org/template-elements/fc4e957d-637c-4a00-b371-d9e981ce3af4",
            "Subject": {
                "@value": null
            }
        }
    ],
    "8_Date": {
        "@context": {
            "datasetDateType": "http://vocab.fairdatacollective.org/gdmt/hasDatasetDateType",
            "datasetDate": "http://vocab.fairdatacollective.org/gdmt/hasDatasetDate"
        },
        "datasetDateType": {
            "rdfs:label": "Submitted",
            "@id": "http://vocab.fairdatacollective.org/gdmt/Submitted"
        },
        "@id": "https://repo.metadatacenter.org/template-elements/1bf3e3d6-c05e-43c6-b39d-c60080365268",
        "datasetDate": {
            "@value": "2022-07-26",
            "@type": "xsd:date"
        }
    }
}
"""
)

SCHEMA_JSON = {
    "pav:version": "1.0.0",
    "schema:name": "DataHub General Schema",
    "description": "Datahub general schema template schema generated by the CEDAR Template Editor 2.6.16",
    "title": "Datahub general schema template schema",
    "type": "object",
    "required": [
        "@context",
        "@id",
        "schema:isBasedOn",
        "schema:name",
        "schema:description",
        "pav:createdOn",
        "pav:createdBy",
        "pav:lastUpdatedOn",
        "oslc:modifiedBy",
        "4_Publisher",
        "8_Date",
        "2_Creator",
        "12_RelatedIdentifier",
        "7_Contributor",
        "3_Title",
        "1_Identifier",
        "17_Description",
        "6_Subject",
        "10_ResourceType",
        "7_ContactPerson",
    ],
    "bibo:status": "bibo:draft",
    "additionalProperties": False,
    "schema:schemaVersion": "1.6.0",
    "properties": {
        "1_Identifier": {
            "skos:prefLabel": "Identifier",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {
                    "datasetIdentifier": "The Identifier is a unique string that identifies a resource",
                    "datasetIdentifierType": "The type of Identifier",
                },
                "propertyLabels": {"datasetIdentifier": "Identifier", "datasetIdentifierType": "identifierType"},
                "order": ["datasetIdentifier", "datasetIdentifierType"],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/cf0b5d0b-650b-4126-9766-f909159255f0",
            "schema:schemaVersion": "1.6.0",
            "title": "1_identifier element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "1_Identifier",
            "description": "1_identifier element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "Identifier",
            "schema:description": "Information about the globally unique and persistent identifier used to identify and optionally access (meta)data of the dataset being described.",
            "@id": "https://repo.metadatacenter.org/template-elements/1a0ab675-8fc9-40bf-a3eb-a6e39d626e5a",
            "properties": {
                "datasetIdentifier": {
                    "_valueConstraints": {"defaultValue": "", "requiredValue": True},
                    "skos:prefLabel": "Dataset Identifier",
                    "bibo:status": "bibo:draft",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:schemaVersion": "1.6.0",
                    "title": "Identifier field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "Identifier",
                    "description": "Identifier field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "The Identifier is a unique string that identifies a resource",
                    "@id": "https://repo.metadatacenter.org/template-fields/8f742ccc-c634-466d-bf00-11ac9e00b8d5",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2022-01-17T01:57:34-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2022-01-17T01:57:34-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "@context": {
                    "additionalProperties": False,
                    "required": ["datasetIdentifier", "datasetIdentifierType"],
                    "type": "object",
                    "properties": {
                        "datasetIdentifier": {"enum": ["http://purl.org/dc/terms/identifier"]},
                        "datasetIdentifierType": {"enum": ["http://purl.org/spar/datacite/usesIdentifierScheme"]},
                    },
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
                "datasetIdentifierType": {
                    "pav:version": "0.0.1",
                    "_valueConstraints": {
                        "branches": [
                            {
                                "acronym": "FDC-GDMT",
                                "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                "maxDepth": 0,
                                "uri": "http://vocab.fairdatacollective.org/gdmt/IdentifierType",
                                "name": "Identifier Type",
                            }
                        ],
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": True,
                    },
                    "description": "identifierType field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "identifierType field schema",
                    "type": "object",
                    "skos:prefLabel": "Dataset Identifier Type",
                    "bibo:status": "bibo:draft",
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@id": {"type": "string", "format": "uri"},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                    },
                    "pav:createdOn": "2022-01-17T01:57:34-08:00",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "schema:name": "identifierType",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "pav:lastUpdatedOn": "2022-01-17T01:57:34-08:00",
                    "schema:description": "The type of Identifier",
                    "@id": "https://repo.metadatacenter.org/template-fields/bc76754a-2779-43cd-a0c8-abd3675816b4",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": ["@context", "@id", "datasetIdentifier", "datasetIdentifierType"],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "oslc:modifiedBy": {"type": ["string", "null"], "format": "uri"},
        "pav:derivedFrom": {"type": "string", "format": "uri"},
        "6_Subject": {
            "minItems": 0,
            "schema:identifier": "Subject",
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/087b8f3f-cde8-4ccb-8015-1f093f62a8d2",
            "type": "array",
            "items": {
                "pav:version": "0.0.1",
                "schema:name": "6_Subject",
                "description": "6_Subject field schema generated by the CEDAR Template Editor 2.6.16",
                "title": "6_Subject field schema",
                "type": "object",
                "skos:prefLabel": "Keyword(s)",
                "required": ["@context", "@id", "subjectSchemeIRI", "Subject", "valueURI"],
                "bibo:status": "bibo:draft",
                "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "properties": {
                    "subjectSchemeIRI": {
                        "_valueConstraints": {"requiredValue": False},
                        "skos:prefLabel": "Subject Scheme URI",
                        "bibo:status": "bibo:draft",
                        "_ui": {"hidden": True, "inputType": "textfield"},
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:schemaVersion": "1.6.0",
                        "title": "schemeURI field schema",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "type": "object",
                        "schema:name": "schemeURI",
                        "description": "schemeURI field schema generated by the CEDAR Template Editor 2.6.16",
                        "schema:description": "Ontology",
                        "@id": "https://repo.metadatacenter.org/template-fields/070ba7de-0695-48b5-acc3-a5da2fddf3b4",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:version": "0.0.1",
                        "pav:createdOn": "2022-01-20T00:19:53-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "pav:lastUpdatedOn": "2022-01-20T00:19:53-08:00",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "valueURI": {
                        "skos:prefLabel": "Subject Value URI",
                        "_valueConstraints": {
                            "branches": [],
                            "multipleChoice": False,
                            "ontologies": [
                                {
                                    "acronym": "EFO",
                                    "numTerms": 28815,
                                    "name": "Experimental Factor Ontology",
                                    "uri": "https://data.bioontology.org/ontologies/EFO",
                                }
                            ],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "valueURI field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "valueURI field schema",
                        "pav:lastUpdatedOn": "2022-01-20T00:19:53-08:00",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2022-01-20T00:19:53-08:00",
                        "_ui": {"hidden": True, "inputType": "textfield"},
                        "schema:name": "valueURI",
                        "@id": "https://repo.metadatacenter.org/template-fields/3fa88d17-a64c-44c0-bf72-c40477d67c04",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The URI of the subject term",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "@context": {
                        "additionalProperties": False,
                        "required": ["subjectSchemeIRI", "Subject", "valueURI"],
                        "type": "object",
                        "properties": {
                            "subjectSchemeIRI": {
                                "enum": ["http://vocab.fairdatacollective.org/gdmt/hasSubjectSchemeIRI"]
                            },
                            "valueURI": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/af9c45ec-d971-4056-a6c2-5ce930b9b181"
                                ]
                            },
                            "Subject": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/71f1a80c-d59e-4d92-a084-4f22f219cb6e"
                                ]
                            },
                        },
                    },
                    "@id": {"type": "string", "format": "uri"},
                    "@type": {
                        "oneOf": [
                            {"type": "string", "format": "uri"},
                            {
                                "minItems": 1,
                                "items": {"type": "string", "format": "uri"},
                                "uniqueItems": True,
                                "type": "array",
                            },
                        ]
                    },
                    "Subject": {
                        "skos:prefLabel": "Keywords",
                        "_valueConstraints": {
                            "branches": [],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "Subject field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "Subject field schema",
                        "pav:lastUpdatedOn": "2022-01-20T00:19:53-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2022-01-20T00:19:53-08:00",
                        "_ui": {"hidden": False, "inputType": "textfield"},
                        "schema:name": "Subject",
                        "@id": "https://repo.metadatacenter.org/template-fields/f6d9c5c3-f376-4744-852b-dbc84ba940ab",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "Keywords describing the data source subjects, methods, protocols, etc.",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                },
                "pav:createdOn": "2022-01-30T23:31:11-08:00",
                "_ui": {
                    "propertyDescriptions": {
                        "subjectSchemeIRI": "Ontology",
                        "valueURI": "The URI of the subject term",
                        "Subject": "Keywords describing the data source subjects, methods, protocols, etc.",
                    },
                    "propertyLabels": {"subjectSchemeIRI": "schemeURI", "valueURI": "valueURI", "Subject": "Subject"},
                    "order": ["Subject", "subjectSchemeIRI", "valueURI"],
                },
                "schema:schemaVersion": "1.6.0",
                "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "additionalProperties": False,
                "@context": {
                    "schema:name": {"@type": "xsd:string"},
                    "pav": "http://purl.org/pav/",
                    "bibo": "http://purl.org/ontology/bibo/",
                    "oslc": "http://open-services.net/ns/core#",
                    "schema:description": {"@type": "xsd:string"},
                    "pav:createdOn": {"@type": "xsd:dateTime"},
                    "pav:createdBy": {"@type": "@id"},
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                    "oslc:modifiedBy": {"@type": "@id"},
                    "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                    "schema": "http://schema.org/",
                },
                "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
                "schema:description": "Concepts that define the dataset or purpose sourced from controlled vocabulary.",
                "@id": "https://repo.metadatacenter.org/template-elements/fc4e957d-637c-4a00-b371-d9e981ce3af4",
                "@type": "https://schema.metadatacenter.org/core/TemplateElement",
                "$schema": "http://json-schema.org/draft-04/schema#",
            },
        },
        "7_Contributor": {
            "minItems": 0,
            "schema:identifier": "Contributor",
            "type": "array",
            "items": {
                "pav:version": "0.0.1",
                "schema:name": "7_Contributor",
                "description": "7_Contributor field schema generated by the CEDAR Template Editor 2.6.16",
                "title": "7_Contributor field schema",
                "type": "object",
                "skos:prefLabel": "Contributor(s)",
                "required": [
                    "@context",
                    "@id",
                    "contributorType",
                    "contributorIdentifier",
                    "contributorIdentifierScheme",
                    "contributorGivenName",
                    "contributorFamilyName",
                    "contributorEmail",
                    "contributorFullName",
                    "contributorAffiliation",
                ],
                "bibo:status": "bibo:draft",
                "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "properties": {
                    "contributorIdentifierScheme": {
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "FDC-GDMT",
                                    "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                    "maxDepth": 0,
                                    "uri": "http://vocab.fairdatacollective.org/gdmt/IdentifierScheme",
                                    "name": "Identifier Scheme",
                                }
                            ],
                            "defaultValue": {"rdfs:label": "ORCiD", "termUri": "https://orcid.org/"},
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "skos:prefLabel": "Contributor Identifier Scheme",
                        "bibo:status": "bibo:draft",
                        "_ui": {"inputType": "textfield"},
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "pav:derivedFrom": "https://repo.metadatacenter.org/template-fields/94536fac-30a0-4ec6-8a3e-372dbb525678",
                        "schema:schemaVersion": "1.6.0",
                        "title": "contributorNameIdentifierScheme field schema",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "type": "object",
                        "schema:name": "contributorNameIdentifierScheme",
                        "description": "contributorNameIdentifierScheme field schema generated by the CEDAR Template Editor 2.6.16",
                        "schema:description": "The name of the name identifier scheme",
                        "@id": "https://repo.metadatacenter.org/template-fields/82817054-a9cc-48d9-b07d-9570274ec7d1",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:version": "0.0.1",
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "additionalProperties": False,
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contributorAffiliation": {
                        "skos:prefLabel": "Contributor Affiliation",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "ZONMW-GENERIC",
                                    "source": "ZonMw Generic Terms (ZONMW-GENERIC)",
                                    "maxDepth": 0,
                                    "uri": "http://purl.org/zonmw/generic/10027",
                                    "name": "institution",
                                }
                            ],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "contributorAffiliation field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contributorAffiliation field schema",
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contributorAffiliation",
                        "@id": "https://repo.metadatacenter.org/template-fields/ea1f3ddd-611c-482f-b022-176d15a64510",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The organizational or institutional affiliation of the contributor",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contributorFullName": {
                        "skos:prefLabel": "Contributor Full Name",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contributorFullName field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contributorFullName field schema",
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "_ui": {"hidden": True, "inputType": "textfield"},
                        "schema:name": "contributorFullName",
                        "@id": "https://repo.metadatacenter.org/template-fields/ff9cf262-2402-4e43-bde3-f8b104501673",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contributorIdentifier": {
                        "_valueConstraints": {"requiredValue": False},
                        "skos:prefLabel": "Contributor Identifier",
                        "bibo:status": "bibo:draft",
                        "_ui": {"inputType": "textfield"},
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "pav:derivedFrom": "https://repo.metadatacenter.org/template-fields/115a2fd8-72a6-48e9-af99-8fc72f982cbb",
                        "schema:schemaVersion": "1.6.0",
                        "title": "contributorNameIdentifier field schema",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "type": "object",
                        "schema:name": "contributorNameIdentifier",
                        "description": "contributorNameIdentifier field schema generated by the CEDAR Template Editor 2.6.16",
                        "schema:description": "Uniquely identifies an individual or legal entity, according to various schemes",
                        "@id": "https://repo.metadatacenter.org/template-fields/683a7926-3743-431d-996c-240f28410e84",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:version": "0.0.1",
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contributorFamilyName": {
                        "skos:prefLabel": "Contributor Last Name",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contributorFamilyName field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contributorFamilyName field schema",
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contributorFamilyName",
                        "@id": "https://repo.metadatacenter.org/template-fields/581f1e1b-ab73-4883-8266-02a2742b86a5",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The surname or last name of the contributor",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contributorEmail": {
                        "skos:prefLabel": "Contributor Email",
                        "_valueConstraints": {"requiredValue": False},
                        "description": "contributorEmail field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contributorEmail field schema",
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "_ui": {"inputType": "email"},
                        "schema:name": "contributorEmail",
                        "@id": "https://repo.metadatacenter.org/template-fields/ad1434e1-d542-4ea1-9180-f7cf8545af73",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The email address of the contributor",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contributorType": {
                        "@id": "https://repo.metadatacenter.org/template-fields/94963cbe-1b05-46ff-82e1-67392c1ef756",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "ZONMW-GENERIC",
                                    "source": "undefined (ZONMW-GENERIC)",
                                    "maxDepth": 0,
                                    "uri": "http://purl.org/zonmw/generic/10075",
                                    "name": "contributor type",
                                }
                            ],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "contributorType field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contributorType field schema",
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contributorType",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "skos:prefLabel": "Contributor Type",
                        "schema:description": "The type of contributor of the resource",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                    },
                    "contributorGivenName": {
                        "skos:prefLabel": "Contributor First Name",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contributorGivenName field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contributorGivenName field schema",
                        "pav:lastUpdatedOn": "2021-12-08T03:34:34-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2021-12-08T03:34:34-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contributorGivenName",
                        "@id": "https://repo.metadatacenter.org/template-fields/dd6848c7-fc04-439f-9c6a-cd329852c69d",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The personal or first name of the contributor",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "@context": {
                        "additionalProperties": False,
                        "required": [
                            "contributorType",
                            "contributorIdentifier",
                            "contributorIdentifierScheme",
                            "contributorGivenName",
                            "contributorFamilyName",
                            "contributorEmail",
                            "contributorFullName",
                            "contributorAffiliation",
                        ],
                        "type": "object",
                        "properties": {
                            "contributorIdentifierScheme": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/264bff35-9c7e-4a84-a722-712217dfa232"
                                ]
                            },
                            "contributorAffiliation": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/73214405-3002-4fde-8f6c-b012faf907ec"
                                ]
                            },
                            "contributorFullName": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/272d6c5e-467c-4c01-a513-23b8df92585d"
                                ]
                            },
                            "contributorIdentifier": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/4636604a-6a42-4257-8a34-b8c68627cf32"
                                ]
                            },
                            "contributorFamilyName": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/510d9317-3658-429b-b773-8f9c0d288668"
                                ]
                            },
                            "contributorType": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/4d0bd488-6d4a-4388-bfa9-3cbb1d941afb"
                                ]
                            },
                            "contributorGivenName": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/1b2e719d-c7cc-4db0-b6f8-22ccdf43a387"
                                ]
                            },
                            "contributorEmail": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/72eb0553-76b7-4ef2-898f-694aa015cdd4"
                                ]
                            },
                        },
                    },
                    "@id": {"type": "string", "format": "uri"},
                    "@type": {
                        "oneOf": [
                            {"type": "string", "format": "uri"},
                            {
                                "minItems": 1,
                                "items": {"type": "string", "format": "uri"},
                                "uniqueItems": True,
                                "type": "array",
                            },
                        ]
                    },
                },
                "pav:createdOn": "2022-01-30T23:31:11-08:00",
                "_ui": {
                    "propertyDescriptions": {
                        "contributorIdentifierScheme": "The name of the name identifier scheme",
                        "contributorAffiliation": "The organizational or institutional affiliation of the contributor",
                        "contributorFullName": "",
                        "contributorIdentifier": "Uniquely identifies an individual or legal entity, according to various schemes",
                        "contributorFamilyName": "The surname or last name of the contributor",
                        "contributorType": "The type of contributor of the resource",
                        "contributorGivenName": "The personal or first name of the contributor",
                        "contributorEmail": "The email address of the contributor",
                    },
                    "propertyLabels": {
                        "contributorIdentifierScheme": "contributorNameIdentifierScheme",
                        "contributorAffiliation": "contributorAffiliation",
                        "contributorFullName": "contributorFullName",
                        "contributorIdentifier": "contributorNameIdentifier",
                        "contributorFamilyName": "contributorFamilyName",
                        "contributorType": "contributorType",
                        "contributorGivenName": "contributorGivenName",
                        "contributorEmail": "contributorEmail",
                    },
                    "order": [
                        "contributorType",
                        "contributorFullName",
                        "contributorGivenName",
                        "contributorFamilyName",
                        "contributorEmail",
                        "contributorIdentifier",
                        "contributorIdentifierScheme",
                        "contributorAffiliation",
                    ],
                },
                "schema:schemaVersion": "1.6.0",
                "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "additionalProperties": False,
                "@context": {
                    "schema:name": {"@type": "xsd:string"},
                    "pav": "http://purl.org/pav/",
                    "bibo": "http://purl.org/ontology/bibo/",
                    "oslc": "http://open-services.net/ns/core#",
                    "schema:description": {"@type": "xsd:string"},
                    "pav:createdOn": {"@type": "xsd:dateTime"},
                    "pav:createdBy": {"@type": "@id"},
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                    "oslc:modifiedBy": {"@type": "@id"},
                    "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                    "schema": "http://schema.org/",
                },
                "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
                "schema:description": "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property.",
                "@id": "https://repo.metadatacenter.org/template-elements/1d979a88-1028-421d-a124-11b5011f278a",
                "@type": "https://schema.metadatacenter.org/core/TemplateElement",
                "$schema": "http://json-schema.org/draft-04/schema#",
            },
        },
        "2_Creator": {
            "skos:prefLabel": "Creator",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {
                    "creatorIdentifier": "",
                    "creatorIdentifierSchemeIRI": "The URI of the name identifier scheme",
                    "creatorGivenName": "The personal or first name of the creator",
                    "creatorAffiliation": "The organizational or institutional affiliation of the creator",
                    "creatorIdentifierScheme": "The name of the name identifier scheme",
                    "creatorFamilyName": "The surname or last name of the creator",
                    "creatorFullName": "",
                },
                "propertyLabels": {
                    "creatorIdentifier": "creatorNameIdentifier",
                    "creatorIdentifierSchemeIRI": "creatorSchemeURI",
                    "creatorGivenName": "creatorGivenName",
                    "creatorAffiliation": "creatorAffiliation",
                    "creatorIdentifierScheme": "creatorNameIdentifierScheme",
                    "creatorFamilyName": "creatorFamilyName",
                    "creatorFullName": "creatorFullName",
                },
                "order": [
                    "creatorFullName",
                    "creatorGivenName",
                    "creatorFamilyName",
                    "creatorIdentifier",
                    "creatorIdentifierScheme",
                    "creatorIdentifierSchemeIRI",
                    "creatorAffiliation",
                ],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "schema:schemaVersion": "1.6.0",
            "title": "2_creator element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "2_Creator",
            "description": "2_creator element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "Creator",
            "schema:description": "The main researcher involved in producing the data.",
            "@id": "https://repo.metadatacenter.org/template-elements/d2e97c7c-90b7-44c4-8d4b-2c43d46c98a9",
            "properties": {
                "creatorIdentifier": {
                    "_valueConstraints": {
                        "minLength": 19,
                        "defaultValue": "0000-0000-0000-0000",
                        "maxLength": 19,
                        "requiredValue": False,
                    },
                    "skos:prefLabel": "ORCID",
                    "bibo:status": "bibo:draft",
                    "_ui": {"inputType": "textfield"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "pav:derivedFrom": "https://repo.metadatacenter.org/template-fields/d221f8bc-d533-4799-ad7d-b33d6846ee98",
                    "schema:schemaVersion": "1.6.0",
                    "title": "creatorNameIdentifier field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "creatorNameIdentifier",
                    "description": "creatorNameIdentifier field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "",
                    "@id": "https://repo.metadatacenter.org/template-fields/7e0529bc-b625-4287-a00e-1e334c90904e",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "creatorIdentifierSchemeIRI": {
                    "_valueConstraints": {
                        "branches": [
                            {
                                "acronym": "FDC-GDMT",
                                "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                "maxDepth": 0,
                                "uri": "http://vocab.fairdatacollective.org/gdmt/IdentifierScheme",
                                "name": "Identifier Scheme",
                            }
                        ],
                        "defaultValue": {"rdfs:label": "ORCiD", "termUri": "https://orcid.org/"},
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": False,
                    },
                    "skos:prefLabel": "Creator Identifier Scheme URI",
                    "bibo:status": "bibo:draft",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "pav:derivedFrom": "https://repo.metadatacenter.org/template-fields/4c5e4472-c959-432b-897f-4ee42be8fa32",
                    "schema:schemaVersion": "1.6.0",
                    "title": "creatorSchemeURI field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "creatorSchemeURI",
                    "description": "creatorSchemeURI field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "The URI of the name identifier scheme",
                    "@id": "https://repo.metadatacenter.org/template-fields/317e8e84-f660-4ec0-9767-5526ebaf6318",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@id": {"type": "string", "format": "uri"},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "creatorGivenName": {
                    "skos:prefLabel": "First Name",
                    "_valueConstraints": {"requiredValue": True},
                    "description": "creatorGivenName field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "creatorGivenName field schema",
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "_ui": {"inputType": "textfield"},
                    "schema:name": "creatorGivenName",
                    "@id": "https://repo.metadatacenter.org/template-fields/aceef3c6-be17-4821-8a94-720bfd8fa4f1",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:description": "The personal or first name of the creator",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "creatorAffiliation": {
                    "skos:prefLabel": "Creator Affiliation",
                    "_valueConstraints": {
                        "branches": [
                            {
                                "acronym": "ZONMW-GENERIC",
                                "source": "undefined (ZONMW-GENERIC)",
                                "maxDepth": 0,
                                "uri": "http://purl.org/zonmw/generic/10027",
                                "name": "institution",
                            }
                        ],
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": False,
                    },
                    "description": "creatorAffiliation field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "creatorAffiliation field schema",
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@id": {"type": "string", "format": "uri"},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                    },
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "schema:name": "creatorAffiliation",
                    "@id": "https://repo.metadatacenter.org/template-fields/032a7947-adcf-4e31-a619-43e3ee30b87d",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:description": "The organizational or institutional affiliation of the creator",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "creatorIdentifierScheme": {
                    "_valueConstraints": {
                        "branches": [
                            {
                                "acronym": "FDC-GDMT",
                                "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                "maxDepth": 0,
                                "uri": "http://vocab.fairdatacollective.org/gdmt/IdentifierScheme",
                                "name": "Identifier Scheme",
                            }
                        ],
                        "defaultValue": {"rdfs:label": "ORCiD", "termUri": "https://orcid.org/"},
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": False,
                    },
                    "skos:prefLabel": "Creator Identifier Scheme",
                    "bibo:status": "bibo:draft",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "pav:derivedFrom": "https://repo.metadatacenter.org/template-fields/7bf1cf76-2edc-4d4b-9c67-a84bb161c6ec",
                    "schema:schemaVersion": "1.6.0",
                    "title": "creatorNameIdentifierScheme field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "creatorNameIdentifierScheme",
                    "description": "creatorNameIdentifierScheme field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "The name of the name identifier scheme",
                    "@id": "https://repo.metadatacenter.org/template-fields/c6f1a433-c7b7-4817-8a5c-54415eb8c1ad",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@id": {"type": "string", "format": "uri"},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "creatorFamilyName": {
                    "skos:prefLabel": "Last Name",
                    "_valueConstraints": {"requiredValue": True},
                    "description": "creatorFamilyName field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "creatorFamilyName field schema",
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "_ui": {"inputType": "textfield"},
                    "schema:name": "creatorFamilyName",
                    "@id": "https://repo.metadatacenter.org/template-fields/7a8ffdf1-8d46-491c-8ada-8f36f289953a",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:description": "The surname or last name of the creator",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "creatorFullName": {
                    "skos:prefLabel": "Creator Full Name",
                    "_valueConstraints": {"requiredValue": True},
                    "description": "creatorFullName field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "creatorFullName field schema",
                    "pav:lastUpdatedOn": "2021-11-24T01:43:12-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:createdOn": "2021-11-24T01:43:12-08:00",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "schema:name": "creatorFullName",
                    "@id": "https://repo.metadatacenter.org/template-fields/e089d9b5-7908-4dee-97cd-d27e70675d3f",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:description": "",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "@context": {
                    "additionalProperties": False,
                    "required": [
                        "creatorIdentifier",
                        "creatorIdentifierScheme",
                        "creatorIdentifierSchemeIRI",
                        "creatorAffiliation",
                        "creatorGivenName",
                        "creatorFamilyName",
                        "creatorFullName",
                    ],
                    "type": "object",
                    "properties": {
                        "creatorIdentifier": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/18e308f9-0286-4d53-9acf-45b64cf13409"
                            ]
                        },
                        "creatorIdentifierSchemeIRI": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/47dbf3ad-a626-47f9-814c-df36df9959bc"
                            ]
                        },
                        "creatorGivenName": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/70630a4c-d76f-46b2-902c-916203a981a1"
                            ]
                        },
                        "creatorAffiliation": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/11ea34dd-138e-4901-8565-c56e8cf980ca"
                            ]
                        },
                        "creatorIdentifierScheme": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/2a4230e0-9dc4-4477-bea8-a718e32106af"
                            ]
                        },
                        "creatorFamilyName": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/356309ef-b052-41ad-97b6-a30f76ba6df4"
                            ]
                        },
                        "creatorFullName": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/34cd0986-098c-4c76-830c-300966ad422a"
                            ]
                        },
                    },
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": [
                "@context",
                "@id",
                "creatorIdentifier",
                "creatorIdentifierScheme",
                "creatorIdentifierSchemeIRI",
                "creatorAffiliation",
                "creatorGivenName",
                "creatorFamilyName",
                "creatorFullName",
            ],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "@id": {"type": ["string", "null"], "format": "uri"},
        "4_Publisher": {
            "skos:prefLabel": "Publisher",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {
                    "Publisher": "The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource"
                },
                "propertyLabels": {"Publisher": "Publisher"},
                "order": ["Publisher"],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "schema:schemaVersion": "1.6.0",
            "title": "4_publisher element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "4_Publisher",
            "description": "4_publisher element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "Publisher",
            "schema:description": "The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
            "@id": "https://repo.metadatacenter.org/template-elements/331f86b7-17c5-4c1c-8be1-41d1c9e084a0",
            "properties": {
                "@context": {
                    "additionalProperties": False,
                    "required": ["Publisher"],
                    "type": "object",
                    "properties": {
                        "Publisher": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/2c80f739-e2c4-425e-9bf0-fa20fffe29ba"
                            ]
                        }
                    },
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
                "Publisher": {
                    "@id": "https://repo.metadatacenter.org/template-fields/16d865ca-bef2-4909-b4c4-421df509a2d0",
                    "_valueConstraints": {"defaultValue": "DataHub", "requiredValue": True},
                    "description": "Publisher field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "Publisher field schema",
                    "pav:lastUpdatedOn": "2021-11-23T02:19:54-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:createdOn": "2021-11-23T02:19:54-08:00",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "schema:name": "Publisher",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "skos:prefLabel": "Publisher",
                    "schema:description": "The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": ["@context", "@id", "Publisher"],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "pav:createdBy": {"type": ["string", "null"], "format": "uri"},
        "@context": {
            "additionalProperties": False,
            "required": [
                "xsd",
                "pav",
                "schema",
                "oslc",
                "schema:isBasedOn",
                "schema:name",
                "schema:description",
                "pav:createdOn",
                "pav:createdBy",
                "pav:lastUpdatedOn",
                "oslc:modifiedBy",
                "4_Publisher",
                "8_Date",
                "2_Creator",
                "12_RelatedIdentifier",
                "7_Contributor",
                "3_Title",
                "1_Identifier",
                "17_Description",
                "6_Subject",
                "10_ResourceType",
                "7_ContactPerson",
            ],
            "type": "object",
            "properties": {
                "schema:isBasedOn": {"type": "object", "properties": {"@type": {"enum": ["@id"], "type": "string"}}},
                "pav:createdOn": {
                    "type": "object",
                    "properties": {"@type": {"enum": ["xsd:dateTime"], "type": "string"}},
                },
                "oslc:modifiedBy": {"type": "object", "properties": {"@type": {"enum": ["@id"], "type": "string"}}},
                "pav:derivedFrom": {"type": "object", "properties": {"@type": {"enum": ["@id"], "type": "string"}}},
                "skos": {"enum": ["http://www.w3.org/2004/02/skos/core#"], "type": "string", "format": "uri"},
                "6_Subject": {
                    "enum": ["https://schema.metadatacenter.org/properties/d8dc1860-b3a5-4547-ad22-0e003dc2e5fc"]
                },
                "7_Contributor": {
                    "enum": ["https://schema.metadatacenter.org/properties/45bffde9-fe61-4479-a70d-953e3aa4a9c9"]
                },
                "2_Creator": {
                    "enum": ["https://schema.metadatacenter.org/properties/6297f721-5a92-4014-9a7d-2eeb9afbe11b"]
                },
                "oslc": {"enum": ["http://open-services.net/ns/core#"], "type": "string", "format": "uri"},
                "pav": {"enum": ["http://purl.org/pav/"], "type": "string", "format": "uri"},
                "rdfs": {"enum": ["http://www.w3.org/2000/01/rdf-schema#"], "type": "string", "format": "uri"},
                "4_Publisher": {
                    "enum": ["https://schema.metadatacenter.org/properties/68a521c1-69af-49e5-95a0-9890642da26d"]
                },
                "pav:createdBy": {"type": "object", "properties": {"@type": {"enum": ["@id"], "type": "string"}}},
                "8_Date": {
                    "enum": ["https://schema.metadatacenter.org/properties/29cd27ea-b7b6-47b7-a82d-ab48ae34396d"]
                },
                "rdfs:label": {"type": "object", "properties": {"@type": {"enum": ["xsd:string"], "type": "string"}}},
                "schema:name": {"type": "object", "properties": {"@type": {"enum": ["xsd:string"], "type": "string"}}},
                "3_Title": {"enum": ["http://purl.org/dc/terms/title"]},
                "7_ContactPerson": {
                    "enum": ["https://schema.metadatacenter.org/properties/9ae72767-4449-4018-9cf0-6da73604d0cc"]
                },
                "schema:description": {
                    "type": "object",
                    "properties": {"@type": {"enum": ["xsd:string"], "type": "string"}},
                },
                "skos:notation": {
                    "type": "object",
                    "properties": {"@type": {"enum": ["xsd:string"], "type": "string"}},
                },
                "1_Identifier": {
                    "enum": ["https://schema.metadatacenter.org/properties/b260286d-3da0-4f53-a40d-eb769c24da8f"]
                },
                "12_RelatedIdentifier": {
                    "enum": ["https://schema.metadatacenter.org/properties/65f55a39-f020-45d6-a071-c8388a12a25f"]
                },
                "17_Description": {
                    "enum": ["https://schema.metadatacenter.org/properties/28d418d7-bfe7-44fb-968f-6e3ae9b68501"]
                },
                "10_ResourceType": {
                    "enum": ["https://schema.metadatacenter.org/properties/8f154e9c-501a-4b80-b148-a74f250edc69"]
                },
                "xsd": {"enum": ["http://www.w3.org/2001/XMLSchema#"], "type": "string", "format": "uri"},
                "schema": {"enum": ["http://schema.org/"], "type": "string", "format": "uri"},
                "pav:lastUpdatedOn": {
                    "type": "object",
                    "properties": {"@type": {"enum": ["xsd:dateTime"], "type": "string"}},
                },
            },
        },
        "8_Date": {
            "skos:prefLabel": "Date",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {
                    "datasetDateType": "The type of date",
                    "datasetDate": "Date relevant to the work",
                },
                "propertyLabels": {"datasetDateType": "submissionDateType", "datasetDate": "submissionDate"},
                "order": ["datasetDate", "datasetDateType"],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/efae07be-d119-4437-adc7-f13e4f83dd11",
            "schema:schemaVersion": "1.6.0",
            "title": "8_date element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "8_Date",
            "description": "8_date element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "Date",
            "schema:description": "Relevant dates related to the resource being described.",
            "@id": "https://repo.metadatacenter.org/template-elements/1bf3e3d6-c05e-43c6-b39d-c60080365268",
            "properties": {
                "@context": {
                    "additionalProperties": False,
                    "required": ["datasetDateType", "datasetDate"],
                    "type": "object",
                    "properties": {
                        "datasetDateType": {"enum": ["http://vocab.fairdatacollective.org/gdmt/hasDatasetDateType"]},
                        "datasetDate": {"enum": ["http://vocab.fairdatacollective.org/gdmt/hasDatasetDate"]},
                    },
                },
                "datasetDateType": {
                    "pav:version": "0.0.1",
                    "_valueConstraints": {
                        "branches": [
                            {
                                "acronym": "FDC-GDMT",
                                "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                "maxDepth": 0,
                                "uri": "http://vocab.fairdatacollective.org/gdmt/DateType",
                                "name": "Date Type",
                            }
                        ],
                        "defaultValue": {
                            "rdfs:label": "Submitted",
                            "termUri": "http://vocab.fairdatacollective.org/gdmt/Submitted",
                        },
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": True,
                    },
                    "description": "submissionDateType field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "submissionDateType field schema",
                    "type": "object",
                    "skos:prefLabel": "Submission Date Type",
                    "bibo:status": "bibo:draft",
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@id": {"type": "string", "format": "uri"},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                    },
                    "pav:createdOn": "2021-11-23T02:36:30-08:00",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "schema:name": "submissionDateType",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "pav:lastUpdatedOn": "2021-11-23T02:36:30-08:00",
                    "schema:description": "The type of date",
                    "@id": "https://repo.metadatacenter.org/template-fields/3799524f-31bb-420c-93c5-60f2d1db44ae",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
                "datasetDate": {
                    "_valueConstraints": {"temporalType": "xsd:date", "requiredValue": True},
                    "skos:prefLabel": "Submission Date",
                    "bibo:status": "bibo:draft",
                    "_ui": {"temporalGranularity": "day", "inputType": "temporal"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:schemaVersion": "1.6.0",
                    "title": "submissionDate field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "submissionDate",
                    "description": "submissionDate field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "Date relevant to the work",
                    "@id": "https://repo.metadatacenter.org/template-fields/1b0531e6-498f-4e57-8ce9-54980cbf3c3a",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2021-11-23T02:36:30-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2021-11-23T02:36:30-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": ["@context", "@id", "datasetDateType", "datasetDate"],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "schema:isBasedOn": {"type": "string", "format": "uri"},
        "schema:name": {"minLength": 1, "type": "string"},
        "3_Title": {
            "skos:prefLabel": "Title",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {"title": "A name or title by which the dataset being described is known"},
                "propertyLabels": {"title": "Title"},
                "order": ["title"],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/d593dc15-f218-4af7-a2da-0ce6fdd4f6b6",
            "schema:schemaVersion": "1.6.0",
            "title": "3_title element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "3_Title",
            "description": "3_title element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "Title",
            "schema:description": "A name or title by which the dataset being described is known.",
            "@id": "https://repo.metadatacenter.org/template-elements/83367232-64e2-4117-9797-98f0d2694698",
            "properties": {
                "@context": {
                    "additionalProperties": False,
                    "required": ["title"],
                    "type": "object",
                    "properties": {
                        "title": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/4ffd7c46-1df8-4885-ade4-50d542d5b81e"
                            ]
                        }
                    },
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
                "title": {
                    "_valueConstraints": {"requiredValue": True},
                    "skos:prefLabel": "Dataset Title",
                    "bibo:status": "bibo:draft",
                    "_ui": {"inputType": "textfield"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:schemaVersion": "1.6.0",
                    "title": "Title field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "Title",
                    "description": "Title field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "A name or title by which the dataset being described is known",
                    "@id": "https://repo.metadatacenter.org/template-fields/e80eaba5-c98b-4598-b5cc-af781b60fa86",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2022-01-06T05:12:52-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2022-01-06T05:12:52-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": ["@context", "@id", "title"],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "7_ContactPerson": {
            "minItems": 1,
            "items": {
                "pav:version": "0.0.1",
                "schema:name": "7_ContactPerson",
                "description": "7_ContactPerson field schema generated by the CEDAR Template Editor 2.6.16",
                "title": "7_ContactPerson field schema",
                "type": "object",
                "skos:prefLabel": "Contact Person",
                "required": [
                    "@context",
                    "@id",
                    "contactType",
                    "contactGivenName",
                    "contactFamilyName",
                    "contactEmail",
                    "contactFullName",
                    "contactAffiliation",
                    "contactNameIdentifier",
                    "contactNameIdentifierScheme",
                ],
                "bibo:status": "bibo:draft",
                "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "properties": {
                    "contactFullName": {
                        "skos:prefLabel": "Contact Person Full Name",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contactFullName field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactFullName field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"hidden": True, "inputType": "textfield"},
                        "schema:name": "contactFullName",
                        "@id": "https://repo.metadatacenter.org/template-fields/d15b083e-f4ea-4f2e-a46b-15f41c876b9c",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactAffiliation": {
                        "skos:prefLabel": "Contact Person Affiliation",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "ZONMW-GENERIC",
                                    "source": "ZonMw Generic Terms (ZONMW-GENERIC)",
                                    "maxDepth": 0,
                                    "uri": "http://purl.org/zonmw/generic/10027",
                                    "name": "institution",
                                }
                            ],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "contactAffiliation field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactAffiliation field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contactAffiliation",
                        "@id": "https://repo.metadatacenter.org/template-fields/3aaaba6a-679a-49db-ae05-cff91a9db625",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The organizational or institutional affiliation of the contact person",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactNameIdentifier": {
                        "skos:prefLabel": "Contact Person Identifier",
                        "_valueConstraints": {"requiredValue": False},
                        "description": "contactNameIdentifier field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactNameIdentifier field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contactNameIdentifier",
                        "@id": "https://repo.metadatacenter.org/template-fields/c8211d44-f0db-4d2c-becc-719e16e3c9b0",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "Uniquely identifies an individual or legal entity, according to various schemes",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactEmail": {
                        "skos:prefLabel": "Contact Person Email",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contactEmail field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactEmail field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"inputType": "email"},
                        "schema:name": "contactEmail",
                        "@id": "https://repo.metadatacenter.org/template-fields/ad1434e1-d542-4ea1-9180-f7cf8545af73",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactNameIdentifierScheme": {
                        "skos:prefLabel": "Contact Person Identifier Scheme",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "FDC-GDMT",
                                    "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                    "maxDepth": 0,
                                    "uri": "http://vocab.fairdatacollective.org/gdmt/IdentifierScheme",
                                    "name": "Identifier Scheme",
                                }
                            ],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "contactNameIdentifierScheme field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactNameIdentifierScheme field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contactNameIdentifierScheme",
                        "@id": "https://repo.metadatacenter.org/template-fields/fe017d4e-36fb-43c3-b302-6de6f03dc1c7",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "The name of the name identifier scheme",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactFamilyName": {
                        "skos:prefLabel": "Contact Person Last Name",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contactFamilyName field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactFamilyName field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "contactFamilyName",
                        "@id": "https://repo.metadatacenter.org/template-fields/581f1e1b-ab73-4883-8266-02a2742b86a5",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactGivenName": {
                        "skos:prefLabel": "Contact Person First Name",
                        "_valueConstraints": {"requiredValue": True},
                        "description": "contactGivenName field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactGivenName field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"hidden": False, "inputType": "textfield"},
                        "schema:name": "contactGivenName",
                        "@id": "https://repo.metadatacenter.org/template-fields/dd6848c7-fc04-439f-9c6a-cd329852c69d",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:description": "",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "contactType": {
                        "@id": "https://repo.metadatacenter.org/template-fields/94963cbe-1b05-46ff-82e1-67392c1ef756",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "ZONMW-GENERIC",
                                    "source": "undefined (ZONMW-GENERIC)",
                                    "maxDepth": 0,
                                    "uri": "http://purl.org/zonmw/generic/10075",
                                    "name": "contributor type",
                                }
                            ],
                            "defaultValue": {
                                "rdfs:label": "contact person",
                                "termUri": "http://purl.org/zonmw/generic/10089",
                            },
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "contactType field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "contactType field schema",
                        "pav:lastUpdatedOn": "2022-01-30T23:25:55-08:00",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2022-01-30T23:25:55-08:00",
                        "_ui": {"hidden": True, "inputType": "textfield"},
                        "schema:name": "contactType",
                        "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "skos:prefLabel": "Contact Type",
                        "schema:description": "The type of contributor of the resource",
                        "type": "object",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                    },
                    "@context": {
                        "additionalProperties": False,
                        "required": [
                            "contactType",
                            "contactGivenName",
                            "contactFamilyName",
                            "contactEmail",
                            "contactFullName",
                            "contactAffiliation",
                            "contactNameIdentifier",
                            "contactNameIdentifierScheme",
                        ],
                        "type": "object",
                        "properties": {
                            "contactFullName": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/9cc96e17-345e-43c1-955d-9777ef8136aa"
                                ]
                            },
                            "contactAffiliation": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/488e6114-b24f-4bf6-83b0-45a33abdabf6"
                                ]
                            },
                            "contactNameIdentifier": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/953598f5-f9f7-4276-899f-09851b9501d1"
                                ]
                            },
                            "contactEmail": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/72eb0553-76b7-4ef2-898f-694aa015cdd4"
                                ]
                            },
                            "contactNameIdentifierScheme": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/d680d7f5-ac6d-4fac-a245-37ca8e41a2f9"
                                ]
                            },
                            "contactFamilyName": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/510d9317-3658-429b-b773-8f9c0d288668"
                                ]
                            },
                            "contactGivenName": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/1b2e719d-c7cc-4db0-b6f8-22ccdf43a387"
                                ]
                            },
                            "contactType": {
                                "enum": [
                                    "https://schema.metadatacenter.org/properties/4d0bd488-6d4a-4388-bfa9-3cbb1d941afb"
                                ]
                            },
                        },
                    },
                    "@id": {"type": "string", "format": "uri"},
                    "@type": {
                        "oneOf": [
                            {"type": "string", "format": "uri"},
                            {
                                "minItems": 1,
                                "items": {"type": "string", "format": "uri"},
                                "uniqueItems": True,
                                "type": "array",
                            },
                        ]
                    },
                },
                "pav:createdOn": "2022-01-30T23:31:11-08:00",
                "_ui": {
                    "propertyDescriptions": {
                        "contactFullName": "",
                        "contactAffiliation": "The organizational or institutional affiliation of the contact person",
                        "contactNameIdentifier": "Uniquely identifies an individual or legal entity, according to various schemes",
                        "contactEmail": "",
                        "contactNameIdentifierScheme": "The name of the name identifier scheme",
                        "contactFamilyName": "",
                        "contactGivenName": "",
                        "contactType": "The type of contributor of the resource",
                    },
                    "propertyLabels": {
                        "contactFullName": "contactFullName",
                        "contactAffiliation": "contactAffiliation",
                        "contactNameIdentifier": "contactNameIdentifier",
                        "contactEmail": "contactEmail",
                        "contactNameIdentifierScheme": "contactNameIdentifierScheme",
                        "contactFamilyName": "contactFamilyName",
                        "contactGivenName": "contactGivenName",
                        "contactType": "contactType",
                    },
                    "order": [
                        "contactType",
                        "contactFullName",
                        "contactGivenName",
                        "contactFamilyName",
                        "contactEmail",
                        "contactNameIdentifier",
                        "contactNameIdentifierScheme",
                        "contactAffiliation",
                    ],
                },
                "schema:schemaVersion": "1.6.0",
                "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "additionalProperties": False,
                "@context": {
                    "schema:name": {"@type": "xsd:string"},
                    "pav": "http://purl.org/pav/",
                    "bibo": "http://purl.org/ontology/bibo/",
                    "oslc": "http://open-services.net/ns/core#",
                    "schema:description": {"@type": "xsd:string"},
                    "pav:createdOn": {"@type": "xsd:dateTime"},
                    "pav:createdBy": {"@type": "@id"},
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                    "oslc:modifiedBy": {"@type": "@id"},
                    "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                    "schema": "http://schema.org/",
                },
                "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
                "schema:description": "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property.",
                "@id": "https://repo.metadatacenter.org/template-elements/a5b4ede8-f284-4991-b2c0-2273b925b2ca",
                "@type": "https://schema.metadatacenter.org/core/TemplateElement",
                "$schema": "http://json-schema.org/draft-04/schema#",
            },
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/1d979a88-1028-421d-a124-11b5011f278a",
            "type": "array",
        },
        "schema:description": {"type": "string"},
        "datasetPagebreak": {
            "@id": "https://repo.metadatacenter.org/template-fields/d3bf9ef4-b9d8-45c2-b9b1-2872fe0c15c5",
            "schema:name": "datasetPagebreak",
            "description": "datasetPagebreak field schema generated by the CEDAR Template Editor 2.6.16",
            "title": "datasetPagebreak field schema",
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "additionalProperties": False,
            "schema:schemaVersion": "1.6.0",
            "schema:description": "Information with regards to the dataset",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "_ui": {"inputType": "page-break", "_content": None},
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "oslc": "http://open-services.net/ns/core#",
                "bibo": "http://purl.org/ontology/bibo/",
                "pav": "http://purl.org/pav/",
                "schema": "http://schema.org/",
            },
            "$schema": "http://json-schema.org/draft-04/schema#",
            "skos:prefLabel": "Dataset",
            "type": "object",
            "@type": "https://schema.metadatacenter.org/core/StaticTemplateField",
        },
        "pav:createdOn": {"type": ["string", "null"], "format": "date-time"},
        "17_Description": {
            "skos:prefLabel": "Description",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {
                    "descriptionType": "The type of the Description",
                    "Description": "Abstract and additional information. May be used for technical information.",
                },
                "propertyLabels": {"descriptionType": "descriptionType", "Description": "Description"},
                "order": ["Description", "descriptionType"],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "schema:schemaVersion": "1.6.0",
            "title": "17_description element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "17_Description",
            "description": "17_description element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "Description",
            "schema:description": "All additional information that does not fit in any of the other categories. May be used for technical information.",
            "@id": "https://repo.metadatacenter.org/template-elements/1595a50e-f0c0-47c6-804e-fff5ac7a7531",
            "properties": {
                "@context": {
                    "additionalProperties": False,
                    "required": ["Description", "descriptionType"],
                    "type": "object",
                    "properties": {
                        "descriptionType": {"enum": ["http://purl.org/spar/datacite/hasDescriptionType"]},
                        "Description": {"enum": ["http://purl.org/dc/terms/description"]},
                    },
                },
                "Description": {
                    "skos:prefLabel": "Description",
                    "_valueConstraints": {"requiredValue": True},
                    "description": "Description field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "Description field schema",
                    "pav:lastUpdatedOn": "2022-01-17T02:35:02-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:createdOn": "2022-01-17T02:35:02-08:00",
                    "_ui": {"inputType": "textarea"},
                    "schema:name": "Description",
                    "@id": "https://repo.metadatacenter.org/template-fields/546de7eb-dd21-4781-9477-922bd72bd2c5",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:description": "Abstract and additional information. May be used for technical information.",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
                "descriptionType": {
                    "skos:prefLabel": "Description Type",
                    "_valueConstraints": {
                        "branches": [],
                        "defaultValue": "Abstract",
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": False,
                    },
                    "description": "descriptionType field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "descriptionType field schema",
                    "pav:lastUpdatedOn": "2022-01-17T02:35:02-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:createdOn": "2022-01-17T02:35:02-08:00",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "schema:name": "descriptionType",
                    "@id": "https://repo.metadatacenter.org/template-fields/2ca64451-cea3-4825-b68c-9a396a0ac822",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "skos:altLabel": [],
                    "schema:description": "The type of the Description",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": ["@context", "@id", "Description", "descriptionType"],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "12_RelatedIdentifier": {
            "minItems": 0,
            "schema:identifier": "RelatedIdentifier",
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/3f77bfc0-6edf-47fa-b6ec-e73813b11e54",
            "type": "array",
            "items": {
                "pav:version": "0.0.1",
                "schema:name": "12_RelatedIdentifier",
                "description": "12_RelatedIdentifier field schema generated by the CEDAR Template Editor 2.6.16",
                "title": "12_RelatedIdentifier field schema",
                "type": "object",
                "skos:prefLabel": "Related Resource(s)",
                "required": [
                    "@context",
                    "@id",
                    "relatedResourceIdentifier",
                    "relatedResourceIdentifierType",
                    "relationType",
                ],
                "bibo:status": "bibo:draft",
                "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "properties": {
                    "relatedResourceIdentifier": {
                        "_valueConstraints": {
                            "branches": [],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "skos:prefLabel": "Related Resource Identifier",
                        "bibo:status": "bibo:draft",
                        "_ui": {"inputType": "textfield"},
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "schema:schemaVersion": "1.6.0",
                        "title": "RelatedIdentifier field schema",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "type": "object",
                        "schema:name": "RelatedIdentifier",
                        "description": "RelatedIdentifier field schema generated by the CEDAR Template Editor 2.6.16",
                        "schema:description": "Identifiers of related resources. These must be globally unique identifiers.",
                        "@id": "https://repo.metadatacenter.org/template-fields/3ed04713-6cfb-4f67-8670-a14fc88e6735",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                            "@value": {"type": ["string", "null"]},
                        },
                        "pav:version": "0.0.1",
                        "pav:createdOn": "2021-10-21T05:06:51-07:00",
                        "required": ["@value"],
                        "additionalProperties": False,
                        "pav:lastUpdatedOn": "2021-10-21T05:06:51-07:00",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                    },
                    "relatedResourceIdentifierType": {
                        "pav:version": "0.0.1",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "FDC-GDMT",
                                    "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                    "maxDepth": 0,
                                    "uri": "http://vocab.fairdatacollective.org/gdmt/IdentifierType",
                                    "name": "Identifier Type",
                                }
                            ],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "relatedIdentifierType field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "relatedIdentifierType field schema",
                        "type": "object",
                        "skos:prefLabel": "Related Resource Identifier Type",
                        "bibo:status": "bibo:draft",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2021-10-21T05:06:51-07:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "relatedIdentifierType",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "pav:lastUpdatedOn": "2021-10-21T05:06:51-07:00",
                        "schema:description": "The type of the RelatedIdentifier",
                        "@id": "https://repo.metadatacenter.org/template-fields/7ff0b82b-0eed-4aaa-921b-bd6a744fd292",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                    },
                    "relationType": {
                        "pav:version": "0.0.1",
                        "_valueConstraints": {
                            "branches": [
                                {
                                    "acronym": "FDC-GDMT",
                                    "source": "Ontology for Generic Dataset Metadata Template (FDC-GDMT)",
                                    "maxDepth": 0,
                                    "uri": "http://vocab.fairdatacollective.org/gdmt/RelationType",
                                    "name": "Relation Type",
                                }
                            ],
                            "multipleChoice": False,
                            "ontologies": [],
                            "classes": [],
                            "valueSets": [],
                            "requiredValue": False,
                        },
                        "description": "relationType field schema generated by the CEDAR Template Editor 2.6.16",
                        "title": "relationType field schema",
                        "type": "object",
                        "skos:prefLabel": "Relation Type",
                        "bibo:status": "bibo:draft",
                        "additionalProperties": False,
                        "schema:schemaVersion": "1.6.0",
                        "properties": {
                            "rdfs:label": {"type": ["string", "null"]},
                            "@id": {"type": "string", "format": "uri"},
                            "@type": {
                                "oneOf": [
                                    {"type": "string", "format": "uri"},
                                    {
                                        "minItems": 1,
                                        "items": {"type": "string", "format": "uri"},
                                        "uniqueItems": True,
                                        "type": "array",
                                    },
                                ]
                            },
                        },
                        "pav:createdOn": "2021-10-21T05:06:51-07:00",
                        "_ui": {"inputType": "textfield"},
                        "schema:name": "relationType",
                        "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                        "@context": {
                            "schema:name": {"@type": "xsd:string"},
                            "pav": "http://purl.org/pav/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "oslc": "http://open-services.net/ns/core#",
                            "schema:description": {"@type": "xsd:string"},
                            "pav:createdOn": {"@type": "xsd:dateTime"},
                            "pav:createdBy": {"@type": "@id"},
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                            "oslc:modifiedBy": {"@type": "@id"},
                            "skos:altLabel": {"@type": "xsd:string"},
                            "skos:prefLabel": {"@type": "xsd:string"},
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "schema": "http://schema.org/",
                        },
                        "pav:lastUpdatedOn": "2021-10-21T05:06:51-07:00",
                        "schema:description": "Description of the relationship of the object being described (A) to the related resource (B)",
                        "@id": "https://repo.metadatacenter.org/template-fields/29b81aed-bff0-441d-825a-823d7a9e6916",
                        "@type": "https://schema.metadatacenter.org/core/TemplateField",
                        "$schema": "http://json-schema.org/draft-04/schema#",
                    },
                    "@context": {
                        "additionalProperties": False,
                        "required": ["relatedResourceIdentifier", "relatedResourceIdentifierType", "relationType"],
                        "type": "object",
                        "properties": {
                            "relationType": {"enum": ["http://rs.tdwg.org/dwc/terms/relationshipOfResource"]},
                            "relatedResourceIdentifierType": {"enum": ["http://schema.org/propertyID"]},
                            "relatedResourceIdentifier": {"enum": ["http://purl.org/dc/terms/identifier"]},
                        },
                    },
                    "@id": {"type": "string", "format": "uri"},
                    "@type": {
                        "oneOf": [
                            {"type": "string", "format": "uri"},
                            {
                                "minItems": 1,
                                "items": {"type": "string", "format": "uri"},
                                "uniqueItems": True,
                                "type": "array",
                            },
                        ]
                    },
                },
                "pav:createdOn": "2022-01-30T23:31:11-08:00",
                "_ui": {
                    "propertyDescriptions": {
                        "relationType": "Description of the relationship of the object being described (A) to the related resource (B)",
                        "relatedResourceIdentifierType": "The type of the RelatedIdentifier",
                        "relatedResourceIdentifier": "Identifiers of related resources. These must be globally unique identifiers.",
                    },
                    "propertyLabels": {
                        "relationType": "relationType",
                        "relatedResourceIdentifierType": "relatedIdentifierType",
                        "relatedResourceIdentifier": "RelatedIdentifier",
                    },
                    "order": ["relatedResourceIdentifier", "relatedResourceIdentifierType", "relationType"],
                },
                "schema:schemaVersion": "1.6.0",
                "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
                "additionalProperties": False,
                "@context": {
                    "schema:name": {"@type": "xsd:string"},
                    "pav": "http://purl.org/pav/",
                    "bibo": "http://purl.org/ontology/bibo/",
                    "oslc": "http://open-services.net/ns/core#",
                    "schema:description": {"@type": "xsd:string"},
                    "pav:createdOn": {"@type": "xsd:dateTime"},
                    "pav:createdBy": {"@type": "@id"},
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                    "oslc:modifiedBy": {"@type": "@id"},
                    "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                    "schema": "http://schema.org/",
                },
                "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
                "schema:description": "Information about resource related to the dataset or other entity being described.",
                "@id": "https://repo.metadatacenter.org/template-elements/c13bdf4e-46a5-4364-925a-c33d33c13256",
                "@type": "https://schema.metadatacenter.org/core/TemplateElement",
                "$schema": "http://json-schema.org/draft-04/schema#",
            },
        },
        "10_ResourceType": {
            "skos:prefLabel": "Resource Type",
            "bibo:status": "bibo:draft",
            "_ui": {
                "propertyDescriptions": {
                    "resourceTypeDetail": "A description of the resource",
                    "resourceTypeGeneral": "The general type of a resource. A collection is a combination of multiple resource types.",
                },
                "propertyLabels": {"resourceTypeDetail": "ResourceType", "resourceTypeGeneral": "resourceTypeGeneral"},
                "order": ["resourceTypeDetail", "resourceTypeGeneral"],
            },
            "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "pav:derivedFrom": "https://repo.metadatacenter.org/template-elements/821ac569-713a-4bd8-95e3-504d1926f401",
            "schema:schemaVersion": "1.6.0",
            "title": "10_resourcetype element schema",
            "pav:createdBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
            "@context": {
                "schema:name": {"@type": "xsd:string"},
                "pav": "http://purl.org/pav/",
                "bibo": "http://purl.org/ontology/bibo/",
                "oslc": "http://open-services.net/ns/core#",
                "schema:description": {"@type": "xsd:string"},
                "pav:createdOn": {"@type": "xsd:dateTime"},
                "pav:createdBy": {"@type": "@id"},
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "oslc:modifiedBy": {"@type": "@id"},
                "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                "schema": "http://schema.org/",
            },
            "type": "object",
            "schema:name": "10_ResourceType",
            "description": "10_resourcetype element schema generated by the CEDAR Template Editor 2.6.16",
            "schema:identifier": "ResourceType",
            "schema:description": "The resource being described with metadata information about the type of the resource.",
            "@id": "https://repo.metadatacenter.org/template-elements/34e8196b-c93f-4a04-a691-42d50da0aebf",
            "properties": {
                "@context": {
                    "additionalProperties": False,
                    "required": ["resourceTypeDetail", "resourceTypeGeneral"],
                    "type": "object",
                    "properties": {
                        "resourceTypeDetail": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/26faf602-2fd3-4e22-818b-32949c82b746"
                            ]
                        },
                        "resourceTypeGeneral": {
                            "enum": [
                                "https://schema.metadatacenter.org/properties/42039c05-9fe3-4e8a-b9f6-f97affc62d3c"
                            ]
                        },
                    },
                },
                "resourceTypeGeneral": {
                    "skos:prefLabel": "Resource Type Category",
                    "_valueConstraints": {
                        "branches": [
                            {
                                "acronym": "FDC-GDMT",
                                "source": "undefined (FDC-GDMT)",
                                "maxDepth": 0,
                                "uri": "http://vocab.fairdatacollective.org/gdmt/ResourceTypeCategory",
                                "name": "Resource Type Category",
                            }
                        ],
                        "defaultValue": {
                            "rdfs:label": "Collection",
                            "termUri": "http://vocab.fairdatacollective.org/gdmt/Collection",
                        },
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": False,
                    },
                    "description": "resourceTypeGeneral field schema generated by the CEDAR Template Editor 2.6.16",
                    "title": "resourceTypeGeneral field schema",
                    "pav:lastUpdatedOn": "2022-01-27T07:40:21-08:00",
                    "additionalProperties": False,
                    "schema:schemaVersion": "1.6.0",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@id": {"type": "string", "format": "uri"},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                    },
                    "pav:createdOn": "2022-01-27T07:40:21-08:00",
                    "_ui": {"inputType": "textfield"},
                    "schema:name": "resourceTypeGeneral",
                    "@id": "https://repo.metadatacenter.org/template-fields/d9f7dc51-2786-448a-b707-3c865f11717c",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:description": "The general type of a resource. A collection is a combination of multiple resource types.",
                    "type": "object",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
                "@id": {"type": "string", "format": "uri"},
                "@type": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {
                            "minItems": 1,
                            "items": {"type": "string", "format": "uri"},
                            "uniqueItems": True,
                            "type": "array",
                        },
                    ]
                },
                "resourceTypeDetail": {
                    "_valueConstraints": {
                        "branches": [],
                        "multipleChoice": False,
                        "ontologies": [],
                        "classes": [],
                        "valueSets": [],
                        "requiredValue": False,
                    },
                    "skos:prefLabel": "Resource Type Detail",
                    "bibo:status": "bibo:draft",
                    "_ui": {"hidden": True, "inputType": "textfield"},
                    "oslc:modifiedBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "schema:schemaVersion": "1.6.0",
                    "title": "ResourceType field schema",
                    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
                    "@context": {
                        "schema:name": {"@type": "xsd:string"},
                        "pav": "http://purl.org/pav/",
                        "bibo": "http://purl.org/ontology/bibo/",
                        "oslc": "http://open-services.net/ns/core#",
                        "schema:description": {"@type": "xsd:string"},
                        "pav:createdOn": {"@type": "xsd:dateTime"},
                        "pav:createdBy": {"@type": "@id"},
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
                        "oslc:modifiedBy": {"@type": "@id"},
                        "skos:altLabel": {"@type": "xsd:string"},
                        "skos:prefLabel": {"@type": "xsd:string"},
                        "skos": "http://www.w3.org/2004/02/skos/core#",
                        "schema": "http://schema.org/",
                    },
                    "type": "object",
                    "schema:name": "ResourceType",
                    "description": "ResourceType field schema generated by the CEDAR Template Editor 2.6.16",
                    "schema:description": "A description of the resource",
                    "@id": "https://repo.metadatacenter.org/template-fields/4693b935-2e84-42ed-b8f8-ec91979f72d2",
                    "properties": {
                        "rdfs:label": {"type": ["string", "null"]},
                        "@type": {
                            "oneOf": [
                                {"type": "string", "format": "uri"},
                                {
                                    "minItems": 1,
                                    "items": {"type": "string", "format": "uri"},
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            ]
                        },
                        "@value": {"type": ["string", "null"]},
                    },
                    "pav:version": "0.0.1",
                    "pav:createdOn": "2022-01-27T07:40:21-08:00",
                    "required": ["@value"],
                    "additionalProperties": False,
                    "pav:lastUpdatedOn": "2022-01-27T07:40:21-08:00",
                    "@type": "https://schema.metadatacenter.org/core/TemplateField",
                },
            },
            "pav:version": "0.0.1",
            "pav:createdOn": "2022-01-30T23:31:11-08:00",
            "required": ["@context", "@id", "resourceTypeDetail", "resourceTypeGeneral"],
            "additionalProperties": False,
            "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
            "@type": "https://schema.metadatacenter.org/core/TemplateElement",
        },
        "pav:lastUpdatedOn": {"type": ["string", "null"], "format": "date-time"},
        "@type": {
            "oneOf": [
                {"type": "string", "format": "uri"},
                {"minItems": 1, "items": {"type": "string", "format": "uri"}, "uniqueItems": True, "type": "array"},
            ]
        },
    },
    "pav:createdOn": "2021-09-17T07:09:47-07:00",
    "_ui": {
        "propertyDescriptions": {
            "7_Contributor": "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property.",
            "2_Creator": "The main researcher involved in producing the data.",
            "10_ResourceType": "The resource being described with metadata information about the type of the resource.",
            "17_Description": "All additional information that does not fit in any of the other categories. May be used for technical information.",
            "12_RelatedIdentifier": "Information about resource related to the dataset or other entity being described.",
            "7 Contributor": "",
            "4_Publisher": "The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role.",
            "3_Title": "A name or title by which the dataset being described is known.",
            "7_ContactPerson": "The institution or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource. To supply multiple contributors, repeat this property.",
            "1_Identifier": "Information about the globally unique and persistent identifier used to identify and optionally access (meta)data of the dataset being described.",
            "datasetPagebreak": "Information with regards to the dataset",
            "2 Creator": "",
            "17 Description": "",
            "8_Date": "Relevant dates related to the resource being described.",
            "6_Subject": "Concepts that define the dataset or purpose sourced from controlled vocabulary.",
            "4 Publisher": "",
        },
        "propertyLabels": {
            "7_Contributor": "7_Contributor",
            "2_Creator": "2_Creator",
            "10_ResourceType": "10_ResourceType",
            "17_Description": "17_Description",
            "12_RelatedIdentifier": "12_RelatedIdentifier",
            "4_Publisher": "4_Publisher",
            "3_Title": "3_Title",
            "7_ContactPerson": "7_ContactPerson",
            "1_Identifier": "1_Identifier",
            "datasetPagebreak": "datasetPagebreak",
            "8_Date": "8_Date",
            "6_Subject": "6_Subject",
        },
        "pages": [],
        "order": [
            "1_Identifier",
            "4_Publisher",
            "8_Date",
            "2_Creator",
            "7_ContactPerson",
            "7_Contributor",
            "datasetPagebreak",
            "3_Title",
            "17_Description",
            "6_Subject",
            "10_ResourceType",
            "12_RelatedIdentifier",
        ],
    },
    "pav:createdBy": "https://metadatacenter.org/users/cfe1eb1f-583f-4564-bba1-fad56d4f9717",
    "oslc:modifiedBy": "https://metadatacenter.org/users/db4f9023-aed2-4f30-bc9a-6005dc6e2fbf",
    "@context": {
        "schema:name": {"@type": "xsd:string"},
        "pav": "http://purl.org/pav/",
        "bibo": "http://purl.org/ontology/bibo/",
        "oslc": "http://open-services.net/ns/core#",
        "schema:description": {"@type": "xsd:string"},
        "pav:createdOn": {"@type": "xsd:dateTime"},
        "pav:createdBy": {"@type": "@id"},
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "oslc:modifiedBy": {"@type": "@id"},
        "pav:lastUpdatedOn": {"@type": "xsd:dateTime"},
        "schema": "http://schema.org/",
    },
    "pav:lastUpdatedOn": "2022-01-30T23:31:11-08:00",
    "schema:description": "This is the basic DataHub General Schema",
    "@id": "https://hdl.handle.net/21.T12996/P000000041C000000002schema.1",
    "@type": "https://schema.metadatacenter.org/core/Template",
    "$schema": "http://json-schema.org/draft-04/schema#",
}
