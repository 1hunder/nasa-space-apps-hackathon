"""Synthetic fallback: bed-rest-like daily vitals plus illness bumps.

Lets the whole pipeline run with zero real data. Everything produced here carries
source = "SYNTHETIC" and must never be presented as a result.
"""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np
import pandas as pd

from spacenormal.config import load_config
from spacenormal.data.schema import (
    DAILY_COLUMNS, EPISODES_COLUMNS, EVENTS_COLUMNS, VITALS,
    validate_daily, validate_episodes, validate_events,
)
from spacenormal.sim.interface import Mission, Scenario

SOURCE = "SYNTHETIC"
_ROUND = {"pulse": 0, "temp_c": 1, "resp_rate": 0, "sbp": 0, "dbp": 0}


def illness_shape(d: np.ndarray) -> np.ndarray:
    """Unit-height bump around onset (d = day - onset): 4-day rise, peak at +1, decay."""
    d = np.asarray(d, dtype=float)
    out = np.zeros_like(d)
    rise = (d >= -3) & (d <= 1)
    out[rise] = (d[rise] + 3) / 4
    decay = (d > 1) & (d <= 12)
    out[decay] = np.exp(-(d[decay] - 1) / 3.0)
    return out


def adaptation_curve(day: np.ndarray, amp: float, tau: float) -> np.ndarray:
    day = np.asarray(day, dtype=float)
    return np.where(day >= 1, amp * (1 - np.exp(-day / tau)), 0.0)


def make_mission(
    crew: Sequence[str],
    scenario: Scenario,
    rng: np.random.Generator,
    cfg: dict[str, Any] | None = None,
) -> Mission:
    cfg = cfg or load_config()
    m, syn, ref_temp = cfg["mission"], cfg["synthetic"], cfg["model"]["room_temp_ref_c"]
    priors = syn["priors"]
    pre_days = np.arange(-m["pre_days"], 0)
    in_days = np.arange(1, m["in_days"] + 1)
    days = np.concatenate([pre_days, in_days])
    is_in = days >= 1

    onsets: dict[int, int] = {}
    for spec in scenario.illness:
        onset = spec.onset
        if onset is None:
            onset = int(rng.integers(m["burn_in_days"] + 8, m["in_days"] - 10))
        onsets[spec.crew] = onset

    shift = np.zeros(len(days))
    for ev in scenario.shared_events:
        shift[(days >= ev.day) & (days < ev.day + ev.duration)] = 1.0

    daily_rows, event_rows, episode_rows, truth_rows = [], [], [], []
    for idx, sid in enumerate(crew):
        group = "exercise" if idx % 2 else "control"
        exercise = ((days % 2 == 0) & is_in).astype(float) if group == "exercise" else np.zeros(len(days))

        room = np.empty(len(days))
        level = rng.normal(0, 0.5)
        for t in range(len(days)):
            level = 0.7 * level + rng.normal(0, 0.45)
            room[t] = ref_temp + 0.5 + level
        room = np.round(room, 1)
        rh = np.round(np.clip(rng.normal(45, 5, len(days)), 20, 80), 0)

        ill = illness_shape(days - onsets[idx]) if idx in onsets else np.zeros(len(days))
        ill = np.where(is_in, ill, 0.0)
        gap = is_in & (rng.random(len(days)) < syn["gap_rate"]) & (ill == 0)

        frame: dict[str, Any] = {
            "subject_id": sid, "campaign": "SYNTHETIC",
            "phase": np.where(is_in, "in", "pre"), "study_day": days,
        }
        for vital in VITALS:
            p = priors[vital]
            base = rng.normal(p["base_mean"], p["base_sd"])
            scale = float(np.clip(rng.normal(1.0, syn["scale_sd"]), 0.5, 1.7))
            tau = p["tau"] * float(np.exp(rng.normal(0, syn["tau_log_sd"])))
            adaptation = scale * adaptation_curve(days, p["amp"], tau)
            beta = p["beta"]
            ev_term = (
                beta["room_temp_c"] * (room - ref_temp)
                + beta["exercise"] * exercise
                + beta["schedule_shift"] * shift
            )
            illness = syn["illness"][vital] * ill
            df_t = syn["noise_df"]
            noise = rng.standard_t(df_t, len(days)) * p["noise_sd"] / np.sqrt(df_t / (df_t - 2))
            noise = np.clip(noise, -5 * p["noise_sd"], 5 * p["noise_sd"])  # heavy-tailed, but physiological
            y = np.round(base + adaptation + ev_term + illness + noise, _ROUND[vital])
            frame[vital] = np.where(gap, np.nan, y)
            for t, day in enumerate(days):
                truth_rows.append((sid, int(day), vital, base, adaptation[t], ev_term[t], illness[t], noise[t]))

        weight0 = rng.normal(75, 9)
        frame["weight_kg"] = np.round(weight0 - 0.02 * np.clip(days, 0, None) + rng.normal(0, 0.3, len(days)), 1)
        frame["room_temp_c"], frame["room_rh"] = room, rh
        frame["group"], frame["source"] = group, SOURCE
        daily_rows.append(pd.DataFrame(frame))

        for day in days[exercise > 0]:
            event_rows.append((sid, int(day), "exercise", 1.0))
        for day in days[shift > 0]:
            event_rows.append((sid, int(day), "schedule_shift", 1.0))
        if idx in onsets:
            episode_rows.append((sid, onsets[idx], "synthetic_illness", "synthetic", SOURCE))

    daily = pd.concat(daily_rows, ignore_index=True)[list(DAILY_COLUMNS)]
    events = pd.DataFrame(event_rows, columns=list(EVENTS_COLUMNS))
    episodes = pd.DataFrame(episode_rows, columns=list(EPISODES_COLUMNS))
    truth = pd.DataFrame(
        truth_rows,
        columns=["subject_id", "study_day", "vital", "baseline", "adaptation", "events", "illness", "noise"],
    )
    return Mission(
        mission_id=f"synthetic_{scenario.name}",
        scenario=scenario.name,
        crew=list(crew),
        daily=validate_daily(daily),
        events=validate_events(events),
        episodes=validate_episodes(episodes),
        provenance={
            "adaptation": SOURCE,
            "illness": SOURCE if onsets else "NONE",
            "events": SOURCE,
        },
        truth=truth,
    )
