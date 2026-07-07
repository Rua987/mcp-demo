from ce_status import format_status


def test_format_status_with_values():
    result = format_status(3, 1)
    assert "coins=3" in result


def test_format_status_zero():
    result = format_status(0, 0)
    assert result == "coins=0 deaths=0"
