import subprocess
import sys
from pathlib import Path


def test_ce_workflow_runs():
    root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / "ce_workflow.py"), "--skip-pytest"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "CE workflow PASS" in result.stdout
    assert "coins=3" in result.stdout
