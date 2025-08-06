import asyncio
import random
from enum import Enum
from typing import Any

import gradio
import uvicorn
from fastapi import FastAPI

from config import Configuration
from src.data.api_manager import CMR_ENDPOINTS, APIManager, CMRQueryParameters
from src.llm_provider import LLM_PROVIDER_ENUM, LLMProvider
from src.user_interface.gui import create_user_interface

print("\n__main__.py\n")

app = FastAPI()  # This is used to enable concurrent handling of requests. We mount the gradio interface as a FastAPI endpoint and then ...???


def connect_to_llm():
    _llm_provider = LLMProvider(LLM_PROVIDER_ENUM.OLLAMA)
    _llm = _llm_provider.get_llm("Ollama")
    return _llm


async def query_agents(*args, **kwargs):
    # TODO: This is where the output from agents should be displayed... NEED TO IMPLEMENT STREAMING TOO!
    # llm = connect_to_llm()
    data = query_cmr()
    return data


async def query_cmr(
    endpoint: str,
    search_query: str,
    page_size: int,
    page_number: int,
    offset: int | None,
    *args,
    **kwargs,
):
    try:
        _endpoint_mapping: CMR_ENDPOINTS = CMR_ENDPOINTS[endpoint]
    except KeyError as e:
        print(f"query_cmr() - CMR_ENDPOINTS[endpoint] - KeyError: {e}")
        return  # Returning if invalid to save program from exiting.

    _params: dict[str, Any] | None = None
    if _endpoint_mapping == CMR_ENDPOINTS.AUTOCOMPLETE:
        _params = {"q": search_query}
    else:
        _params = {
            "keyword": search_query
        }  # Might also want to have a parameter for type of search... Like "keyword" or not.
    if _params:
        _return_value = await APIManager.query_cmr(
            _endpoint_mapping,
            params={**_params, "page_size": page_size},
        )
        return _return_value  # TODO: Just return the call after this is ironed out... Can do debugging in APIManager class if needed.


user_interface: gradio.Blocks = create_user_interface(query_agents, query_cmr)
app = gradio.mount_gradio_app(
    app, user_interface, path=""
)  # TODO: Figure out why we're using FastAPI and uvicorn instead of just calling gradio (Probably to prevent the UI thread from blocking the main thread)

if __name__ == "__main__":
    config = Configuration()
    if config.is_debug_mode_activated:
        print("DEBUG FUNCTIONALITY ENABLED")
        test_cmr_query = asyncio.run(
            query_cmr(CMR_ENDPOINTS.COLLECTIONS.name, "MODIS", 10, 1, 0)
        )
        print("END")
    else:
        uvicorn.run(app, host=config.host, port=config.port)
