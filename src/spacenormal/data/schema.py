"""Common tables shared by every data source.

daily:    one row per subject per study day.
events:   logged events (exercise sessions, schedule shifts, ...).
episodes: ground-truth or reported illness episodes.

study_day convention: pre-bed-rest days are negative (-1 is the last day before
tilt), in-bed days run 1..N, post-bed-rest days continue from N+1. `phase` carries
the same information explicitly.
"""

from __future__ import annotations

import pandas as pd

VITALS: tuple[str, ...] = ("pulse", "temp_c", "resp_rate", "sbp", "dbp")
PHASES: tuple[str, ...] = ("pre", "in", "post")
SOURCES: tuple[str, ...] = ("REAL_BEDREST", "REAL_EARTH_ILLNESS", "SYNTHETIC")

DAILY_COLUMNS: tuple[str, ...] = (
    "subject_id", "campaign", "phase", "study_day",
    *VITALS,
    "weight_kg", "room_temp_c", "room_rh", "group", "source",
)
EVENTS_COLUMNS: tuple[str, ...] = ("subject_id", "study_day", "event_type", "value")
EPISODES_COLUMNS: tuple[str, ...] = ("subject_id", "onset_day", "label_type", "pathogen", "source")

# Wide physiological plausibility limits; anything outside is a data error, not a finding.
PLAUSIBLE: dict[str, tuple[float, float]] = {
    "pulse": (25, 220),
    "temp_c": (33.0, 42.0),
    "resp_rate": (4, 60),
    "sbp": (60, 260),
    "dbp": (30, 160),
    "weight_kg": (30, 250),
    "room_temp_c": (5, 45),
    "room_rh": (0, 100),
}


class SchemaError(ValueError):
    pass


def _require_columns(df: pd.DataFrame, columns: tuple[str, ...], name: str) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise SchemaError(f"{name} table is missing columns: {missing}")


def validate_daily(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, DAILY_COLUMNS, "daily")
    bad_phase = set(df["phase"].unique()) - set(PHASES)
    if bad_phase:
        raise SchemaError(f"daily.phase has unknown values: {sorted(bad_phase)}")
    bad_source = set(df["source"].unique()) - set(SOURCES)
    if bad_source:
        raise SchemaError(f"daily.source has unknown values: {sorted(bad_source)}")
    if df.duplicated(["subject_id", "study_day"]).any():
        raise SchemaError("daily has duplicate (subject_id, study_day) rows")
    if (df.loc[df["phase"] == "pre", "study_day"] >= 0).any():
        raise SchemaError("pre-phase study_day must be negative")
    if (df.loc[df["phase"] == "in", "study_day"] < 1).any():
        raise SchemaError("in-phase study_day must start at 1")
    for col, (lo, hi) in PLAUSIBLE.items():
        values = df[col].dropna()
        if ((values < lo) | (values > hi)).any():
            raise SchemaError(f"daily.{col} has values outside [{lo}, {hi}]")
    return df


def validate_events(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, EVENTS_COLUMNS, "events")
    return df


def validate_episodes(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, EPISODES_COLUMNS, "episodes")
    return df


def empty_events() -> pd.DataFrame:
    return pd.DataFrame({c: [] for c in EVENTS_COLUMNS}).astype(
        {"subject_id": str, "study_day": int, "event_type": str, "value": float}
    )


def empty_episodes() -> pd.DataFrame:
    return pd.DataFrame({c: [] for c in EPISODES_COLUMNS}).astype(
        {"subject_id": str, "onset_day": int, "label_type": str, "pathogen": str, "source": str}
    )
