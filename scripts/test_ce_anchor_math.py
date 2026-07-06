"""Tests for ce_anchor_math.py — mirrors game.gd CE anchor encode/decode."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ce_anchor_math import (  # noqa: E402
    CE_SCAN_COINS,
    CE_SCAN_DEATHS,
    decode_counter,
    encode_anchor,
)


def test_constants_match_game_gd():
    assert CE_SCAN_COINS == 0xCE0DE000
    assert CE_SCAN_DEATHS == 0xCE0DE100


def test_round_trip_coins_zero():
    anchor = encode_anchor(CE_SCAN_COINS, 0)
    assert decode_counter(CE_SCAN_COINS, anchor) == 0
    assert anchor == CE_SCAN_COINS


def test_round_trip_coins_ninety_nine():
    anchor = encode_anchor(CE_SCAN_COINS, 99)
    assert decode_counter(CE_SCAN_COINS, anchor) == 99


def test_round_trip_deaths_zero():
    anchor = encode_anchor(CE_SCAN_DEATHS, 0)
    assert decode_counter(CE_SCAN_DEATHS, anchor) == 0


def test_round_trip_deaths_ninety_nine():
    anchor = encode_anchor(CE_SCAN_DEATHS, 99)
    assert decode_counter(CE_SCAN_DEATHS, anchor) == 99
