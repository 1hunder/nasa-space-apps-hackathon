"""Pydantic mirror of web/src/contract.ts. The UI shows no number that is not in this JSON."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

from spacenormal.data.schema import VITALS

Provenance = Literal["REAL_BEDREST", "REAL_EARTH_ILLNESS", "SYNTHETIC"]
State = Literal["expected", "event", "unexplained", "crew", "not_monitored"]
Level = Literal["yellow", "red"]
Truth = Literal["hit", "false_alarm", "near_episode"]
DETECTORS: tuple[str, ...] = ("fixed_thresholds", "frozen_baseline", "rolling_14", "space_normal")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class VitalSeries(_Strict):
    y: list[float | None]          # daily mean; null = no measurement that day
    y_hourly: list[float | None]   # samples_per_day readings per day, time-of-day pattern removed
    baseline: list[float]
    adaptation: list[float]
    events: list[float]
    residual: list[float | None]
    z: list[float | None]
    band_low: list[float]
    band_high: list[float]
    earth_low: list[float]         # fixed band around the pre-mission baseline
    earth_high: list[float]


class SystemsDay(_Strict):
    day: int
    cardio: State
    resp: State
    thermo: State
    fluids: State


class CrewMember(_Strict):
    id: str
    name: str                      # display name; equals id when none is given
    group: str
    vitals: dict[str, VitalSeries]
    systems: list[SystemsDay]


class Alert(_Strict):
    id: str
    detector: str
    crew_id: str
    day: int
    level: Level
    vital: str
    z: float
    truth: Truth                   # scored against known episodes; false_alarm when there are none nearby


class MissionEvent(_Strict):
    day: int
    type: str
    crew_ids: list[str]


class Episode(_Strict):
    crew_id: str
    onset_day: int
    provenance: Provenance


class CrewAlert(_Strict):
    day: int
    crew_ids: list[str]
    onsets: list[int]


class ContextItem(_Strict):
    text: str
    source_ref: str


class Note(_Strict):
    text: str
    numbers_verified: bool
    bytes: int
    context_items: list[ContextItem]
    questions: list[str]


class MissionProvenance(_Strict):
    adaptation: Provenance
    illness: Provenance | Literal["NONE"]
    events: Provenance


class Mission(_Strict):
    mission_id: str
    scenario: str
    days: list[int]
    samples_per_day: int           # length of y_hourly = len(days) * samples_per_day
    provenance: MissionProvenance
    crew: list[CrewMember]
    events: list[MissionEvent]
    alerts: list[Alert]
    crew_alerts: list[CrewAlert]
    episodes: list[Episode]
    notes: dict[str, Note]

    @model_validator(mode="after")
    def _consistent(self) -> "Mission":
        n, day_set = len(self.days), set(self.days)
        if self.days != sorted(day_set):
            raise ValueError("days must be strictly increasing")
        crew_ids = {c.id for c in self.crew}
        if len(crew_ids) != len(self.crew):
            raise ValueError("duplicate crew ids")
        for member in self.crew:
            if set(member.vitals) != set(VITALS):
                raise ValueError(f"{member.id}: vitals must be exactly {VITALS}")
            for name, series in member.vitals.items():
                for field, values in series:
                    if field == "y_hourly":
                        if len(values) != n * self.samples_per_day:
                            raise ValueError(f"{member.id}.{name}.y_hourly: wrong length")
                        continue
                    if len(values) != n:
                        raise ValueError(f"{member.id}.{name}.{field}: length {len(values)} != {n} days")
            if [s.day for s in member.systems] != self.days:
                raise ValueError(f"{member.id}: systems must have one entry per day")
        alert_ids = set()
        for a in self.alerts:
            if a.id in alert_ids:
                raise ValueError(f"duplicate alert id {a.id}")
            alert_ids.add(a.id)
            if a.crew_id not in crew_ids or a.day not in day_set:
                raise ValueError(f"alert {a.id} refers to an unknown crew member or day")
            if a.detector not in DETECTORS:
                raise ValueError(f"alert {a.id}: unknown detector {a.detector}")
            if a.vital not in VITALS:
                raise ValueError(f"alert {a.id}: unknown vital {a.vital}")
        for e in self.events:
            if not set(e.crew_ids) <= crew_ids:
                raise ValueError(f"event on day {e.day} refers to unknown crew")
        for ca in self.crew_alerts:
            if not set(ca.crew_ids) <= crew_ids or len(ca.crew_ids) != len(ca.onsets):
                raise ValueError(f"crew alert on day {ca.day} is inconsistent")
        for ep in self.episodes:
            if ep.crew_id not in crew_ids:
                raise ValueError(f"episode refers to unknown crew member {ep.crew_id}")
        if not set(self.notes) <= alert_ids:
            raise ValueError("notes must be keyed by existing alert ids")
        return self


class MissionIndexEntry(_Strict):
    file: str
    mission_id: str
    scenario: str
    provenance: MissionProvenance


class MissionIndex(_Strict):
    missions: list[MissionIndexEntry]
