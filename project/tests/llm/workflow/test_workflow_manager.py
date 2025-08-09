import asyncio
import unittest
from typing import Any

import pytest

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager


class TestCMRApiAgent(unittest.TestCase):
    workflow: WorkflowManager

    def setUp(self):
        workflow = WorkflowManager(LLMProvider(LLM_PROVIDER.OLLAMA))

    def test_01(self) -> None:
        test = self.workflow
        print("DEBUG")
