prompt_template = """
    You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.

    Analyze the following news article and determine its potential impact on crypto asset prices.
    Focus on both direct mentions and indirect implications for each asset.

    Do not output data for a given coin if the news is not relevant to it.

    ## Example input
    "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

    ## Example output
    [
        {"coin": "BTC", "signal": 1},
        {"coin": "ETH", "signal": 1},
        {"coin": "XRP", "signal": -1},
    ]

    News article to analyze:
    {news_article}
"""
