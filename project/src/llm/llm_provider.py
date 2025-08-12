from typing import Type, TypeVar

import langchain.chat_models
import langchain.chat_models.base
import langchain_core.language_models
import langchain_ollama.llms
import langchain_openai.llms

import src.ENUMS

T_BaseLLM = TypeVar("T_BaseLLM", bound=Type[langchain_core.language_models.BaseLLM])


class LLMProvider:
    """
    Class used for handling connections to different LLMs
    """

    _llm: langchain.chat_models.base._ConfigurableModel | langchain_core.language_models.BaseLLM | None = None
    _llm_class: Type[langchain_core.language_models.BaseLLM] = langchain_core.language_models.BaseLLM

    def __init__(self, llm_provider: src.ENUMS.LLM_PROVIDER) -> None:
        if llm_provider == src.ENUMS.LLM_PROVIDER.OLLAMA:
            self._llm_class = langchain_ollama.llms.OllamaLLM
        if llm_provider == src.ENUMS.LLM_PROVIDER.LM_STUDIO:
            self._llm_class = langchain_openai.llms.OpenAI  # TODO: This needs to work similar to an OpenAI model, however, the parameters will point it to a localhost URL instead.

    def get_llm(
        self, model_name: str = "gemma3:latest"
    ) -> langchain.chat_models.base._ConfigurableModel | langchain_core.language_models.BaseLLM:
        """
        Returns the value of the _llm variable.

        Args:
            model_name (str): The name of the model to initialize.

        Returns:
            The value of the _llm variable.

        Notes:
            TODO: Expand this function to handle API keys, and other parameters based on the LLM_PROVIDER passed in.
        """
        if self._llm is not None:
            return self._llm
        if self._llm_class is None:
            self._llm = self._get_dynamic_llm(model_name)
        else:
            try:
                self._llm = self._llm_class(model=model_name)  # type: ignore
            except Exception as exception:
                print(f"LLMProvider.get_llm() - Exception: {exception}")
                raise exception
        return self._llm

    def _get_dynamic_llm(self, model_name) -> langchain.chat_models.base._ConfigurableModel:
        """
        Dynamically initialize a chat model based on model name.

        Args:
            model_name: The name of the model to initialize.

        Returns:
            The initialized chat model.
        """
        try:
            return langchain.chat_models.init_chat_model(model_name=model_name)
        except Exception as exception:
            print(f"LLMProvider._get_dynamic_llm() - Exception: {exception}")
            raise exception

    def set_llm(self, llm: langchain.chat_models.base._ConfigurableModel | langchain_core.language_models.BaseLLM) -> None:
        """
        Sets the value of the _llm variable.

        Args:
            llm: The value to set the _llm variable to.

        Returns:
            None
        """
        self._llm = llm
