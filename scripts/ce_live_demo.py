#!/usr/bin/env python3
"""Reproducible CE × Godot live demo with JSON receipts (T3MP3ST-style).

Prerequisites (human):
  - Godot editor open on mcp-demo, MCP plugin connected (Agents green)
  - Main.tscn in play (F5) OR let --prepare launch it via CE write script

Steps:
  1. ce_workflow (anchors + pytest + ce_cli snapshot)
  2. MCP runtime probe (coins, era, ce_scan_coins)
  3. CE write (--skip-prepare --no-reset) without resetting era

Usage:
    python scripts/ce_live_demo.py
    python scripts/ce_live_demo.py --write-target 2 --skip-pytest
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = _ROOT / "scripts"
_REPORTS = _ROOT / "reports"
_LINUS_WRITE = Path(
    r"C:\Users\admin\.claude-worktrees\templates\hopeful-banach"
    r"\linus_nanochat\scripts\ce_godot_coins_write.py"
)
_CE_PIPE = r"\\.\pipe\CE_MCP_Bridge_v99"
_GODOT_EXE = "Godot_v4.6.1-stable_win64"


def _ce_pipe_ready() -> bool:
    """Pipe CE present (exists may raise WinError 231 when all instances busy)."""
    try:
        return Path(_CE_PIPE).exists()
    except OSError as exc:
        if getattr(exc, "winerror", None) == 231:
            return True
        return False


def _step(name: str, ok: bool, detail: dict | None = None) -> dict:
    return {
        "name": name,
        "ok": ok,
        "ts": datetime.now(timezone.utc).isoformat(),
        **(detail or {}),
    }


def _parse_json_stdout(stdout: str) -> dict | None:
    text = stdout.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.rfind("{")
    if start >= 0:
        try:
            return json.loads(text[start:])
        except json.JSONDecodeError:
            return None
    return None


def _run(cmd: list[str], *, cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or _ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def _godot_running() -> bool:
    try:
        import psutil  # optional
    except ImportError:
        out = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"if (Get-Process -Name '{_GODOT_EXE}' -EA SilentlyContinue) {{ exit 0 }} else {{ exit 1 }}",
            ],
            capture_output=True,
        )
        return out.returncode == 0
    for p in psutil.process_iter(["name"]):
        if (p.info.get("name") or "").startswith("Godot"):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="CE × Godot live demo with JSON receipt.")
    ap.add_argument("--write-target", type=int, default=2)
    ap.add_argument("--skip-pytest", action="store_true", help="Faster demo (~2s vs ~1s pytest).")
    ap.add_argument("--skip-write", action="store_true", help="Probe only, no CE memory write.")
    ap.add_argument(
        "--out",
        default=str(_REPORTS / "ce_live_demo.json"),
        help="JSON receipt path.",
    )
    args = ap.parse_args()

    receipt: dict = {
        "generated_by": "scripts/ce_live_demo.py",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "steps": [],
    }
    all_ok = True

    pipe_ok = _ce_pipe_ready()
    receipt["steps"].append(_step("ce_pipe", pipe_ok, {"pipe": _CE_PIPE}))
    all_ok &= pipe_ok

    godot_ok = _godot_running()
    receipt["steps"].append(_step("godot_process", godot_ok))
    all_ok &= godot_ok

    wf_cmd = [sys.executable, str(_SCRIPTS / "ce_workflow.py")]
    if args.skip_pytest:
        wf_cmd.append("--skip-pytest")
    t0 = time.time()
    code, stdout, stderr = _run(wf_cmd)
    wf_ok = code == 0
    receipt["steps"].append(
        _step(
            "ce_workflow",
            wf_ok,
            {"elapsed_s": round(time.time() - t0, 2), "stdout_tail": stdout.strip()[-500:]},
        )
    )
    all_ok &= wf_ok

    if not _LINUS_WRITE.is_file():
        receipt["steps"].append(_step("linus_write_script", False, {"path": str(_LINUS_WRITE)}))
        all_ok = False
    elif not args.skip_write and pipe_ok:
        write_cmd = [
            sys.executable,
            str(_LINUS_WRITE),
            "--target",
            str(args.write_target),
            "--skip-prepare",
            "--no-reset",
        ]
        t0 = time.time()
        code, stdout, stderr = _run(write_cmd)
        write_detail: dict = {"elapsed_s": round(time.time() - t0, 2)}
        parsed = _parse_json_stdout(stdout)
        if parsed is not None:
            write_detail["result"] = parsed
            write_ok = bool(parsed.get("ok"))
        else:
            write_ok = code == 0
            write_detail["raw_stdout"] = stdout.strip()[-800:]
            write_detail["stderr"] = stderr.strip()[-400:]
        receipt["steps"].append(_step("ce_write_live", write_ok, write_detail))
        all_ok &= write_ok

    receipt["ok"] = all_ok
    receipt["finished_at"] = datetime.now(timezone.utc).isoformat()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"== CE live demo: {'PASS' if all_ok else 'FAIL'} ==")
    for s in receipt["steps"]:
        mark = "OK" if s["ok"] else "FAIL"
        print(f"  [{mark}] {s['name']}")
    print(f"receipt: {out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
