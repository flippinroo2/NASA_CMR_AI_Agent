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
        pass

    def test_identifying_sub_queries(self):
        pass

    def test_process_output(self):
        response: AgentState = self.agent.process(self.test_state)
        self.assertIsInstance(response, AgentState)


if __name__ == "__main__":
    unittest.main()
