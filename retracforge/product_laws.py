# Copyright (c) 2026 Martial Systems LLC
"""Refuse laws. Verify-before-done is the finish gate."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from retracforge.graphs.claim_bans import build_graph as claim_bans
    from retracforge.graphs.completeness import build_graph as completeness
    from retracforge.graphs.no_hero import build_graph as no_hero
    from retracforge.graphs.no_live_login import build_graph as no_live_login
    from retracforge.graphs.no_ridge import build_graph as no_ridge
    from retracforge.graphs.temporal_split import build_graph as temporal_split

    return [
        {
            "id": "retrac.no_ridge",
            "build": no_ridge,
            "state": {"ridge": False, "hgb": False, "sklearn_contestant": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "retrac.no_live_login",
            "build": no_live_login,
            "state": {"live_retrac_login": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "retrac.completeness",
            "build": completeness,
            "state": {"xlsx_ok": True, "coords_ok": True},
            "allow_decisions": ["allow"],
        },
        {
            "id": "retrac.temporal_split",
            "build": temporal_split,
            "state": {
                "temporal_ok": True,
                "confirm_in_train": False,
                "confirm_in_j": False,
                "random_split": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "retrac.claim_bans",
            "build": claim_bans,
            "state": {
                "flood_warning": False,
                "p_sfha": False,
                "casualty": False,
                "will_get_tons": False,
                "unmapped_risk": False,
                "frost_hero": False,
                "trust_the_stripe": False,
                "n_figures": 2,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "retrac.no_hero",
            "build": no_hero,
            "state": {
                "winter_page_hero": False,
                "readme_states_result": True,
            },
            "allow_decisions": ["allow"],
        },
    ]
