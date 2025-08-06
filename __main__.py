import asyncio
import random
from enum import Enum
from typing import Any

import gradio
import uvicorn
from fastapi import FastAPI

from config import Configuration
from src.data.api_manager import CMR_ENDPOINTS, APIManager, CMRQueryParameters
from src.llm.agent_manager import AgentManager
from src.llm.llm_provider import LLM_PROVIDER_ENUM, LLMProvider
from src.user_interface.gui import create_user_interface
from src.workflow_manager import WorkflowManager

app = FastAPI()  # This is used to enable concurrent handling of requests.


def connect_to_llm():
    _llm_provider = LLMProvider(LLM_PROVIDER_ENUM.OLLAMA)
    _llm = _llm_provider.get_llm("Ollama")
    return _llm


async def query_agents(*args, **kwargs):
    workflow_manager = WorkflowManager()
    compiled_workflow = workflow_manager.workflow.compile()

    llm_provider = LLMProvider(LLM_PROVIDER_ENUM.OLLAMA)
    agent_manager = AgentManager(llm_provider)
    return workflow_manager


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
        return  # Returning "None" if invalid endpoint is supplied to prevent program from exiting.

    _params: dict[str, Any] | None = None
    if _endpoint_mapping == CMR_ENDPOINTS.AUTOCOMPLETE:
        _params = {"q": search_query}
    else:
        _params = {"keyword": search_query}  # TODO: Extend types of searches allowed
    if _params:
        return await APIManager.query_cmr(
            _endpoint_mapping,
            params={**_params, "page_size": page_size},
        )


user_interface: gradio.Blocks = create_user_interface(query_agents, query_cmr)
app = gradio.mount_gradio_app(app, user_interface, path="")

if __name__ == "__main__":
    if Configuration.is_debug_mode_activated:
        print("DEBUG FUNCTIONALITY ENABLED")
        # test_cmr_query = asyncio.run(
        #     query_cmr(CMR_ENDPOINTS.COLLECTIONS.name, "MODIS", 10, 1, 0)
        # )
        test_agent_query = asyncio.run(query_agents())
        print("END")
    else:
        uvicorn.run(app, host=Configuration.host, port=Configuration.port)
