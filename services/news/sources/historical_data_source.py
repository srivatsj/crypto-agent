from quixstreams.sources import CSVSource

HistoricalNewsDataSource = CSVSource


def get_historical_data_source() -> CSVSource:
    # TODO: Download the rar file, Extract the rar file and Return the CSVSource

    path_to_csv_file = '/home/srivats/AI-ML/crypto-agent/services/news-signal/data/cryptopanic_news.csv'
    return CSVSource(
        path=path_to_csv_file,
        name='historical_news',
    )
