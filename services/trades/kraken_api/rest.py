import json
import time
from typing import List

import requests
from loguru import logger

from .base import TradesApi
from .trade import Trade


class KrakenRestAPI(TradesApi):
    def __init__(self, pairs: List[str], last_n_days: int):
        self.pairs = pairs
        self.last_n_days = last_n_days

        self.apis = [
            KrakenRestAPISinglePair(pair=pair, last_n_days=self.last_n_days)
            for pair in self.pairs
        ]

    def get_trades(self) -> List[Trade]:
        """
        Get trades for each pair, sort them by timestamp and return the list of trades
        """
        trades = []
        for api in self.apis:
            if not api.is_done():
                trades += api.get_trades()

        # Sort the trades by timestamp
        trades.sort(key=lambda x: x.timestamp_ms)

        return trades

    def is_done(self) -> bool:
        """
        We are done when all the APIs are done
        """
        return all(api.is_done() for api in self.apis)


class KrakenRestAPISinglePair(TradesApi):
    URL = 'https://api.kraken.com/0/public/Trades'

    def __init__(self, pair: str, last_n_days: int) -> None:
        self.pair = pair
        self.last_n_days = last_n_days
        self._is_done = False

        # Get Current timestamp in nanoseconds
        self.since_timestamp_nanoseconds = int(
            time.time_ns() - last_n_days * 24 * 60 * 60 * 1000000000
        )

        logger.info(
            f'Initializing KrakenRestAPISinglePair for pair {self.pair} and last {int(self.since_timestamp_nanoseconds * 1e9)} seconds'
        )

    def get_trades(self) -> List[Trade]:
        """
        Send a request to Kraken API and return a list of trades
        """
        headers = {'Accept': 'application/json'}
        params = {'pair': self.pair, 'since': self.since_timestamp_nanoseconds}

        response = requests.request('GET', self.URL, headers=headers, params=params)
        logger.info(f'Response from Krakpe rest API: {response.text}')

        # Parse the response as json
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f'Failed to parse response as JSON: {e}')
            return []

        # TODO: Check if the request is throttled, we need implement a retry and slow down mechanism

        # Get the trades for the self.pair cryptocurrency
        try:
            trades = data['result'][self.pair]
        except KeyError as e:
            logger.error(f'Failed to get trades for pair {self.pair}: {e}')
            return []

        # Transform the trades to a list of Trade objects
        trades = [
            Trade.from_kraken_rest_api_response(
                pair=self.pair,
                price=trade[0],
                volume=trade[1],
                timestamp_sec=trade[2],
            )
            for trade in trades
        ]

        # Update the since_timestamp_nanoseconds to the timestamp of the last trade
        self.since_timestamp_nanoseconds = int(float(data['result']['last']))

        # Check if the since_timestamp_nanoseconds is greater than the current timestamp
        if self.since_timestamp_nanoseconds > int(time.time_ns() - 1e9):
            self._is_done = True

        if self.since_timestamp_nanoseconds == 0:
            self._is_done = True

        return trades

    def is_done(self) -> bool:
        return self._is_done
