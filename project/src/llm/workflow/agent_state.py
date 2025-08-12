from typing import Optional

import pydantic

import src.llm.tools.cmr


class AgentState(pydantic.BaseModel):
    query: str
    api_responses: list[
        list[src.llm.tools.cmr.AutocompleteEntry | src.llm.tools.cmr.CollectionEntry]
    ] = pydantic.Field(
        default_factory=list[
            list[
                src.llm.tools.cmr.AutocompleteEntry | src.llm.tools.cmr.CollectionEntry
            ]
        ]
    )
    current_task: Optional[str] = pydantic.Field(default=None)
    final_response: Optional[str] = pydantic.Field(default=None)
    intent: Optional[int] = pydantic.Field(default=None)
    sub_queries: list[str] = pydantic.Field(default_factory=list[str])

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True
    )  # TODO: Remove this at some point.
