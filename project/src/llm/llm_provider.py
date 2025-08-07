from enum import Enum

from langchain_community.llms.anthropic import Anthropic
from langchain_community.llms.openai import OpenAI
from langchain_ollama.llms import OllamaLLM


class LLM_PROVIDER_ENUM(Enum):
    ANTHROPIC = "anthropic"
    LM_STUDIO = "lmstudio"
    OLLAMA = "ollama"


class LLMProvider:
    llm_class = OllamaLLM

    def __init__(self, llm_provider: LLM_PROVIDER_ENUM):
        match llm_provider:
            case LLM_PROVIDER_ENUM.ANTHROPIC:
                self.llm_class = Anthropic
            case LLM_PROVIDER_ENUM.LM_STUDIO:
                self.llm_class = OpenAI
            case LLM_PROVIDER_ENUM.OLLAMA:
                self.llm_class = OllamaLLM
            case _:
                self.llm_class = OllamaLLM

    # TODO: Remove hard-coded LLM name
    def get_llm(self, model_name="gemma3:latest"):
        try:
            return self.llm_class(model=model_name)
        except Exception as e:
            print(f"LLMProvider.get_llm() - Exception: {e}")
