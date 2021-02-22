class Collection:
    def __init__(self, creator, size, title, pid, num_files):
        self.creator = creator
        self.size = size
        self.title = title
        self.pid = pid
        self.num_files = num_files

    @classmethod
    def create_from_rule_result(cls, result):
        user = cls(result["creator"], result["size"], result["title"], result["PID"], result["numFiles"])
        return user
