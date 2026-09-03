# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from retracforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from retracforge.gate import (
    require_claims,
    require_completeness,
    require_no_hero,
    require_no_live_login,
    require_no_ridge,
    require_split,
)
from retracforge.product_laws import laws


def test_laws() -> None:
    require_no_ridge(thread_id="t.r.ok")
    with pytest.raises(LawBlockedError):
        require_no_ridge(ridge=True, thread_id="t.r.ridge")
    with pytest.raises(LawBlockedError):
        require_no_ridge(hgb=True, thread_id="t.r.hgb")
    require_no_live_login(thread_id="t.u.ok")
    with pytest.raises(LawBlockedError):
        require_no_live_login(live_retrac_login=True, thread_id="t.u.live")
    require_completeness(xlsx_ok=True, coords_ok=True, thread_id="t.c.ok")
    with pytest.raises(LawBlockedError):
        require_completeness(xlsx_ok=False, coords_ok=True, thread_id="t.c.xlsx")
    with pytest.raises(LawBlockedError):
        require_completeness(xlsx_ok=True, coords_ok=False, thread_id="t.c.coords")
    require_split(thread_id="t.s.ok")
    with pytest.raises(LawBlockedError):
        require_split(confirm_in_j=True, thread_id="t.s.j")
    require_claims(n_figures=2, thread_id="t.k.ok")
    with pytest.raises(LawBlockedError):
        require_claims(n_figures=3, thread_id="t.k.fig")
    require_no_hero(readme_states_result=True, thread_id="t.p.ok")
    with pytest.raises(LawBlockedError):
        require_no_hero(winter_page_hero=True, readme_states_result=True, thread_id="t.p.hero")
    assert {row["id"] for row in laws()} == {
        "retrac.no_ridge",
        "retrac.no_live_login",
        "retrac.completeness",
        "retrac.temporal_split",
        "retrac.claim_bans",
        "retrac.no_hero",
    }
