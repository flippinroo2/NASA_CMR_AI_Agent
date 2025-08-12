from src.llm.agents.agent import Agent
from src.llm.workflow.agent_state import AgentState


class ResponseSynthesisAndFormattingAgent(Agent):
    async def process(self, state: AgentState) -> AgentState:
        return state

    async def _update_context():
        pass
