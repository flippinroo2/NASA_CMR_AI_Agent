
import asyncio
from types import CoroutineType
from typing import Any

import httpx
import langchain.agents
import langchain.chains.llm
import langchain.output_parsers
import langchain.prompts
import langchain_core.prompts
import langchain_core.tools

import src.llm.agents.agent
import src.llm.tools.cmr
from src.llm.workflow.agent_state import AgentState

"""
1st - Run a collections request to get datasets
2nd - Use those values to determine arguments for the granules request
"""

class CMRApiAgent(src.llm.agents.agent.Agent):
    def __init__(self, llm):
        super().__init__(llm)
        self.session = httpx.AsyncClient()

    async def process(self, state: AgentState) -> AgentState:
        query_intent: int | None = state.intent
        sub_queries: list[str] = state.sub_queries
        if len(sub_queries):
            cmr_queries = await self._build_cmr_requests_from_subqueries(
                sub_queries, query_intent
            )
            results = await asyncio.gather(*cmr_queries)
            cleaned_results = [result for result in results if result]
            return state.model_copy(update={"api_responses": cleaned_results})
        return state.model_copy(update={"api_responses": []})

    async def _build_cmr_requests_from_subqueries(self, subqueries, query_intent):
        # TODO: If looping through here it would make sense to have an intent for each sub-query???
        return_value = []
        for subquery in subqueries:
            query_parameters: src.llm.tools.cmr.CMRQueryParameters = (
                await self._extract_cmr_request_parameters_from_query(subquery)
            )
            cmr_request: CoroutineType[
                Any, Any, list[src.llm.tools.cmr.AutocompleteEntry | src.llm.tools.cmr.CollectionEntry]
            ] = self._send_cmr_api_request(subquery, query_parameters)
            return_value.append(cmr_request)
        return return_value

    async def _send_cmr_api_request(
        self, query, query_parameters
    ) -> list[src.llm.tools.cmr.AutocompleteEntry | src.llm.tools.cmr.CollectionEntry]:
        tools_list: list[langchain_core.tools.BaseTool] = [
            src.llm.tools.cmr.query_cmr_autocomplete_endpoint,
            src.llm.tools.cmr.query_cmr_collections_endpoint,
            src.llm.tools.cmr.query_cmr_granules_endpoint,
        ]
        tool_string: str = "\n".join(
            f"{tool.name}: {tool.description}" for tool in tools_list
        )
        tool_names: str = ", ".join(tool.name for tool in tools_list)

        template = """
        You are a system that must ONLY respond by calling a tool and never answer directly.

        You have access to the following tools:
        {tools}

        Use the following format:
        Thought: reflect on what to do
        Action: one of [{tool_names}]
        Action Input: the input to the action

        Observation: the result of the action
        ... (this Thought/Action/Observation can repeat multiple times)
        Final Answer: the final answer (only if no tool use is needed)

        Question: {input}
        {agent_scratchpad}
        """
        prompt_template: langchain_core.prompts.BasePromptTemplate[Any] = langchain.prompts.PromptTemplate(
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            template=template,
        ).partial(tools=tool_string, tool_names=tool_names)
        llm_chain: langchain.chains.llm.LLMChain = langchain.chains.llm.LLMChain(llm=self.get_llm(), prompt=prompt_template)
        agent: langchain.agents.ZeroShotAgent = langchain.agents.ZeroShotAgent(
            llm_chain=llm_chain, allowed_tools=[tool.name for tool in tools_list]
        )
        executor: langchain.agents.AgentExecutor = langchain.agents.AgentExecutor(
            verbose=True,
            agent=agent,
            tools=tools_list,
            handle_parsing_errors=True,
        )
        agent_executor_response: dict[str, Any] = await executor.ainvoke(
            {"input": (query)}
        )

        return agent_executor_response.get(
            "output", []
        )  # NOTE: Returning empty list by default instead of None

    async def _extract_cmr_request_parameters_from_query(
        self, query
    ) -> src.llm.tools.cmr.CMRQueryParameters:
        """
        NOTE: This function doesn't really seem necessary. It would probably be more valuable to use the "CMRSearchParameters" object to dynamically choose what to search on?
        """
        parser: langchain.output_parsers.PydanticOutputParser[src.llm.tools.cmr.CMRQueryParameters] = langchain.output_parsers.PydanticOutputParser(
            pydantic_object=src.llm.tools.cmr.CMRQueryParameters
        )
        template = """Extract the following parameters from this query:

        - keyword: The search term used to query the CMR API

        - page_size: Number of results per page

        - page_num: The page number to return

        - offset: As an alternative to page_num, a 0-based offset of individual results may be specified.

        - scroll: A boolean flag (true/false) that allows all results to be retrieved efficiently. page_size is supported with scroll while page_num and offset are not. If scroll is true then the first call of a scroll session sets the page size; page_size is ignored on subsequent calls

        - sort_key: Indicates one or more Fields to sort on

        - pretty: Return formatted results if set to true

        - token: Specifies a user token from EDL or Launchpad for use as authentication. Using the standard Authorization header is the prefered way to supply a token. This parameter may be deprecated in the future
  
        {format_instructions}
    
        Query: {query}
        """
        format_instructions: str = parser.get_format_instructions()
        prompt_template = langchain.prompts.PromptTemplate(
            input_variables=["query"],
            template=template,
            partial_variables={"format_instructions": format_instructions},
        )

        chain = prompt_template | self.get_llm() | parser
        query_parameters = chain.invoke({"query": query})
        return query_parameters

    async def _implement_query_intent(self, query, query_intent) -> str:
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
