from .resource import Resource


class Resources:
    def __init__(self, resources):
        self.resources = resources

    @classmethod
    def create_from_rule_result(cls, result):
        output = []
        for item in result:
            resource = Resource.create_from_rule_result(item)
            output.append(resource)
        resources = cls(output)
        return resources
