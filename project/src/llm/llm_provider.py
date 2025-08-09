from enum import Enum
from typing import Any, Type, TypeVar

from langchain.chat_models import init_chat_model
from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseLLM
from langchain_ollama.llms import OllamaLLM
from langchain_openai.llms import OpenAI

from src.ENUMS import LLM_PROVIDER

T_BaseLLM = TypeVar("T_BaseLLM", bound=Type[BaseLLM])


class LLMProvider:
    _llm: _ConfigurableModel | BaseLLM | None = None
    _llm_class: Type[BaseLLM] = BaseLLM

    def __init__(self, llm_provider: LLM_PROVIDER):
        if llm_provider == LLM_PROVIDER.OLLAMA:
            self._llm_class = OllamaLLM
        if llm_provider == LLM_PROVIDER.LM_STUDIO:
            self._llm_class = OpenAI  # TODO: Fix this inside the get_llm() function, because an API key must be passed in... Also the other parameters to make it act as if it is an OpenAI LLM

    # TODO: Remove hard-coded LLM name and fix type safety stuff
    def get_llm(self, model_name="gemma3:latest") -> _ConfigurableModel | BaseLLM:
        if self._llm is not None:
            return self._llm
        if self._llm_class is None:
            self._llm = self._get_dynamic_llm(model_name)
        else:
            try:
                self._llm = self._llm_class(model=model_name)  # type: ignore
            except Exception as e:
                print(f"LLMProvider.get_llm() - Exception: {e}")
                raise e
        return self._llm

    def _get_dynamic_llm(self, model_name) -> _ConfigurableModel:
        try:
            return init_chat_model(model_name=model_name)
        except Exception as e:
            print(f"LLMProvider._get_dynamic_llm() - Exception: {e}")
            raise e

    def set_llm(self, llm: _ConfigurableModel | BaseLLM) -> None:
        self._llm = llm
