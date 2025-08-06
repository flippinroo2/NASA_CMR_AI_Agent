from enum import Enum

from langchain_community.llms.anthropic import Anthropic
from langchain_community.llms.ollama import Ollama


class LLM_PROVIDER_ENUM(Enum):
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class LLMProvider:
    llm_class = None

    def __init__(self, llm_provider: LLM_PROVIDER_ENUM):
        match llm_provider:
            case LLM_PROVIDER_ENUM.ANTHROPIC:
                self.llm_class = Anthropic
            case LLM_PROVIDER_ENUM.OLLAMA:
                self.llm_class = Ollama

    # TODO: Remove hard-coded LLM name
    def get_llm(self, model_name="gemma3:latest"):
        try:
            return Ollama(model=model_name)
        except Exception as e:
            print(f"LLMProvider.get_llm() - Exception: {e}")
