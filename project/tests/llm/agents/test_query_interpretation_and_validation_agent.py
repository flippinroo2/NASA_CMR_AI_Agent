import unittest

from src.llm.agents.agent_state import AgentState
from src.llm.agents.query_interpretation_and_validation_agent import (
    QueryInterpretationAndValidationAgent,
)
from src.llm.llm_provider import LLM_PROVIDER_ENUM, LLMProvider


class TestQueryInterpretationAndValidationAgent(unittest.TestCase):
    test_query = (
        "Why do you think 2024 had such powerful storms towards the end of the year?"
    )

    def setUp(self):
        llm = LLMProvider(LLM_PROVIDER_ENUM.OLLAMA).get_llm()
        self.agent = QueryInterpretationAndValidationAgent(llm)

    def test_structured_output(self):
        _simulated_agent_state = AgentState(
            query=self.test_query,
        )
        _response = self.agent.process(_simulated_agent_state)
        print("DEBUG")


if __name__ == "__main__":
    unittest.main()
