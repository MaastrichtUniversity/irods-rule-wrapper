from .project_overview import ProjectOverview
from typing import List, Dict
from irodsrulewrapper.cache import CacheTTL


class ProjectsOverview:
    def __init__(self, projects: List['ProjectOverview']):
        self.projects: List['ProjectOverview'] = projects

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'ProjectsOverview':
        CacheTTL.check_if_cache_expired()
        output = []
        for item in result:
            project = ProjectOverview.create_from_rule_result(item, )
            output.append(project)
        projects = cls(output)
        return projects
