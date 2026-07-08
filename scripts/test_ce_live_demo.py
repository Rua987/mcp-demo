"""Tests for ce_live_demo (offline)."""
import json
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _ROOT / "scripts" / "ce_live_demo.py"


def test_parse_json_stdout_with_prefix():
    import ce_live_demo as demo

    raw = 'PID 3392: ok\n{\n  "ok": true,\n  "era_before": 1\n}\n'
    parsed = demo._parse_json_stdout(raw)
    assert parsed == {"ok": True, "era_before": 1}


def test_ce_pipe_ready_treats_busy_pipe_as_ready(monkeypatch):
    import ce_live_demo as demo

    def busy_exists(self):
        err = OSError("all pipe instances busy")
        err.winerror = 231
        raise err

    monkeypatch.setattr(demo.Path, "exists", busy_exists)
    assert demo._ce_pipe_ready() is True


def test_help_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        cwd=str(_ROOT),
    )
    assert proc.returncode == 0
    assert "skip-write" in proc.stdout


def test_skip_write_writes_receipt(tmp_path):
    out = tmp_path / "receipt.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--skip-write",
            "--skip-pytest",
            "--out",
            str(out),
        ],
        capture_output=True,
        text=True,
        cwd=str(_ROOT),
    )
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "steps" in data
    assert any(s["name"] == "ce_workflow" for s in data["steps"])
    assert not any(s["name"] == "ce_write_live" for s in data["steps"])
