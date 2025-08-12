import asyncio

import gradio
import uvicorn
from fastapi import FastAPI

from config import Configuration
from lib.file_functions import (
    get_files_by_extension_in_directory,
    read_file_as_text_string,
)
from src.ENUMS import LLM_PROVIDER
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager
from src.user_interface.gui import create_user_interface

app = FastAPI()  # This is used to enable concurrent handling of requests.


async def create_workflow(*args, **kwargs):
    """
    Create a compiled StateGraph from langgraph.
    """
    llm_provider = LLMProvider(LLM_PROVIDER.OLLAMA)
    workflow_manager = WorkflowManager(llm_provider)
    compiled_workflow = workflow_manager.state_graph.compile()
    return compiled_workflow


async def debug(*args, **kwargs):
    """
    A debug function used for quick development.
    """
    text_files: list[str] = get_files_by_extension_in_directory(
        Configuration.prompt_folder_path, "txt"
    )  # NOTE: These are not going to be returned sorted.
    workflow = await create_workflow()
    workflow_results = []
    for text_file in text_files:
        text_file_content: str = read_file_as_text_string(text_file)
        # test_agent_query = asyncio.run(query_agents(text_file_content))
        workflow_result = await workflow.ainvoke(AgentState(query=text_file_content))
        workflow_results.append(workflow_result)
    return workflow_results


async def test(*args, **kwargs):
    """
    A test function used for even-quicker development.
    """
    print("test()")


user_interface: gradio.Blocks = create_user_interface(
    lambda *args, **kwargs: None
)  # TODO: Remove static lambda function
app = gradio.mount_gradio_app(
    app, user_interface, path=""
)  # NOTE: Creating a gradio application to be used as the user interface.

if __name__ == "__main__":
    if Configuration.is_debug_mode_activated:
        print("DEBUG FUNCTIONALITY ENABLED")
        test_output = asyncio.run(test())
        debut_output = asyncio.run(debug())
        print("END")
    else:
        uvicorn.run(
            app, host=Configuration.host, port=Configuration.port
        )  # NOTE: Running the gradio application with uvicorn to allow for concurrency.
