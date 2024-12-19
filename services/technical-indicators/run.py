from candle import update_candles
from config import config
from loguru import logger
from quixstreams import Application
from technical_indicators import compute_technical_indicators


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    max_candles_in_state: int,
    candle_seconds: int,
):
    """
    3 steps:
    1. Ingest candles from kafka_input_topic
    2. Compute technical indicators
    3. Send technical indicators to kafka_output_topic

    Args:
        kafka_broker_address: The address of the Kafka broker.
        kafka_input_topic: The topic to consume candles from.
        kafka_output_topic: The topic to produce technical indicators to.
        kafka_consumer_group: The consumer group to use for the Kafka consumer.
        max_candles_in_state: The maximum number of candles to keep in the state.
        candle_seconds: The number of seconds per candle.
    Returns:
        None
    """
    logger.info('Startingtechnical-indicators service!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    input_topic = app.topic(name=kafka_input_topic, value_deserializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Create streaming dataframes so we can start transforming the data in real-time
    sdf = app.dataframe(topic=input_topic)

    # We only want to keep the candles with the same window size as the candle_seconds
    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    sdf = sdf.apply(update_candles, stateful=True)

    sdf = sdf.apply(compute_technical_indicators, stateful=True)

    sdf.update(lambda value: logger.debug(f'final message: {value}'))

    sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        max_candles_in_state=config.max_candles_in_state,
        candle_seconds=config.candle_seconds,
    )
