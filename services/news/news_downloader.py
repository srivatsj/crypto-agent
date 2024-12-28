from datetime import datetime
from typing import List, Tuple

import requests
from config import cryptopanic_config
from loguru import logger
from pydantic import BaseModel


class News(BaseModel):
    """
    This is the model for a news article.
    """

    title: str
    published_at: str
    source: str

    def to_dict(self) -> dict:
        try:
            timestamp = datetime.strptime(self.published_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            timestamp = datetime.strptime(self.published_at, '%Y-%m-%dT%H:%M:%S%z')

        return {
            **self.model_dump(),
            'timestamp_ms': int(timestamp.timestamp() * 1000),
        }


class NewsDownloader:
    URL = 'https://cryptopanic.com/api/free/v1/posts/'

    def __init__(self, cryptopanic_api_key):
        self.cryptopanic_api_key = cryptopanic_api_key

    def _get_batch_of_news(self, url: str) -> Tuple[List[News], str]:
        """
        Connect to the Cryptopanic API and fetches one batch of news.

        Returns:
            List[dict]: List of news articles.
        """

        response = requests.get(url)

        try:
            response = response.json()
        except Exception as e:
            logger.error(f'Failed to parse response from CryptoPanic API. Error: {e}')
            return ([], '')

        # Parse the response and create a list of news objects
        news = [
            News(
                title=post['title'],
                published_at=post['published_at'],
                source=post['domain'],
            )
            for post in response['results']
        ]

        next_url = response['next']
        return news, next_url

    def get_news(self) -> List[News]:
        """
        Keeps on calling _get_batch_of_news until all news articles are fetched or gets an empty list.
        """
        news = []
        url = self.URL + '?auth_token=' + self.cryptopanic_api_key

        while True:
            logger.debug(f'Fetching news from {url}')
            batch_of_news, next_url = self._get_batch_of_news(url)
            news += batch_of_news
            logger.debug(f'Fetching {len(batch_of_news)} batched news articles')
            if not batch_of_news:
                break
            if not next_url:
                logger.debug('next url is empty. Breaking the loop.')
                break

            url = next_url

        # Sort the news by published_at
        news.sort(key=lambda x: x.published_at, reverse=False)
        return news


if __name__ == '__main__':
    news_downloader = NewsDownloader(cryptopanic_config.api_key)
    news = news_downloader.get_news()
    logger.debug(f'Fetched {len(news)} news articles')
