"""Synthetic fallback: hourly vitals with a spaceflight-like adaptation plus illness bumps.

Lets the whole pipeline run with zero real data. Everything produced here carries
source = "SYNTHETIC" and must never be presented as a result.
"""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np
import pandas as pd

from spacenormal.config import load_config, load_journal
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


def _ar1(rng: np.random.Generator, n: int, sd: float, rho: float) -> np.ndarray:
    out, x = np.empty(n), 0.0
    innov = sd * np.sqrt(1 - rho**2)
    for k in range(n):
        x = rho * x + rng.normal(0, innov)
        out[k] = x
    return out


def make_mission(
    crew: Sequence[str],
    scenario: Scenario,
    rng: np.random.Generator,
    cfg: dict[str, Any] | None = None,
) -> Mission:
    """Hourly readings for each crew member; `daily` holds their daily means.

    Each reading = baseline + time-of-day pattern + adaptation + logged events + illness
    + day-level noise + hour-level noise. The time-of-day pattern is then estimated from
    the pre-mission days only and removed, as a real pipeline would have to do.
    """
    cfg = cfg or load_config()
    m, syn, ref_temp = cfg["mission"], cfg["synthetic"], cfg["model"]["room_temp_ref_c"]
    priors, spd = syn["priors"], syn["samples_per_day"]
    days = np.concatenate([np.arange(-m["pre_days"], 0), np.arange(1, m["in_days"] + 1)])
    is_in = days >= 1
    n_days = len(days)
    day_idx = np.repeat(np.arange(n_days), spd)
    hour = np.tile(np.arange(spd) * (24 // spd), n_days)
    t = np.repeat(days.astype(float), spd) + (hour + 0.5) / 24 - 0.5   # fractional mission day
    in_h = np.repeat(is_in, spd)

    onsets: dict[int, int] = {}
    for spec in scenario.illness:
        onset = spec.onset
        if onset is None:
            onset = int(rng.integers(m["burn_in_days"] + 8, m["in_days"] - 10))
        onsets[spec.crew] = onset

    shift = np.zeros(n_days)
    for ev in scenario.shared_events:
        shift[(days >= ev.day) & (days < ev.day + ev.duration)] = 1.0

    daily_rows, hourly_rows, event_rows, episode_rows, truth_rows = [], [], [], [], []
    for idx, sid in enumerate(crew):
        group = "exercise" if idx % 2 else "control"
        exercise = ((days % 2 == 0) & is_in).astype(float) if group == "exercise" else np.zeros(n_days)

        room = np.empty(n_days)
        level = rng.normal(0, 0.5)
        for k in range(n_days):
            level = 0.7 * level + rng.normal(0, 0.45)
            room[k] = ref_temp + 0.5 + level
        room = np.round(room, 1)
        rh = np.round(np.clip(rng.normal(45, 5, n_days), 20, 80), 0)

        ill_h = np.where(in_h, illness_shape(t - onsets[idx]), 0.0) if idx in onsets else np.zeros(len(t))
        ill_d = ill_h.reshape(n_days, spd).mean(axis=1)
        gap = is_in & (rng.random(n_days) < syn["gap_rate"]) & (ill_d == 0)

        frame: dict[str, Any] = {
            "subject_id": sid, "campaign": "SYNTHETIC",
            "phase": np.where(is_in, "in", "pre"), "study_day": days,
        }
        hframe: dict[str, Any] = {"subject_id": sid, "study_day": days[day_idx], "hour": hour}
        phase_shift = rng.normal(0, 1.0)  # hours; people differ in when their daily low falls
        for vital in VITALS:
            p = priors[vital]
            base = rng.normal(p["base_mean"], p["base_sd"])
            scale = float(np.clip(rng.normal(1.0, syn["scale_sd"]), *syn["scale_clip"]))
            tau = p["tau"] * float(np.exp(rng.normal(0, syn["tau_log_sd"])))
            adaptation = scale * adaptation_curve(np.clip(t, 0, None), p["amp"], tau) * in_h
            beta = p["beta"]
            ev_term = (beta["room_temp_c"] * (room - ref_temp) + beta["exercise"] * exercise
                       + beta["schedule_shift"] * shift)
            illness = syn["illness"][vital] * ill_h
            df_t = syn["noise_df"]
            noise_day = rng.standard_t(df_t, n_days) * p["noise_sd"] / np.sqrt(df_t / (df_t - 2))
            noise_day = np.clip(noise_day, -5 * p["noise_sd"], 5 * p["noise_sd"])  # heavy-tailed, but physiological
            noise_hour = _ar1(rng, len(t), p["hour_sd"], syn["hour_ar"])
            circadian = -p["circadian"] * np.cos(2 * np.pi * (hour - 4 - phase_shift) / 24)  # lowest around 04:00
            raw = np.round(base + circadian + adaptation + ev_term[day_idx] + illness
                           + noise_day[day_idx] + noise_hour, _ROUND[vital])
            # Time-of-day pattern: mean by hour over the pre-mission days, centred on zero.
            pre_raw = raw[~in_h].reshape(-1, spd)
            profile = pre_raw.mean(axis=0) - pre_raw.mean()
            adjusted = np.where(np.repeat(gap, spd), np.nan, raw - profile[hour * spd // 24])
            hframe[vital] = np.round(adjusted, 2)
            by_day = adjusted.reshape(n_days, spd)
            frame[vital] = np.round(np.where(gap, np.nan, np.nanmean(np.where(np.isnan(by_day), 0, by_day), axis=1)), 2)
            adapt_d = adaptation.reshape(n_days, spd).mean(axis=1)
            ill_vd = illness.reshape(n_days, spd).mean(axis=1)
            for k, day in enumerate(days):
                truth_rows.append((sid, int(day), vital, base, adapt_d[k], ev_term[k], ill_vd[k],
                                   float(by_day[k].mean()) - base - adapt_d[k] - ev_term[k] - ill_vd[k] if not gap[k] else np.nan))

        weight0 = rng.normal(75, 9)
        frame["weight_kg"] = np.round(weight0 - 0.02 * np.clip(days, 0, None) + rng.normal(0, 0.3, n_days), 1)
        frame["room_temp_c"], frame["room_rh"] = room, rh
        frame["group"], frame["source"] = group, SOURCE
        daily_rows.append(pd.DataFrame(frame))
        hourly_rows.append(pd.DataFrame(hframe))

        for day in days[exercise > 0]:
            event_rows.append((sid, int(day), "exercise", 1.0))
        for day in days[shift > 0]:
            event_rows.append((sid, int(day), "schedule_shift", 1.0))
        if idx in onsets:
            episode_rows.append((sid, onsets[idx], "synthetic_illness", "synthetic", SOURCE))

    # Journal entries are drawn last so they never change the simulated vitals.
    jr = load_journal()
    journal: list[dict] = []
    for ev in scenario.shared_events:
        journal.append({"day": ev.day, "hour": 8, "crew_ids": list(crew), "accounted": True, **jr[ev.type]})
    # Each crew member gets their own shuffled run through the entries, so nobody repeats themselves.
    per_person = {c: list(rng.permutation(len(jr["personal"]))) for c in crew}
    for who in rng.choice(list(crew), size=jr["personal_entries_per_mission"]):
        k = per_person[who].pop()
        journal.append({"day": int(rng.integers(2, m["in_days"])), "hour": int(rng.integers(7, 23)),
                        "crew_ids": [str(who)], "accounted": False, **jr["personal"][int(k)]})
    for entry in jr["shared"]:
        journal.append({"day": int(rng.integers(5, m["in_days"] - 3)), "hour": int(rng.integers(9, 18)),
                        "crew_ids": list(crew), "accounted": False, **entry})
    journal = [{**j, "reader": "mock"} for j in sorted(journal, key=lambda j: (j["day"], j["hour"]))]

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
        hourly=pd.concat(hourly_rows, ignore_index=True),
        journal=journal,
    )
