# Copyright (c) 2026 Martial Systems LLC
"""Call sites for refuse laws."""

from __future__ import annotations

from typing import Any

from retracforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from retracforge.graphs.claim_bans import build_graph as build_claims
from retracforge.graphs.completeness import build_graph as build_complete
from retracforge.graphs.no_hero import build_graph as build_hero
from retracforge.graphs.no_live_login import build_graph as build_login
from retracforge.graphs.no_ridge import build_graph as build_ridge
from retracforge.graphs.temporal_split import build_graph as build_split


def require_no_ridge(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "retrac_ridge"))
    state = {"ridge": False, "hgb": False, "sklearn_contestant": False}
    state.update(flags)
    require_law(build_ridge(), state, allow_decisions=["allow"], law_id="retrac.no_ridge", thread_id=thread_id, raise_error=True)


def require_no_live_login(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "retrac_login"))
    state = {"live_retrac_login": False}
    state.update(flags)
    require_law(build_login(), state, allow_decisions=["allow"], law_id="retrac.no_live_login", thread_id=thread_id, raise_error=True)


def require_completeness(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "retrac_complete"))
    state = {"xlsx_ok": False, "coords_ok": False}
    state.update(flags)
    require_law(build_complete(), state, allow_decisions=["allow"], law_id="retrac.completeness", thread_id=thread_id, raise_error=True)


def require_split(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "retrac_split"))
    state = {
        "temporal_ok": True,
        "confirm_in_train": False,
        "confirm_in_j": False,
        "random_split": False,
    }
    state.update(flags)
    require_law(build_split(), state, allow_decisions=["allow"], law_id="retrac.temporal_split", thread_id=thread_id, raise_error=True)


def require_claims(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "retrac_claims"))
    state = {
        "flood_warning": False,
        "p_sfha": False,
        "casualty": False,
        "will_get_tons": False,
        "unmapped_risk": False,
        "frost_hero": False,
        "trust_the_stripe": False,
        "n_figures": 2,
    }
    state.update(flags)
    require_law(build_claims(), state, allow_decisions=["allow"], law_id="retrac.claim_bans", thread_id=thread_id, raise_error=True)


def require_no_hero(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "retrac_hero"))
    state = {
        "winter_page_hero": False,
        "readme_states_result": False,
    }
    state.update(flags)
    require_law(build_hero(), state, allow_decisions=["allow"], law_id="retrac.no_hero", thread_id=thread_id, raise_error=True)
