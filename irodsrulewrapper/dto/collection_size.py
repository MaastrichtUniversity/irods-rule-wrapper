class CollectionSize:
    def __init__(self, resource: str, size: float, relative_size: float):
        self.resource: str = resource
        self.size: float = size
        self.relative_size: float = relative_size

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "CollectionSize":
        collection_size = cls(result["resourceName"], float(result["size"]), float(result["relativeSize"]))

        return collection_size
