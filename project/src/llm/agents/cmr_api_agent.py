from asyncio import gather
from typing import Any

from httpx import AsyncClient
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableSerializable

from src.data.api_manager import CMR_ENDPOINTS, APIManager
from src.llm.agents.agent import Agent
from src.llm.tools.cmr import query_cmr_autocomplete_endpoint
from src.llm.workflow.agent_state import AgentState


class CMRApiAgent(Agent):
    def __init__(self, llm):
        super().__init__(llm)
        self.session = AsyncClient()

    async def process(self, state: AgentState):
        query_intent = state.intent
        sub_queries = state.sub_queries
        if len(sub_queries):
            cmr_queries = self._build_cmr_requests_from_subqueries(
                sub_queries, query_intent
            )
            results = await gather(*cmr_queries)
            cleaned_results = [result for result in results if result]
            return {**state.model_dump(), "api_responses": cleaned_results}
        return AgentState(**{**state.model_dump(), "api_responses": []})

    def _build_cmr_requests_from_subqueries(self, subqueries, query_intent):
        # TODO: If looping through here it would make sense to have an intent for each sub-query???
        return_value = []
        for query in subqueries:
            return_value.append(self._build_cmr_request_from_query(query, query_intent))
        return return_value

    def _build_cmr_request_from_query(self, query, query_intent):
        # TODO: Expand this function here to actually handle parameters better.
        endpoint = CMR_ENDPOINTS.get_item_from_index(query_intent)
        query_parameters = self._build_cmr_request_parameters(query, query_intent)
        api_query = APIManager.query_cmr(
            CMR_ENDPOINTS.AUTOCOMPLETE, params={"q": query_parameters}
        )
        return_value = api_query
        return return_value

    def _call_tool(self, query):
        agent_scratchpad = ""
        template = f"""You are a system that must ONLY respond by calling the query_cmr_autocomplete_endpoint tool.

        The tool will then provide the answer. Never produce plain natural language answers yourself.

        Query: {input}
        {agent_scratchpad}"""
        chat_prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(
            template
        )
        chain: RunnableSerializable[dict[str, Any], str] = (
            chat_prompt_template | self.get_llm()
        )

        response: str | Any = chain.invoke({"query": chat_prompt_template})
        print(response)

        prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["input", "agent_scratchpad"], template=template
        )
        # prompt_template: PromptTemplate = PromptTemplate.from_template(template)
        llm_chain: LLMChain = LLMChain(llm=self.get_llm(), prompt=prompt_template)
        agent = ZeroShotAgent(
            llm_chain=llm_chain, allowed_tools=["query_cmr_autocomplete_endpoint"]
        )
        # executor = AgentExecutor.from_agent_and_tools()
        executor = AgentExecutor(
            agent=agent, tools=[query_cmr_autocomplete_endpoint], verbose=True
        )
        test = executor.invoke({"input": query})
        return response

    def _infer_parameters_from_query(self, query):
        prompt = f"""Extract the following parameters from this query:
        - Temporal range (start/end dates)
        - Spatial bounds (region, coordinates)
        - Data types (satellite, ground-based, etc.)
        - Research purpose

        Query: {query}

        Return as JSON with null values for any missing parameters."""
        response = self._invoke(prompt)
        # return json.loads(response) # NOTE: Commenting out because it was causing errors
        return response

    def _build_cmr_request_parameters(self, query, query_intent):
        # TODO: Actually make this do something...
        match query_intent:
            case 1:
                prompt = f"""Here is a query: {query}
        Break this query down into a search term to use for a single NASA Common Metadata Repository API request.

        ONLY RETURN THE SEARCH TERM! DO NOT PROVIDE ANY OTHER EXPLANATION! DO NOT USE ANY VERBS!"""
            case 2:
                prompt = f"""Here is a query: {query}
        Break this query down into a search term to use for a single NASA Common Metadata Repository API request.

        ONLY RETURN THE SEARCH TERM! DO NOT PROVIDE ANY OTHER EXPLANATION! DO NOT USE ANY VERBS!"""
            case 3:
                prompt = f"""Here is a query: {query}
          Break this query down into a search term to use for a single NASA Common Metadata Repository API request.

          ONLY RETURN THE SEARCH TERM! DO NOT PROVIDE ANY OTHER EXPLANATION! DO NOT USE ANY VERBS!"""
            case _:
                raise ValueError(
                    f"CMRApiAgent._build_cmr_request_parameters() - Invalid query intent: {query_intent}"
                )
        llm_response = self._invoke(prompt)
        return llm_response
