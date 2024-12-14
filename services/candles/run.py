from datetime import timedelta
from typing import Any, List, Optional, Tuple

from config import config
from loguru import logger
from quixstreams import Application
from quixstreams.models import TimestampType


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload instead of Kafka timestamp.
    """
    return value['timestamp_ms']


def init_candle(trade: dict) -> dict:
    """
    Initializes a candle with the first trade.
    """
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['volume'],
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair'],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Updates a candle with a latest trade.
    """
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['volume']
    candle['timestamp_ms'] = trade['timestamp_ms']
    candle['pair'] = trade['pair']
    return candle


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candles_seconds: int,
):
    """
    3 steps:
    1. Ingests trades from kafka
    2. Generates candles using tumbling window and
    3. Outputs candles to kafka

    Args:
        kafka_broker_address: str
        kafka_input_topic: str
        kafka_output_topic: str
        kafka_consumer_group: str
        candles_seconds: int
    Returns:
        None
    """
    logger.info('Starting candles service!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        timestamp_extractor=custom_ts_extractor,
    )
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Create streaming dataframes
    sdf = app.dataframe(topic=input_topic)

    # Create a tumbling window
    sdf = sdf.tumbling_window(timedelta(seconds=candles_seconds))

    # Apply the reducer to update the candle or initialize the candle with the first trade
    sdf = sdf.reduce(
        reducer=update_candle,
        initializer=init_candle,
    )

    # Emity all intermediate candles to make the system more responsive
    sdf = sdf.current()

    # Exrtract open, high, low, close, volume, timestamp_ms, pair from the dataframe
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    sdf['timestamp_ms'] = sdf['value']['timestamp_ms']
    sdf['pair'] = sdf['value']['pair']
    sdf['window_start_ms'] = sdf['start']
    sdf['window_end_ms'] = sdf['end']

    sdf = sdf[
        [
            'open',
            'high',
            'low',
            'close',
            'volume',
            'timestamp_ms',
            'pair',
            'window_start_ms',
            'window_end_ms',
        ]
    ]

    sdf = sdf.update(lambda value: logger.info(f'Candle: {value}'))

    # Push the candle to the output topic
    sdf.to_topic(topic=output_topic)

    # Start the application
    app.run()


if __name__ == '__main__':
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candles_seconds=config.candles_seconds,
    )
