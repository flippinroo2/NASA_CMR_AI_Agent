import src.llm.agents.agent
from src.llm.workflow.agent_state import AgentState


class ResponseSynthesisAndFormattingAgent(src.llm.agents.agent.Agent):
    async def process(self, state: AgentState) -> AgentState:
        return state

    async def _update_context():
        pass
