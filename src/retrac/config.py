# Copyright (c) 2026 Martial Systems LLC
"""Locked last-year Re-TRAC shipments vs origin-pop / miles."""

from __future__ import annotations

from pathlib import Path

QUESTION = (
    "Do last year’s Re-TRAC county-to-facility shipments beat a "
    "mileage-plus-population assignment on held-out quarters?"
)
USER_AGENT = "MartialSystemsResearch/indiana_retrac_last_year"
MAX_FIGURES = 2
MILE_EPS = 1.0
EARTH_MI = 3958.7613

TRAIN_YEARS = (2021, 2022, 2023)
HOLDOUT_YEARS = (2024,)
CONFIRM_YEARS = (2025,)

TON_COLS = (
    "Municipal Solid Waste",
    "Construction/Demolition",
    "Foundry",
    "Coal Ash",
    "Flue Gas Desulfurization Waste",
    "Other Non-Municipal",
    "Alternate Daily Cover/Reuse",
)

IDEM_XLSX_URL = "https://www.in.gov/idem/waste/files/reporting_sw_quarterly_report_2025.xlsx"
GIS_URL = (
    "https://gisdata.in.gov/server/rest/services/Hosted/"
    "Authorized_Operating_Solid_Waste_Facilities/FeatureServer/2120/query"
    "?where=1%3D1&outFields=sw_program_id,facility_name,county,facility_type"
    "&returnGeometry=true&outSR=4326&f=geojson"
)
RETRAC_LOGIN = "https://app.re-trac.com/"

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_GIST = "https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3"

LIVE_SCATTER_SUBTITLE = "Holdout tons. Last year vs mileage-plus-population. Tons of error, not a landfill siting."
LIVE_BARS_SUBTITLE = "Holdout RMSE in tons. Largest origin counties. County error, not a hauling route."
FIXTURE_SCATTER_SUBTITLE = "Fixture planted last-year persistence. Does not rescue live."
FIXTURE_BARS_SUBTITLE = "Fixture RMSE. Does not rescue live."
