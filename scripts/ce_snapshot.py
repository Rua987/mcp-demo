from ce_report import build_report
from ce_progress import coins_match_era, expected_coins_for_era


def build_snapshot(coins: int, deaths: int, era_index: int) -> str:
    return (
        build_report(coins, deaths)
        + " era="
        + str(era_index)
        + " expected="
        + str(expected_coins_for_era(era_index))
        + " match="
        + str(coins_match_era(coins, era_index))
    )
