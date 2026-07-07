"""Real-alignment: ce_cli snapshots vs era_data.gd totals on disk."""
import subprocess
import sys
from pathlib import Path

from era_totals import ERA_TOTAL_COINS, sum_coins_through_era

_ROOT = Path(__file__).resolve().parent.parent
_CLI = Path(__file__).resolve().parent / "ce_cli.py"

# Same totals as scripts/era_data.gd (verified by verify_ce_anchors.py).
_ERA_EXPECTED = [sum_coins_through_era(i) for i in range(len(ERA_TOTAL_COINS))]


def test_era_totals_match_gd_constants():
    assert ERA_TOTAL_COINS == [3, 4, 4, 5]
    assert _ERA_EXPECTED == [3, 7, 11, 16]


def test_cli_match_true_at_each_era_ceiling():
    for era, coins in enumerate(_ERA_EXPECTED):
        result = subprocess.run(
            [
                sys.executable,
                str(_CLI),
                "--coins",
                str(coins),
                "--deaths",
                "0",
                "--era",
                str(era),
            ],
            cwd=str(_ROOT),
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "match=True" in result.stdout
        assert f"expected={coins}" in result.stdout


def test_cli_match_false_when_coins_off():
    result = subprocess.run(
        [sys.executable, str(_CLI), "--coins", "99", "--deaths", "0", "--era", "0"],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "match=False" in result.stdout
