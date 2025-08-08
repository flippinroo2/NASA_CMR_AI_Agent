import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph

from src.llm.agents.enums import CMR_QUERY_INTENTION_ENUM


@dataclass
class ConversationContext:
    """Stores conversation context and metadata"""

    messages: List[BaseMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ContextManager:
    def __init__(self, max_history_length: int = 50):
        self.max_history_length = max_history_length
        self.context = ConversationContext()
        self.checkpoints: List[ConversationContext] = []

    def get_context(self):
        return self.context

    def get_relevant_context(
        self, original_query: str, intent: CMR_QUERY_INTENTION_ENUM
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
