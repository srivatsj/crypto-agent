from config import config
from loguru import logger
from quixstreams import State

MAX_CANDLES_IN_STATE = config.max_candles_in_state


def same_window(candle_1: dict, candle_2: dict) -> bool:
    """
    Check if candle1 and candle 2 are in the same window.

    Args:
        candle_1: The first candle.
        candle_2: The last candle.

    Returns:
        True if the candles are in the same window, False otherwise.
    """
    return (
        candle_1['window_start_ms'] == candle_2['window_start_ms']
        and candle_1['window_end_ms'] == candle_2['window_end_ms']
        and candle_1['pair'] == candle_2['pair']
    )


def update_candles(candle: dict, state: State) -> dict:
    """
    Update the list of candles we have in our state using the last candle.

    if the latest candle corresponds to new window, we just add it to the list.
    If it corresponds to the last window, we update the last candle in the list.

    Args:
        candle: The latest candle.
        state: The state of the application.

    Returns:
        The updated list of candles.
    """
    # Get the list of candles from the state
    candles = state.get('candles', default=[])

    if not candles:
        candles.append(candle)
    # If the latest candle corresponds to new window, we just add it to the list.
    elif same_window(candle, candles[-1]):
        # Update the last candle in the list
        candles[-1] = candle
    else:
        candles.append(candle)

    # If the total number of candles is greater than the number of candles we want to keep, we remove the oldest candle.
    if len(candles) > MAX_CANDLES_IN_STATE:
        candles.pop(0)

    logger.info(f'Number of candles in state for {candle["pair"]}: {len(candles)}')

    # Update the state with the new list of candles
    state.set('candles', candles)

    return candles
