import src.llm.agents.agent
from src.llm.workflow.agent_state import AgentState


class DataAnalysisAndRecommendationAgent(src.llm.agents.agent.Agent):
    async def process(self, state: AgentState) -> AgentState:
        query: str | None = state.query
        if query is None:
            raise ValueError(
                "WorkflowManager.intent_classifier - There was no query in AgentState"
            )
        best_datasets = self._determine_best_datasets(query)
        return {**state}

    async def _determine_best_datasets(self, query: str) -> list[str]:
        return self.knowledge_graph.get_best_datasets(query)
