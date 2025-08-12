from enum import StrEnum
from io import TextIOWrapper
from json import dumps
from os import getcwd, listdir, makedirs
from os.path import abspath, dirname, exists, isdir, isfile, join, splitext
from typing import IO, Any, Literal

from yaml import YAMLError, safe_load

from lib.json_functions import format_json_string


class FILE_EXTENSIONS(StrEnum):
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
    """
    Helper function for checking if a string is a file.

    Args:
        file_string (str): A string that should represent the path to a file.

    Returns:
        bool: Does the string represent a file? True if so, False if not.
    """
    if isfile(file_string):
        return True
    if isfile(join(getcwd(), file_string)):
        print(
            f"The provided file string: {file_string} was not a file, however, appending the string to the current working directory did return a valid file string... Returning True."
        )
        return True
    return False


def check_if_string_matches_file_extension(uri: str, file_extension: str) -> bool:
    """
    Helper function to check if a URI and a file extension match a valid file.

    Args:
        uri (str): A string that should represent the path to a file.
        file_extension (str): A string that should represent a file extension.

    Returns:
        bool: Does the concatenated string represent a file? True if so, False if not.
    """
    does_string_match_file: bool = check_if_string_is_a_file(uri)
    if does_string_match_file:
        if uri.endswith(file_extension):
            return True
        else:
            print(
                f"check_if_string_matches_file_extension() {uri} did not have the {file_extension} extension."
            )
            return False
    else:
        print(f"check_if_string_matches_file_extension() -> {uri} is not a file.")
        return does_string_match_file


def check_if_string_is_a_directory(directory_string: str) -> bool:
    """
    Helper function to check if a URI and a file extension match a valid file.

    Args:
        uri (str): A string that should represent the path to a file.
        file_extension (str): A string that should represent a file extension.

    Returns:
        bool: Does the concatenated string represent a file? True if so, False if not.
    """
    if isdir(directory_string):
        return True
    if isdir(join(getcwd(), directory_string)):
        print(
            f"The provided directory string: {directory_string} was not a directory, however, appending the string to the current working directory did return a valid sub-directory... Returning True"
        )
        return True
    return False


def create_directory(directory_string: str) -> bool:
    """
    Helper function to create a directory.

    Args:
        directory_string (str): A string that should represent the path to a directory.

    Returns:
        bool: Does the directory exist? True if so, False if not.

    Raises:
        FileNotFoundError: A non-existent parent directory in the path could not be created. (Examples: A non-existent drive or missing intermediate directories.)
        NotADirectoryError: A filepath was provided instead of a directory.
        PermissionError: Insufficient permissions to create a directory in the specified location.
        Exception: A catch-all exception for anything not covered above.

    Notes:
        A "FileExistsError" is possible in this function. It is purposely not caught, because of the initial exists() function check.
    """
    if not exists(directory_string):
        try:
            makedirs(directory_string, exist_ok=True)
        except FileNotFoundError as exception:
            print(f"create_directory() - FileNotFoundError: {exception}")
            raise exception
        except NotADirectoryError as exception:
            print(f"create_directory() - NotADirectoryError: {exception}")
            raise exception
        except PermissionError as exception:
            print(f"create_directory() - PermissionError: {exception}")
            raise exception
        except Exception as exception:
            print(f"create_directory() - Exception: {exception}")
            raise exception
        return True
    else:
        print("create_directory() - Directory already exists.")
        return False


def get_file_extension_from_filepath(uri: str) -> str:
    """
    Helper function to get the extension of a file from a URI.

    Args:
        uri (str): A string that should represent the path to a file.

    Returns:
        str: The specified file's extension.
    """
    file_extension: str = splitext(uri)[1]
    return file_extension


def get_files_by_extension_in_directory(
    directory_string: str = getcwd(),  # TODO: Make sure this is okay to call this function as a default argument.
    file_extension: list[str] | str | None = None,
) -> list[str]:
    """
    Helper function to get a list of all files with a specified extension in a directory.

    Args:
        directory_string (str): A string that should represent the path to a directory.
        file_extension (str): A string that should represent a file extension.

    Returns:
        list[str]: A list of all files with a specified extension in a directory.
    """
    if file_extension is None:
        file_extension = ["txt"]  # NOTE: Setting the default file extension to "txt"
    file_list: list[str] = []
    for file in listdir(directory_string):
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
    """
    Helper function to get the parent directory name of a directory.

    Args:
        directory_string (str): A string that should represent the path to a directory.
        depth_upwards (int): The number of directories to go up from the specified directory.

    Returns:
        str: The name of the parent directory.
    """
    # NOTE: This function feels a little sloppy, and could probably be refactored to use recursion?
    return_directory_name: str = abspath(directory_string)
    for _ in range(depth_upwards):
        return_directory_name = dirname(return_directory_name)
    return return_directory_name


def open_file(
    uri: str,
    mode: Literal[
        "r",
        "w",
        "a",
        "x",
        "r+",
        "w+",
        "a+",
        "rb",
        "wb",
        "ab",
        "rb+",
        "wb+",
        "ab+",
        "r+b",
        "w+b",
        "a+b",
    ],  # NOTE: Adding both "rb+" and "r+b" syntax because they are 100% equal in Python, but up to user preference.
    encoding: str = "utf-8",
) -> IO[Any] | None:
    """
    Helper function to safely open a file.

    Args:
        uri (str): A string that should represent the path to a file.
        mode (Literal[str]): The mode to open the file in. (Choices: "r", "w", "a", "x", "r+", "w+", "a+", "rb", "wb", "ab", "rb+", "wb+", "ab+", "r+b", "w+b", "a+b")
        encoding (str): The encoding to use when opening the file. Setting default to utf-8, because that is the most standard.

    Returns:
        IO[Any] | None: The file object, or None if the file could not be opened.

    Raises:
        FileNotFoundError: The file does not exist.
        PermissionError: The file could not be opened due to insufficient permissions.
        IsADirectoryError: The path is a directory, not a file.
        UnicodeDecodeError: The file could not be decoded with UTF-8.
        OSError: An operating system error occurred. (Examples: Disk full, too many files, path issues, etc...) (This type of exception is actually raised)
        TypeError, ValueError: Invalid arguments.
        MemoryError: Insufficient memory. (This type of exception is actually raised)
        YAMLError: An error occurred while parsing a YAML file.
        Exception: An unexpected error occurred. (This type of exception is actually raised)
    """
    try:
        with open(file=uri, mode=mode, encoding=encoding) as file:
            return file
    except FileNotFoundError as exception:
        print("File not found.", exception)
    except PermissionError as exception:
        print("Permission denied.", exception)
    except IsADirectoryError as exception:
        print("Path is a directory, not a file.", exception)
    except UnicodeDecodeError as exception:
        print("Cannot decode file with UTF-8.", exception)
    except OSError as exception:
        print(f"OS error: {exception.strerror} (errno: {exception.errno})", exception)
        raise exception
    except (TypeError, ValueError) as exception:
        print(f"Invalid arguments: {exception}")
    except MemoryError as exception:
        print(f"Memory error: {exception}", exception)
        raise exception
    except YAMLError as exception:
        print(f"YAML error: {exception}", exception)
    except Exception as exception:
        print(f"Error opening file: {uri} | mode: {mode}")
        raise exception


def read_file_as_text_string(uri: str) -> str | None:
    """
    Helper function to read a file into a string.

    Args:
        uri (str): A string that should represent the path to a file.

    Returns:
        str | None: The contents of the file as a string, or None if any errors occurred when opening the file.
    """
    file_content: IO[Any] | None = open_file(uri, "r")
    if file_content is not None:
        return file_content.read()


def read_yaml_file_as_dictionary(yaml_filepath: str) -> dict[str, Any] | None:
    """
    Helper function to read a YAML file into a dictionary.

    Args:
        yaml_filepath (str): A string that should represent the path to a YAML file.

    Returns:
        dict[str, Any] | None: The contents of the YAML file as a dictionary, or None if any errors occurred when opening the file.
    """
    file: IO[Any] | None = open_file(yaml_filepath, "r")
    if file is not None:
        return safe_load(file)


def write_dictionary_to_file(
    uri: str, dictionary_to_write: dict[Any, Any]
) -> IO[Any] | None:
    """
    Helper function to write a dictionary to a file.

    Args:
        uri (str): A string that should represent the path to a file.
        dictionary_to_write (dict[Any, Any]): The dictionary to write to the file.

    Returns:
        IO[Any] | None: The file object, or None if the file could not be opened.
    """
    parent_directory: str = get_parent_directory_name(uri)
    directory_check: bool = check_if_string_is_a_directory(parent_directory)
    if not directory_check:
        create_directory(parent_directory)
    formatted_string: str = dumps(
        obj=dictionary_to_write, indent=2, sort_keys=True
    )  # TODO: Fix this so that we don't perform the formatting twice... Once here and once in "write_stirng_to_file()"
    return write_string_to_file(uri=uri, text_to_write=formatted_string)


def write_string_to_file(uri: str, text_to_write: str) -> IO[Any] | None:
    """
    Helper function to write a string to a file.

    Args:
        uri (str): A string that should represent the path to a file.
        text_to_write (str): The string to write to the file.

    Returns:
        IO[Any] | None: The file object, or None if the file could not be opened.
    """
    parent_directory: str = get_parent_directory_name(uri)
    directory_check: bool = check_if_string_is_a_directory(parent_directory)
    if not directory_check:
        create_directory(parent_directory)
    _file_extension: str = get_file_extension_from_filepath(uri)
    if _file_extension == FILE_EXTENSIONS.JSON.value:
        text_to_write = format_json_string(text_to_write)
    file: IO[Any] | None = open_file(uri, "w")
    if file is not None:
        file.write(text_to_write)
    return file
