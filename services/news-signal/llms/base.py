from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, Field


class NewsSignalOneCoin(BaseModel):
    coin: Literal[
        'BTC',
        'ETH',
        'SOL',
        'XRP',
        'DOGE',
        'ADA',
        'XLM',
        'LTC',
        'BCH',
        'DOT',
        'XMR',
        'EOS',
        'XEM',
        'ZEC',
        'ETC',
        'XLM',
        'LTC',
        'BCH',
        'DOT',
        'XMR',
        'EOS',
        'XEM',
        'ZEC',
        'ETC',
        'LINK',
        'AAVE',
    ] = Field(description='The coin that the news is about')
    signal: Literal[1, -1] = Field(
        description="""
        The signal of the news on the coin price.
        1 if the price is expected to go up
        -1 if the price is expected to go down.

        If the news is not related to the coin, no need to create a news signal.
        """
    )


class NewsSignal(BaseModel):
    news_signals: list[NewsSignalOneCoin]

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the NewsSignal object.
        """
        raise NotImplementedError()


class BaseNewsSignalExtractor(ABC):
    @abstractmethod
    def get_news_signals(
        self, text: str, output_format: Literal['dict', 'NewsSignal'] = 'dict'
    ) -> NewsSignal | dict:
        pass
