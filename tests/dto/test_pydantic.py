import pytest
from pydantic import BaseModel, ValidationError

from irodsrulewrapper.dto.collection_stats import CollectionStats
from irodsrulewrapper.dto.groups import Groups
from irodsrulewrapper.dto.projects_minimal import ProjectsMinimal
from irodsrulewrapper.dto.users import Users
from irodsrulewrapper.dto.users_groups_expanded import UsersGroupsExpanded


@pytest.mark.parametrize("dto_class", [Groups, ProjectsMinimal, Users, UsersGroupsExpanded])
def test_dto_serialization_round_trip(dto_class):
    dto = dto_class.create_from_mock_result()

    restored = dto_class.model_validate_json(dto.model_dump_json())

    assert restored.model_dump() == dto.model_dump()


def test_dto_nested_in_pydantic_model():
    class Response(BaseModel):
        users: Users

    users = Users.create_from_rule_result([{"userName": "test_user", "userId": "10001", "displayName": "Test User"}])
    response = Response(users=users)

    assert response.model_dump() == {
        "users": {"users": [{"user_name": "test_user", "user_id": "10001", "display_name": "Test User"}]}
    }
    assert Response.model_validate_json(response.model_dump_json()).users == users


def test_collection_stats_validation():
    stats = CollectionStats.create_from_rule_result({"total_file_count": "2", "total_file_size": "205503"})
    assert stats.model_dump() == {"total_file_count": 2, "total_file_size": 205503}

    with pytest.raises(ValidationError) as error:
        CollectionStats.create_from_rule_result({"total_file_count": "invalid", "total_file_size": "205503"})

    assert error.value.errors()[0]["loc"] == ("total_file_count",)
