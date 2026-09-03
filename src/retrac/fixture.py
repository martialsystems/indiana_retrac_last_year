# Copyright (c) 2026 Martial Systems LLC
"""Synthetic counties with planted last-year persistence. Does not rescue live."""

from __future__ import annotations

from typing import Any

import numpy as np


def build_fixture() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    rng = np.random.default_rng(3)
    counties = {
        "alpha": {"name": "Alpha", "lat": 41.0, "lon": -86.0, "pop_2020": 10000, "fips": "18001", "key": "alpha"},
        "beta": {"name": "Beta", "lat": 40.0, "lon": -86.2, "pop_2020": 20000, "fips": "18003", "key": "beta"},
        "gamma": {"name": "Gamma", "lat": 39.0, "lon": -87.0, "pop_2020": 5000, "fips": "18005", "key": "gamma"},
    }
    facilities = {
        "01-01": {"lat": 41.05, "lon": -86.05, "how": "gis", "name": "North Fill"},
        "02-01": {"lat": 39.05, "lon": -87.05, "how": "gis", "name": "South Fill"},
    }
    rows = []
    for ok, oc in counties.items():
        base = 80.0 if ok == "alpha" else 40.0 if ok == "beta" else 20.0
        near = "01-01" if oc["lat"] > 40 else "02-01"
        far = "02-01" if near == "01-01" else "01-01"
        for year in (2021, 2022, 2023, 2024, 2025):
            for q in (1, 2, 3, 4):
                noise = float(rng.normal(0, 2))
                t_near = max(0.0, 0.8 * base + noise)
                t_far = max(0.0, 0.2 * base - 0.3 * noise)
                rows.append(
                    {
                        "origin_key": ok,
                        "origin_name": oc["name"],
                        "facility_id": near,
                        "facility_name": facilities[near]["name"],
                        "year": year,
                        "quarter": q,
                        "tons": t_near,
                    }
                )
                rows.append(
                    {
                        "origin_key": ok,
                        "origin_name": oc["name"],
                        "facility_id": far,
                        "facility_name": facilities[far]["name"],
                        "year": year,
                        "quarter": q,
                        "tons": t_far,
                    }
                )
    return rows, counties, facilities
