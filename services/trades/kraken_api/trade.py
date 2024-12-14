from datetime import datetime

from pydantic import BaseModel


class Trade(BaseModel):
    """
    A Trade from Kraken API.

    symbol": "MATIC/USD",
    "side": "sell",
    "price": 0.5117,
    "qty": 40.0,
    "ord_type": "market",
    "trade_id": 4665906,
    "timestamp": "2023-09-25T07:49:37.708706Z"
    """

    pair: str
    price: float
    volume: float
    timestamp: datetime

    @property
    def timestamp_ms(self) -> int:
        """
        Return the timestamp in milliseconds.
        """
        return int(self.timestamp.timestamp() * 1000)

    def to_dict(self) -> dict:
        return self.model_dump_json()
