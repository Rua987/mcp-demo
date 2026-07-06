#!/usr/bin/env python3
"""verify_ce_anchors.py
Verifie que scripts/game.gd declare les ancres CE attendues et que
scripts/era_data.gd contient bien les total_coins 3/4/4/5.
Exit 0 si tout est coherent, 1 sinon.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME_GD = ROOT / "scripts" / "game.gd"
ERA_GD = ROOT / "scripts" / "era_data.gd"

EXPECTED_COINS_ANCHOR = 0xCE0DE000
EXPECTED_DEATHS_ANCHOR = 0xCE0DE100
EXPECTED_TOTAL_COINS = [3, 4, 4, 5]


def check_anchors() -> bool:
    ok = True
    src = GAME_GD.read_text(encoding="utf-8", errors="replace")

    m_coins = re.search(r"CE_SCAN_COINS\s*:?="
                        r"\s*(?:int\()?(0x[0-9A-Fa-f]+)", src)
    m_deaths = re.search(r"CE_SCAN_DEATHS\s*:?="
                         r"\s*(?:int\()?(0x[0-9A-Fa-f]+)", src)

    if not m_coins:
        print("FAIL: CE_SCAN_COINS non trouve dans game.gd")
        ok = False
    else:
        val = int(m_coins.group(1), 16)
        if val == EXPECTED_COINS_ANCHOR:
            print("OK   CE_SCAN_COINS = 0x{:08X}".format(val))
        else:
            print("FAIL CE_SCAN_COINS = 0x{:08X} (attendu 0x{:08X})"
                  .format(val, EXPECTED_COINS_ANCHOR))
            ok = False

    if not m_deaths:
        print("FAIL: CE_SCAN_DEATHS non trouve dans game.gd")
        ok = False
    else:
        val = int(m_deaths.group(1), 16)
        if val == EXPECTED_DEATHS_ANCHOR:
            print("OK   CE_SCAN_DEATHS = 0x{:08X}".format(val))
        else:
            print("FAIL CE_SCAN_DEATHS = 0x{:08X} (attendu 0x{:08X})"
                  .format(val, EXPECTED_DEATHS_ANCHOR))
            ok = False

    # Verification de la formule de conversion (ce_scan - base)
    if "ce_scan_coins - CE_SCAN_COINS" in src:
        print("OK   formule coins = ce_scan_coins - CE_SCAN_COINS presente")
    else:
        print("FAIL: formule coins = ce_scan_coins - CE_SCAN_COINS absente")
        ok = False
    if "ce_scan_deaths - CE_SCAN_DEATHS" in src:
        print("OK   formule deaths = ce_scan_deaths - CE_SCAN_DEATHS presente")
    else:
        print("FAIL: formule deaths = ce_scan_deaths - CE_SCAN_DEATHS absente")
        ok = False

    return ok


def check_eras() -> bool:
    src = ERA_GD.read_text(encoding="utf-8", errors="replace")
    totals = [int(x) for x in re.findall(r'"total_coins"\s*:\s*(\d+)', src)]
    if totals == EXPECTED_TOTAL_COINS:
        print("OK   total_coins par ere = {}".format(totals))
        return True
    print("FAIL total_coins = {} (attendu {})".format(totals, EXPECTED_TOTAL_COINS))
    return False


def main() -> int:
    print("--- verify_ce_anchors ---")
    print("game.gd      : {}".format(GAME_GD))
    print("era_data.gd  : {}".format(ERA_GD))
    if not GAME_GD.exists():
        print("FAIL: game.gd introuvable")
        return 1
    if not ERA_GD.exists():
        print("FAIL: era_data.gd introuvable")
        return 1
    ok = check_anchors() and check_eras()
    print("Resultat : {}".format("SUCCES" if ok else "ECHEC"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
