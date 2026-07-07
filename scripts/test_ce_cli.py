import subprocess
import sys
from pathlib import Path


def test_cli_snapshot():
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "ce_cli.py"),
         "--coins", "3", "--deaths", "1", "--era", "0"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "coins=3" in result.stdout
    assert "match=True" in result.stdout
