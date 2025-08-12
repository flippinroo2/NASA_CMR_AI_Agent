from dataclasses import dataclass, field
from typing import Any, NotRequired, Optional, TypedDict

from pydantic import BaseModel, ConfigDict, Field


@dataclass
class __AgentState:
    query: str
    # analysis_results: dict[str, Any] = field(default_factory=dict[str, Any])
    api_requests: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]])
    api_responses: list[list[dict[str, Any]]] = field(
        default_factory=list[list[dict[str, Any]]]
    )
    # context: ContextManager = field(default_factory=ContextManager)
    current_task: Optional[str] = None
    final_response: Optional[str] = None
    intent: Optional[int] = None
    # memory: Any
    # messages: Any
    sub_queries: list[str] = field(default_factory=list[str])


class _AgentState(TypedDict):
    # analysis_results: NotRequired[dict[str, Any]]
    api_requests: NotRequired[list[dict[str, Any]]]
    api_responses: NotRequired[list[list[dict[str, Any]]]]
    # context: ContextManager
    current_task: NotRequired[str]
    final_response: NotRequired[str]
    intent: NotRequired[int]
    # memory: NotRequired[Any]
    # messages: NotRequired[Any]
    query: str
    sub_queries: NotRequired[list[str]]


class AgentState(BaseModel):
    query: str
    api_requests: list[dict[str, Any]] = Field(default_factory=list[dict[str, Any]])
    api_responses: list[list[dict[str, Any]]] = Field(
        default_factory=list[list[dict[str, Any]]]
    )
    current_task: Optional[str] = Field(default=None)
    final_response: Optional[str] = Field(default=None)
    intent: Optional[int] = Field(default=None)
    sub_queries: list[str] = Field(default_factory=list[str])

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # TODO: Fix this because it's a easy solution, but maybe not the best. (I believe correct way is to define def __get_pydantic_core_schema__ within the ContextManager class... OR making that class a Pydantic model as well.)
