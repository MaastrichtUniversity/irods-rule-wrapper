import json


class ManagingProjects:
    def __init__(
        self,
        managers: list[str],
        contributors: list[str],
        viewers: list[str],
        principal_investigator: str,
        data_steward: str,
    ):
        self.managers: list[str] = managers
        self.contributors: list[str] = contributors
        self.viewers: list[str] = viewers
        self.principal_investigator: str = principal_investigator
        self.data_steward: str = data_steward

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ManagingProjects":
        # get_project_acl_for_manager returns an empty list, if the user is not a manager for the project
        if len(result) == 0:
            return None

        managers = result["managers"]["users"]
        contributors = result["contributors"]["users"] + result["contributors"]["groups"]
        viewers = result["viewers"]["users"] + result["viewers"]["groups"]
        projects = cls(managers, contributors, viewers, result["principal_investigator"], result["data_steward"])

        return projects

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> "ManagingProjects":
        if mock_json is None:
            mock_json = cls.MOCK_JSON
        return cls.create_from_rule_result(json.loads(mock_json))

    MOCK_JSON = """
    {
      "principal_investigator": "psuppers",
      "managers": {
        "userObjects": [
          {
            "userName": "psuppers",
            "userId": "10058",
            "displayName": "psuppers"
          },
          {
            "userName": "opalmen",
            "userId": "10088",
            "displayName": "opalmen"
          }
        ],
        "users": [
          "psuppers",
          "opalmen"
        ],
        "groups": [],
        "groupObjects": []
      },
      "viewers": {
        "userObjects": [],
        "users": [],
        "groups": [
          "datahub"
        ],
        "groupObjects": [
          {
            "groupName": "datahub",
            "displayName": "datahub",
            "groupId": "10127",
            "description": ""
          }
        ]
      },
      "contributors": {
        "userObjects": [],
        "users": [],
        "groups": [],
        "groupObjects": []
      },
      "data_steward": "opalmen"
    }
    """
