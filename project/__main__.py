import asyncio
import random
from enum import Enum
from typing import Any

import gradio
import uvicorn
from fastapi import FastAPI

from config import Configuration
from lib.file_functions import (
    get_files_by_extension_in_directory,
    read_file_as_text_string,
)
from src.data.api_manager import CMR_ENDPOINTS, APIManager, CMRQueryParameters
from src.llm.llm_provider import LLM_PROVIDER_ENUM, LLMProvider
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager
from src.user_interface.gui import create_user_interface

app = FastAPI()  # This is used to enable concurrent handling of requests.


async def create_workflow(*args, **kwargs):
    llm_provider = LLMProvider(LLM_PROVIDER_ENUM.OLLAMA)
    workflow_manager = WorkflowManager(llm_provider)
    compiled_workflow = workflow_manager.workflow.compile()
    return compiled_workflow


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


user_interface: gradio.Blocks = create_user_interface(
    lambda *args, **kwargs: None, query_cmr
)  # TODO: Remove static lambda function
app = gradio.mount_gradio_app(app, user_interface, path="")

if __name__ == "__main__":
    if Configuration.is_debug_mode_activated:
        print("DEBUG FUNCTIONALITY ENABLED")
        # test_cmr_query = asyncio.run(
        #     query_cmr(CMR_ENDPOINTS.COLLECTIONS.name, "MODIS", 10, 1, 0)
        # )
        text_files: list[str] = get_files_by_extension_in_directory(
            Configuration.prompt_folder_path, "txt"
        )  # NOTE: These are not going to be returned sorted.
        workflow = asyncio.run(create_workflow())
        for text_file in text_files:
            text_file_content: str = read_file_as_text_string(text_file)
            # test_agent_query = asyncio.run(query_agents(text_file_content))
            workflow_result = workflow.invoke(
                AgentState(**{"query": text_file_content})
            )
        print("END")
    else:
        uvicorn.run(app, host=Configuration.host, port=Configuration.port)
