"""This module contains functions to help to return mock api call result. It is part of the MOCK_RULE_WRAPPER mode."""
import json
import os
import pathlib


def read_mock_json_file(base_file_name: str):
    """
    Read and parse the mock json file linked to the api function name

    Parameters
    ----------
    base_file_name: str
        The file to read and parse

    Returns
    -------
    Any
        Parsed json file
    """
    dto_folder = pathlib.Path(__file__).parent.resolve()
    mock_path = os.path.join(dto_folder, "mocks", f"{base_file_name}.json")
    try:
        with open(mock_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def get_api_mock_result(function_name: str):
    """
    Based on the function name, mock the api call return value.

    Parameters
    ----------
    function_name: str
        API function name to mock

    Returns
    -------
    Any
        Mock api result
    """
    if "read_instance" in function_name:
        return read_mock_json_file("instance")
    if "read_schema" in function_name:
        return read_mock_json_file("schema")

    return read_mock_json_file(f"{function_name}.mock")
