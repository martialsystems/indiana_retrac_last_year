# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from retrac.config import QUESTION
from retrac.errors import FigureCapError
from retrac.figure import _cap
from retrac.pipeline import stage0_fixture


def test_fixture_two_figures(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["figures"] == ["scatter.png", "rmse_bars.png"]
    assert (tmp_path / "scatter.png").is_file()
    assert (tmp_path / "rmse_bars.png").is_file()
    assert report["contestant"] == "last_year"
    assert report["ridge"] is False
    assert report["live_retrac_login"] is False
    assert report["winter_page_hero"] is False
    assert report["confirm_in_train"] is False
    assert report["confirm_in_j"] is False
    assert report["origin_pop_cancels"] is True
    assert report["last_year_beats_bar"] is True
    hold = report["holdout"]
    assert hold["last_year"]["rmse_tons"] < hold["bar"]["rmse_tons"]
    assert hold["origin_total"]["bar_rmse"] == 0.0
    assert hold["n_last_year"] == hold["n_cells"]
    assert (tmp_path / "stage0_report.json").is_file()


def test_live_holdout_split() -> None:
    import json

    path = Path(__file__).resolve().parents[1] / "logs" / "in_live" / "stage_c_report.json"
    live = json.loads(path.read_text(encoding="utf-8"))
    assert live["contestant"] == "last_year"
    assert live["live_retrac_login"] is False
    assert live["ridge"] is False
    assert live["confirm_in_j"] is False
    assert live["confirm_in_train"] is False
    assert live["origin_pop_cancels"] is True
    assert live["holdout_years"] == [2024]
    assert live["confirm_years"] == [2025]
    assert live["n_holdout"] > 0
    assert live["n_confirm"] > 0
    hold = live["holdout"]
    assert hold["n_last_year"] > 0
    assert hold["origin_total"]["bar_rmse"] == 0.0
    assert "rmse_tons" in hold["last_year"]
    assert "rmse_tons" in hold["bar"]
    assert live["last_year_beats_bar"] == (hold["last_year"]["rmse_tons"] < hold["bar"]["rmse_tons"])
    assert live["figures"] == ["scatter.png", "rmse_bars.png"]
    assert live["fetch_meta"]["n_counties"] == 92


def test_third_figure_refused() -> None:
    try:
        _cap(3)
        raise AssertionError("cap allowed 3")
    except FigureCapError:
        pass
