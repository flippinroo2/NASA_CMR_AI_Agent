import asyncio
from pprint import pformat
from typing import Any, TypedDict

from langgraph.graph import StateGraph

from config import Configuration
from lib.file_functions import write_dictionary_to_file, write_string_to_file
from lib.time_functions import get_timestamp
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.agents.query_interpretation_and_validation_agent import (
    QueryInterpretationAndValidationAgent,
)
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState

from langgraph.checkpoint.memory import MemorySaver

class WorkflowManager:
    workflow: StateGraph = StateGraph(AgentState)

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider.get_llm()

        # Add nodes
        self.workflow.add_node(
            "query_interpretation_and_validation_agent",
            self._query_interpretation_and_validation_agent,
        )
        self.workflow.add_node("cmr_api_agent", self._cmr_api_agent)
        self.workflow.add_node(
            "data_analysis_and_recommendation_agent",
            self._data_analysis_and_recommendation_agent,
        )
        self.workflow.add_node(
            "response_synthesis_and_formatting_agent",
            self._response_synthesis_and_formatting_agent,
        )

        # Define edges
        self.workflow.add_edge(
            "query_interpretation_and_validation_agent", "cmr_api_agent"
        )
        self.workflow.add_edge(
            "cmr_api_agent", "data_analysis_and_recommendation_agent"
        )
        self.workflow.add_edge(
            "data_analysis_and_recommendation_agent",
            "response_synthesis_and_formatting_agent",
        )

        # Set entry point
        self.workflow.set_entry_point("query_interpretation_and_validation_agent")

    def checkpoint(self):
      self.workflow.compile(
          checkpointer=MemorySaver()
      )
    def _query_interpretation_and_validation_agent(
        self, state: AgentState
    ) -> AgentState:
        return QueryInterpretationAndValidationAgent(self.llm).process(state)

    def _cmr_api_agent(self, state: AgentState) -> AgentState:
        _response = asyncio.run(CMRApiAgent(self.llm).process(state))
        return {**state.model_dump(), **_response}  # TODO: Figure out how to cast this to AgentState

    def _data_analysis_and_recommendation_agent(self, state: AgentState) -> AgentState:
        self._log_workflow_state(state)  # TODO: Remove logging statement here
        _api_responses: list[dict[str, Any]] | None = state.api_responses
        if _api_responses is not None:
            for _api_response in _api_responses:
                print("DEBUG")
        return state

    def _response_synthesis_and_formatting_agent(self, state: AgentState) -> AgentState:
        return state

    def _log_workflow_state(self, state: AgentState) -> None:
        _curent_timestamp: int = get_timestamp()
        write_dictionary_to_file(
            f"{Configuration.log_folder_path}/{_curent_timestamp}/state.json",
            dict(state),
        )
        # _pretty_text: str = pformat(state, indent=2, width=80, sort_dicts=False)
        # _sanitized_output = sanitize_llm_output(_pretty_text)
        # write_string_to_file(
        #     f"{Configuration.log_folder_path}/{_curent_timestamp}/state.txt",
        #     _sanitized_output,
        # )
