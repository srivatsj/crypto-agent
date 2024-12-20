from config import config, hopsworks_credentials
from loguru import logger
from quixstreams import Application
from sink import HopsworksFeatureStoreSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    output_sink: HopsworksFeatureStoreSink,
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

    sdf = app.dataframe(input_topic)

    sdf.sink(output_sink)

    app.run()


if __name__ == '__main__':
    hopsworks_sink = HopsworksFeatureStoreSink(
        # Hopsworks credentials
        api_key=hopsworks_credentials.hopsworks_api_key,
        project_name=hopsworks_credentials.hopsworks_project_name,
        # Feature group configuration
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
        feature_group_primary_keys=config.feature_group_primary_keys,
        feature_group_event_time=config.feature_group_event_time,
    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        output_sink=hopsworks_sink,
    )
