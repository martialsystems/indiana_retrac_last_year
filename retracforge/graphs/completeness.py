# Copyright (c) 2026 Martial Systems LLC
"""Empty XLSX or missing facility coordinates stop."""

from __future__ import annotations

from typing import Any

from retracforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if not state.get("xlsx_ok"):
        v.append("xlsx")
    if not state.get("coords_ok"):
        v.append("coords")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="retrac.completeness", evaluate=_evaluate, extra=["xlsx_ok", "coords_ok"])
