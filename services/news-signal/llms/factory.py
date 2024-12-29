from typing import Literal

from .base import BaseNewsSignalExtractor
from .config import ollama_config, openai_config
from .ollama import OllamaNewsSignalExtractor
from .openai import OpenAINewsSignalExtractor


def get_llm(model_provider: Literal['openai', 'ollama']) -> BaseNewsSignalExtractor:
    """
    Get the LLMs we want for the news signal extracter

    Args:
    - model_provider: The provider of the LLMs

    Returns:
    - BaseNewsSignalExtractor: The LLMs we want for the news signal extracter
    """

    if model_provider == 'openai':
        return OpenAINewsSignalExtractor(
            model_name=openai_config.model_name, api_key=openai_config.api_key
        )
    elif model_provider == 'ollama':
        return OllamaNewsSignalExtractor(model_name=ollama_config.model_name)
    else:
        raise ValueError(f'Unsupported model provider: {model_provider}')
