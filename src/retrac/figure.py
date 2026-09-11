# Copyright (c) 2026 Martial Systems LLC
"""Two figures: holdout scatter, two-answer RMSE bars."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from retrac.claims import require_clean
from retrac.config import (
    FIXTURE_BARS_SUBTITLE,
    FIXTURE_SCATTER_SUBTITLE,
    LIVE_SCATTER_SUBTITLE,
    MAX_FIGURES,
)
from retrac.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def _fmt_rmse(val: float | None) -> str:
    if val is None:
        return ""
    if abs(float(val)) < 0.05:
        return "0"
    return f"{float(val):,.1f}"


def _has_arrays(hold: dict[str, Any]) -> bool:
    return bool(hold.get("obs_ly")) and bool(hold.get("pred_ly"))


def _cell_pair(hold: dict[str, Any]) -> tuple[float | None, float | None]:
    ly = (hold.get("last_year") or {}).get("rmse_tons")
    bar = (hold.get("bar") or {}).get("rmse_tons")
    return ly, bar


def _total_pair(hold: dict[str, Any], key: str) -> tuple[float | None, float | None]:
    block = hold.get(key) or {}
    return block.get("last_year_rmse"), block.get("bar_rmse")


def _needs_zoom(obs: np.ndarray) -> bool:
    pos = obs[np.isfinite(obs) & (obs > 0)]
    if pos.size < 8:
        return False
    return float(np.nanmax(pos)) > 8.0 * float(np.nanmedian(pos))


def _cell_note(ly: float | None, bar: float | None) -> str:
    text = (
        f"Last year RMSE {_fmt_rmse(ly)}\n"
        f"vs mileage-plus-population {_fmt_rmse(bar)}"
    )
    require_clean(text.replace("\n", " "), source="fig1_rmse")
    return text


def _annotate_cell(ax: Any, ly: float | None, bar: float | None) -> None:
    if ly is None or bar is None:
        return
    ax.text(
        0.98,
        0.02,
        _cell_note(ly, bar),
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "#0f172a",
            "alpha": 0.92,
        },
    )


def _overlay_cell_rmse(dest: Path, hold: dict[str, Any]) -> Path:
    ly, bar = _cell_pair(hold)
    if ly is None or bar is None or not dest.is_file():
        return dest
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt

    img = mpimg.imread(dest)
    height, width = img.shape[:2]
    dpi = 130.0
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img)
    ax.set_axis_off()
    ax.text(
        0.93,
        0.48,
        _cell_note(ly, bar),
        transform=ax.transAxes,
        ha="right",
        va="center",
        fontsize=8,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "#0f172a",
            "alpha": 0.92,
        },
    )
    fig.savefig(dest, dpi=int(dpi), pad_inches=0)
    plt.close(fig)
    return dest


def live_bars_subtitle(
    hold: dict[str, Any],
    *,
    total_key: str = "origin_total",
    total_name: str = "Origin-quarter totals",
) -> str:
    ly, bar = _cell_pair(hold)
    t_ly, t_bar = _total_pair(hold, total_key)
    text = (
        f"Two answers. Do not average. "
        f"Cell assignment: last year {_fmt_rmse(ly)} vs mileage-plus-population {_fmt_rmse(bar)}. "
        f"{total_name}: last year {_fmt_rmse(t_ly)} vs bar {_fmt_rmse(t_bar)}."
    )
    require_clean(text, source="fig2_sub")
    return text


def write_scatter(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    h = fit["holdout"]
    if not _has_arrays(h):
        return _overlay_cell_rmse(dest, h)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    obs_ly = np.array(h["obs_ly"], dtype=float)
    pred_ly = np.array(h["pred_ly"], dtype=float)
    obs_bar = np.array(h["obs_bar"], dtype=float)
    pred_bar = np.array(h["pred_bar"], dtype=float)
    ly, bar = _cell_pair(h)
    zoom = _needs_zoom(obs_ly) or _needs_zoom(obs_bar)
    if zoom:
        fig, axes = plt.subplots(1, 2, figsize=(10.2, 5.2))
        panels = [(axes[0], False), (axes[1], True)]
    else:
        fig, ax = plt.subplots(figsize=(6.4, 6.2))
        panels = [(ax, False)]
    hi = float(
        np.nanmax(
            [
                obs_bar.max() if obs_bar.size else 0,
                pred_bar.max() if pred_bar.size else 0,
                obs_ly.max() if obs_ly.size else 0,
                pred_ly.max() if pred_ly.size else 0,
            ]
            or [1.0]
        )
    )
    pos = obs_ly[np.isfinite(obs_ly) & (obs_ly > 0)]
    zoom_hi = float(np.nanpercentile(pos, 80)) * 1.4 if pos.size else hi / 8.0
    for ax, is_zoom in panels:
        ax.scatter(obs_bar, pred_bar, s=12, c="#64748b", alpha=0.5, label="mileage-plus-population")
        ax.scatter(obs_ly, pred_ly, s=12, c="#b45309", alpha=0.7, marker="x", label="last year")
        cap = zoom_hi if is_zoom else hi
        ax.plot([0, cap], [0, cap], color="#0f172a", lw=1.0, label="1:1")
        ax.set_xlim(0, cap)
        ax.set_ylim(0, cap)
        ax.set_xlabel("observed tons")
        ax.set_ylabel("predicted tons")
        if zoom:
            ax.set_title("Zoom" if is_zoom else "Full scale", fontsize=9)
        ax.legend(fontsize=7, loc="upper left")
        if not is_zoom:
            _annotate_cell(ax, ly, bar)
    fig.suptitle(title, fontsize=11)
    fig.subplots_adjust(bottom=0.18, top=0.88 if zoom else 0.90)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_bars(
    dest: Path,
    *,
    fit: dict[str, Any],
    title: str,
    subtitle: str,
    total_key: str = "origin_total",
    panel_b: str = "Origin-quarter totals",
) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    hold = fit["holdout"]
    cell_ly, cell_bar = _cell_pair(hold)
    tot_ly, tot_bar = _total_pair(hold, total_key)
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.8))
    panels = (
        (axes[0], "A. Cell assignment", cell_ly, cell_bar),
        (axes[1], f"B. {panel_b}", tot_ly, tot_bar),
    )
    labels = ("last year", "mileage-plus-population")
    colors = ("#b45309", "#64748b")
    x = np.arange(2, dtype=float)
    for ax, panel_title, ly, bar_v in panels:
        ys = (
            0.0 if ly is None else float(ly),
            0.0 if bar_v is None else float(bar_v),
        )
        rects = ax.bar(x, ys, color=colors, width=0.62)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_ylabel("RMSE (tons)")
        ax.set_title(panel_title, fontsize=9)
        ymax = max(ys) if max(ys) > 0 else 1.0
        ax.set_ylim(0, ymax * 1.22)
        for rect, val in zip(rects, ys):
            ax.text(
                rect.get_x() + rect.get_width() / 2.0,
                rect.get_height() + ymax * 0.03,
                _fmt_rmse(val),
                ha="center",
                va="bottom",
                fontsize=8,
            )
    fig.suptitle(title, fontsize=11)
    fig.subplots_adjust(bottom=0.24, top=0.86, wspace=0.34)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8, wrap=True)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any], live: bool) -> list[str]:
    _cap(2)
    log_dir.mkdir(parents=True, exist_ok=True)
    hold = fit["holdout"]
    a = write_scatter(
        log_dir / "scatter.png",
        fit=fit,
        title="Holdout county-to-facility tons",
        subtitle=LIVE_SCATTER_SUBTITLE if live else FIXTURE_SCATTER_SUBTITLE,
    )
    b = write_bars(
        log_dir / "rmse_bars.png",
        fit=fit,
        title="Two answers. Do not average.",
        subtitle=live_bars_subtitle(hold) if live else FIXTURE_BARS_SUBTITLE,
        total_key="origin_total",
        panel_b="Origin-quarter totals",
    )
    paths = [a, b]
    _cap(len(paths))
    return [p.name for p in paths]
