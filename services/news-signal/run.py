from config import config
from llms.base import BaseNewsSignalExtractor
from llms.factory import get_llm
from llms.openai import OpenAINewsSignalExtractor
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafa_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    llm: OpenAINewsSignalExtractor,
):
    logger.info('Starting news-signal service!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest',
    )

    input_topic = app.topic(name=kafa_input_topic, value_deserializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    sdf = app.dataframe(input_topic)

    # Process the incoming news into a news signal
    sdf = sdf.apply(
        lambda value: {
            'news': value['title'],
            **llm.get_news_signals(value['title']),
            'model_name': llm.model_name,
            'timestamp_ms': value['timestamp_ms'],
        }
    )

    sdf = sdf.update(lambda value: logger.info(value))

    sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    logger.info(f'Get llm for model provider: {config.model_provider}')
    # Get the LLM we want for the news signal extracter
    llm: BaseNewsSignalExtractor = get_llm(config.model_provider)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafa_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        llm=llm,
    )
