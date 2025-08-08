from src.llm.llm_provider import LLMProvider, LLM_PROVIDER_ENUM
import unittest

class TestLLMProvider(unittest.TestCase):
  def test_ollama(self):
    llm_provider = LLMProvider(LLM_PROVIDER_ENUM.OLLAMA)
    llm = llm_provider.get_llm()
    self.assertIsNotNone(llm)

  def test_lm_studio(self):
    llm_provider = LLMProvider(LLM_PROVIDER_ENUM.LM_STUDIO)
    llm = llm_provider.get_llm()
    self.assertIsNotNone(llm)

if __name__ == '__main__':
    unittest.main()