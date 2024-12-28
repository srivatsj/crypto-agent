from typing import Literal, Optional

from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI

from .base import BaseNewsSignalExtractor, NewsSignal
from .config import openai_config
from .prompt_template import prompt_template


class OpenAINewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = OpenAI(model=model_name, api_key=api_key, temperature=temperature)
        self.prompt_template = PromptTemplate(template=prompt_template)
        self.model_name = model_name

    def get_news_signals(
        self, text: str, output_format: Literal['dict', 'NewsSignal'] = 'NewsSignal'
    ) -> NewsSignal | dict:
        response: NewsSignal = self.llm.structured_predict(
            NewsSignal, prompt=self.prompt_template, news_article=text
        )

        if output_format == 'dict':
            return response.to_dict()
        else:
            return response


if __name__ == '__main__':
    llm = OpenAINewsSignalExtractor(
        model_name=openai_config.model_name, api_key=openai_config.api_key
    )

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
        'reasoning': 'The presence of Bitcoin ETF ads on a major payment
        app like Alipay in China indicates increased interest and accessibility
        for Bitcoin investments, which is likely to drive up demand and
        consequently the price of Bitcoin. However, this news does not
        have a direct impact on Ethereum.'
        }
        {
        'btc_signal': 1,
        'eth_signal': 0,
        'reasoning': 'The presence of Bitcoin ETF ads on a major payment
        app like Alipay in China indicates increased interest and
        accessibility for Bitcoin investments, which is likely to drive
        up demand and consequently the price of Bitcoin. However, this
        news does not have a direct impact on Ethereum.'
        }
        {
        'btc_signal': 1,
        'eth_signal': 0,
        'reasoning': 'The presence of Bitcoin ETF ads on a major payment
        app like Alipay in China indicates increased interest and
        accessibility for Bitcoin investments, which is likely to drive
        up demand and consequently the price of Bitcoin. However, this
        news does not have a direct impact on Ethereum.'
        }
        """
        response = llm.get_news_signals(example)
        print(response)
