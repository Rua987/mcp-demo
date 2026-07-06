"""Tests for verify_ce_anchors.py against real game.gd / era_data.gd."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_ce_anchors as v  # noqa: E402


def test_expected_anchor_constants():
    assert v.EXPECTED_COINS_ANCHOR == 0xCE0DE000
    assert v.EXPECTED_DEATHS_ANCHOR == 0xCE0DE100


def test_expected_total_coins():
    assert v.EXPECTED_TOTAL_COINS == [3, 4, 4, 5]


def test_check_anchors_on_real_game_gd():
    assert v.GAME_GD.is_file()
    assert v.check_anchors() is True


def test_check_eras_on_real_era_data_gd():
    assert v.ERA_GD.is_file()
    assert v.check_eras() is True
