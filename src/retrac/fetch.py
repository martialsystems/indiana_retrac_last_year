# Copyright (c) 2026 Martial Systems LLC
"""Live IDEM XLSX + GIS. Empty Indiana rows or unmatched origin county stops."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from retrac.config import REPO_ROOT
from retrac.counties import load_counties
from retrac.errors import FetchError
from retrac.facilities import load_gis, locate_all
from retrac.xlsx import parse_received


def fetch_live(
    *, cache_dir: Path
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    xlsx = cache_dir / "reporting_sw_quarterly_report_2025.xlsx"
    gis_path = cache_dir / "facilities.geojson"
    cty_path = cache_dir / "indiana_counties.json"
    if not xlsx.is_file():
        xlsx = REPO_ROOT / "data" / "raw" / "reporting_sw_quarterly_report_2025.xlsx"
    if not gis_path.is_file():
        gis_path = REPO_ROOT / "data" / "raw" / "facilities.geojson"
    if not cty_path.is_file():
        cty_path = REPO_ROOT / "data" / "raw" / "indiana_counties.json"
    if not xlsx.is_file() or xlsx.stat().st_size == 0:
        raise FetchError("empty IDEM quarterly XLSX")
    counties = load_counties(cty_path)
    rows, stats = parse_received(xlsx, counties=counties)
    gis = load_gis(gis_path)
    facilities = locate_all(rows, gis=gis, counties=counties)
    digest = hashlib.sha256(xlsx.read_bytes()).hexdigest()
    meta = {
        "n_rows": len(rows),
        "n_counties": len({r["origin_key"] for r in rows}),
        "n_facilities": len(facilities),
        "xlsx": str(xlsx),
        "xlsx_sha256": digest,
        "live_retrac_login": False,
        **stats,
    }
    return rows, counties, facilities, meta
