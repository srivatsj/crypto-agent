from config import config
from kraken_api.base import TradesApi
from kraken_api.mock import KrakenMockAPI
from kraken_api.rest import KrakenRestAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    trades_api: TradesApi,
):
    """
    It does 2 things:
    1. Listens to trades from Kraken API
    2. Saves trades to a kafka topic

    Args:
        Kafka broker address: str
        Kafka topic: str
        Trades API: TradesApi with get_trades() and is_done() methods

    Returns:
        None
    """
    logger.info('Starting trades service')

    app = Application(
        broker_address=kafka_broker_address,
    )

    topic = app.topic(name=kafka_topic, value_serializer='json')

    with app.get_producer() as producer:
        while not trades_api.is_done():
            trades = trades_api.get_trades()

            for trade in trades:
                # serialize the trade as bytes
                message = topic.serialize(
                    key=trade.pair.replace('/', '-'),
                    value=trade.to_dict(),
                )

                # push the serialized message to the topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Produced trade to topic {trade}')


if __name__ == '__main__':
    # Initialize the Kraken API based on the data source
    if config.data_source == 'live':
        kraken_api = KrakenWebsocketAPI(pairs=config.pairs)
    elif config.data_source == 'historical':
        kraken_api = KrakenRestAPI(pairs=config.pairs, last_n_days=config.last_n_days)
    elif config.data_source == 'test':
        kraken_api = KrakenMockAPI(pairs=config.pairs)
    else:
        raise ValueError(f'Invalid data source: {config.data_source}')

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trades_api=kraken_api,
    )
