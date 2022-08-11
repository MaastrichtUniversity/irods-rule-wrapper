import json
import os
import pathlib


def read_mock_json_file(base_file_name):
    dto_folder = pathlib.Path(__file__).parent.resolve()
    mock_path = os.path.join(dto_folder, "mocks", f"{base_file_name}.json")
    try:
        with open(mock_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def get_api_mock_result(function_name):
    if "read_instance" in function_name:
        return read_mock_json_file("instance")
    elif "read_schema" in function_name:
        return read_mock_json_file("schema")

    return read_mock_json_file(f"{function_name}.mock")
