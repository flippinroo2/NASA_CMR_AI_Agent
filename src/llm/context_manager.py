from src.workflow_manager import AgentState
from typing import Any, Optional
from langgraph.graph import StateGraph

class ContextManager:
    """Context manager specifically designed for LangGraph applications"""

    def __init__(self):
        self.state: AgentState = {
            "messages": [],
            "context": {},
            "current_task": None,
            "memory": {"short_term": [], "long_term": {}, "working_memory": {}},
        }
        self.graph = None

    def initialize_graph(self, graph: StateGraph) -> None:
        """Initialize with a LangGraph StateGraph"""
        self.graph = graph

    def update_state(self, updates: dict[str, Any]) -> AgentState:
        """Update the agent state"""
        for key, value in updates.items():
            if key in self.state:
                if key == "messages":
                    # Append messages rather than replace
                    self.state["messages"].extend(
                        value if isinstance(value, list) else [value]
                    )
                else:
                    self.state[key] = value
        return self.state

    def add_to_memory(self, memory_type: str, key: str, value: Any) -> None:
        """Add information to specific memory type"""
        if memory_type == "short_term":
            self.state["memory"]["short_term"].append(
                {"key": key, "value": value, "timestamp": datetime.now().isoformat()}
            )
            # Limit short-term memory size
            if len(self.state["memory"]["short_term"]) > 20:
                self.state["memory"]["short_term"] = self.state["memory"]["short_term"][
                    -20:
                ]
        elif memory_type == "long_term":
            self.state["memory"]["long_term"][key] = value
        elif memory_type == "working":
            self.state["memory"]["working_memory"][key] = value

    def get_from_memory(self, memory_type: str, key: Optional[str] = None) -> Any:
        """Retrieve from memory"""
        if memory_type == "short_term":
            return self.state["memory"]["short_term"]
        elif memory_type == "long_term":
            return (
                self.state["memory"]["long_term"].get(key)
                if key
                else self.state["memory"]["long_term"]
            )
        elif memory_type == "working":
            return (
                self.state["memory"]["working_memory"].get(key)
                if key
                else self.state["memory"]["working_memory"]
            )

    def set_current_task(self, task: str) -> None:
        """Set the current task"""
        self.state["current_task"] = task

    def get_state(self) -> AgentState:
        """Get current state"""
        return self.state

    def clear_working_memory(self) -> None:
        """Clear working memory"""
        self.state["memory"]["working_memory"] = {}
