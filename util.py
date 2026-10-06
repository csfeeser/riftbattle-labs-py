def clamp(value: int, minimum: int, maximum: int) -> int:
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value
