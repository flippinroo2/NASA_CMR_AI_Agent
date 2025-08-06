from enum import Enum
import os
from typing import Any, ClassVar
import yaml
import threading
from dotenv import dotenv_values, find_dotenv, load_dotenv
from dataclasses import dataclass, field

load_dotenv(find_dotenv())

# NOTE: IF THIS CLASS IS GOING TO BE STATIC WE NEED TO USE LOCKS FOR THREAD SAFETY


class CONFIGURATION_VALUE_ENUM(Enum):
    AGENT_LIST = "AGENT_LIST"
    DEBUG = "is_debug_mode_activated"
    HOST = "host"
    LLM_PROVIDERS = "available_llm_providers"
    PORT = "port"
    PRODUCTION_MODE = "is_production_mode_activated"
    PRODUCTION_ENDPOINT = "_production_endpoint"
    TEST_ENDPOINT = "_test_endpoint"


@dataclass
class EnvironmentVariableConfiguration:
    # credentials: str | None = None
    credentials: str = field()


DEBUG: bool = False


class Configuration:
    _initialized: ClassVar[bool] = False
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _production_endpoint: ClassVar[str] = ""
    _test_endpoint: ClassVar[str] = ""
    available_llm_providers: ClassVar[list[dict[str, str]]] = []
    base_endpoint: ClassVar[str] = ""
    configuration_filepath: ClassVar[str] = "config.yaml"
    host: ClassVar[str] = "0.0.0.0"
    is_debug_mode_activated: ClassVar[bool] = False
    is_production_mode_activated: ClassVar[bool] = False
    port: ClassVar[int] = 5050

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
        with cls._lock: # TODO: This is used to ensure thread safety when changing static values.
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
        # TODO: Handle credentials here
        with cls._lock:
          if _credentials is not None and _credentials != "":
              # CONFIGURATION_VALUE_ENUM.PRODUCTION_ENDPOINT = "base_endpoint"
              print("TODO: Handle credentials here")
          else:
              # CONFIGURATION_VALUE_ENUM.TEST_ENDPOINT = "base_endpoint"
              print("TODO: Handle credentials here")


# Configuration()  # TODO: Put this back and make this static somehow so we don't need to create an instance and have it global?
