"""This module contains the ProjectsCost DTO class, its factory constructors and mock_json."""
import json

from irodsrulewrapper.dto.project_cost import ProjectCost


class ProjectsCost:
    """This class represents a list of iRODS ProjectCost DTOs."""

    def __init__(self, projects_cost: list["ProjectCost"]):
        self.projects_cost: list["ProjectCost"] = projects_cost

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectsCost":
        # get_projects_finance returns an empty list, if the user is not the PI or data steward of the project
        if len(result) == 0:
            return None

        output = []
        for item in result:
            project = ProjectCost.create_from_rule_result(item)
            output.append(project)
        projects = cls(output)
        return projects

    @classmethod
    def create_from_mock_result(cls, projects_cost_json=None) -> "ProjectsCost":
        if projects_cost_json is None:
            projects_cost_json = cls.PROJECTS_COST_JSON
        return ProjectsCost.create_from_rule_result(json.loads(projects_cost_json))

    PROJECTS_COST_JSON = """
    [
      {
        "project_cost_monthly": 0.003420780458333333,
        "title": "Compatible disintermediate productivity",
        "project_size_gb": 0.31576435,
        "budget_number": "XXXXXXXXX",
        "collections": [
          {
            "collection": "/nlmumc/projects/P000000020/C000000001",
            "collection_storage_cost": 0.0410493655,
            "data_size_gib": 0.2940784674137831,
            "details_per_resource": [
              {
                "price_per_gb_per_year": 0.13,
                "resource": "10160",
                "storage_cost_on_resource": 0.0410493655,
                "data_size_gb_on_resource": 0.31576434999999997
              }
            ]
          }
        ],
        "project_cost_yearly": 0.0410493655,
        "project_size_gib": 0.2940784674137831,
        "project_id": "P000000020"
      },
      {
        "project_cost_monthly": 0,
        "title": "(HVC) Placeholder project",
        "project_size_gb": 0.0,
        "budget_number": "AZM-123456",
        "collections": [
          {
            "collection": "/nlmumc/projects/P000000011/C000000001",
            "collection_storage_cost": 0,
            "data_size_gib": 0.0,
            "details_per_resource": []
          }
        ],
        "project_cost_yearly": 0,
        "project_size_gib": 0.0,
        "project_id": "P000000011"
      },
      {
        "project_cost_monthly": 0,
        "title": "(MDL) Placeholder project",
        "project_size_gb": 0.0,
        "budget_number": "AZM-123456",
        "collections": [
          {
            "collection": "/nlmumc/projects/P000000010/C000000001",
            "collection_storage_cost": 0,
            "data_size_gib": 0.0,
            "details_per_resource": []
          }
        ],
        "project_cost_yearly": 0,
        "project_size_gib": 0.0,
        "project_id": "P000000010"
      },
      {
        "project_cost_monthly": 0,
        "title": "(ScaNxs) The Bulwer-Lytton fiction contest is held ever year at San Jose State",
        "project_size_gb": 0.0,
        "budget_number": "UM-30009999X",
        "collections": [],
        "project_cost_yearly": 0,
        "project_size_gib": 0,
        "project_id": "P000000016"
      },
      {
        "project_cost_monthly": 0.00050000455,
        "title": "Cold hands, no gloves.",
        "project_size_gb": 0.30000042000000005,
        "budget_number": "UM-30009998X",
        "collections": [
          {
            "collection": "/nlmumc/projects/P000000015/C000000001",
            "collection_storage_cost": 0.0060000546000000005,
            "data_size_gib": 0.2793971635401249,
            "details_per_resource": [
              {
                "price_per_gb_per_year": 0.02,
                "resource": "10017",
                "storage_cost_on_resource": 0.006,
                "data_size_gb_on_resource": 0.3
              },
              {
                "price_per_gb_per_year": 0.13,
                "resource": "10160",
                "storage_cost_on_resource": 5.459999999999999e-08,
                "data_size_gb_on_resource": 4.1999999999999995e-07
              }
            ]
          }
        ],
        "project_cost_yearly": 0.0060000546000000005,
        "project_size_gib": 0.2793971635401249,
        "project_id": "P000000015"
      },
      {
        "project_cost_monthly": 0,
        "title": "There is no distinctly native American criminal class except Congress.",
        "project_size_gb": 0.0,
        "budget_number": "UM-30009998X",
        "collections": [],
        "project_cost_yearly": 0,
        "project_size_gib": 0,
        "project_id": "P000000014"
      },
      {
        "project_cost_monthly": 0.003420248606666667,
        "title": "Ergonomic demand-driven orchestration",
        "project_size_gb": 0.315715256,
        "budget_number": "XXXXXXXXX",
        "collections": [
          {
            "collection": "/nlmumc/projects/P000000019/C000000001",
            "collection_storage_cost": 0.04104298328,
            "data_size_gib": 0.2940327450633049,
            "details_per_resource": [
              {
                "price_per_gb_per_year": 0.13,
                "resource": "10160",
                "storage_cost_on_resource": 0.04104298328,
                "data_size_gb_on_resource": 0.315715256
              }
            ]
          }
        ],
        "project_cost_yearly": 0.04104298328,
        "project_size_gib": 0.2940327450633049,
        "project_id": "P000000019"
      },
      {
        "project_cost_monthly": 8.948333333333333e-09,
        "title": "Fundamental local capability",
        "project_size_gb": 8.26e-07,
        "budget_number": "XXXXXXXXX",
        "collections": [
          {
            "collection": "/nlmumc/projects/P000000018/C000000001",
            "collection_storage_cost": 5.33e-08,
            "data_size_gib": 3.818422555923462e-07,
            "details_per_resource": [
              {
                "price_per_gb_per_year": 0.13,
                "resource": "10160",
                "storage_cost_on_resource": 5.33e-08,
                "data_size_gb_on_resource": 4.1e-07
              }
            ]
          },
          {
            "collection": "/nlmumc/projects/P000000018/C000000002",
            "collection_storage_cost": 5.408e-08,
            "data_size_gib": 3.8743019104003906e-07,
            "details_per_resource": [
              {
                "price_per_gb_per_year": 0.13,
                "resource": "10160",
                "storage_cost_on_resource": 5.408e-08,
                "data_size_gb_on_resource": 4.1599999999999997e-07
              }
            ]
          }
        ],
        "project_cost_yearly": 1.0738e-07,
        "project_size_gib": 7.692724466323853e-07,
        "project_id": "P000000018"
      }
    ]
    """
