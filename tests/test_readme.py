# Copyright (c) 2026 Martial Systems LLC

import json
import re
from pathlib import Path

from retrac.claims import scan_text
from retrac.config import QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    live = json.loads((REPO / "logs" / "in_live" / "stage_c_report.json").read_text(encoding="utf-8"))
    ly = live["holdout"]["last_year"]["rmse_tons"]
    bar = live["holdout"]["bar"]["rmse_tons"]
    assert f"{ly:.1f}" in text
    assert f"{bar:.1f}" in text
    if live["last_year_beats_bar"]:
        assert "yes" in text.lower()
    else:
        assert re.search(r"\bno\b", text, re.I)
    assert "origin pop cancels" in text.lower() or "origin population cancels" in text.lower()
    assert "scatter.png" in text
    assert "rmse_bars.png" in text
    assert ".venv/bin/python -m pytest" in text
    assert "Open_the_research_console" not in text
    assert "labelColor" not in text
    assert "indiana_wx_pages" not in text
    assert scan_text(text) == []
    assert "\u2014" not in text
    assert "What it is not" not in text
    assert re.search(r"Locked `[0-9a-f]{7}`", text)
    assert "METHODOLOGY.md" in text
    assert "retracforge/" in text
