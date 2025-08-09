import asyncio
import unittest
from typing import Any

import pytest
from langgraph.graph.state import CompiledStateGraph

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager


class TestCMRApiAgent(unittest.TestCase):
    test_query: str = "Why do you think 2024 had such powerful storms towards the end of the year?"  # TODO: Load the json file with test cases instead of using this hard coded string here.
    test_state: AgentState | None = None
    workflow_manager: WorkflowManager | None = None

    def setUp(self) -> None:
        test_state = AgentState(query=self.test_query)
        workflow_manager = WorkflowManager(LLMProvider(LLM_PROVIDER.OLLAMA))

    def test_01(self) -> None:
        test: CompiledStateGraph = self.workflow_manager.workflow.compile()
        if test is not None:
            print("DEBUG")
