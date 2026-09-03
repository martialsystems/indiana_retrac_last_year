# Copyright (c) 2026 Martial Systems LLC

from retrac.fixture import build_fixture
from retrac.skill import score


def test_origin_pop_cancels_and_fixture_beats() -> None:
    rows, counties, facilities = build_fixture()
    fit = score(rows, counties=counties, facilities=facilities)
    assert fit["origin_pop_cancels"] is True
    assert fit["last_year_beats_bar"] is True
    assert fit["holdout"]["origin_total"]["bar_rmse"] == 0.0
    doubled = {k: {**v, "pop_2020": v["pop_2020"] * 10} for k, v in counties.items()}
    fit2 = score(rows, counties=doubled, facilities=facilities)
    assert abs(fit["holdout"]["bar"]["rmse_tons"] - fit2["holdout"]["bar"]["rmse_tons"]) < 1e-9
