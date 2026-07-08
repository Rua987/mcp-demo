#!/usr/bin/env python3
"""Launcher CE coins write (calls linus_nanochat recipe). ~60-90s."""
import subprocess
import sys

_SCRIPT = (
    r"C:\Users\admin\.claude-worktrees\templates\hopeful-banach"
    r"\linus_nanochat\scripts\ce_godot_coins_write.py"
)
TARGET = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "3"
extra = [a for a in sys.argv[1:] if a not in ("--target", TARGET)]
cmd = [sys.executable, _SCRIPT, "--target", TARGET, *extra]
raise SystemExit(subprocess.call(cmd))
