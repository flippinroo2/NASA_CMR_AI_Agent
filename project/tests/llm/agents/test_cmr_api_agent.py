import asyncio
from typing import Any, Coroutine

import pytest

from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager
from tests.fixtures import get_fixture_agent, get_fixture_workflow_manager
from tests.test_data import TEST_AGENT_STATE, TEST_QUERY


@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
def test_01_call_tool(get_fixture_agent) -> None:
    test = get_fixture_agent._call_tool(TEST_QUERY)
    print("DEBUG")


@pytest.mark.skip
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
def test_02_determine_endpoint_to_search(get_fixture_agent):
    # endpoint = get_fixture_agent._determine_endpoint_to_search(TEST_QUERY)
    print("DEBUG")


@pytest.mark.skip
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
def test_09_infer_parameters_from_query(get_fixture_agent):
    query_parameters = get_fixture_agent._infer_parameters_from_query(TEST_QUERY)
    print("DEBUG")


@pytest.mark.skip
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
def test_10_ensure_the_usage_of_tools(get_fixture_agent):
    response: Coroutine[Any, Any, dict[str, Any] | AgentState] = (
        get_fixture_agent.process(TEST_AGENT_STATE)
    )
    print("DEBUG")


@pytest.mark.skip
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
def test_11_test_api_request(get_fixture_agent):
    response = None

    def test_query_intent_1() -> None:
        """
        query_intent 1 represents a call to the /autocomplete endpoint of the CMR API
        """
        response = asyncio.run(
            main=get_fixture_agent._build_cmr_request_from_query(TEST_QUERY, 1)
        )
        assert isinstance(response, list)
        assert all(isinstance(sub_response, dict) for sub_response in response)

    test_query_intent_1()

    def test_query_intent_2() -> None:
        """
        query_intent 2 represents a call to the /collections endpoint of the CMR API
        """
        response = asyncio.run(
            get_fixture_agent._build_cmr_request_from_query(TEST_QUERY, 2)
        )
        assert isinstance(response, list)
        assert all(isinstance(sub_response, dict) for sub_response in response)
        print("TODO: test_query_intent_2")

    test_query_intent_2()

    def test_query_intent_3() -> None:
        """
        query_intent  represents a call to the /granules endpoint of the CMR API
        """
        response = asyncio.run(
            get_fixture_agent._build_cmr_request_from_query(TEST_QUERY, 3)
        )
        assert isinstance(response, list)
        assert all(isinstance(sub_response, dict) for sub_response in response)
        print("TODO: test_query_intent_3")

    test_query_intent_3()

    print("DEBUG")


@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
def test_12_process_output(get_fixture_agent):
    """
    Ensures that the process() method returns an AgentState object.
    """
    response: dict[str, Any] | AgentState = asyncio.run(
        get_fixture_agent.process(TEST_AGENT_STATE)
    )
    assert isinstance(response, AgentState)
