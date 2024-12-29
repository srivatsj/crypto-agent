import json
import random
from typing import Literal

import pandas as pd
from fire import Fire
from llms.factory import get_llm
from llms.prompt_template import prompt_template
from loguru import logger
from tqdm import tqdm


def generate_golden_dataset(
    model_provider: Literal['openai', 'ollama'], n: int, output_file: str
):
    """
    Generate a golden dataset of instruction input and output tuples
    to fine tune our model.

    Args:
        model_provider: The model provider to use for generating the golden dataset
        n: The number of news articles to sample
        output_file: The file to write the golden dataset to

    Returns:
        None
    """
    # Load dataset
    df = pd.read_csv('./data/cryptopanic_news.csv')
    news = df['title'].tolist()

    # Sample n news
    news = random.sample(news, n)

    # Get LLM
    llm = get_llm(model_provider)

    for news_item in tqdm(news):
        try:
            signals = llm.get_news_signals(news_item)

            output = {
                'instruction': prompt_template,
                'input': news_item,
                'output': signals.model_dump_json(),
                'teacher_model_name': llm.model_name,
            }

            with open(output_file, 'a') as f:
                f.write(json.dumps(output) + '\n')
        except Exception as e:
            logger.error(f'Error creating instructtion: {e}')
            continue


if __name__ == '__main__':
    Fire(generate_golden_dataset)
