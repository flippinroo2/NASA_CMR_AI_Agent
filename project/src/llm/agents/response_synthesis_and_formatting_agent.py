from src.llm.agents.agent import Agent
from src.llm.knowledge_graph import KnowledgeGraph
from src.llm.workflow.agent_state import AgentState


class ResponseSynthesisAndFormattingAgent(Agent):
    def process(self, state: AgentState) -> AgentState:
        return state

    def _update_context():
        pass
