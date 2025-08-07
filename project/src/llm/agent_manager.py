import json

from config import Configuration
from lib.file_functions import write_string_to_file
from lib.time_functions import get_timestamp
from src.knowledge_graph import KnowledgeGraph
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.agents.query_interpretation_and_validation_agent import (
    QueryInterpretationAndValidationAgent,
)
from src.llm.context_manager import ContextManager
from src.llm.llm_provider import LLMProvider
from lib.string_functions import sanitize_llm_output


class AgentManager:
    available_agents = []
    running_agents = []

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider.get_llm()  # With fallback providers
        self.context_manager = ContextManager()
        self.knowledge_graph = KnowledgeGraph()

    def process_query(self, query: str):
        # Step 1: Intent classification
        intent = QueryInterpretationAndValidationAgent(self.llm).process(query)

        # Step 2: Context enrichment
        enriched_query = self._enrich_with_context(query, intent)

        # Step 3: Query decomposition
        subqueries = self._decompose_query(enriched_query)

        # Step 4: Parameter inference
        params = self._infer_parameters(query)

        self._output_to_file(query, intent, enriched_query, subqueries, params)

        return {
            "intent": intent,
            "subqueries": subqueries,
            "parameters": params,
            "context": self.context_manager.get_context(),
        }

    def _output_to_file(self, query, intent, enriched_query, subqueries, params):
        if Configuration.is_debug_mode_activated:
            current_timestamp = get_timestamp()
            _sanitized_output = sanitize_llm_output(_pretty_text)
            write_string_to_file(
                filename=f"logs/{current_timestamp}/query.txt",
                text_to_write=json.dumps(_sanitized_output),
            )
            write_string_to_file(
                filename=f"logs/{current_timestamp}/intent.txt",
                text_to_write=json.dumps(_sanitized_output),
            )
            write_string_to_file(
                filename=f"logs/{current_timestamp}/enriched_query.txt",
                text_to_write=json.dumps(_sanitized_output),
            )
            write_string_to_file(
                filename=f"logs/{current_timestamp}/subqueries.txt",
                text_to_write=json.dumps(_sanitized_output),
            )
            write_string_to_file(
                filename=f"logs/{current_timestamp}/params.txt",
                text_to_write=json.dumps(_sanitized_output),
            )

    def _enrich_with_context(self, query: str, intent: str) -> str:
        """Add relevant context from conversation history"""
        context = self.context_manager.get_relevant_context(query, intent)
        return f"{query}\n\nRelevant context: {context}"

    def _decompose_query(self, query: str) -> list[str]:
        """Break complex query into sub-queries"""
        prompt = f"""Break this complex query into simpler sub-queries:
        {query}

        Return as a numbered list of distinct questions."""
        response = self.llm.invoke(prompt)
        # return self._parse_subqueries(response) # TODO: Create method for parsing sub-queries
        return response

    def _infer_parameters(self, query: str) -> dict:
        """Extract temporal, spatial, and other parameters"""
        prompt = f"""Extract the following parameters from this query:
        - Temporal range (start/end dates)
        - Spatial bounds (region, coordinates)
        - Data types (satellite, ground-based, etc.)
        - Research purpose

        Query: {query}

        Return as JSON with null values for any missing parameters."""
        response = self.llm.invoke(prompt)
        # return json.loads(response) # NOTE: Commenting out because it was causing errors
        return response
