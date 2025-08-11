import asyncio
from typing import Any

import pytest
from langgraph.graph.state import CompiledStateGraph

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager
from tests.fixtures import get_fixture_workflow_manager


def test_01(get_fixture_workflow_manager: WorkflowManager) -> None:
    if get_fixture_workflow_manager.state_graph is not None:
        # compiled_state_graph: CompiledStateGraph = (
        #     get_fixture_workflow_manager.state_graph.compile()
        # )
        print("DEBUG")
