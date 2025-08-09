import unittest
from src.ENUMS import LLM_PROVIDER
from src.llm.llm_provider import LLMProvider


class TestLLMProvider(unittest.TestCase):
    def test_01_ollama_llm(self) -> None:
        llm_provider = LLMProvider(LLM_PROVIDER.OLLAMA)
        llm = llm_provider.get_llm()
        self.assertIsNotNone(llm)

    # TODO: Re-enable this test
    # def test_02_lm_studio_llm(self) -> None:
    #     llm_provider = LLMProvider(LLM_PROVIDER.LM_STUDIO)
    #     llm = llm_provider.get_llm()
    #     self.assertIsNotNone(llm)


if __name__ == "__main__":
    unittest.main()
