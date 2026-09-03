# Copyright (c) 2026 Martial Systems LLC
"""A Re-TRAC result does not rewrite the winter page."""

from __future__ import annotations

from typing import Any

from retracforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if state.get("winter_page_hero"):
        v.append("winter_page_hero")
    if not state.get("readme_states_result"):
        v.append("readme_silent")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="retrac.no_hero",
        evaluate=_evaluate,
        extra=["winter_page_hero", "readme_states_result"],
    )
