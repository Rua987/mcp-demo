"""ERA_TOTAL_COINS matches the total_coins values from scripts/era_data.gd."""

ERA_TOTAL_COINS = [3, 4, 4, 5]


def sum_coins_through_era(era_index: int) -> int:
    """Return the sum of total_coins for eras 0..era_index inclusive.

    Raises IndexError if era_index is out of range.
    """
    if era_index < 0 or era_index >= len(ERA_TOTAL_COINS):
        raise IndexError(f"era_index {era_index} out of range (0..{len(ERA_TOTAL_COINS) - 1})")
    return sum(ERA_TOTAL_COINS[:era_index + 1])
