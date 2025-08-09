from enum import Enum, StrEnum
from typing import Type, TypeVar

T_Enum = TypeVar("T_Enum", bound=Enum)


# TODO: Is this function used?
def convert_string_enum_to_string(enum_to_convert: StrEnum) -> str:
    return str(enum_to_convert)


# TODO: Is this function used?
def convert_string_to_string_enum(
    string_to_convert: str, enum_to_convert_to: StrEnum
) -> StrEnum:
    pass


def safe_get_enum_value(
    enum_type: Type[T_Enum], value_to_get, is_in_debug_mode=False
) -> T_Enum | None:
    try:
        return enum_type[value_to_get]
    except KeyError as e:
        if is_in_debug_mode:
            print("safe_get_enum_value() - Invalid Enum Value", e)
