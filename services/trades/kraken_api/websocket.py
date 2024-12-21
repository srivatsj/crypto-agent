import json
from typing import List

from loguru import logger
from websocket import create_connection

from .base import TradesApi
from .trade import Trade


class KrakenWebsocketAPI(TradesApi):
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # Create a websocket client
        self._ws_client = create_connection(self.URL)

        self._subscribe()

    def _subscribe(self):
        # Subscribe to the Kraken websocket API
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': self.pairs,
                        'snapshot': True,
                    },
                }
            )
        )

        for _ in self.pairs:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()

    def get_trades(self) -> List[Trade]:
        """
        Fetch trades from the Kraken websocket API and return them as a list of Trade objects.

        Returns:
            List[Trade]: A list of Trade objects.
        """
        # Fetch trades from the Kraken websocket API
        data = self._ws_client.recv()

        if 'heartbeat' in data:
            logger.info(f'Heartbeat received: {data}')
            return []

        # Transform the data into JSON object
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            logger.error(f'Failed to decode JSON: {data}')
            return []

        try:
            trades_data = data['data']
        except KeyError:
            logger.error(f'No data field with trades in the message: {data}')
            return []

        trades = [
            Trade.from_kraken_websocket_api_response(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp'],
            )
            for trade in trades_data
        ]

        return trades

    def is_done(self) -> bool:
        return False
