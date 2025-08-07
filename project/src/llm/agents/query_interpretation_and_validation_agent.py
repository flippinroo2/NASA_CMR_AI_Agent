from lib.string_functions import sanitize_llm_output
from src.knowledge_graph import KnowledgeGraph
from src.llm.agents.agent import Agent
from src.llm.agents.agent_state import AgentState
from src.llm.context_manager import ContextManager


class QueryInterpretationAndValidationAgent(Agent):
    def invoke(self, query: str) -> str:
        return self.llm.invoke(query)

    def get_query_intent(self, query: str):
        _prompt = f"""Classify the following query into one of these categories:
        1. Exploratory request
        2. Specific data request
        3. Analytical query

        ONLY RETURN THE NUMBER OF THE CATEGORY, DO NOT PROVIDE ANY OTHER EXPLANATION!

        Query: {query}"""
        _llm_output = self.invoke(_prompt)
        _return_value = sanitize_llm_output(_llm_output)
        # TODO: Do some type of validation here to ensure the return value is only a single number... (Possibly cast it to integer here?)
        return _return_value

    def identify_sub_queries(self, query: str) -> list[str]:
        _prompt = f"""Break this complex query into simpler sub-queries:
        {query}

        Return as a list of distinct sub-queries separated by a single newline character.
        
        DO NOT INCLUDE ANY EXPLANATION! ONLY RETURN AN UNORDERED LIST OF QUESTIONS! DO NOT NUMBER THE LIST ITEMS!
        """
        _llm_output = self.invoke(_prompt)
        _identified_subqueries = _llm_output.splitlines()
        # TODO: Do some type of validation here to ensure we get a list of strings back.
        return _identified_subqueries

    def process(self, state: AgentState) -> AgentState:
        _query: str | None = state.get("query")
        if _query is None:
            raise ValueError(
                "WorkflowManager.intent_classifier - There was no query in AgentState"
            )
        intent = self.get_query_intent(_query)
        sub_queries = self.identify_sub_queries(_query)
        return {**state, "intent": intent, "sub_queries": sub_queries}
