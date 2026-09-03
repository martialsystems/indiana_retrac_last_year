# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

import pytest

from retrac.errors import FetchError
from retrac.fetch import fetch_live
from retrac.xlsx import parse_received


def test_empty_xlsx_stops(tmp_path: Path) -> None:
    (tmp_path / "reporting_sw_quarterly_report_2025.xlsx").write_bytes(b"")
    (tmp_path / "facilities.geojson").write_text('{"type":"FeatureCollection","features":[]}\n', encoding="utf-8")
    (tmp_path / "indiana_counties.json").write_text("[]\n", encoding="utf-8")
    with pytest.raises(FetchError, match="empty IDEM quarterly XLSX"):
        fetch_live(cache_dir=tmp_path)


def test_unmatched_origin_stops(tmp_path: Path) -> None:
    from datetime import date

    import openpyxl

    from retrac.config import TON_COLS

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Start Date", "ID Number", "Facility Name", "Origin State", "Origin County", *TON_COLS])
    ws.append([date(2021, 1, 1), "01-01", "North Fill", "Indiana", "NotACounty", *([1] * len(TON_COLS))])
    path = tmp_path / "tiny.xlsx"
    wb.save(path)
    counties = {"alpha": {"name": "Alpha", "lat": 41.0, "lon": -86.0, "pop_2020": 1, "fips": "18001", "key": "alpha"}}
    with pytest.raises(FetchError, match="unmatched origin counties"):
        parse_received(path, counties=counties)
