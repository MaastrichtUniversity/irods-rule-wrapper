"""This module contains the custom class DTOBaseModel"""
import json
import os
import pathlib

from pydantic import BaseModel


class DTOBaseModel(BaseModel):
    """
    This class inherits pydantic BaseModel and define custom factory class methods
    """

    @classmethod
    def create_from_rule_result(cls, result: dict):
        """
        Factory class method to create dto instance from iRODS server rule result.

        Parameters
        ----------
        result
            Json parsed iRODS rule result

        Returns
        -------
        DTOBaseModel
            Mock class dto instance
        """

    @classmethod
    def create_from_mock_result(cls, mock_json=None):
        """
        Factory class method to create dto instance from an inline mock rule result.

        Parameters
        ----------
        mock_json:Any
            Inline mock rule result

        Returns
        -------
        DTOBaseModel
            Mock class dto instance
        """

    @classmethod
    def create_from_mock_json(cls):
        """
        Factory class method to create dto instance from predefined mock.json file.
        It is part of the MOCK_RULE_WRAPPER mode.

        Returns
        -------
        DTOBaseModel
            Mock class dto instance
        """
        dto_folder = pathlib.Path(__file__).parent.resolve()
        mock_path = os.path.join(dto_folder, "mocks", f"{cls.__name__}.mock.json")
        with open(mock_path, "r", encoding="utf-8") as file:
            return cls(**json.load(file))
