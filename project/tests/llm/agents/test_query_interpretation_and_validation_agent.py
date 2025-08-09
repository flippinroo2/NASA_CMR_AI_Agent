import unittest

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

    def test_query_intent(self):
        query_intent: int | None = self.agent._get_query_intent(self.test_query)
        self.assertIsNotNone(query_intent)
        self.assertIsInstance(query_intent, int)
        self.assertGreaterEqual(query_intent, 1)
        self.assertLessEqual(query_intent, 3)

    def test_identifying_sub_queries(self):
        response: AgentState = self.agent.process(self.test_state)
        print("DEBUG: ", response)

    def test_process_output(self):
        """
        Ensures that the process method returns an AgentState object.
        """
        response: AgentState = self.agent.process(self.test_state)
        self.assertIsInstance(response, AgentState)


if __name__ == "__main__":
    unittest.main()
