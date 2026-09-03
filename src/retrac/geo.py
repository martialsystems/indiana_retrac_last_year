# Copyright (c) 2026 Martial Systems LLC
"""Great-circle miles. Road miles is a sequel."""

from __future__ import annotations

import math

from retrac.config import EARTH_MI


def miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return EARTH_MI * 2 * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1.0 - a)))
