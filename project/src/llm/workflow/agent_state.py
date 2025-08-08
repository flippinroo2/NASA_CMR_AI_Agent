from typing import Any, TypedDict

from src.llm.agents.enums import CMR_QUERY_INTENTION_ENUM
from src.llm.workflow.context_manager import ContextManager

# TODO: Remove this duplicate state and try to import it on its own without circular imports to the Workflow manager


class AgentState(TypedDict, total=False):
    # analysis_results: dict
    api_requests: list[dict] = []
    api_responses: list[dict]
    context: ContextManager
    current_task: str
    final_response: str
    intent: CMR_QUERY_INTENTION_ENUM
    # memory: Any
    # messages: Any
    query: str
    sub_queries: list[str]
