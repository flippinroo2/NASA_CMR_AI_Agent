import json


def format_json_string(json_string: str, indent_size: int = 2) -> str | None:
    """
    Helper function for formatting a JSON string.

    Args:
        json_string (str): The JSON string to format.
        indent_size (int): The number of spaces to indent the JSON string.

    Returns:
        str: The formatted JSON string.

    Notes:
        This function is a bit hard to read with the tested error handling. This was by design so the outer "try" block catches common errors and any catch-all errors that might occur.
    """
    json_loaded_string: str | bytes | bytearray | None = None
    formatted_json_string: str | None = None
    try:
        try:
            json_loaded_string = json.loads(json_string)
        except json.JSONDecodeError as exception:
            print(f"format_json_string() - JSONDecodeError: {exception}")
        except TypeError as exception:
            print(f"format_json_string() - TypeError: {exception}")
        except UnicodeDecodeError as exception:
            print(f"format_json_string() - UnicodeDecodeError: {exception}")

        if json_loaded_string is not None:
            try:
                formatted_json_string = json.dumps(json_loaded_string, indent=indent_size)
            except TypeError as exception:
                print(f"format_json_string() - TypeError: {exception}")
            except OverflowError as exception:
                print(f"format_json_string() - OverflowError: {exception}")
            except RecursionError as exception:
                print(f"format_json_string() - RecursionError: {exception}")

    except OSError as exception:
        print(f"format_json_string() - OSError: {exception}")
    except Exception as exception:
        print(f"format_json_string() - Exception: {exception}")
    return formatted_json_string
