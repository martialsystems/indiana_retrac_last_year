# Copyright (c) 2026 Martial Systems LLC
"""Fail closed: last year vs assignment, not a waste forecast."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from retrac.errors import ClaimBanError

_BANS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("casualty", re.compile(r"\b(deaths?|fatalit(?:y|ies)|casualt(?:y|ies)|killed)\b", re.I)),
    ("flood_warning", re.compile(r"\bflood warning\b", re.I)),
    ("p_sfha", re.compile(r"\bP\(sfha\b|\bp_sfha\b", re.I)),
    ("will_get_tons", re.compile(r"will get\s+\d", re.I)),
    ("unmapped_risk", re.compile(r"\bunmapped risk\b", re.I)),
    ("frost_hero", re.compile(r"\bfrost (outlook|warning|hero)\b", re.I)),
    ("trust_the_stripe", re.compile(r"\btrust the stripe\b", re.I)),
    ("ridge_contestant", re.compile(r"\bRidge\b.{0,40}\b(RMSE|contestant|beats)\b", re.I)),
)


def scan_text(text: str) -> list[str]:
    hits = [name for name, pat in _BANS if pat.search(text or "")]
    if "\u2014" in (text or ""):
        hits.append("em_dash")
    return hits


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
