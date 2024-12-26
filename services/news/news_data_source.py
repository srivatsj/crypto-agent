import time
from typing import Optional

from news_downloader import NewsDownloader
from quixstreams.sources.base import StatefulSource


class NewsDataSource(StatefulSource):
    def __init__(
        self,
        news_downloader: NewsDownloader,
        polling_interval_seconds: Optional[int] = 10,
    ):
        super().__init__(name='news_data_source')
        self.news_downloader = news_downloader
        self.polling_interval_seconds = polling_interval_seconds

    def run(self):
        last_published_at = self.state.get('last_published_at', None)

        while self.running:
            # Download news, the output is sorted by published_at in increasing order
            news = self.news_downloader.get_news()

            # Keep only the news that are newer than the last_published_at
            if last_published_at is not None:
                news = [
                    news_item
                    for news_item in news
                    if news_item.published_at > last_published_at
                ]

            # Produce the news
            for news_item in news:
                # Serialize the news_item and produce it
                message = self.serialize(key='news', value=news_item.to_dict())
                self.produce(key=message.key, value=message.value)

            # Update the last_published_at in the state
            if news:
                last_published_at = news[-1].published_at

            # Update the state
            self.state.set('last_published_at', last_published_at)

            # Flush the state
            self.flush()

            # sleep for the poll interval
            time.sleep(self.polling_interval_seconds)
