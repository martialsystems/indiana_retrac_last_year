# Copyright (c) 2026 Martial Systems LLC
"""RMSE tons. Last year vs mileage-plus-population. Origin pop cancels per county."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np

from retrac.config import MILE_EPS
from retrac.geo import miles
from retrac.split import CONFIRM, HOLDOUT, TRAIN, role


def _rmse(err: np.ndarray) -> float:
    if err.size == 0:
        return float("nan")
    return float(np.sqrt(np.mean(np.square(err))))


def _mae(err: np.ndarray) -> float:
    if err.size == 0:
        return float("nan")
    return float(np.mean(np.abs(err)))


def _finite(x: float) -> bool:
    return bool(np.isfinite(x))


def score(
    rows: list[dict[str, Any]],
    *,
    counties: dict[str, dict[str, Any]],
    facilities: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    train = [r for r in rows if role(r["year"]) == TRAIN]
    hold = [r for r in rows if role(r["year"]) == HOLDOUT]
    confirm = [r for r in rows if role(r["year"]) == CONFIRM]
    j = {r["facility_id"] for r in train}
    confirm_in_train = any(role(r["year"]) == CONFIRM for r in train)
    # J is train-only. Confirmation facilities may overlap J; they do not set J.
    confirm_in_j = confirm_in_train

    weights: dict[tuple[str, str], float] = {}
    for ok, oc in counties.items():
        for fid, fac in facilities.items():
            if fid not in j:
                continue
            d = miles(oc["lat"], oc["lon"], fac["lat"], fac["lon"])
            weights[(ok, fid)] = float(oc["pop_2020"]) / (d + MILE_EPS)
    denom: dict[str, float] = defaultdict(float)
    for (ok, _fid), w in weights.items():
        denom[ok] += w

    shares_pop: dict[tuple[str, str], float] = {}
    shares_miles: dict[tuple[str, str], float] = {}
    for (ok, fid), w in weights.items():
        den = denom[ok]
        shares_pop[(ok, fid)] = (w / den) if den else 0.0
    miles_w: dict[tuple[str, str], float] = {}
    miles_den: dict[str, float] = defaultdict(float)
    for ok, oc in counties.items():
        for fid, fac in facilities.items():
            if fid not in j:
                continue
            d = miles(oc["lat"], oc["lon"], fac["lat"], fac["lon"])
            miles_w[(ok, fid)] = 1.0 / (d + MILE_EPS)
            miles_den[ok] += miles_w[(ok, fid)]
    for (ok, fid), w in miles_w.items():
        den = miles_den[ok]
        shares_miles[(ok, fid)] = (w / den) if den else 0.0
    origin_pop_cancels = True
    for key, share in shares_pop.items():
        if abs(share - shares_miles[key]) > 1e-12:
            origin_pop_cancels = False
            break

    by_cell: dict[tuple[str, str, int, int], float] = {}
    origin_tot: dict[tuple[str, int, int], float] = defaultdict(float)
    for r in rows:
        by_cell[(r["origin_key"], r["facility_id"], r["year"], r["quarter"])] = r["tons"]
        origin_tot[(r["origin_key"], r["year"], r["quarter"])] += r["tons"]

    def _block(subset: list[dict[str, Any]]) -> dict[str, Any]:
        obs_ly: list[float] = []
        pred_ly: list[float] = []
        obs_bar_ix: list[float] = []
        pred_bar_ix: list[float] = []
        obs_bar: list[float] = []
        pred_bar: list[float] = []
        origin_obs: list[float] = []
        origin_ly: list[float] = []
        by_county: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: {"ly": [], "bar": [], "bar_all": []}
        )
        n_skip_ly = 0
        for r in subset:
            obs = float(r["tons"])
            prev = by_cell.get((r["origin_key"], r["facility_id"], r["year"] - 1, r["quarter"]))
            t_iq = origin_tot[(r["origin_key"], r["year"], r["quarter"])]
            w = weights.get((r["origin_key"], r["facility_id"]), 0.0)
            den = denom.get(r["origin_key"]) or 0.0
            bar = (t_iq * w / den) if den else 0.0
            obs_bar.append(obs)
            pred_bar.append(bar)
            by_county[r["origin_key"]]["bar_all"].append(obs - bar)
            if prev is None:
                n_skip_ly += 1
                continue
            obs_ly.append(obs)
            pred_ly.append(float(prev))
            obs_bar_ix.append(obs)
            pred_bar_ix.append(bar)
            by_county[r["origin_key"]]["ly"].append(obs - float(prev))
            by_county[r["origin_key"]]["bar"].append(obs - bar)

        seen_oq: set[tuple[str, int, int]] = set()
        for r in subset:
            key = (r["origin_key"], r["year"], r["quarter"])
            if key in seen_oq:
                continue
            seen_oq.add(key)
            tot = origin_tot[key]
            prev_tot = origin_tot.get((r["origin_key"], r["year"] - 1, r["quarter"]))
            origin_obs.append(tot)
            origin_ly.append(float(prev_tot) if prev_tot is not None else float("nan"))

        ly_err = np.array(obs_ly, dtype=float) - np.array(pred_ly, dtype=float) if obs_ly else np.array([])
        bar_ix_err = (
            np.array(obs_bar_ix, dtype=float) - np.array(pred_bar_ix, dtype=float) if obs_bar_ix else np.array([])
        )
        bar_err = np.array(obs_bar, dtype=float) - np.array(pred_bar, dtype=float) if obs_bar else np.array([])
        o_obs = np.array(origin_obs, dtype=float)
        o_ly = np.array(origin_ly, dtype=float)
        mask = np.isfinite(o_ly) if o_ly.size else np.array([], dtype=bool)
        county_rows = []
        for ok, rec in counties.items():
            ly = np.array(by_county[ok]["ly"], dtype=float) if by_county[ok]["ly"] else np.array([])
            br = np.array(by_county[ok]["bar"], dtype=float) if by_county[ok]["bar"] else np.array([])
            br_all = np.array(by_county[ok]["bar_all"], dtype=float) if by_county[ok]["bar_all"] else np.array([])
            if ly.size == 0 and br_all.size == 0:
                continue
            county_rows.append(
                {
                    "origin": rec["name"],
                    "last_year_rmse": _rmse(ly) if ly.size else None,
                    "bar_rmse": _rmse(br) if br.size else None,
                    "bar_all_rmse": _rmse(br_all) if br_all.size else None,
                    "n_ly": int(ly.size),
                    "n_bar": int(br.size),
                    "n_bar_all": int(br_all.size),
                    "holdout_tons": float(sum(r["tons"] for r in subset if r["origin_key"] == ok)),
                }
            )
        county_rows.sort(key=lambda r: -r["holdout_tons"])
        ly_rmse = _rmse(ly_err)
        bar_ix_rmse = _rmse(bar_ix_err)
        bar_all_rmse = _rmse(bar_err)
        return {
            "n_cells": len(subset),
            "n_last_year": int(ly_err.size),
            "n_skip_last_year": n_skip_ly,
            "last_year": {"rmse_tons": ly_rmse, "mae_tons": _mae(ly_err)},
            "bar": {"rmse_tons": bar_ix_rmse, "mae_tons": _mae(bar_ix_err)},
            "bar_all": {"rmse_tons": bar_all_rmse, "mae_tons": _mae(bar_err), "n": int(bar_err.size)},
            "origin_total": {
                "last_year_rmse": _rmse(o_obs[mask] - o_ly[mask]) if mask.size and mask.any() else None,
                "bar_rmse": 0.0,
                "n": int(mask.sum()) if mask.size else 0,
            },
            "last_year_beats_bar": bool(_finite(ly_rmse) and _finite(bar_ix_rmse) and ly_rmse < bar_ix_rmse),
            "by_county": county_rows,
            "obs_ly": obs_ly,
            "pred_ly": pred_ly,
            "obs_bar": obs_bar_ix,
            "pred_bar": pred_bar_ix,
        }

    hold_s = _block(hold)
    conf_s = _block(confirm)
    hold_ids = {r["facility_id"] for r in hold}
    return {
        "n_rows": len(rows),
        "n_train": len(train),
        "n_holdout": len(hold),
        "n_confirm": len(confirm),
        "n_facilities_j": len(j),
        "n_holdout_only_facilities": len(hold_ids - j),
        "n_gis": sum(1 for f in facilities.values() if f.get("how") == "gis"),
        "n_centroid": sum(1 for f in facilities.values() if f.get("how") == "county_centroid"),
        "holdout": hold_s,
        "confirm": conf_s,
        "confirm_in_train": confirm_in_train,
        "confirm_in_j": confirm_in_j,
        "random_split": False,
        "train_years": [2021, 2022, 2023],
        "holdout_years": [2024],
        "confirm_years": [2025],
        "origin_pop_cancels": origin_pop_cancels,
        "last_year_beats_bar": hold_s["last_year_beats_bar"],
    }
