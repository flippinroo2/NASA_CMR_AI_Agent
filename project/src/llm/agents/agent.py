from abc import ABC, abstractmethod

from src.llm.agents.knowledge_graph import KnowledgeGraph

# NOTE: Wanted to use an abstract class here even though it isn't very useful at the moment to show my knowledge of how they work.


# Abstract Agent class
class Agent(ABC):
    knowledge_graph: KnowledgeGraph

    def __init__(self, llm) -> None:
        self.llm = llm
        self.knowledge_graph = KnowledgeGraph()

    @abstractmethod
    def _invoke(self, query: str):
        return self.llm.invoke(query)

    def get_agent_class(self) -> str:
        # return self.llm
        return ""
