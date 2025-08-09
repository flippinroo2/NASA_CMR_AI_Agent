import unittest

import pytest

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.query_interpretation_and_validation_agent import (
    QueryInterpretationAndValidationAgent,
)
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState


class TestQueryInterpretationAndValidationAgent(unittest.TestCase):
    test_query = "Why do you think 2024 had such powerful storms towards the end of the year?"  # TODO: Load the json file with test cases instead of using this hard coded string here.

    def setUp(self):
        llm = LLMProvider(LLM_PROVIDER.OLLAMA).get_llm()
        self.agent = QueryInterpretationAndValidationAgent(llm)
        self.test_state = AgentState(query=self.test_query)

    @pytest.mark.mypy_testing
    def test_01_query_intent(self) -> None:
        """
        Ensures that the query_intent() method returns a value that is an integer between 1 and 3
        """
        query_intent: int | None = self.agent._get_query_intent(self.test_query)
        assert isinstance(query_intent, int)
        if query_intent is not None:
            self.assertGreaterEqual(query_intent, 1)
            self.assertLessEqual(query_intent, 3)
        self.assertIsNotNone(query_intent)

    @pytest.mark.mypy_testing
    def test_02_identifying_sub_queries(self) -> None:
        """
        Ensures that the identify_sub_queries() method returns a list of strings.
        """
        sub_queries: list[str] = self.agent._identify_sub_queries(self.test_query)
        assert isinstance(sub_queries, list)
        assert all(isinstance(sub_query, str) for sub_query in sub_queries)

    def test_03_process_output(self) -> None:
        """
        Ensures that the process() method returns an AgentState object.
        """
        response: AgentState = self.agent.process(self.test_state)
        self.assertIsInstance(response, AgentState)


if __name__ == "__main__":
    unittest.main()
