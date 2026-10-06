import random


def clamp(value: int, minimum: int, maximum: int) -> int:
    """Return value bounded by minimum and maximum."""
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def min_of(a: int, b: int) -> int:
    """Return the minimum of two values."""
    if a < b:
        return a
    return b


def max_of(a: int, b: int) -> int:
    """Return the maximum of two values."""
    if a > b:
        return a
    return b


def random_int(minimum: int, maximum: int) -> int:
    """Return a random integer between minimum and maximum (inclusive)."""
    return random.randint(minimum, maximum)


def random_bool(percent_chance: int) -> bool:
    """Return True with the given percentage chance."""
    return random_int(1, 100) <= percent_chance


def calculate_critical_chance(base_crit_chance: int) -> bool:
    """Calculate crit chance."""
    return random_int(1, 100) <= base_crit_chance


def abs_value(value: int) -> int:
    """Return the absolute value of an integer."""
    if value < 0:
        return -value
    return value


def percentage_of(value: int, percentage: int) -> int:
    """Calculate a percentage of a value."""
    return (value * percentage) // 100


def average(a: int, b: int) -> int:
    """Return the average of two values."""
    return (a + b) // 2


def scale(value: int, numerator: int, denominator: int) -> int:
    """Scale a value based on a ratio."""
    if denominator == 0:
        return 0
    return (value * numerator) // denominator
