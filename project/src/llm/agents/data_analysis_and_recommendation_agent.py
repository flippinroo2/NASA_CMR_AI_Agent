from src.knowledge_graph import KnowledgeGraph
from src.llm.context_manager import ContextManager
from src.llm.agents.agent import Agent


class DataAnalysisAndRecommendationAgent(Agent):
    def invoke(self, query: str):
        return self.llm.invoke(query)

    def process(self, query: str):
        """Classify query intent using LLM"""
        prompt = f"""Classify the following query into one of these categories:
        1. Exploratory request
        2. Specific data request
        3. Analytical query
        4. Comparative analysis
        5. Methodology recommendation

        Query: {query}"""
        return self.llm.invoke(prompt)
