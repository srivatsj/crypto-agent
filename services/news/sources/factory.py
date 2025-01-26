from typing import Literal, Optional, Union

from config import cryptopanic_config

from .historical_data_source import HistoricalNewsDataSource, get_historical_data_source
from .news_data_source import NewsDataSource as LiveNewsDataSource
from .news_downloader import NewsDownloader

NewsDataSource = Union[LiveNewsDataSource, HistoricalNewsDataSource]


def get_source(
    data_source: Literal['live', 'historical'],
    polling_interval_seconds: Optional[int] = 10,
) -> NewsDataSource:
    if data_source == 'live':
        # News Downlaoder object
        news_downloader = NewsDownloader(cryptopanic_config.api_key)

        # Quixstreams data source that wraps the news downloader
        news_data_source = LiveNewsDataSource(
            news_downloader=news_downloader,
            polling_interval_seconds=polling_interval_seconds,
        )
        return news_data_source
    elif data_source == 'historical':
        return get_historical_data_source()
    else:
        raise ValueError(f'Invalid data source type: {data_source}')
