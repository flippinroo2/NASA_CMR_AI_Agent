from abc import ABC, abstractmethod

from lib.string_functions import replace_double_newline
from src.llm.knowledge_graph import KnowledgeGraph
from src.llm.workflow.agent_state import AgentState

# NOTE: Wanted to use an abstract class here even though it isn't very useful at the moment to show my knowledge of how they work.


# Abstract Agent class
class Agent(ABC):
    knowledge_graph: KnowledgeGraph

    def __init__(self, llm) -> None:
        self.llm = llm
        self.knowledge_graph = KnowledgeGraph()

    def _invoke(self, query: str):
        _llm_response = self.llm.invoke(query)
        _sanitized_llm_response = self._sanitize_llm_output(_llm_response)
        return _sanitized_llm_response
    
    def _sanitize_llm_output(self, llm_output: str) -> str:
        return replace_double_newline(llm_output)

    def get_agent_llm_class(self) -> str:
        # TODO: Is this function needed?
        return self.llm.__class__.__name__

    @abstractmethod
    def process(self, state: AgentState) -> AgentState:
        pass
