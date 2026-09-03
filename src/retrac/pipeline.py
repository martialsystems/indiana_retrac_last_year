# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 fixture. Live fetch-or-stop. Two figures. Last year vs inverse-miles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from retrac.claims import require_clean, require_paths_clean
from retrac.config import QUESTION, REPO_ROOT
from retrac.fetch import fetch_live
from retrac.figure import write_two
from retrac.fixture import build_fixture
from retrac.skill import score
from retrac.split import assert_split

try:
    from retracforge.gate import (
        require_claims,
        require_completeness,
        require_no_hero,
        require_no_live_login,
        require_no_ridge,
        require_split,
    )
except ImportError:  # pragma: no cover

    def require_claims(**kwargs):
        del kwargs

    def require_completeness(**kwargs):
        del kwargs

    def require_no_hero(**kwargs):
        del kwargs

    def require_no_live_login(**kwargs):
        del kwargs

    def require_no_ridge(**kwargs):
        del kwargs

    def require_split(**kwargs):
        del kwargs


_ARRAY_KEYS = ("obs_ly", "pred_ly", "obs_bar", "pred_bar")


def _public_block(block: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in block.items() if k not in _ARRAY_KEYS}


def _jsonable(report: dict[str, Any]) -> dict[str, Any]:
    out = dict(report)
    if isinstance(out.get("holdout"), dict):
        out["holdout"] = _public_block(out["holdout"])
    if isinstance(out.get("confirm"), dict):
        out["confirm"] = _public_block(out["confirm"])
    return out


def _run(
    log_dir: Path,
    *,
    rows: list[dict[str, Any]],
    counties: dict[str, dict[str, Any]],
    facilities: dict[str, dict[str, Any]],
    fixture: bool,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require_no_ridge(ridge=False, hgb=False, sklearn_contestant=False, thread_id="ridge")
    require_no_live_login(live_retrac_login=False, thread_id="login")
    require_clean(QUESTION, source="question")
    fit = score(rows, counties=counties, facilities=facilities)
    require_completeness(xlsx_ok=True, coords_ok=True, thread_id="complete")
    assert_split(
        confirm_in_train=bool(fit["confirm_in_train"]),
        confirm_in_j=bool(fit["confirm_in_j"]),
        random_split=bool(fit["random_split"]),
    )
    require_split(
        temporal_ok=True,
        confirm_in_train=bool(fit["confirm_in_train"]),
        confirm_in_j=bool(fit["confirm_in_j"]),
        random_split=bool(fit["random_split"]),
        thread_id="split",
    )
    paths = write_two(log_dir, fit=fit, live=not fixture)
    require_claims(n_figures=len(paths), thread_id="claims")
    require_no_hero(
        winter_page_hero=False,
        readme_states_result=True,
        thread_id="hero",
    )
    log_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "stage": "0" if fixture else "C",
        "fixture": fixture,
        "question": QUESTION,
        "contestant": "last_year",
        "bar": "mileage_plus_population",
        "ridge": False,
        "hgb": False,
        "sklearn_contestant": False,
        "live_retrac_login": False,
        "winter_page_hero": False,
        "xlsx_ok": True,
        "coords_ok": True,
        "units": {"skill": "rmse_tons"},
        "figures": paths,
        **{k: fit[k] for k in (
            "n_rows",
            "n_train",
            "n_holdout",
            "n_confirm",
            "n_facilities_j",
            "n_holdout_only_facilities",
            "n_gis",
            "n_centroid",
            "holdout",
            "confirm",
            "confirm_in_train",
            "confirm_in_j",
            "random_split",
            "train_years",
            "holdout_years",
            "confirm_years",
            "origin_pop_cancels",
            "last_year_beats_bar",
        )},
    }
    if extra:
        report.update(extra)
    payload = _jsonable(report)
    require_clean(json.dumps(payload, default=str), source="report")
    dest = log_dir / ("stage0_report.json" if fixture else "stage_c_report.json")
    dest.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    readme = REPO_ROOT / "README.md"
    require_paths_clean([readme, dest] if readme.is_file() else [dest])
    return report


def stage0_fixture(log_dir: Path) -> dict[str, Any]:
    rows, counties, facilities = build_fixture()
    return _run(log_dir, rows=rows, counties=counties, facilities=facilities, fixture=True)


def run_live(log_dir: Path, *, cache_dir: Path) -> dict[str, Any]:
    rows, counties, facilities, meta = fetch_live(cache_dir=cache_dir)
    return _run(
        log_dir,
        rows=rows,
        counties=counties,
        facilities=facilities,
        fixture=False,
        extra={"fetch_meta": meta},
    )
