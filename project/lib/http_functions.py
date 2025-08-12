from typing import Any

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError, InvalidUrlClientError


async def get_request(url: str, parameters: dict[str, Any] | None = None) -> Any:
    """
    Helper function for making a HTTP GET request.

    Args:
        url (str): The URL to make the request to.
        parameters (dict[str, Any] | None): The parameters to include in the request. Defaults to None.

    Returns:
        Any: The response from the request in JSON format.

    Raises:
        ClientResponseError: The HTTP response returned an invalid status code.
        InvalidUrlClientError: The URL provided was not valid.
        TypeError: The parameters given were not of the appropriate type.
        Exception: A catch-all exception for anything not covered above.
    """
    if parameters is None:
        parameters = {}
    try:
        async with (
            ClientSession() as session,
            session.get(url, params=parameters) as response,
        ):
            response.raise_for_status()
            return await response.json()
    except ClientResponseError as exception:
        print(f"get_request() - ClientResponseError: {exception}")
    except InvalidUrlClientError as exception:
        print(f"get_request() - InvalidUrlClientError: {exception}")
    except TypeError as exception:
        print(f"get_request() - TypeError: {exception}")
    except Exception as exception:
        print(f"get_request() - Exception: {exception}")
        raise exception
