from config import config
from loguru import logger
from quixstreams import Application
from quixstreams.sinks.core.csv import CSVSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    feature_group_name: str,
    feature_group_version: str,
):
    """
    2 things to do:
    1. Read messages from kafka topic
    2. Store messages to feature store

    Args:
        kafka_broker_address: str
        kafka_input_topic: str
        kafka_consumer_group: str
        feature_group_name: str
        feature_group_version: str

    Returns:
        None
    """
    logger.info('Starting to-feature-store service!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    input_topic = app.topic(kafka_input_topic, value_deserializer='json')

    csv_sink = CSVSink(path='technical_indicators.csv')

    sdf = app.dataframe(input_topic)

    # TODO: Need to extract features to store to the feature store.

    sdf.sink(csv_sink)

    app.run()


if __name__ == '__main__':
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )
