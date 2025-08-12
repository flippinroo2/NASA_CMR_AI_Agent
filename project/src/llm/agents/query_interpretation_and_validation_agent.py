from src.llm.agents.agent import Agent
from src.llm.workflow.agent_state import AgentState


class QueryInterpretationAndValidationAgent(Agent):
    async def process(self, state: AgentState) -> AgentState:
        query: str = state.query
        if query is None:
            raise ValueError(
                "WorkflowManager.intent_classifier - There was no query in AgentState"
            )
        enriched_query = await self._enrich_query_with_context(state)
        intent = await self._get_query_intent(enriched_query)
        sub_queries = await self._identify_sub_queries(enriched_query)
        return AgentState(
            **{**state.model_dump(), "intent": intent, "sub_queries": sub_queries}
        )

    async def _get_query_intent(self, query: str) -> int | None:
        prompt = f"""Classify the following query into one of these categories:
        1. Exploratory request
        2. Specific data request
        3. Analytical query

        ONLY RETURN THE NUMBER OF THE CATEGORY, DO NOT PROVIDE ANY OTHER EXPLANATION!

        Query: {query}"""
        llm_output: str = self._invoke(prompt)
        if llm_output is None:
            raise ValueError(
                "QueryInterpretationAndValidationAgent._get_query_intent() - LLM returned None"
            )
        try:
            llm_output_as_integer = int(llm_output)
            return llm_output_as_integer
        except (ValueError, TypeError) as e:
            print(
                f"QueryInterpretationAndValidationAgent._get_query_intent() - Error: {e}"
            )

    async def _enrich_query_with_context(self, state: AgentState) -> str:
        # TODO: Add context management here
        # _context_manager = state.context
        # _relevant_context = _context_manager.get_relevant_context(
        #     state.query, state.intent
        # )
        relevant_context = state.query
        return f"{state.query}\n\nRelevant context: {relevant_context}"

    async def _identify_sub_queries(self, query: str) -> list[str]:
        _prompt = f"""Break this complex query into simpler sub-queries:
        {query}

        Return as a list of distinct sub-queries separated by a single newline character.
        
        DO NOT INCLUDE ANY EXPLANATION! ONLY RETURN AN UNORDERED LIST OF QUESTIONS! DO NOT NUMBER THE LIST ITEMS!
        """
        llm_output = self._invoke(_prompt)
        identified_subqueries = llm_output.splitlines()
        # TODO: Do some type of validation here to ensure we get a list of strings back.
        return identified_subqueries
