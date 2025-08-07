from typing import Any, TypedDict

# TODO: Remove this duplicate state and try to import it on its own without circular imports to the Workflow manager


class AgentState(TypedDict, total=False):
    # analysis_results: dict
    api_requests: list[dict] = []
    api_responses: list[dict]
    # context: dict
    current_task: str
    final_response: str
    intent: str
    # memory: Any
    # messages: Any
    query: str
    sub_queries: list[str]
