from abc import ABC, abstractmethod

import langchain.chat_models.base
import langchain_core.language_models
import langchain_core.language_models.base

import lib.string_functions
import src.data.knowledge_graph
from src.llm.workflow.agent_state import AgentState

# NOTE: Wanted to use an abstract class here even though it isn't very useful at the moment to show my knowledge of how they work.


# Abstract Agent class
class Agent(ABC):
    _llm: langchain.chat_models.base._ConfigurableModel | langchain_core.language_models.BaseLLM
    knowledge_graph: src.data.knowledge_graph.KnowledgeGraph | None = (
        None  # TODO: Remove the None and actually implement a knowledge graph
    )

    def __init__(self, llm: langchain.chat_models.base._ConfigurableModel | langchain_core.language_models.BaseLLM) -> None:
        self._llm = llm
        # self.knowledge_graph = KnowledgeGraph() # TODO: Re-enable knowledge graph

    def _invoke(self, query: langchain_core.language_models.base.LanguageModelInput) -> str:
        llm_response = self._llm.invoke(query)
        sanitized_llm_response = self._sanitize_llm_output(llm_response)
        return sanitized_llm_response

    def _sanitize_llm_output(self, llm_output: str) -> str:
        return lib.string_functions.replace_double_newline(llm_output)

    def get_agent_llm_class(self) -> str:
        # TODO: Is this function needed?
        return self._llm.__class__.__name__

    def get_llm(self) -> langchain.chat_models.base._ConfigurableModel | langchain_core.language_models.BaseLLM:
        return self._llm

    @abstractmethod
    async def process(self, state: AgentState) -> AgentState:
        pass
