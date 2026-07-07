import pytest
from ce_snapshot import build_snapshot


def test_build_snapshot_era_3():
    result = build_snapshot(16, 1, 3)
    assert "coins=16" in result
    assert "match=True" in result
    assert "expected=16" in result


def test_build_snapshot_era_0():
    result = build_snapshot(3, 0, 0)
    assert "coins=3" in result
    assert "match=True" in result
    assert "expected=3" in result
