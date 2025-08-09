import asyncio
import unittest
from typing import Any

import pytest

from src.ENUMS import LLM_PROVIDER
from src.llm.agents.cmr_api_agent import CMRApiAgent
from src.llm.llm_provider import LLMProvider
from src.llm.workflow.agent_state import AgentState
from src.llm.workflow.workflow_manager import WorkflowManager


class TestCMRApiAgent(unittest.TestCase):
    test_query: str = "Why do you think 2024 had such powerful storms towards the end of the year?"  # TODO: Load the json file with test cases instead of using this hard coded string here.
    mock_response: list[dict[str, Any]] = [
        {
            "score": 11.292702,
            "type": "science_keywords",
            "value": "Storms",
            "fields": "Atmosphere:Atmospheric Phenomena:Storms",
        },
        {
            "score": 10.4967785,
            "type": "science_keywords",
            "value": "Wind Storms",
            "fields": "Atmosphere:Weather Events:Wind Storms",
        },
        {
            "score": 9.457564,
            "type": "science_keywords",
            "value": "Hail Storms",
            "fields": "Atmosphere:Weather Events:Hail Storms",
        },
        {
            "score": 9.398698,
            "type": "science_keywords",
            "value": "Ice Storms",
            "fields": "Atmosphere:Weather Events:Ice Storms",
        },
        {
            "score": 9.398698,
            "type": "science_keywords",
            "value": "Snow Storms",
            "fields": "Atmosphere:Weather Events:Snow Storms",
        },
        {
            "score": 9.3680105,
            "type": "instrument",
            "value": "R2Sonic 2024",
            "fields": "R2Sonic 2024",
        },
        {
            "score": 8.260969,
            "type": "science_keywords",
            "value": "Rain Storms",
            "fields": "Atmosphere:Weather Events:Rain Storms",
        },
        {
            "score": 7.1282506,
            "type": "science_keywords",
            "value": "Severe Cyclonic Storms",
            "fields": "Human Dimensions:Natural Hazards:Tropical Cyclones:Severe Cyclonic Storms",
        },
        {
            "score": 6.985186,
            "type": "science_keywords",
            "value": "Severe Cyclonic Storms (N. Indian)",
            "fields": "Atmosphere:Weather Events:Tropical Cyclones:Tropical Cyclone Force Wind Extent:Severe Cyclonic Storms (N. Indian)",
        },
        {
            "score": 5.8516717,
            "type": "science_keywords",
            "value": "Severe Cyclonic Storms (N. Indian)",
            "fields": "Atmosphere:Weather Events:Tropical Cyclones:Landfall Intensity:Severe Cyclonic Storms (N. Indian)",
        },
    ]

    def setUp(self):
        llm = LLMProvider(LLM_PROVIDER.OLLAMA).get_llm()
        self.agent = CMRApiAgent(llm)
        self.test_state = AgentState(query=self.test_query)

    def test_01_call_tool(self) -> None:
        test = WorkflowManager._cmr_api_agent({"query", self.test_query})
        print("DEBUG")

    @pytest.mark.skip
    def test_02_determine_endpoint_to_search(self):
        # endpoint = self.agent._determine_endpoint_to_search(self.test_query)
        print("DEBUG")

    @pytest.mark.skip
    def test_09_infer_parameters_from_query(self):
        query_parameters = self.agent._infer_parameters_from_query(self.test_query)
        print("DEBUG")

    @pytest.mark.skip
    def test_10_ensure_the_usage_of_tools(self):
        response: AgentState = self.agent.process(self.test_state)
        print("DEBUG")

    @pytest.mark.skip
    def test_11_test_api_request(self):
        response = None

        @pytest.mark.mypy_testing
        def test_query_intent_1(self) -> None:
            """
            query_intent 1 represents a call to the /autocomplete endpoint of the CMR API
            """
            response = asyncio.run(
                self.agent._build_cmr_request_from_query(self.test_query, 1)
            )
            assert isinstance(response, list)
            assert all(isinstance(sub_response, dict) for sub_response in response)

        test_query_intent_1(self)

        @pytest.mark.mypy_testing
        def test_query_intent_2(self) -> None:
            """
            query_intent 2 represents a call to the /collections endpoint of the CMR API
            """
            response = asyncio.run(
                self.agent._build_cmr_request_from_query(self.test_query, 2)
            )
            assert isinstance(response, list)
            assert all(isinstance(sub_response, dict) for sub_response in response)
            print("TODO: test_query_intent_2")

        test_query_intent_2(self)

        @pytest.mark.mypy_testing
        def test_query_intent_3(self) -> None:
            """
            query_intent  represents a call to the /granules endpoint of the CMR API
            """
            response = asyncio.run(
                self.agent._build_cmr_request_from_query(self.test_query, 3)
            )
            assert isinstance(response, list)
            assert all(isinstance(sub_response, dict) for sub_response in response)
            print("TODO: test_query_intent_3")

        test_query_intent_3(self)

        print("DEBUG")

    def test_12_process_output(self):
        """
        Ensures that the process() method returns an AgentState object.
        """
        response: AgentState = asyncio.run(self.agent.process(self.test_state))
        self.assertIsInstance(response, AgentState)


if __name__ == "__main__":
    unittest.main()
