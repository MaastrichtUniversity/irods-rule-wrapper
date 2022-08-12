"""This module contains the Token DTO class and its factory constructor."""
from irodsrulewrapper.dto.dto_base_model import DTOBaseModel


class Token(DTOBaseModel):
    """
    This class represents the Dropzone token. It is the output of the rule generate_token.

    TO_REFACTOR: AttributeValue & Token are very similar, refactor them as a StringValue DTO (same a Boolean)
    """

    token: str

    @classmethod
    def create_from_rule_result(cls, result: dict) -> "Token":
        token = cls(token=result)
        return token
