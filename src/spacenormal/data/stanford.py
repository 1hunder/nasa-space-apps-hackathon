"""Loaders for the Stanford COVID-19 wearables data (illness signatures only).

Phase 1 (Mishra et al. 2020):  data/raw/stanford_p1/COVID-19-Wearables/<ID>_{hr,steps,sleep}.csv
    hr:    "user","datetime","heartrate"   (one row per minute)
    steps: "user","datetime","steps"       (one row per minute, zeros included)
Phase 2 (Alavi et al. 2022):   data/raw/stanford_p2/COVID-19-Phase2-Wearables/<ID>/Orig_{Fitbit,NonFitbit}_{HR,ST}.csv
    one blank line, then  datetime,heartrate  /  datetime,steps  (NonFitbit adds a leading device column;
    Fitbit HR is every few seconds; steps list only minutes with steps)

Dates in both releases are shifted per participant, so only day offsets are meaningful.
Symptom-onset dates are NOT in the archives: they come from the papers' supplementary
tables and must be saved as labels.csv next to the data (see docs/data_notes.md).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from spacenormal.config import REPO_ROOT

RAW_P1 = REPO_ROOT / "data" / "raw" / "stanford_p1"
RAW_P2 = REPO_ROOT / "data" / "raw" / "stanford_p2"
LABEL_COLUMNS = ("participant_id", "symptom_onset_date")
NIGHT_HOURS = (0, 6)
MIN_NIGHT_MINUTES = 30


def participant_files(phase: int, root: Path | None = None) -> dict[str, dict[str, Path]]:
    """participant id -> {"hr": path, "steps": path}; only participants with both files."""
    out: dict[str, dict[str, Path]] = {}
    if phase == 1:
        base = (root or RAW_P1)
        for hr in sorted(base.rglob("*_hr.csv")):
            pid = hr.name[: -len("_hr.csv")]
            steps = hr.with_name(f"{pid}_steps.csv")
            if steps.exists():
                out[pid] = {"hr": hr, "steps": steps}
    elif phase == 2:
        base = (root or RAW_P2)
        for hr in sorted(base.rglob("Orig_*_HR.csv")):
            if "__MACOSX" in hr.parts:
                continue
            steps = hr.with_name(hr.name.replace("_HR.csv", "_ST.csv"))
            pid = hr.parent.name
            if steps.exists() and (pid not in out or "Orig_Fitbit" in hr.name):
                out[pid] = {"hr": hr, "steps": steps}  # prefer the Fitbit stream when both exist
    else:
        raise ValueError("phase must be 1 or 2")
    return out


def _read_stream(path: Path, value: str) -> pd.Series:
    """Minute-resolution series indexed by timestamp, whatever the release's layout."""
    df = pd.read_csv(path, skip_blank_lines=True, usecols=lambda c: c in ("datetime", value))
    ts = pd.to_datetime(df["datetime"], errors="coerce")
    series = pd.Series(pd.to_numeric(df[value], errors="coerce").to_numpy(), index=ts).dropna()
    series = series[series.index.notna()]
    grouped = series.groupby(series.index.floor("min"))
    return grouped.mean() if value == "heartrate" else grouped.sum()


def night_resting_hr(hr_path: Path, steps_path: Path) -> pd.DataFrame:
    """Daily night resting HR: mean heart rate 00:00-06:00 over minutes with zero steps.

    Returns columns date, night_rhr, night_minutes; nights with too few minutes are dropped.
    """
    hr = _read_stream(hr_path, "heartrate")
    hr = hr[(hr > 25) & (hr < 220)]
    steps = _read_stream(steps_path, "steps").reindex(hr.index).fillna(0)  # a minute absent from steps = no steps
    night = (hr.index.hour >= NIGHT_HOURS[0]) & (hr.index.hour < NIGHT_HOURS[1]) & (steps.to_numpy() == 0)
    rest = hr[night]
    daily = rest.groupby(rest.index.normalize()).agg(["mean", "size"])
    daily = daily[daily["size"] >= MIN_NIGHT_MINUTES]
    return pd.DataFrame({
        "date": daily.index, "night_rhr": daily["mean"].round(2).to_numpy(),
        "night_minutes": daily["size"].to_numpy(),
    }).reset_index(drop=True)


def load_labels(phase: int, root: Path | None = None) -> pd.DataFrame:
    """labels.csv: participant_id, symptom_onset_date (in the release's shifted dates)."""
    path = (root or (RAW_P1 if phase == 1 else RAW_P2)) / "labels.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Build it from the paper's supplementary table: one row per "
            f"positive participant with columns {LABEL_COLUMNS}.")
    labels = pd.read_csv(path, dtype={"participant_id": str})
    missing = [c for c in LABEL_COLUMNS if c not in labels.columns]
    if missing:
        raise ValueError(f"{path} is missing columns {missing}")
    labels["symptom_onset_date"] = pd.to_datetime(labels["symptom_onset_date"], errors="coerce")
    return labels.dropna(subset=["symptom_onset_date"]).reset_index(drop=True)


def split_participants(ids: list[str], seed: int, fractions=(0.4, 0.4, 0.2)) -> dict[str, list[str]]:
    """Deterministic tune / eval / demo split by participant."""
    order = np.random.default_rng(seed).permutation(sorted(ids))
    a = int(round(fractions[0] * len(order)))
    b = a + int(round(fractions[1] * len(order)))
    return {"tune": sorted(order[:a]), "eval": sorted(order[a:b]), "demo": sorted(order[b:])}
