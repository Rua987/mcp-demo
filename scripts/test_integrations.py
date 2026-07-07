"""Integration tests for ce_anchor_math and era_totals."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ce_anchor_math import CE_SCAN_COINS, decode_counter, encode_anchor  # noqa: E402
from era_totals import sum_coins_through_era  # noqa: E402


def test_ce_anchor_round_trip_counter_three():
    anchor = encode_anchor(CE_SCAN_COINS, 3)
    assert decode_counter(CE_SCAN_COINS, anchor) == 3


def test_era_totals_through_era_three():
    assert sum_coins_through_era(3) == 16
