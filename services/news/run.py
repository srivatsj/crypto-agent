from config import config, cryptopanic_config
from loguru import logger
from news_data_source import NewsDataSource
from news_downloader import NewsDownloader
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_output_topic: str,
    news_source: NewsDataSource,
):
    """
    Gets news from the Cryptopanic API and sends it to the Kafka topic.

    Args:
        kafka_broker_address (str): Kafka broker address.
        kafka_output_topic (str): Kafka output topic.
        news_source (NewsDataSource): News data source.
    Returns:
        None
    """
    logger.info('Starting news service!')

    app = Application(
        broker_address=kafka_broker_address,
    )

    # Create the output topic
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Create the streaming dataframe
    sdf = app.dataframe(source=news_source)

    sdf.print(metadata=True)

    # Send the news to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    # News Downlaoder object
    news_downloader = NewsDownloader(cryptopanic_config.api_key)

    # Quixstreams data source that wraps the news downloader
    news_data_source = NewsDataSource(
        news_downloader=news_downloader,
        polling_interval_seconds=config.polling_interval_seconds,
    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_output_topic=config.kafka_output_topic,
        news_source=news_data_source,
    )
