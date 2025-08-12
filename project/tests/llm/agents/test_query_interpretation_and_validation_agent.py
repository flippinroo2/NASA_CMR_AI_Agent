import pytest

from src.llm.agents.query_interpretation_and_validation_agent import (
    QueryInterpretationAndValidationAgent,
)
from src.llm.workflow.agent_state import AgentState
from tests.test_data import TEST_AGENT_STATE, TEST_QUERY


@pytest.mark.skip
@pytest.mark.parametrize(
    "get_fixture_agent", [QueryInterpretationAndValidationAgent], indirect=True
)
def test_01_test_enriching_query_with_context(get_fixture_agent) -> None:
    """
    Ensures that the enrich_query_with_context() method returns a string.
    """
    enriched_query: str = get_fixture_agent._enrich_query_with_context(TEST_AGENT_STATE)
    print("TODO Implement this entire feature")  # TODO Implement this entire feature


@pytest.mark.parametrize(
    "get_fixture_agent", [QueryInterpretationAndValidationAgent], indirect=True
)
def test_02_query_intent(get_fixture_agent) -> None:
    """
    Ensures that the query_intent() method returns a value that is an integer between 1 and 3
    """
    query_intent: int | None = get_fixture_agent._get_query_intent(TEST_QUERY)
    assert isinstance(query_intent, int)
    if query_intent is not None:
        assert query_intent >= 1
        assert query_intent <= 3
    assert query_intent is not None


@pytest.mark.parametrize(
    "get_fixture_agent", [QueryInterpretationAndValidationAgent], indirect=True
)
def test_03_identifying_sub_queries(get_fixture_agent) -> None:
    """
    Ensures that the identify_sub_queries() method returns a list of strings.
    """
    sub_queries: list[str] = get_fixture_agent._identify_sub_queries(TEST_QUERY)
    assert isinstance(sub_queries, list)
    assert all(isinstance(sub_query, str) for sub_query in sub_queries)


@pytest.mark.parametrize(
    "get_fixture_agent", [QueryInterpretationAndValidationAgent], indirect=True
)
def test_04_process_output(get_fixture_agent) -> None:
    """
    Ensures that the process() method returns an AgentState object.
    """
    response: AgentState = get_fixture_agent.process(TEST_AGENT_STATE)
    assert isinstance(response, AgentState)
