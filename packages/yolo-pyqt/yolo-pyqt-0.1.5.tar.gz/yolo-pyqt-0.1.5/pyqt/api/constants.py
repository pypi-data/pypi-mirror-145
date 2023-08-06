from enum import Enum


class TradeSide(Enum):
    BUY = 1
    SELL = 2


class OrderType(Enum):
    NORMAL = 1
    MARKET = 2


class OrderStatus(Enum):
    FILLED = 1  # including all filled and partly filled
    FAILED = 2  # including failed, canceling, canceled, disabled, deleted, inactive etc.
    SUBMITTED = 3  # including pre-submitted, submitted, pending etc.


DICT_KEY_MAX_BUY = "max_buy"
DICT_KEY_MAX_SELL = "max_sell"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MS_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
