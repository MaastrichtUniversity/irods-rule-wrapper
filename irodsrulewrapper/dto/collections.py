from .project import Project
from .collection import Collection
from typing import List, Dict


class Collections:
    def __init__(self, project: Project, collections):
        self.project: List['Project'] = project
        self.collections = collections

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Collections':
        project = Project.create_from_rule_result(result['project'])
        collections = []
        for item in result['collections']:
            collection = Collection.create_from_rule_result(item)
            collections.append(collection)
        output = cls(project, collections)
        return output
