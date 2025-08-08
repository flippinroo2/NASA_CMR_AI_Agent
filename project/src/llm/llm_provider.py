from enum import Enum
from typing import Any

from langchain.chat_models import init_chat_model
from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseLLM
from langchain_ollama.llms import OllamaLLM


class LLM_PROVIDER_ENUM(Enum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    BEDROCK_CONVERSE = "bedrock_converse"
    DEEPSEEK = "deepseek"
    GOOGLE = "google"
    GROQ = "groq"
    HUGGING_FACE = "huggingface"
    LM_STUDIO = "lmstudio"
    MISTRAL = "mistralai"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"
    OPEN_AI = "openai"
    PERPLEXITY = "perplexity"
    XAI = "xai"


class LLMProvider:
    _llm_class = None
    llm: BaseLLM | _ConfigurableModel | None = None

    def __init__(self, llm_provider: LLM_PROVIDER_ENUM):
        if llm_provider == LLM_PROVIDER_ENUM.OLLAMA:
            self._llm_class = OllamaLLM

    # TODO: Remove hard-coded LLM name
    def get_llm(
        self, model_name="gemma3:latest"
    ) -> _ConfigurableModel | OllamaLLM | Any | None:
        if self.llm is not None:
            return self.llm
        if self._llm_class is None:
            self.llm = self._get_dynamic_llm(model_name)
        else:
            try:
                self.llm = self._llm_class(model=model_name)
            except Exception as e:
                print(f"LLMProvider.get_llm() - Exception: {e}")
        return self.llm

    def _get_dynamic_llm(self, model_name) -> _ConfigurableModel | None:
        try:
            return init_chat_model(model_name=model_name)
        except Exception as e:
            print(f"LLMProvider._get_dynamic_llm() - Exception: {e}")

    def set_llm(self, llm) -> None:
        self.llm = llm
