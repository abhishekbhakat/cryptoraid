import math


def round_down(n: float, decimals: int = 0) -> float:
    multiplier = 10**decimals
    return math.floor(n * multiplier) / multiplier


def round_up(n: float, decimals: int = 0) -> float:
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier
