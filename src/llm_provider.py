from enum import Enum
from langgraph.prebuilt import create_react_agent
from langchain_community.llms import Anthropic, Ollama
from langchain_core.tools import tool


class LLM_PROVIDER_ENUM(Enum):
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"

class LLMProvider():
  llm_class = None

  def __init__(self, llm_provider: LLM_PROVIDER_ENUM):
    match llm_provider:
      case LLM_PROVIDER_ENUM.ANTHROPIC:
        self.llm_class = Anthropic
      case LLM_PROVIDER_ENUM.OLLAMA:
        self.llm_class = Ollama

  def get_llm(self, model_name):
    try:
      return Ollama(model="gemma3:latest")
    except Exception as e:
      print(f"ERROR: {e}")
