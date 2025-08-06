# Create sample tools for agents
@tool
def search_tool(query: str) -> str:
    """Search for information"""
    return f"Search results for: {query}"

@tool
def calculate_tool(expression: str) -> str:
    """Perform calculations"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid expression"

@tool
def analyze_tool(data: str) -> str:
    """Analyze data"""
    return f"Analysis of: {data}"

class MultiAgentSystem:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.agents = self._create_agents()
        self.graph = self._build_graph()
        self.active_tasks = {}
        self.task_queue = Queue()
        
    def _create_agents(self):
        """Create specialized agents"""
        agents = {
            "researcher": {
                "tools": [search_tool],
                "system_prompt": "You are a research agent. Search for information and provide comprehensive answers."
            },
            "calculator": {
                "tools": [calculate_tool],
                "system_prompt": "You are a calculation agent. Perform mathematical operations and numerical analysis."
            },
            "analyzer": {
                "tools": [analyze_tool],
                "system_prompt": "You are an analysis agent. Analyze data and provide insights."
            },
            "coordinator": {
                "tools": [],
                "system_prompt": "You are a coordinator agent. Delegate tasks to appropriate agents based on the query."
            }
        }
        return agents
    
    def _build_graph(self) -> CompiledStateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(dict)
        
        # Define nodes for each agent
        def coordinator_node(state):
            messages = state.get("messages", [])
            current_message = messages[-1] if messages else ""
            
            # Determine which agent to use
            response = self.llm.invoke([
                SystemMessage(content=self.agents["coordinator"]["system_prompt"]),
                HumanMessage(content=f"Route this query to the appropriate agent: {current_message}")
            ])
            
            # Simple routing logic (you can make this more sophisticated)
            content_lower = str(current_message).lower()
            if "calculate" in content_lower or "math" in content_lower:
                state["current_agent"] = "calculator"
            elif "search" in content_lower or "find" in content_lower:
                state["current_agent"] = "researcher"
            elif "analyze" in content_lower:
                state["current_agent"] = "analyzer"
            else:
                state["current_agent"] = "researcher"
            
            state["messages"].append(f"Routing to {state['current_agent']}")
            return state
        
        def researcher_node(state):
            messages = state.get("messages", [])
            result = search_tool.invoke(messages[-1] if messages else "")
            state["results"]["researcher"] = result
            state["messages"].append(f"Researcher: {result}")
            return state
        
        def calculator_node(state):
            messages = state.get("messages", [])
            result = calculate_tool.invoke(messages[-1] if messages else "")
            state["results"]["calculator"] = result
            state["messages"].append(f"Calculator: {result}")
            return state
        
        def analyzer_node(state):
            messages = state.get("messages", [])
            result = analyze_tool.invoke(messages[-1] if messages else "")
            state["results"]["analyzer"] = result
            state["messages"].append(f"Analyzer: {result}")
            return state
        
        # Add nodes
        workflow.add_node("coordinator", coordinator_node)
        workflow.add_node("researcher", researcher_node)
        workflow.add_node("calculator", calculator_node)
        workflow.add_node("analyzer", analyzer_node)
        
        # Define edges
        workflow.set_entry_point("coordinator")
        
        def route_to_agent(state):
            return state.get("current_agent", "researcher")
        
        workflow.add_conditional_edges(
            "coordinator",
            route_to_agent,
            {
                "researcher": "researcher",
                "calculator": "calculator",
                "analyzer": "analyzer"
            }
        )
        
        workflow.add_edge("researcher", END)
        workflow.add_edge("calculator", END)
        workflow.add_edge("analyzer", END)
        
        return workflow.compile()
    
    async def process_query_async(self, query: str, task_id: str) -> Dict[str, Any]:
        """Process a query asynchronously"""
        initial_state = {
            "messages": [query],
            "current_agent": "",
            "task_id": task_id,
            "status": "processing",
            "results": {}
        }
        
        try:
            # Run the graph
            result = await self.graph.ainvoke(initial_state)
            result["status"] = "completed"
            return result
        except Exception as e:
            return {
                "task_id": task_id,
                "status": "error",
                "error": str(e),
                "results": {}
            }