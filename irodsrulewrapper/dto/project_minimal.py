from pydantic import BaseModel


class ProjectMinimal(BaseModel):
    id: str
    title: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "ProjectMinimal":
        project = cls(
            id=result["id"],
            title=result["title"],
        )
        return project
