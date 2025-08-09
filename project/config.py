import os
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar

from lib.enum_functions import safe_get_enum_value
from lib.environment_functions import get_env_file_values
from lib.file_functions import does_file_exist, read_yaml_file_as_dictionary


class CONFIGURATION_VALUE_ENUM(Enum):
    AVAILABLE_LLM_PROVIDERS = "available_llm_providers"
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


class ENVIRONMENT_VARIABLE_ENUM(Enum):
    CONFIGURATION_FILEPATH = "configuration_filepath"
    CREDENTIALS = "credentials"


class Configuration:
    _initialized: ClassVar[bool] = False
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _production_endpoint: ClassVar[str] = "https://cmr.earthdata.nasa.gov/search/"
    _test_endpoint: ClassVar[str] = "https://cmr.uat.earthdata.nasa.gov/search/"
    available_llm_providers: ClassVar[list[str]] = []
    base_endpoint: ClassVar[str] = ""
    configuration_filepath: ClassVar[str] = "project/config.yaml"
    credentials: ClassVar[str | None] = None
    host: ClassVar[str] = "0.0.0.0"
    is_debug_mode_activated: ClassVar[bool] = False
    is_production_mode_activated: ClassVar[bool] = False
    is_streaming_enabled: ClassVar[bool] = True
    log_folder_path: ClassVar[str] = "project/logs"
    max_concurrent_requests: ClassVar[int] = 10
    port: ClassVar[int] = 5050
    prompt_folder_path: ClassVar[str] = "project/prompts"
    request_timeout: ClassVar[int] = 30
    stream_chunk_size: ClassVar[int] = 10

    @classmethod
    def __init__(cls) -> None:
        if cls._initialized:
            return  # NOTE: This ensures we only initialize the class one time. Creating a proper singleton object useable throughout the entire application.

        cls._set_env_file_values()
        cls._set_configuration_file_values()

        if cls.is_production_mode_activated:
            cls.base_endpoint = cls._production_endpoint
        else:
            cls.base_endpoint = cls._test_endpoint

        if not does_file_exist(cls.prompt_folder_path):
            cls.prompt_folder_path = f"project/{cls.prompt_folder_path}"  # TODO: Make this more dynamic instead of hard coding.

    @classmethod
    def _get_filepaths(cls):
        pass

    @classmethod
    def _get_configuration_file_content(cls):
        _configuration_file_content = read_yaml_file_as_dictionary(
            cls.configuration_filepath
        )
        if _configuration_file_content is not None:
            return _configuration_file_content
        if cls.is_debug_mode_activated:
            print(
                f"Attempting to read configuration file from project/{cls.configuration_filepath}..."
            )
        return read_yaml_file_as_dictionary(
            f"project/{cls.configuration_filepath}"
        )  # TODO: Make this a bit more dynamic instead of hard coding.

    @classmethod
    def _safe_set_class_value(cls, key: str, value: Any) -> None:
        try:
            setattr(cls, key, value)
        except AttributeError as e:
            print(f"AttributeError: {e}")
        except RecursionError as e:
            print(f"RecursionError: {e}")
            raise e  # NOTE: Only raising the Exception for non-acceptable errors.
        except TypeError as e:
            print(f"TypeError: {e}")
        except Exception as e:
            print(f"Exception: {e}")
            raise e  # NOTE: Only raising the Exception for non-acceptable errors.

    @classmethod
    def _set_configuration_file_values(cls) -> None:
        with (
            cls._lock
        ):  # NOTE: This is used to ensure thread safety when changing static values.
            _configuration_file_values: dict[str, Any] | None = (
                cls._get_configuration_file_content()
            )
            if _configuration_file_values is not None:
                for _configuration_item in _configuration_file_values.items():
                    _configuration_name, _configuration_value = _configuration_item
                    _configuration_value_to_property_mapping: (
                        CONFIGURATION_VALUE_ENUM | None
                    ) = safe_get_enum_value(
                        CONFIGURATION_VALUE_ENUM, _configuration_name
                    )  # NOTE: This is to ensure that values in the configuration file are valid. These values are mapped to properties defined in the Configuration class.
                    if _configuration_value_to_property_mapping is not None:
                        cls._safe_set_class_value(
                            _configuration_value_to_property_mapping.value,
                            _configuration_value,
                        )  # NOTE: Setting the values in the Configuration class to the mapping values from above.
                    else:
                        print("Invalid Configuration Value", _configuration_name)
            else:
                print("config.py - Configuration file contained no values.")

    @classmethod
    def _set_env_file_values(cls) -> None:
        _env_file_values: dict[str, str | None] = get_env_file_values()
        _credentials: str | None = _env_file_values.get("CREDENTIALS", None)
        with cls._lock:
            if _credentials is not None and _credentials != "":
                print("TODO: Handle credentials here")  # TODO: Handle credentials here
            for _env_file_key, _env_file_value in _env_file_values.items():
                _env_value_to_property_mapping: ENVIRONMENT_VARIABLE_ENUM | None = (
                    safe_get_enum_value(ENVIRONMENT_VARIABLE_ENUM, _env_file_key)
                )
                if _env_value_to_property_mapping is not None:
                    cls._safe_set_class_value(
                        _env_value_to_property_mapping.value, _env_file_value
                    )
                else:
                    cls._safe_set_class_value(_env_file_key, _env_file_value)


Configuration()  # NOTE: This is a singleton since there is protection inside the __init__ method to prevent multiple instances from being created.
