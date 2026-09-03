# Copyright (c) 2026 Martial Systems LLC

from retrac.geo import miles


def test_miles_zero_and_known() -> None:
    assert miles(40.0, -86.0, 40.0, -86.0) == 0.0
    d = miles(39.7683, -86.1581, 41.6764, -86.2500)
    assert 120 < d < 140
