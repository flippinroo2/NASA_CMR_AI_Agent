from src.ENUMS import LLM_PROVIDER
from src.llm.llm_provider import LLMProvider


def test_01_ollama_llm() -> None:
    llm_provider = LLMProvider(LLM_PROVIDER.OLLAMA)
    llm = llm_provider.get_llm()
    assert llm is not None


# TODO: Re-enable this test
# def test_02_lm_studio_llm() -> None:
#     llm_provider = LLMProvider(LLM_PROVIDER.LM_STUDIO)
#     llm = llm_provider.get_llm()
#     assert llm is not None
