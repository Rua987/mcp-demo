from ce_progress import expected_coins_for_era, coins_match_era


def test_expected_coins_for_era_3():
    assert expected_coins_for_era(3) == 16


def test_coins_match_era_16_3():
    assert coins_match_era(16, 3) is True


def test_coins_match_era_3_0():
    assert coins_match_era(3, 0) is True
