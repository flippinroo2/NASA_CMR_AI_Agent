import asyncio
from typing import Any

import pytest

from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.workflow.agent_state import AgentState
from tests.test_data import TEST_AGENT_STATE, TEST_QUERY, TEST_QUERY_PARAMETERS


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
async def test_01_determine_endpoint_to_search(get_fixture_agent):
    # endpoint = await get_fixture_agent._determine_endpoint_to_search(TEST_QUERY)
    print("DEBUG")


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
async def test_02_extract_cmr_request_parameters_from_query(get_fixture_agent):
    query_parameters = await get_fixture_agent._extract_cmr_request_parameters_from_query(
        TEST_QUERY
    )
    print("DEBUG")


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
async def test_03_sending_cmr_api_request(get_fixture_agent) -> None:
    tool_call_response = await get_fixture_agent._send_cmr_api_request(
        TEST_QUERY, TEST_QUERY_PARAMETERS
    )
    assert isinstance(tool_call_response, list)
    # assert all(
    #     isinstance(sub_response, AutocompleteEntry)
    #     for sub_response in tool_call_response
    # )

@pytest.mark.asyncio
@pytest.mark.parametrize("get_fixture_agent", [CMRApiAgent], indirect=True)
async def test_12_process_output(get_fixture_agent):
    """
    Ensures that the process() method returns an AgentState object.
    """
    test_agent_state: AgentState = TEST_AGENT_STATE.model_copy(
        update={"sub_queries": [TEST_QUERY]}
    )
    response: dict[str, Any] | AgentState = await get_fixture_agent.process(test_agent_state)
    assert isinstance(response, AgentState)
