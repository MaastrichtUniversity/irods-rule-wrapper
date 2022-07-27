"""This module contains the Token DTO class and its factory constructor."""


class Token:
    """
    This class represents the Dropzone token. It is the output of the rule generate_token.

    TO_REFACTOR: AttributeValue & Token are very similar, refactor them as a StringValue DTO (same a Boolean)
    """

    def __init__(self, token: str):
        self.token: str = token

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Token":
        token = cls(result)
        return token
