"""Space-Normal, simple version.

For each person and vital:
    y_t = baseline + s * g(day) + beta . e_t + residual_t
    z_t = residual_t / sigma_t

- baseline: pre-bed-rest median (event effects removed), sigma0 from the MAD with a
  small-sample correction.
- g: population adaptation prior. s: per-person scale, prior N(1, sd^2), fitted by a
  Huber-weighted MAP on in-bed days 4-21 only, excluding flagged days, frozen after.
- Scoring is causal: day t is scored with the scale fitted on days before t.
- sigma_t widens early on by the remaining uncertainty in s.
- The 10-16 day baseline leaves a persistent error in each person's level. After the
  burn-in a slow, gated update corrects it: days with |z| above the gate never update,
  so an illness bump is not absorbed. The noise scale is tracked the same way and can
  only widen relative to the baseline estimate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from spacenormal.data.schema import VITALS

EVENT_TYPES: tuple[str, ...] = ("exercise", "schedule_shift")


@dataclass
class Decomposition:
    days: np.ndarray
    y: np.ndarray
    baseline: np.ndarray
    adaptation: np.ndarray
    events: np.ndarray
    residual: np.ndarray
    z: np.ndarray
    sigma: np.ndarray
    band_low: np.ndarray
    band_high: np.ndarray
    scale: np.ndarray
    sigma0: float
    earth_low: np.ndarray
    earth_high: np.ndarray


def prior_curve(day: np.ndarray, prior: dict[str, Any]) -> np.ndarray:
    day = np.asarray(day, dtype=float)
    return np.where(day >= 1, prior["amp"] * (1 - np.exp(-day / prior["tau"])), 0.0)


def baseline_stats(values: np.ndarray, floor: float, min_days: int) -> tuple[float, float]:
    """Median and robust SD of the pre-bed-rest values, inflated for the short baseline."""
    values = values[np.isfinite(values)]
    n = len(values)
    if n < min_days:
        raise ValueError(f"baseline needs at least {min_days} valid days, got {n}")
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    sd = max(1.4826 * mad * n / (n - 0.8), floor)
    return median, sd * float(np.sqrt(1 + 1 / n))


def event_regressors(sub: pd.DataFrame, events: pd.DataFrame, ref_temp: float) -> dict[str, np.ndarray]:
    """Logged covariates per row of `sub` (one subject, sorted by study_day)."""
    days = sub["study_day"].to_numpy()
    room = sub["room_temp_c"].to_numpy(dtype=float) - ref_temp
    out = {"room_temp_c": np.where(np.isfinite(room), room, 0.0)}
    for etype in EVENT_TYPES:
        logged = events.loc[events["event_type"] == etype, "study_day"].to_numpy()
        out[etype] = np.isin(days, logged).astype(float)
    return out


def _fit_scale(g, r, sigma0, prior_sd, huber_c, bounds) -> tuple[float, float]:
    if len(g) == 0 or not np.any(g):
        return 1.0, prior_sd
    s, precision = 1.0, 1 / prior_sd**2
    for _ in range(5):
        u = (r - s * g) / sigma0
        w = np.minimum(1.0, huber_c / np.maximum(np.abs(u), 1e-9))
        precision = 1 / prior_sd**2 + np.sum(w * g * g) / sigma0**2
        s = (1 / prior_sd**2 + np.sum(w * g * r) / sigma0**2) / precision
    return float(np.clip(s, *bounds)), float(1 / np.sqrt(precision))


def decompose_vital(
    sub: pd.DataFrame, regressors: dict[str, np.ndarray], vital: str,
    prior: dict[str, Any], cfg: dict[str, Any],
) -> Decomposition:
    mc = cfg["model"]
    days_all = sub["study_day"].to_numpy()
    y_all = sub[vital].to_numpy(dtype=float)
    ev_all = sum(prior["beta"].get(name, 0.0) * x for name, x in regressors.items())
    pre, inn = days_all < 0, days_all >= 1

    baseline, sigma0 = baseline_stats((y_all - ev_all)[pre], prior["sigma_floor"], mc["min_baseline_days"])
    days, y, ev = days_all[inn], y_all[inn], ev_all[inn]
    g = prior_curve(days, prior)
    r = y - baseline - ev
    fit_lo, fit_hi = mc["scale_fit_days"]

    n = len(days)
    adaptation, sigma, scale, level = np.zeros(n), np.zeros(n), np.ones(n), np.zeros(n)
    eligible: list[int] = []
    s, post_sd = 1.0, mc["scale_prior_sd"]
    lvl, var = 0.0, sigma0**2
    a_level = 1 - 0.5 ** (1 / mc["level_halflife_days"])
    a_var = 1 - 0.5 ** (1 / mc["var_halflife_days"])
    burn_in = cfg["mission"]["burn_in_days"]
    for i in range(n):
        if days[i] <= fit_hi + 1:
            idx = np.array(eligible, dtype=int)
            s, post_sd = _fit_scale(g[idx], (r - level)[idx], sigma0, mc["scale_prior_sd"], mc["huber_c"], mc["scale_bounds"])
        scale[i], level[i] = s, lvl
        adaptation[i] = s * g[i]
        sigma[i] = np.sqrt(max(sigma0**2, var) + (post_sd * g[i]) ** 2)
        resid_i = r[i] - lvl - adaptation[i]
        z_i = resid_i / sigma[i]
        if not np.isfinite(z_i):
            continue
        if fit_lo <= days[i] <= fit_hi and abs(z_i) <= mc["exclude_abs_z"]:
            eligible.append(i)
        if days[i] > burn_in:  # updates apply from the next day on: scoring stays causal
            if abs(z_i) <= mc["level_gate_z"]:
                lvl += a_level * resid_i
            if abs(z_i) <= 3:
                var += a_var * (resid_i**2 - var)

    residual = r - level - adaptation
    expected = baseline + level + adaptation + ev
    return Decomposition(
        days=days, y=y, baseline=baseline + level, adaptation=adaptation, events=ev,
        residual=residual, z=residual / sigma, sigma=sigma,
        band_low=expected - mc["band_sigma"] * sigma, band_high=expected + mc["band_sigma"] * sigma,
        scale=scale, sigma0=sigma0,
        earth_low=np.full(n, baseline - mc["band_sigma"] * sigma0),
        earth_high=np.full(n, baseline + mc["band_sigma"] * sigma0),
    )


def decompose_subject(
    sub: pd.DataFrame, events: pd.DataFrame, priors: dict[str, dict[str, Any]], cfg: dict[str, Any],
) -> dict[str, Decomposition]:
    """`sub` and `events` hold one subject. Returns one Decomposition per vital, in-bed days only."""
    sub = sub.sort_values("study_day").reset_index(drop=True)
    regressors = event_regressors(sub, events, cfg["model"]["room_temp_ref_c"])
    return {v: decompose_vital(sub, regressors, v, priors[v], cfg) for v in VITALS}
