from .user import User
from typing import List, Dict
import json



class Users:
    def __init__(self, users: List['User']):
        self.users: List['User'] = users

    @classmethod
    def create_from_rule_result(cls, result: Dict) -> 'Users':
        output = []
        for item in result:
            user = User.create_from_rule_result(item)
            output.append(user)
        users = cls(output)
        return users

    @classmethod
    def create_from_mock_result(cls, mock_json=None) -> 'Users':
        if mock_json is None:
            mock_json = cls.MOCK_JSON
        return cls.create_from_rule_result(json.loads(mock_json))

    MOCK_JSON = """
    [
        {
            "displayName": "Jonathan Melius",
            "userId": "10043",
            "userName": "jmelius"
        },
        {
            "displayName": "Paul van Schayck",
            "userId": "10053",
            "userName": "pvanschay2"
        },
        {
            "displayName": "Dr. Maarten Coonen (MUMC+)",
            "userId": "10033",
            "userName": "mcoonen2"
        },
        {
            "displayName": "Olav Palmen",
            "userId": "10088",
            "userName": "opalmen"
        },
        {
            "displayName": "service-mdl",
            "userId": "10112",
            "userName": "service-mdl"
        },
        {
            "displayName": "minimalist",
            "userId": "10093",
            "userName": "minimalist"
        },
        {
            "displayName": "Additional User newly created in LDAP",
            "userId": "10103",
            "userName": "auser"
        },
        {
            "displayName": "service-dropzones",
            "userId": "10108",
            "userName": "service-dropzones"
        },
        {
            "displayName": "Koert Heinen",
            "userId": "10073",
            "userName": "kheinen"
        },
        {
            "displayName": "Ralph Brecheisen",
            "userId": "10068",
            "userName": "rbrecheis"
        },
        {
            "displayName": "Maarten Coonen",
            "userId": "10028",
            "userName": "mcoonen"
        },
        {
            "displayName": "Daniel Theunissen",
            "userId": "10038",
            "userName": "dtheuniss"
        },
        {
            "displayName": "Pascal Suppers",
            "userId": "10058",
            "userName": "psuppers"
        },
        {
            "displayName": "Rickest Rick",
            "userId": "10098",
            "userName": "rvoncken"
        },
        {
            "displayName": "Raimond Ravelli",
            "userId": "10078",
            "userName": "rravelli"
        },
        {
            "displayName": "service-disqover",
            "userId": "10118",
            "userName": "service-disqover"
        },
        {
            "displayName": "service-pid",
            "userId": "10115",
            "userName": "service-pid"
        },
        {
            "displayName": "Dean Linssen",
            "userId": "10048",
            "userName": "dlinssen"
        },
        {
            "displayName": "Patrick Ahles",
            "userId": "10083",
            "userName": "pahles"
        },
        {
            "displayName": "delnoy",
            "userId": "10063",
            "userName": "delnoy"
        }
    ]
    """