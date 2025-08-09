import unittest

from src.ENUMS import LLM_PROVIDER
from src.llm.llm_provider import LLMProvider


class TestLLMProvider(unittest.TestCase):
    def test_ollama(self):
        llm_provider = LLMProvider(LLM_PROVIDER.OLLAMA)
        llm = llm_provider.get_llm()
        self.assertIsNotNone(llm)

    def test_lm_studio(self):
        llm_provider = LLMProvider(LLM_PROVIDER.LM_STUDIO)
        llm = llm_provider.get_llm()
        self.assertIsNotNone(llm)


if __name__ == "__main__":
    unittest.main()
