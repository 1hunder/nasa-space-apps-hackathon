"""Baseline detectors' z-scores. They share the CUSUM machinery with Space-Normal."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from spacenormal.model.simple import baseline_stats


def frozen_z(sub: pd.DataFrame, vital: str, floor: float, min_days: int) -> np.ndarray:
    """Deviation from the frozen pre-bed-rest baseline; no adaptation, no events."""
    days = sub["study_day"].to_numpy()
    y = sub[vital].to_numpy(dtype=float)
    baseline, sd = baseline_stats(y[days < 0], floor, min_days)
    return (y[days >= 1] - baseline) / sd


def rolling_z(sub: pd.DataFrame, vital: str, window: int, floor: float, min_points: int = 5) -> np.ndarray:
    """Deviation from the median of the previous `window` days (causal recalibration)."""
    days = sub["study_day"].to_numpy()
    y = sub[vital].to_numpy(dtype=float)
    out = np.full(len(y), np.nan)
    for i in range(len(y)):
        hist = y[max(0, i - window):i]
        hist = hist[np.isfinite(hist)]
        if len(hist) >= min_points and np.isfinite(y[i]):
            med = np.median(hist)
            sd = max(1.4826 * np.median(np.abs(hist - med)), floor)
            out[i] = (y[i] - med) / sd
    return out[days >= 1]


def fixed_breaches(sub: pd.DataFrame, thresholds: dict[str, dict[str, Any]]) -> dict[str, np.ndarray]:
    """Per vital, True on in-bed days outside the fixed clinical limits."""
    inn = sub["study_day"].to_numpy() >= 1
    out = {}
    for vital, lim in thresholds.items():
        y = sub[vital].to_numpy(dtype=float)[inn]
        breach = np.zeros(len(y), dtype=bool)
        if "high" in lim:
            breach |= y > lim["high"]
        if "low" in lim:
            breach |= y < lim["low"]
        out[vital] = breach
    return out
