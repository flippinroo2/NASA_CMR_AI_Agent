from src.llm.llm_provider import LLMProvider
from src.llm.agents.cmr_agent import CMRAgent
from src.llm.agents.data_analysis_agent import DataAnalysisAgent
from src.llm.agents.query_agent import QueryAgent
from src.llm.agents.response_agent import ResponseAgent
from src.llm.context_manager import ContextManager
from src.knowledge_graph import KnowledgeGraph
import json


class AgentManager:
    available_agents = []
    running_agents = []

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider.get_llm()  # With fallback providers
        self.context_manager = ContextManager()
        self.knowledge_graph = KnowledgeGraph()

    def process_query(self, query: str):
        # Step 1: Intent classification
        intent = self._classify_intent(query)

        # Step 2: Context enrichment
        enriched_query = self._enrich_with_context(query)

        # Step 3: Query decomposition
        subqueries = self._decompose_query(enriched_query)

        # Step 4: Parameter inference
        params = self._infer_parameters(query)

        return {
            "intent": intent,
            "subqueries": subqueries,
            "parameters": params,
            "context": self.context_manager.get_context(),
        }

    def _classify_intent(self, query: str) -> str:
        """Classify query intent using LLM"""
        prompt = f"""Classify the following query into one of these categories:
        1. Exploratory request
        2. Specific data request
        3. Analytical query
        4. Comparative analysis
        5. Methodology recommendation

        Query: {query}"""
        return self.llm.invoke(prompt)

    def _enrich_with_context(self, query: str) -> str:
        """Add relevant context from conversation history"""
        context = self.context_manager.get_relevant_context(query)
        return f"{query}\n\nRelevant context: {context}"

    def _decompose_query(self, query: str) -> list[str]:
        """Break complex query into sub-queries"""
        prompt = f"""Break this complex query into simpler sub-queries:
        {query}

        Return as a numbered list of distinct questions."""
        response = self.llm.invoke(prompt)
        return self._parse_subqueries(response)

    def _infer_parameters(self, query: str) -> dict:
        """Extract temporal, spatial, and other parameters"""
        prompt = f"""Extract the following parameters from this query:
        - Temporal range (start/end dates)
        - Spatial bounds (region, coordinates)
        - Data types (satellite, ground-based, etc.)
        - Research purpose

        Query: {query}

        Return as JSON with null values for any missing parameters."""
        return json.loads(self.llm.invoke(prompt))
