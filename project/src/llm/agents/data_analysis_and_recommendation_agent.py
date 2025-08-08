from src.llm.agents.agent import Agent
from src.llm.agents.knowledge_graph import KnowledgeGraph
from src.llm.workflow.agent_state import AgentState


class DataAnalysisAndRecommendationAgent(Agent):
    def _invoke(self, query: str):
        return self.llm.invoke(query)

    def process(self, state: AgentState) -> AgentState:
        _query: str | None = state.get("query")
        if _query is None:
            raise ValueError(
                "WorkflowManager.intent_classifier - There was no query in AgentState"
            )
        best_datasets = self._determine_best_datasets(_query)
        return {**state}

    def _determine_best_datasets(self, query: str) -> list[str]:
        return self.knowledge_graph.get_best_datasets(query)
