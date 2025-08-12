import dotenv


def get_env_file_path() -> str:
    """
    Helper function for getting the path to the .env file.

    Returns:
        str: The path to the .env file.

    Raises:
        ValueError: If no .env file is found. (This type of exception is actually raised)
    """
    env_file: str = dotenv.find_dotenv()
    if env_file is None:
        raise ValueError(
            "No .env file found"
        )  # TODO: Maybe turn this into a debug message instead of raising an error here because the Configuration class has default arguments.
    return env_file


dotenv.load_dotenv(
    get_env_file_path()
)  # NOTE: This will be called when importing this module.


def get_env_file_values() -> dict[str, str | None]:
    """
    Helper function to get the values from the .env file.

    Returns:
        dict[str, str | None]: The values from the .env file.
    """
    return dotenv.dotenv_values(get_env_file_path())
