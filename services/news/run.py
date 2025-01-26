from config import config
from loguru import logger
from quixstreams import Application
from sources.factory import get_source
from sources.news_data_source import NewsDataSource


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

    # sdf.print(metadata=True)

    # Send the news to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    # Get the news data source either live or historical
    # - live: from the Cryptopanic API
    # - historical: from a CSV file
    news_data_source = get_source(config.data_source, config.polling_interval_seconds)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_output_topic=config.kafka_output_topic,
        news_source=news_data_source,
    )
