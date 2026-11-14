"""One-sided CUSUM on the signature-weighted residual z."""

from __future__ import annotations

import numpy as np

NONE, YELLOW, RED = 0, 1, 2
LEVEL_NAMES = {YELLOW: "yellow", RED: "red"}


def combine_z(zs: dict[str, np.ndarray], weights: dict[str, float]) -> np.ndarray:
    """Weighted sum of z over vitals, rescaled to unit variance over the vitals present that day."""
    names = [v for v in weights if v in zs]
    z = np.vstack([zs[v] for v in names])
    w = np.array([weights[v] for v in names])[:, None] * np.isfinite(z)
    norm = np.sqrt((w**2).sum(axis=0))
    total = np.nansum(w * np.nan_to_num(z), axis=0)
    return np.where(norm > 0, total / np.where(norm > 0, norm, 1), np.nan)


def cusum(z: np.ndarray, k: float, cap: float | None = None) -> np.ndarray:
    """S_t = max(0, S_{t-1} + z_t - k). Missing days carry S forward."""
    s, out = 0.0, np.zeros(len(z))
    for i, value in enumerate(z):
        if np.isfinite(value):
            s = max(0.0, s + value - k)
            if cap is not None:
                s = min(s, cap)
        out[i] = s
    return out


def levels(s: np.ndarray, days: np.ndarray, yellow: float, red: float | np.ndarray, burn_in: int) -> np.ndarray:
    """0 / yellow / red per day. Red is withheld during the burn-in days."""
    out = np.where(s >= yellow, YELLOW, NONE)
    out = np.where((s >= red) & (days > burn_in), RED, out)
    return out


def upcrossings(level: np.ndarray) -> list[tuple[int, int]]:
    """(index, level) each time an excursion reaches a new, higher level.

    An excursion ends when the level returns to 0, so one illness gives at most one
    yellow and one red alert.
    """
    out, peak = [], NONE
    for i, lv in enumerate(level):
        if lv == NONE:
            peak = NONE
        elif lv > peak:
            out.append((i, int(lv)))
            peak = int(lv)
    return out
