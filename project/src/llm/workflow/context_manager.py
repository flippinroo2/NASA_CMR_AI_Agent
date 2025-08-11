import json
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from src.ENUMS import CMR_QUERY_INTENTION


class ConversationContext(BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list[BaseMessage])
    metadata: dict[str, Any] = Field(default_factory=dict[str, Any])
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ContextManager(BaseModel):
    checkpoints: list[ConversationContext] = Field(
        default_factory=list[ConversationContext]
    )
    context: ConversationContext = Field(default_factory=ConversationContext)
    max_history_length: int = 50

    def get_context(self):
        return self.context

    def get_relevant_context(
        self, original_query: str, intent: CMR_QUERY_INTENTION
    ) -> str:
        if original_query is not None and intent is not None:
            enriched_context = {}

            if intent == "information_retrieval":
                enriched_context = self.enrich_for_information_retrieval(original_query)
                return enriched_context  # TODO: Expand on the context management here.
            elif intent == "question_answering":
                print("Question Answering")
            elif intent == "query_decomposition":
                print("Query Decomposition")
            elif intent == "query_execution":
                print("Query Execution")
            return original_query
        return original_query  # TODO: Actually enrich with context here

    def enrich_for_information_retrieval(self, original_query: str) -> str:
        return original_query
