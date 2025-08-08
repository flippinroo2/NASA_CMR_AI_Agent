import enum
import os
from io import TextIOWrapper
import json
from lib.json_functions import format_json_string
from typing import Any
import yaml


class FILE_EXTENSIONS(enum.StrEnum):
    CSV = ".csv"
    HTML = ".html"
    JSON = ".json"
    PICKLE = ".pickle"
    TEXT = ".txt"
    XLS = ".xls"
    XLSX = ".xlsx"
    XML = ".xml"
    YAML = ".yaml"


def check_if_string_is_a_file(file_string: str) -> bool:
    if os.path.isfile(file_string):
        return True
    if os.path.isfile(os.path.join(os.getcwd(), file_string)):
        print(
            f"The provided file string: {file_string} was not a file, however, appending the string to the current working directory did return a valid file string... Returning True"
        )
        return True
    return False


def check_if_string_matches_file_extension(
    file_path: str, file_extension: str
) -> bool | None:
    if check_if_string_is_a_file(file_path):
        if file_path.endswith(file_extension):
            return True
        else:
            print(
                f"check_if_string_matches_file_extension()\n{file_path} did not have the {file_extension} extension"
            )
            return False
    else:
        print(f"check_if_string_matches_file_extension() -> {file_path} is not a file")


def check_if_string_is_a_directory(directory_string: str) -> bool:
    if os.path.isdir(directory_string):
        return True
    if os.path.isdir(os.path.join(os.getcwd(), directory_string)):
        print(
            f"The provided directory string: {directory_string} was not a directory, however, appending the string to the current working directory did return a valid sub-directory... Returning True"
        )
        return True
    return False


def create_directory(directory_string: str) -> bool:
    if not os.path.exists(directory_string):
        try:
            os.makedirs(directory_string, exist_ok=True)
        except Exception as e:
            print(f"create_directory() - Exception: {e}")
        return True
    else:
        print("create_directory() - Directory already exists.")
        return False


def does_file_exist(file_string: str) -> bool:
    return os.path.exists(file_string)


def get_file_extension_from_filepath(filepath: str) -> str:
    _file_extension: str = os.path.splitext(filepath)[1]
    return _file_extension


def get_files_by_extension_in_directory(
    directory_string: str = os.getcwd(),
    file_extension: list[str] | str = ["txt"],
) -> list[str]:
    file_list: list[str] = []
    for file in os.listdir(directory_string):
        full_file_path: str = f"{directory_string}/{file}"
        if isinstance(file_extension, list):
            for extension in file_extension:
                if check_if_string_matches_file_extension(full_file_path, extension):
                    file_list.append(full_file_path)
        else:
            if check_if_string_matches_file_extension(full_file_path, file_extension):
                file_list.append(full_file_path)
    return file_list


def get_parent_directory_name(directory_string: str, depth_upwards: int = 1) -> str:
    return_directory_name: str = os.path.abspath(directory_string)
    for _ in range(depth_upwards):
        return_directory_name = os.path.dirname(return_directory_name)
    return return_directory_name


def read_file_as_text_string(filename: str) -> str:
    try:
        with open(file=filename, mode="r") as file:
            file_content: str = file.read()
            return file_content
    except Exception as exception:
        print(f"Error reading file: {filename}")
        raise exception

def read_yaml_file_as_dictionary(yaml_filepath: str) -> dict[str, Any] | None:
    try:
        with open(yaml_filepath, "r") as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error reading {yaml_filepath}: {e}")

def write_dictionary_to_file(
    filename: str, dictionary_to_write: dict[Any, Any]
) -> TextIOWrapper:
    parent_directory: str = get_parent_directory_name(filename)
    directory_check = check_if_string_is_a_directory(
        parent_directory
    )  # TODO: Turn this into a function to use for checking filepaths later.
    if not directory_check:
        create_directory(parent_directory)
    formatted_string = json.dumps(
        obj=dictionary_to_write, indent=2, sort_keys=True
    )  # TODO: Fix this so that we don't perform the formatting twice... Once here and once in "write_stirng_to_file()"
    return write_string_to_file(filename=filename, text_to_write=formatted_string)


def write_string_to_file(filename: str, text_to_write: str) -> TextIOWrapper:
    try:
        parent_directory: str = get_parent_directory_name(filename)
        directory_check = check_if_string_is_a_directory(
            parent_directory
        )  # TODO: Turn this into a function to use for checking filepaths later.
        if not directory_check:
            create_directory(parent_directory)
        _file_extension = get_file_extension_from_filepath(filename)
        if _file_extension == FILE_EXTENSIONS.JSON.value:
            text_to_write = format_json_string(text_to_write)
        with open(file=filename, mode="w", encoding="utf-8") as file:
            file.write(text_to_write)
        return file
    except Exception as exception:
        print(f"Error writing file: {filename}", exception)
        raise exception
