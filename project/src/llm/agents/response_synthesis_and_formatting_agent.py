from src.llm.agents.agent import Agent
from src.llm.agents.knowledge_graph import KnowledgeGraph
from src.llm.workflow.agent_state import AgentState


class ResponseSynthesisAndFormattingAgent(Agent):
    def _invoke(self, query: str):
        return self.llm.invoke(query)

    def process(self, state: AgentState) -> AgentState:
        return state

    def _update_context():
        pass
