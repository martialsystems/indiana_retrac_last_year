# Copyright (c) 2026 Martial Systems LLC

import pytest

from retrac.claims import require_clean, scan_text
from retrac.errors import ClaimBanError


def test_allowed_and_banned() -> None:
    assert scan_text("last year RMSE vs mileage-plus-population. Tons of error.") == []
    assert "will_get_tons" in scan_text("Marion will get 20 tons")
    assert "flood_warning" in scan_text("flood warning tonight")
    assert "p_sfha" in scan_text("p_sfha as a waste score")
    assert "trust_the_stripe" in scan_text("trust the stripe this winter")
    assert "casualty" in scan_text("casualties from landfill siting")
    assert "em_dash" in scan_text("skill — not a forecast")
    with pytest.raises(ClaimBanError):
        require_clean("will get 12 tons next quarter", source="t")
