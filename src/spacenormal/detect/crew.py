"""Crew layer: outbreak alert when several crew drift together with no logged cause.

No crew median is ever subtracted from anyone's signal; this layer only reads the
individual residuals.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def drift_onsets(z: np.ndarray, days: np.ndarray, threshold: float, min_run: int, burn_in: int,
                 explained_days: set[int]) -> list[int]:
    """First day of each run of >= min_run consecutive days with z above threshold."""
    onsets, run_start, run_len = [], None, 0
    for i, value in enumerate(z):
        above = np.isfinite(value) and value > threshold and days[i] > burn_in
        if above:
            run_start = i if run_len == 0 else run_start
            run_len += 1
            if run_len == min_run and int(days[run_start]) not in explained_days:
                onsets.append(int(days[run_start]))
        elif np.isfinite(value) or days[i] <= burn_in:
            run_len = 0
    return onsets


def outbreak_alerts(z_by_crew: dict[str, np.ndarray], days: np.ndarray, explained_days: set[int],
                    cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Alert when >= min_crew members start drifting within window_days of each other,
    not all on the same day, on days with no logged shared event."""
    cc, burn_in = cfg["crew"], cfg["mission"]["burn_in_days"]
    onsets = sorted(
        (day, cid)
        for cid, z in z_by_crew.items()
        for day in drift_onsets(z, days, cc["z_threshold"], cc["min_run_days"], burn_in, explained_days)
    )
    alerts, used = [], set()
    for i, (day, cid) in enumerate(onsets):
        if (day, cid) in used:
            continue
        cluster = {cid: day}
        for other_day, other in onsets[i + 1:]:
            if other_day - day > cc["window_days"]:
                break
            if (other_day, other) not in used:
                cluster.setdefault(other, other_day)
        if len(cluster) >= cc["min_crew"] and len(set(cluster.values())) > 1:
            members = sorted(cluster, key=lambda c: (cluster[c], c))
            # The alert can fire once the min_crew-th member's drift is confirmed.
            confirm = sorted(cluster.values())[cc["min_crew"] - 1] + cc["min_run_days"] - 1
            alerts.append({"day": int(confirm), "crew_ids": members, "onsets": [cluster[c] for c in members]})
            used.update((d, c) for c, d in cluster.items())
    return alerts
