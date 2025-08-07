import json
from typing import Any


def format_json_string(json_string: str, indent_size: int = 2) -> str:
    json_loaded_string: Any = json.loads(json_string)
    formatted_json_string: str = json.dumps(json_loaded_string, indent=indent_size)
    return formatted_json_string
