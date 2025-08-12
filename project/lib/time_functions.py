from time import time


def get_timestamp() -> int:
    """
    Helper function for getting the current UNIX timestamp.

    Returns:
        int: The current UNIX timestamp.
    """
    return int(time())
