from ce_report import build_report


def test_build_report_contains_coins_and_anchor():
    report = build_report(3, 1)
    assert "coins=3" in report
    assert "0xCE0DE003" in report
