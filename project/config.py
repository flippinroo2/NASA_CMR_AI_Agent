import os
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar

import yaml
from dotenv import dotenv_values, find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# NOTE: IF THIS CLASS IS GOING TO BE STATIC WE NEED TO USE LOCKS FOR THREAD SAFETY


class CONFIGURATION_VALUE_ENUM(Enum):
    DEBUG = "is_debug_mode_activated"
    ENABLE_STREAMING = "is_streaming_enabled"
    HOST = "host"
    LLM_PROVIDERS = "available_llm_providers"
    LOG_FOLDER_PATH = "log_folder_path"
    MAX_CONCURRENT_REQUESTS = "max_concurrent_requests"
    PORT = "port"
    PRODUCTION_MODE = "is_production_mode_activated"
    PRODUCTION_ENDPOINT = "_production_endpoint"
    PROMPT_FOLDER_PATH = "prompt_folder_path"
    REQUEST_TIMEOUT = "request_timeout"
    STREAM_CHUNK_SIZE = "stream_chunk_size"
    TEST_ENDPOINT = "_test_endpoint"


@dataclass
class EnvironmentVariableConfiguration:
    configuration_filepath: str = field()
    credentials: str | None = None


DEBUG: bool = False


class Configuration:
    _initialized: ClassVar[bool] = False
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _production_endpoint: ClassVar[str] = "https://cmr.earthdata.nasa.gov/search/"
    _test_endpoint: ClassVar[str] = "https://cmr.uat.earthdata.nasa.gov/search/"
    available_llm_providers: ClassVar[list[dict[str, str]]] = []
    base_endpoint: ClassVar[str] = ""
    configuration_filepath: ClassVar[str] = "project/config.yaml"
    host: ClassVar[str] = "0.0.0.0"
    is_debug_mode_activated: ClassVar[bool] = False
    is_production_mode_activated: ClassVar[bool] = False
    is_streaming_enabled: ClassVar[bool] = True
    log_folder_path: ClassVar[str] = "logs"
    max_concurrent_requests: ClassVar[int] = 10
    port: ClassVar[int] = 5050
    prompt_folder_path: ClassVar[str] = "prompts"
    request_timeout: ClassVar[int] = 30
    stream_chunk_size: ClassVar[int] = 10

    @classmethod
    def __init__(cls) -> None:
        if cls._initialized:
            return  # This ensures we only set these values one time.
        cls.read_env_file()
        cls._set_configuration_file_values()
        if cls.is_production_mode_activated:
            cls.base_endpoint = cls._production_endpoint
        else:
            cls.base_endpoint = cls._test_endpoint
        global DEBUG
        DEBUG = cls.is_debug_mode_activated

    @staticmethod
    def get_env_file_values():
        return dotenv_values(find_dotenv())

    @staticmethod
    def get_yaml_file_values(yaml_filepath: str):
        try:
            with open(yaml_filepath, "r") as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error reading {yaml_filepath}: {e}")

    @classmethod
    def get_configuration_file_values(cls) -> dict[str, Any] | None:
        _configuration_file_values = cls.get_yaml_file_values(
            cls.configuration_filepath
        )
        return _configuration_file_values

    @classmethod
    def _set_configuration_file_values(cls):
        with (
            cls._lock
        ):  # TODO: This is used to ensure thread safety when changing static values.
            _configuration_file_values = cls.get_configuration_file_values()
            if _configuration_file_values is not None:
                for _configuration_item in _configuration_file_values.items():
                    _configuration_name, _configuration_value = _configuration_item
                    try:
                        _configuration_value_to_property_mapping = CONFIGURATION_VALUE_ENUM[
                            _configuration_name
                        ]  # This is to ensure that values in the configuration file are valid. These values are mapped to properties defined in the Configuration class.
                        setattr(
                            cls,
                            _configuration_value_to_property_mapping.value,
                            _configuration_value,
                        )  # Setting the values in the Configuration class to the mapping values from above.
                    except AttributeError as e:
                        print(f"AttributeError: {e}")
                    except KeyError as e:
                        print("Invalid Configuration File")
                        print(f"KeyError: {e}")
                    except RecursionError as e:
                        print(f"RecursionError: {e}")
                    except TypeError as e:
                        print(f"TypeError: {e}")

    @classmethod
    def read_env_file(cls):
        _env_file_values = cls.get_env_file_values()
        _credentials = _env_file_values.get("CREDENTIALS", None)
        with cls._lock:
            if _credentials is not None and _credentials != "":
                # TODO: Handle credentials here
                return


Configuration()  # NOTE: This is a singleton since there is protection inside the __init__ method to prevent multiple instances from being created.
