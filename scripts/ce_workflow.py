#!/usr/bin/env python3
"""End-to-end CE sanity check for mcp-demo (Godot anchors + Python chain).

Run before a Cheat Engine session to confirm game.gd anchors and the Python
mirror modules agree. Exit 0 = safe to attach CE and use ce_cli for snapshots.

Usage:
    python scripts/ce_workflow.py
    python scripts/ce_workflow.py --coins 5 --deaths 2 --era 1
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_ROOT = _SCRIPTS.parent


def _run(cmd: list[str]) -> bool:
    proc = subprocess.run(cmd, cwd=str(_ROOT))
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="CE pre-flight for mcp-demo.")
    parser.add_argument("--coins", type=int, default=3)
    parser.add_argument("--deaths", type=int, default=0)
    parser.add_argument("--era", type=int, default=0)
    parser.add_argument("--skip-pytest", action="store_true")
    args = parser.parse_args()

    print("== CE workflow ==")

    if not _run([sys.executable, str(_SCRIPTS / "verify_ce_anchors.py")]):
        print("FAIL: verify_ce_anchors.py")
        return 1
    print("OK   Godot anchor files")

    if not args.skip_pytest:
        if not _run([sys.executable, "-m", "pytest", "scripts/", "-q", "--tb=line"]):
            print("FAIL: pytest scripts/")
            return 1
        print("OK   pytest scripts/")

    snap = subprocess.run(
        [
            sys.executable,
            str(_SCRIPTS / "ce_cli.py"),
            "--coins",
            str(args.coins),
            "--deaths",
            str(args.deaths),
            "--era",
            str(args.era),
        ],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
    )
    if snap.returncode != 0:
        print("FAIL: ce_cli.py", snap.stderr.strip())
        return 1
    print("OK   snapshot:", snap.stdout.strip())
    print("== CE workflow PASS ==")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
