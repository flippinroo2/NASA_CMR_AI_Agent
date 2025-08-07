from typing import TypedDict


class AgentState(TypedDict):
    api_responses: list[dict]
    current_task: str
    final_response: str
    intent: str
    query: str
