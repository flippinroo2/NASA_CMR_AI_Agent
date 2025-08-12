def replace_double_newline(string_with_double_newline: str) -> str:
    """
    Helper function for replacing a double newline character with a single newline character.

    Args:
        string_with_double_newline (str): The string to replace the double newline character in.

    Returns:
        str: The string with the double newline character replaced by a single newline character.
    """
    return_string: str = string_with_double_newline.replace("\\n", "\n")
    return return_string.strip()
