from pprint import pformat
from typing import Any, TypedDict

from langgraph.graph import StateGraph

from lib.file_functions import write_dictionary_to_file, write_string_to_file
from lib.time_functions import get_timestamp
from src.llm.agents.cmr_agent import CMRAgent
from src.llm.agents.query_intent_analysis_agent import QueryIntentAnalysisAgent
from src.llm.llm_provider import LLMProvider


class AgentState(TypedDict):
    query: str
    intent: str
    # decomposed_queries: list[str]
    api_responses: list[dict]
    # analysis_results: dict
    # context: dict
    final_response: str
    # messages: Any
    current_task: Any
    memory: Any


class WorkflowManager:
    workflow = StateGraph(AgentState)

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider.get_llm()

        # Add nodes
        self.workflow.add_node("intent_classification", self.intent_classifier)
        self.workflow.add_node("cmr_api_agent", self.cmr_api_agent)
        # Define edges
        self.workflow.add_edge("intent_classification", "cmr_api_agent")
        # Set entry point
        self.workflow.set_entry_point("intent_classification")

    def intent_classifier(self, state: AgentState) -> AgentState:
        _query: str | None = state.get("query")
        if _query is None:
            raise ValueError(
                "WorkflowManager.intent_classifier - There was no query in AgentState"
            )
        _response = QueryIntentAnalysisAgent(self.llm).process(_query)
        return {**state, "intent": _response}

    def cmr_api_agent(self, state: AgentState):
        _query: str | None = state.get("query")
        _response = CMRAgent(self.llm).process(state)
        self._log_workflow_state(state)  # TODO: Remove logging statement here
        return {**state, "api_responses": [{"data": "..."}, {"data": "..."}]}

    def _log_workflow_state(self, state: AgentState) -> None:
        _curent_timestamp: int = get_timestamp()
        write_dictionary_to_file(f"logs/{_curent_timestamp}/state.json", dict(state))
        _pretty_text: str = pformat(state, indent=2, width=80, sort_dicts=False)
        write_string_to_file(f"logs/{_curent_timestamp}/state.txt", _pretty_text)
