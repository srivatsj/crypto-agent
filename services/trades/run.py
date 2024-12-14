from loguru import logger
from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from quixstreams import Application
from config import config
from time import sleep
from typing import Union

def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: Union[KrakenMockAPI, KrakenWebsocketAPI]
):
    """
    It does 2 things:
    1. Listens to trades from Kraken API
    2. Saves trades to a kafka topic

    Args:
        Kafka broker address
        Kafka topic
        Kraken API

    Returns:
        None
    """
    logger.info("Starting trades service")

    app = Application(
        broker_address=kafka_broker_address,
    )

    topic = app.topic(name=kafka_topic, value_serializer='json')

    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()
            
            for trade in trades:
                # Serialize the trade to bytes
                message = topic.serialize(key=trade.pair, value=trade.to_dict())
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f"Produced trade to topic {trade}")
                sleep(1)
    
        


if __name__ == "__main__":

    kraken_api = KrakenWebsocketAPI(pairs=config.pairs)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api
    )
