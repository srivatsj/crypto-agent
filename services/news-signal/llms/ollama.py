from typing import Literal, Optional

from llama_index.core.prompts import PromptTemplate
from llama_index.llms.ollama import Ollama

from .base import BaseNewsSignalExtractor, NewsSignal
from .config import ollama_config
from .prompt_template import prompt_template


class OllamaNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = Ollama(model=model_name, temperature=temperature)
        self.prompt_template = PromptTemplate(template=prompt_template)
        self.model_name = model_name

    def get_news_signals(
        self, text: str, output_format: Literal['dict', 'NewsSignal'] = 'dict'
    ) -> NewsSignal | dict:
        response: NewsSignal = self.llm.structured_predict(
            NewsSignal, prompt=self.prompt_template, news_article=text
        )

        if output_format == 'dict':
            return response.to_dict()
        else:
            return response


if __name__ == '__main__':
    llm = OllamaNewsSignalExtractor(model_name=ollama_config.model_name)

    examples = [
        "Bitcoin ETF ads spotted on China's Alipay payment app",
        "U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward",
        "Trump's World Liberty Acquires ETH, LINK and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        """
        {
        'btc_signal': 1,
        'eth_signal': 0,
        'reasoning': "The news of Bitcoin ETF ads being spotted on China's Alipay
        payment app suggests a growing interest in Bitcoin among Chinese investors.
        This could lead to increased demand for BTC, causing its price to rise."
        }
        {
        'btc_signal': -1,
        'eth_signal': -1,
        'reasoning': "The US Supreme Court has ruled in favor of Nvidia's crypto
        lawsuit, which could lead to increased regulatory scrutiny for the entire
        cryptocurrency industry. This is likely to negatively impact both BTC and
        ETH prices as investors become more cautious."
        }
        {
        'btc_signal': 0,
        'eth_signal': 1,
        'reasoning': "The acquisition of ETH by a major company like Trump's World
        Liberty suggests that there is increased demand for Ethereum, which could
        lead to an increase in its price."
        }
        """
        response = llm.get_news_signals(example)
        print(response)
