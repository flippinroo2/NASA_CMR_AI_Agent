from unittest.mock import Mock

from _pytest.fixtures import SubRequest
from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseLLM
from pytest import fixture

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.agent import Agent
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.workflow_manager import WorkflowManager
from tests.test_data import MOCK_CMR_AUTOCOMPLETE_RESPONSE


@fixture(scope="module")
def get_fixture_agent(request: SubRequest):
    agent_class: Agent = request.param
    return agent_class(LLMProvider(LLM_PROVIDER.OLLAMA).get_llm()) # type: ignore


@fixture(scope="session")
def get_fixture_cmr_response() -> Mock:
    mock: Mock = Mock()
    mock.get.return_value = MOCK_CMR_AUTOCOMPLETE_RESPONSE
    return mock


@fixture(scope="session")
def get_fixture_llm() -> _ConfigurableModel | BaseLLM:
    return LLMProvider(LLM_PROVIDER.OLLAMA).get_llm()


@fixture(scope="session")
def get_fixture_workflow_manager() -> WorkflowManager:
    return WorkflowManager(LLMProvider(LLM_PROVIDER.OLLAMA))
