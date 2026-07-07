from ce_status import format_status
from ce_anchor_math import encode_anchor, CE_SCAN_COINS


def build_report(coins: int, deaths: int) -> str:
    return format_status(coins, deaths) + " " + f"0x{encode_anchor(CE_SCAN_COINS, coins):X}"
