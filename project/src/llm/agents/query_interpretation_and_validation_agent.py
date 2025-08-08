from lib.string_functions import sanitize_llm_output
from src.llm.agents.agent import Agent
from src.llm.agents.enums import CMR_QUERY_INTENTION_ENUM
from src.llm.agents.knowledge_graph import KnowledgeGraph
from src.llm.workflow.agent_state import AgentState


class QueryInterpretationAndValidationAgent(Agent):
    def _invoke(self, query: str) -> str:
        return self.llm.invoke(query)

    def _get_query_intent(self, query: str) -> CMR_QUERY_INTENTION_ENUM | None:
        _prompt = f"""Classify the following query into one of these categories:
        1. Exploratory request
        2. Specific data request
        3. Analytical query

        ONLY RETURN THE NUMBER OF THE CATEGORY, DO NOT PROVIDE ANY OTHER EXPLANATION!

        Query: {query}"""
        _llm_output: str = self._invoke(_prompt)
        if _llm_output is None:
            raise ValueError(
                "QueryInterpretationAndValidationAgent._get_query_intent() - LLM returned None"
            )
        _sanitized_llm_output = sanitize_llm_output(_llm_output)
        try:
            _llm_output_as_integer = int(_sanitized_llm_output)
            _llm_output_as_enum = CMR_QUERY_INTENTION_ENUM(_llm_output_as_integer)
            return _llm_output_as_enum
        except (ValueError, TypeError) as e:
            print(
                f"QueryInterpretationAndValidationAgent._get_query_intent() - Error: {e}"
            )

    def _enrich_query_with_context(self, state: AgentState) -> str:
        _query: str | None = state.get("query")
        _context_manager = state.get("context")
        context = self.context_manager.get_relevant_context(query, intent)
        return f"{query}\n\nRelevant context: {context}"

    def _identify_sub_queries(self, query: str) -> list[str]:
        _prompt = f"""Break this complex query into simpler sub-queries:
        {query}

        Return as a list of distinct sub-queries separated by a single newline character.
        
        DO NOT INCLUDE ANY EXPLANATION! ONLY RETURN AN UNORDERED LIST OF QUESTIONS! DO NOT NUMBER THE LIST ITEMS!
        """
        _llm_output = self._invoke(_prompt)
        _identified_subqueries = _llm_output.splitlines()
        # TODO: Do some type of validation here to ensure we get a list of strings back.
        return _identified_subqueries

    def process(self, state: AgentState) -> AgentState:
        _query: str | None = state.get("query")
        if _query is None:
            raise ValueError(
                "WorkflowManager.intent_classifier - There was no query in AgentState"
            )
        _enriched_query = self._enrich_query_with_context(state)
        _intent = self._get_query_intent(_enriched_query)
        sub_queries = self._identify_sub_queries(_enriched_query)
        return {**state, "intent": _intent, "sub_queries": sub_queries}
