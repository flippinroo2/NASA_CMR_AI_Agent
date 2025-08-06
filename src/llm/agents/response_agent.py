from typing import Optional
import json

class ResponseAgent:
    def __init__(self):
        self.llm = initialize_llm()
        self.template_engine = TemplateEngine()

    def synthesize_response(
        self,
        query: str,
        analysis_results: dict,
        context: Optional[dict] = None
    ) -> str:
        """Combine all information into a coherent response"""
        # Generate structured data
        structured_data = self._prepare_structured_data(analysis_results)

        # Create natural language summary
        summary = self._generate_summary(query, structured_data)

        # Format the final response
        return self.template_engine.render(
            "response_template",
            {
                "query": query,
                "summary": summary,
                "detailed_results": structured_data,
                "visualization_suggestions": self._generate_visualization_suggestions(analysis_results)
            }
        )

    def _prepare_structured_data(self, analysis_results: dict) -> dict:
        """Organize analysis results into structured format"""
        return {
            "top_datasets": analysis_results["top_datasets"],
            "comparative_analysis": analysis_results["comparative_analysis"],
            "quality_metrics": {
                dataset["dataset_id"]: dataset["quality_metrics"]
                for dataset in analysis_results["top_datasets"]
            },
            "methodology_suggestions": analysis_results["methodology_suggestions"]
        }

    def _generate_summary(self, query: str, structured_data: dict) -> str:
        """Generate natural language summary using LLM"""
        prompt = f"""Summarize the following analysis results in response to this query:
        Query: {query}

        Analysis Results:
        {json.dumps(structured_data, indent=2)}

        Provide a concise summary highlighting:
        1. The most relevant datasets found
        2. Key quality metrics and comparisons
        3. Any gaps or limitations identified
        4. Recommended methodologies"""

        return self.llm.invoke(prompt)

    def _generate_visualization_suggestions(self, analysis_results: dict) -> list[dict]:
        """Suggest appropriate visualizations for the data"""
        suggestions = []

        for dataset in analysis_results["top_datasets"]:
            suggestions.append({
                "dataset_id": dataset["dataset_id"],
                "visualizations": self._get_visualizations_for_dataset(dataset)
            })

        return suggestions

class ResponseSynthesizer2:
    templates = {
        "gap_analysis": "Gap Analysis Report:\n{gaps}\nRecommendations: {rec}",
        "comparison": "Dataset Comparison:\n{comparison}\nBest for: {purpose}"
    }
    
    def process(self, state):
        if state.intent == "analytical":
            response = self.templates["gap_analysis"].format(
                gaps=state.analysis["temporal_gaps"],
                rec=generate_recommendations(state)
            )
        else:
            response = self.templates["comparison"].format(
                comparison=state.analysis["comparison"],
                purpose=state.query
            )
        return {**state, "response": response}
    
class QueryInterpreter:
    def process(self, state):
        # Intent classification using zero-shot LLM
        intent = llm.classify_intent(state.query)
        
        # Query decomposition
        sub_queries = llm.decompose(state.query, intent)
        
        # Validation against CMR constraints
        validated = [
            {"query": q, "valid": self._validate(q)}
            for q in sub_queries
        ]
        
        return {**state, "intent": intent, "validated_queries": validated}
    
    def _validate(self, query):
        # Check temporal bounds
        if "2015-2023" not in query:
            return False
        
        # Validate spatial region
        if "Sub-Saharan Africa" not in query:
            return False
            
        return True