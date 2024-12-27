from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, Field


class NewsSignal(BaseModel):
    """
    Represents a market sentiment for the crypto.
    """

    btc_signal: Literal[1, 0, -1] = Field(
        description="""
        The impact of the news on the BTC price.
        1 if the price is expected to go up
        0 if the price is expected to remain the same,
        -1 if the price is expected to go down.

        If the news is not related to BTC, the value is 0.
                                          """
    )
    eth_signal: Literal[1, 0, -1] = Field(
        description="""
        The impact of the news on the ETH price.
        1 if the price is expected to go up
        0 if the price is expected to remain the same,
        -1 if the price is expected to go down.

        if the news is not related to ETH, the value is 0.
        """
    )
    reasoning: str = Field(
        description="""
        The reasoning behind the btc_signal and eth_signal extracted from the news article.
        """
    )

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the NewsSignal object.
        """
        return {
            'btc_signal': self.btc_signal,
            'eth_signal': self.eth_signal,
            'reasoning': self.reasoning,
        }


class BaseNewsSignalExtractor(ABC):
    @abstractmethod
    def get_news_signals(
        self, text: str, output_format: Literal['dict', 'NewsSignal'] = 'dict'
    ) -> NewsSignal | dict:
        pass
