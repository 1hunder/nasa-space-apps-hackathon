"""Mission -> decomposition -> detectors -> contract JSON."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from spacenormal import baselines, contract
from spacenormal.config import load_config, load_eval_config
from spacenormal.data.schema import VITALS
from spacenormal.detect import crew as crew_layer
from spacenormal.detect.cusum import LEVEL_NAMES, RED, combine_z, cusum, levels, upcrossings
from spacenormal.llm.note import build_note
from spacenormal.model.simple import Decomposition, decompose_subject
from spacenormal.sim.interface import Mission

SYSTEM_VITALS = {"cardio": ("pulse", "sbp", "dbp"), "resp": ("resp_rate",), "thermo": ("temp_c",)}


def _num(x: float) -> float | None:
    return None if not np.isfinite(x) else round(float(x), 3)


def _series(values: np.ndarray, nullable: bool = False) -> list[float | None]:
    out = [_num(v) for v in values]
    if not nullable and any(v is None for v in out):
        raise ValueError("non-nullable series contains a missing value")
    return out


def _cusum_alerts(detector: str, cid: str, days: np.ndarray, zs: dict[str, np.ndarray],
                  cfg: dict[str, Any]) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    dc = cfg["detector"]
    z = combine_z(zs, dc["weights"])
    s = cusum(z, dc["k"], cap=2 * dc["red"])
    lv = levels(s, days, dc["yellow"], dc["red"], cfg["mission"]["burn_in_days"])
    alerts = []
    for i, level in upcrossings(lv):
        contrib = {v: dc["weights"][v] * zs[v][i] for v in dc["weights"] if np.isfinite(zs[v][i])}
        vital = max(contrib, key=contrib.get) if contrib else "pulse"
        name = LEVEL_NAMES[level]
        alerts.append({
            "id": f"{detector}:{cid}:{int(days[i])}:{name}", "detector": detector, "crew_id": cid,
            "day": int(days[i]), "level": name, "vital": vital, "z": _num(zs[vital][i]) or 0.0,
        })
    return alerts, z, lv


def _fixed_alerts(cid: str, days: np.ndarray, breaches: dict[str, np.ndarray],
                  frozen: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    """One red alert at the start of each run of days outside fixed clinical limits."""
    alerts, prev = [], False
    for i, day in enumerate(days):
        hit = [v for v, b in breaches.items() if b[i]]
        if hit and not prev:
            vital = hit[0]
            alerts.append({
                "id": f"fixed_thresholds:{cid}:{int(day)}:red", "detector": "fixed_thresholds",
                "crew_id": cid, "day": int(day), "level": "red", "vital": vital,
                "z": _num(frozen[vital][i]) or 0.0,
            })
        prev = bool(hit)
    return alerts


def _system_states(dec: dict[str, Decomposition], red_days: np.ndarray, crew_days: set[int],
                   days: np.ndarray) -> list[dict[str, Any]]:
    out = []
    for i, day in enumerate(days):
        row: dict[str, Any] = {"day": int(day), "fluids": "expected"}
        for system, vitals in SYSTEM_VITALS.items():
            state = "expected"
            for v in vitals:
                d = dec[v]
                if not np.isfinite(d.z[i]):
                    continue
                if d.z[i] > 2 or (red_days[i] and d.z[i] > 1):
                    state = "unexplained"
                    break
                deviation = d.y[i] - d.baseline[i] - d.adaptation[i]
                if abs(d.events[i]) > abs(d.residual[i]) and abs(deviation) > d.sigma[i]:
                    state = "event"
            if state == "unexplained" and int(day) in crew_days:
                state = "crew"
            row[system] = state
        out.append(row)
    return out


def _context_items(events: pd.DataFrame, day: int, journal: list[dict], cid: str) -> list[dict[str, str]]:
    near = events[(events["study_day"] >= day - 1) & (events["study_day"] <= day)]
    from_journal = [
        {"text": f"Journal, day {j['day']}: \"{j['text']}\"", "source_ref": f"journal:{j['day']}:{j['hour']}"}
        for j in journal if cid in j["crew_ids"] and day - 2 <= j["day"] <= day
    ]
    return from_journal + [
        {"text": f"{r.event_type.replace('_', ' ')} logged on day {int(r.study_day)}",
         "source_ref": f"events:{r.event_type}:{int(r.study_day)}"}
        for r in near.itertuples()
    ]


def run_pipeline(mission: Mission, cfg: dict[str, Any] | None = None,
                 priors: dict[str, dict[str, Any]] | None = None) -> contract.Mission:
    cfg = cfg or load_config()
    priors = priors or cfg["synthetic"]["priors"]
    min_days = cfg["model"]["min_baseline_days"]
    window = cfg["baselines"]["rolling_windows"][0]

    alerts: list[dict[str, Any]] = []
    notes: dict[str, dict[str, Any]] = {}
    decs: dict[str, dict[str, Decomposition]] = {}
    sn_z: dict[str, np.ndarray] = {}
    sn_levels: dict[str, np.ndarray] = {}
    days: np.ndarray | None = None

    for cid in mission.crew:
        sub = mission.daily[mission.daily["subject_id"] == cid].sort_values("study_day").reset_index(drop=True)
        ev = mission.events[mission.events["subject_id"] == cid]
        dec = decompose_subject(sub, ev, priors, cfg)
        decs[cid] = dec
        member_days = dec["pulse"].days
        if days is None:
            days = member_days
        elif not np.array_equal(days, member_days):
            raise ValueError("crew members must share the same in-bed day grid")

        sn_alerts, sn_z[cid], sn_levels[cid] = _cusum_alerts(
            "space_normal", cid, days, {v: dec[v].z for v in VITALS}, cfg)
        frozen = {v: baselines.frozen_z(sub, v, priors[v]["sigma_floor"], min_days) for v in VITALS}
        rolling = {v: baselines.rolling_z(sub, v, window, priors[v]["sigma_floor"]) for v in VITALS}
        alerts += sn_alerts
        alerts += _cusum_alerts("frozen_baseline", cid, days, frozen, cfg)[0]
        alerts += _cusum_alerts(f"rolling_{window}", cid, days, rolling, cfg)[0]
        alerts += _fixed_alerts(cid, days, baselines.fixed_breaches(sub, cfg["baselines"]["fixed_thresholds"]), frozen)

        for a in sn_alerts:
            if a["level"] != "red":
                continue
            i = int(np.where(days == a["day"])[0][0])
            d = dec[a["vital"]]
            numbers = {k: float(getattr(d, k)[i]) for k in ("y", "baseline", "adaptation", "events", "residual", "z")}
            notes[a["id"]] = build_note(mission.names.get(cid, cid), a["day"], a["vital"], numbers, _context_items(ev, a["day"], mission.journal, cid))

    assert days is not None
    in_events = mission.events[mission.events["study_day"] >= 1]
    grouped = in_events.groupby(["study_day", "event_type"])["subject_id"].apply(list)
    events = [{"day": int(day), "type": etype, "crew_ids": sorted(ids)} for (day, etype), ids in grouped.items()]
    shared_days = {e["day"] for e in events if e["type"] != "exercise" and len(e["crew_ids"]) >= 2}

    crew_alerts = crew_layer.outbreak_alerts(sn_z, days, shared_days, cfg)
    crew_days: dict[str, set[int]] = {cid: set() for cid in mission.crew}
    for ca in crew_alerts:
        for cid, onset in zip(ca["crew_ids"], ca["onsets"]):
            crew_days[cid].update(range(onset, ca["day"] + 6))

    spd = 1
    if mission.hourly is not None:
        spd = int(mission.hourly.groupby(["subject_id", "study_day"]).size().iloc[0])

    def hourly_series(cid: str, vital: str, daily_y: np.ndarray) -> list[float | None]:
        if mission.hourly is None:
            return _series(daily_y, True)
        h = mission.hourly[(mission.hourly["subject_id"] == cid) & (mission.hourly["study_day"] >= 1)]
        return _series(h.sort_values(["study_day", "hour"])[vital].to_numpy(dtype=float), True)

    crew = []
    for cid in mission.crew:
        dec = decs[cid]
        group = mission.daily.loc[mission.daily["subject_id"] == cid, "group"].iloc[0]
        crew.append({
            "id": cid, "name": mission.names.get(cid, cid), "group": group,
            "vitals": {
                v: {
                    "y": _series(d.y, True), "y_hourly": hourly_series(cid, v, d.y),
                    "baseline": _series(d.baseline),
                    "adaptation": _series(d.adaptation), "events": _series(d.events),
                    "residual": _series(d.residual, True), "z": _series(d.z, True),
                    "band_low": _series(d.band_low), "band_high": _series(d.band_high),
                    "earth_low": _series(d.earth_low), "earth_high": _series(d.earth_high),
                    "fixed_low": cfg["baselines"]["fixed_thresholds"].get(v, {}).get("low"),
                    "fixed_high": cfg["baselines"]["fixed_thresholds"].get(v, {}).get("high"),
                } for v, d in dec.items()
            },
            "systems": _system_states(dec, sn_levels[cid] == RED, crew_days[cid], days),
        })

    lo, hi = load_eval_config()["scoring"]["hit_window"]
    far = load_eval_config()["scoring"]["false_alarm_exclusion_days"]
    onsets: dict[str, list[int]] = {}
    for ep in mission.episodes.itertuples():
        onsets.setdefault(ep.subject_id, []).append(int(ep.onset_day))
    for a in alerts:
        offsets = [a["day"] - o for o in onsets.get(a["crew_id"], [])]
        if any(lo <= off <= hi for off in offsets):
            a["truth"] = "hit"
        elif all(abs(off) > far for off in offsets):
            a["truth"] = "false_alarm"
        else:
            a["truth"] = "near_episode"
    episodes = [{"crew_id": ep.subject_id, "onset_day": int(ep.onset_day), "provenance": ep.source}
                for ep in mission.episodes.itertuples()]

    return contract.Mission.model_validate({
        "mission_id": mission.mission_id, "scenario": mission.scenario,
        "days": [int(d) for d in days], "samples_per_day": spd, "provenance": mission.provenance,
        "crew": crew, "events": events,
        "alerts": sorted(alerts, key=lambda a: (a["day"], a["detector"], a["crew_id"])),
        "crew_alerts": crew_alerts, "episodes": episodes, "journal": mission.journal, "notes": notes,
    })
