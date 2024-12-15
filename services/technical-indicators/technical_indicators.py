import numpy as np
from quixstreams import State
from talib import stream


def compute_technical_indicators(candles: list, state: State) -> dict:
    candles = state.get('candles', default=[])

    # Extract open, high, low, close and volume prices from the candles
    # open = np.array([candle['open'] for candle in candles])
    # high = np.array([candle['high'] for candle in candles])
    # low = np.array([candle['low'] for candle in candles])
    close = np.array([candle['close'] for candle in candles])
    # volume = np.array([candle['volume'] for candle in candles])

    # Compute the technical indicators
    _sma = stream.SMA(close, 3)
