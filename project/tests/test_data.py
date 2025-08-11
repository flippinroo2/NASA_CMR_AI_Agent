from typing import Any

from src.llm.workflow.agent_state import AgentState

TEST_QUERY: str = "Why do you think 2024 had such powerful hurricanes towards the end of the year?"  # TODO: Load the json file with test cases instead of using this hard coded string here.

TEST_AGENT_STATE: AgentState = AgentState(query=TEST_QUERY)

MOCK_CMR_AUTOCOMPLETE_RESPONSE: list[dict[str, Any]] = [
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
