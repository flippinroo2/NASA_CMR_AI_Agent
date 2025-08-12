from enum import Enum
from typing import Type, TypeVar

T_Enum = TypeVar("T_Enum", bound=Enum)


def safe_get_enum_value(enum_type: Type[T_Enum], value_to_get: str) -> T_Enum | None:
    # TODO: Verify only strings are used here for "value_to_get"
    """
    Helper function for safely getting the value from an Enum type based on a provided key.

    Args:
        enum_type (T_Enum): The type of Enum to select a value from.
        value_to_get (str): The key to use for selecting a value from an Enum type.

    Returns:
        T_Enum | None: Will return the value from the Enum type as long as the provided key is valid. If not, will return None

    Raises:
        KeyError: If the provided key is not found in the Enum type.

    Notes:
        If the value is not valid we are capturing the error to allow the application to continue running.
    """
    # TODO: Verify the return is actually "T_Enum"?
    try:
        return enum_type[value_to_get]
    except KeyError as e:
        print("safe_get_enum_value() - Invalid Enum Value", e)
