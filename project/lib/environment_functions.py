from dotenv import dotenv_values, find_dotenv, load_dotenv


def get_env_file_path() -> str:
    env_file: str = find_dotenv()
    if env_file is None:
        raise ValueError(
            "No .env file found"
        )  # TODO: Make this occur on MacBook and then solve for this.
    return env_file


load_dotenv(get_env_file_path())


def get_env_file_values() -> dict[str, str | None]:
    return dotenv_values(get_env_file_path())
