from era_totals import sum_coins_through_era


def expected_coins_for_era(era_index: int) -> int:
    return sum_coins_through_era(era_index)


def coins_match_era(coins: int, era_index: int) -> bool:
    return coins == expected_coins_for_era(era_index)
