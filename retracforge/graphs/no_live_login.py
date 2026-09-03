# Copyright (c) 2026 Martial Systems LLC
"""Live Re-TRAC login is not the science lock."""

from __future__ import annotations

from typing import Any

from retracforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if state.get("live_retrac_login"):
        v.append("live_retrac_login")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="retrac.no_live_login", evaluate=_evaluate, extra=["live_retrac_login"])
