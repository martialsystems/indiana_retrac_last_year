# Copyright (c) 2026 Martial Systems LLC
"""Two figures: holdout scatter, largest-origin RMSE bars."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from retrac.claims import require_clean
from retrac.config import (
    FIXTURE_BARS_SUBTITLE,
    FIXTURE_SCATTER_SUBTITLE,
    LIVE_BARS_SUBTITLE,
    LIVE_SCATTER_SUBTITLE,
    MAX_FIGURES,
)
from retrac.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_scatter(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    h = fit["holdout"]
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    obs_ly = np.array(h["obs_ly"], dtype=float)
    pred_ly = np.array(h["pred_ly"], dtype=float)
    obs_bar = np.array(h["obs_bar"], dtype=float)
    pred_bar = np.array(h["pred_bar"], dtype=float)
    ax.scatter(obs_bar, pred_bar, s=12, c="#64748b", alpha=0.5, label="mileage-plus-population")
    ax.scatter(obs_ly, pred_ly, s=12, c="#b45309", alpha=0.7, marker="x", label="last year")
    hi = float(np.nanmax([obs_bar.max() if obs_bar.size else 0, pred_bar.max() if pred_bar.size else 0, obs_ly.max() if obs_ly.size else 0, pred_ly.max() if pred_ly.size else 0] or [1.0]))
    ax.plot([0, hi], [0, hi], color="#0f172a", lw=1.0, label="1:1")
    ax.set_xlabel("observed tons")
    ax.set_ylabel("predicted tons")
    ax.legend(fontsize=7, loc="upper left")
    fig.suptitle(title, fontsize=11)
    fig.subplots_adjust(bottom=0.18, top=0.90)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_bars(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [r for r in fit["holdout"]["by_county"] if r["last_year_rmse"] is not None][:12]
    labels = [r["origin"] for r in rows]
    ly = [r["last_year_rmse"] for r in rows]
    bar = [r["bar_rmse"] for r in rows]
    x = np.arange(len(labels), dtype=float)
    width = 0.38
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.bar(x - width / 2, bar, width, color="#64748b", label="mileage-plus-population")
    ax.bar(x + width / 2, ly, width, color="#b45309", label="last year")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8, rotation=32, ha="right")
    ax.set_ylabel("RMSE (tons)")
    ax.legend(fontsize=7, loc="upper right")
    fig.suptitle(title, fontsize=11)
    fig.subplots_adjust(bottom=0.28, top=0.88)
    fig.text(0.5, 0.03, subtitle, ha="center", fontsize=8)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any], live: bool) -> list[str]:
    _cap(2)
    log_dir.mkdir(parents=True, exist_ok=True)
    a = write_scatter(
        log_dir / "scatter.png",
        fit=fit,
        title="Holdout county-to-facility tons",
        subtitle=LIVE_SCATTER_SUBTITLE if live else FIXTURE_SCATTER_SUBTITLE,
    )
    b = write_bars(
        log_dir / "rmse_bars.png",
        fit=fit,
        title="Largest-origin holdout RMSE",
        subtitle=LIVE_BARS_SUBTITLE if live else FIXTURE_BARS_SUBTITLE,
    )
    paths = [a, b]
    _cap(len(paths))
    return [p.name for p in paths]
