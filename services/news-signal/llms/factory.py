from typing import Literal

from .base import BaseNewsSignalExtractor
from .config import openai_config
from .openai import OpenAINewsSignalExtractor


def get_llms(model_provider: Literal['openai', 'ollama']) -> BaseNewsSignalExtractor:
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
    else:
        raise ValueError(f'Unsupported model provider: {model_provider}')
