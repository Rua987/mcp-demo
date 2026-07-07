import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_ce_anchors import (
    EXPECTED_COINS_ANCHOR,
    check_anchors,
    check_eras,
)


def test_expected_coins_anchor():
    assert EXPECTED_COINS_ANCHOR == 0xCE0DE000


def test_check_anchors():
    assert check_anchors() is True


def test_check_eras():
    assert check_eras() is True
