from typing import Any, Callable

from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseLLM
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

from config import Configuration
from lib.file_functions import write_dictionary_to_file
from lib.time_functions import get_timestamp
from src.llm.agents.agent import Agent
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.agents.data_analysis_and_recommendation_agent import (
    DataAnalysisAndRecommendationAgent,
)
from src.llm.agents.query_interpretation_and_validation_agent import (
    QueryInterpretationAndValidationAgent,
)
from src.llm.agents.response_synthesis_and_formatting_agent import (
    ResponseSynthesisAndFormattingAgent,
)
from src.llm.llm_provider import LLMProvider
from src.llm.tools.cmr import (
    query_cmr_autocomplete_endpoint,
    query_cmr_collections_endpoint,
    query_cmr_granules_endpoint,
)
from src.llm.workflow.agent_state import AgentState


class WorkflowManager:
    """
    A class to used to handle the creation of a langgraph state graph and agents / agent states.
    """

    _agents: list[Agent] = []
    state_graph: StateGraph = StateGraph(AgentState)

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm: _ConfigurableModel | BaseLLM = llm_provider.get_llm()

        # Add nodes
        self._add_node_if_missing(
            self._query_interpretation_and_validation_agent,
        )
        self._add_node_if_missing(
            self._cmr_api_agent,
        )
        self._add_node_if_missing(
            self._data_analysis_and_recommendation_agent,
        )
        self._add_node_if_missing(
            self._response_synthesis_and_formatting_agent,
        )

        # Define edges
        self.state_graph.add_edge(
            "_query_interpretation_and_validation_agent", "_cmr_api_agent"
        )
        self.state_graph.add_edge(
            "_cmr_api_agent", "_data_analysis_and_recommendation_agent"
        )
        self.state_graph.add_edge(
            "_data_analysis_and_recommendation_agent",
            "_response_synthesis_and_formatting_agent",
        )

        # Set entry point
        self.state_graph.set_entry_point("_query_interpretation_and_validation_agent")

    def _add_node_if_missing(self, node: Callable) -> None:
        """
        Helper function to add a node to the state graph if it doesn't already exist

        Args:
            node (Callable): The node to add

        Returns:
            None
        """
        name: str = getattr(node, "__name__", None) or node.__class__.__name__
        if name not in self.state_graph.nodes:
            self.state_graph.add_node(node)

    def checkpoint(self) -> None:
        """
        Checkpoint the state graph.

        Returns:
            None

        Notes:
            TODO: This function needs to be fleshed out still.
        """
        self.state_graph.compile(checkpointer=MemorySaver())

    async def _query_interpretation_and_validation_agent(
        self, state: AgentState
    ) -> AgentState:
        """
        Function for the query interpretation and validation agent.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            AgentState: The new state of the agent.
        """
        agent: QueryInterpretationAndValidationAgent = (
            QueryInterpretationAndValidationAgent(self.llm)
        )
        self._agents.append(
            agent
        )  # TODO: Do we want to actually cache the agents in this class though?
        new_agent_state: AgentState = await agent.process(state)
        return state.model_copy(update=new_agent_state.model_dump())

    async def _cmr_api_agent(self, state: AgentState) -> AgentState:
        """
        Function for the CMR API agent.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            AgentState: The new state of the agent.
        """
        agent: CMRApiAgent = CMRApiAgent(self.llm)
        self._agents.append(
            agent
        )  # TODO: Do we want to actually cache the agents in this class though?
        agent.get_llm().bind(
            tools=[
                query_cmr_autocomplete_endpoint,
                query_cmr_collections_endpoint,
                query_cmr_granules_endpoint,
            ]
        )  # NOTE: Binding the nasa tool... Should also create an output parser here
        new_agent_state: AgentState = await agent.process(state)
        return state.model_copy(update=new_agent_state.model_dump())

    async def _data_analysis_and_recommendation_agent(
        self, state: AgentState
    ) -> AgentState:
        """
        Function for the data analysis and recommendation agent.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            AgentState: The new state of the agent.

        Notes:
            TODO: This function needs to be fleshed out still.
        """
        self._log_workflow_state(state)  # TODO: Remove logging statement here
        agent: DataAnalysisAndRecommendationAgent = DataAnalysisAndRecommendationAgent(
            self.llm
        )
        api_responses: list[dict[str, Any]] | None = state.api_responses
        if api_responses is not None:
            for api_response in api_responses:
                print("DEBUG")
        return state

    async def _response_synthesis_and_formatting_agent(
        self, state: AgentState
    ) -> AgentState:
        """
        Function for the response synthesis and formatting agent.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            AgentState: The new state of the agent.

        Notes:
            TODO: This function needs to be fleshed out still.
        """
        agent: ResponseSynthesisAndFormattingAgent = (
            ResponseSynthesisAndFormattingAgent(self.llm)
        )
        return state

    def _log_workflow_state(self, state: AgentState) -> None:
        """
        Helper function for logging the state of the workflow to a JSON file located a directory that is formatted by {LOG_FOLDER_PATH}/{curent_timestamp}

        Notes:
            TODO: Add a new parameter that allows the specification of a custom directory name and then use timestamps for each individual file. (For the purpose of multiple state logs within a single run.)
        """
        curent_timestamp: int = get_timestamp()
        write_dictionary_to_file(
            f"{Configuration.log_folder_path}/{curent_timestamp}/state.json",
            dict(state),
        )
