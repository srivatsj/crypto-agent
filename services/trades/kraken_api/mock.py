# Mock the Kraken API
from datetime import datetime
from typing import List

from .trade import Trade


class KrakenMockAPI:
    def __init__(self, pair: str):
        self.pair = pair

    def get_trades(self) -> List[Trade]:
        """
        Returns mock trades.
        """
        mock_trades = [
            Trade(
                pair=self.pair,
                price=0.5117,
                volume=40.0,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
            Trade(
                pair=self.pair,
                price=0.5217,
                volume=40.0,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
            Trade(
                pair=self.pair,
                price=0.5317,
                volume=40.0,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
        ]
        return mock_trades
