"""Tests for era_totals.py — mirrors era_data.gd total_coins per era."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from era_totals import ERA_TOTAL_COINS, sum_coins_through_era  # noqa: E402


def test_era_total_coins_matches_gd():
    assert ERA_TOTAL_COINS == [3, 4, 4, 5]


def test_sum_era_zero():
    assert sum_coins_through_era(0) == 3


def test_sum_era_three():
    assert sum_coins_through_era(3) == 16


def test_invalid_index_raises():
    with pytest.raises(IndexError):
        sum_coins_through_era(4)
    with pytest.raises(IndexError):
        sum_coins_through_era(-1)
