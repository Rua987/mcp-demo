"""CE anchor math mirroring game.gd CE scan anchors.

Anchors are a base scan address plus a counter. Encoding produces the
combined anchor; decoding recovers the counter by subtracting the base.
"""

# Mirrors scripts/game.gd
CE_SCAN_COINS: int = 0xCE0DE000
CE_SCAN_DEATHS: int = 0xCE0DE100


def encode_anchor(base: int, counter: int) -> int:
    """Return the anchor value for a base and counter (base + counter)."""
    return base + counter


def decode_counter(base: int, anchor: int) -> int:
    """Return the counter encoded in an anchor (anchor - base)."""
    return anchor - base
