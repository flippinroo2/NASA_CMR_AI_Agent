import unittest

import pytest

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState


class TestCMRApiAgent(unittest.TestCase):
    test_query = "Why do you think 2024 had such powerful storms towards the end of the year?"  # TODO: Load the json file with test cases instead of using this hard coded string here.

    def setUp(self):
        llm = LLMProvider(LLM_PROVIDER.OLLAMA).get_llm()
        self.agent = CMRApiAgent(llm)
        self.test_state = AgentState(query=self.test_query)

    def test_01_test_api_request(self):
        response = None

        def test_query_intent_1(self) -> None:
            response = self.agent._build_cmr_request_from_query(self.test_query, 1)
            print("DEBUG")

        def test_query_intent_2(self) -> None:
            response = self.agent._build_cmr_request_from_query(self.test_query, 2)
            print("DEBUG")

        def test_query_intent_3(self) -> None:
            response = self.agent._build_cmr_request_from_query(self.test_query, 3)
            print("DEBUG")

        self.assertIsNotNone(response)

    def test_05_process_output(self):
        """
        Ensures that the process() method returns an AgentState object.
        """
        response: AgentState = self.agent.process(self.test_state)
        self.assertIsInstance(response, AgentState)


if __name__ == "__main__":
    unittest.main()
