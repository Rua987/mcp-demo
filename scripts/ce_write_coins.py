#!/usr/bin/env python3
"""Launcher CE coins write (calls linus_nanochat recipe). ~60-90s."""
import subprocess
import sys

_SCRIPT = (
    r"C:\Users\admin\.claude-worktrees\templates\hopeful-banach"
    r"\linus_nanochat\scripts\ce_godot_coins_write.py"
)
TARGET = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "3"
raise SystemExit(subprocess.call([sys.executable, _SCRIPT, "--target", TARGET]))
