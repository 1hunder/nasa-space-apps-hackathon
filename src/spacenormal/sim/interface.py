"""The mission interface. Generators implement `make_mission`; models never see `truth`.

This file is the ONLY thing the blind generator session (P5) is allowed to read.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class IllnessSpec:
    crew: int                 # index into the crew list
    onset: int | None = None  # in-bed day; None = random day after burn-in


@dataclass(frozen=True)
class SharedEventSpec:
    type: str
    day: int
    duration: int = 1


@dataclass(frozen=True)
class Scenario:
    name: str
    illness: tuple[IllnessSpec, ...] = ()
    shared_events: tuple[SharedEventSpec, ...] = ()

    @classmethod
    def from_dict(cls, name: str, spec: dict) -> "Scenario":
        return cls(
            name=name,
            illness=tuple(IllnessSpec(**i) for i in spec.get("illness") or []),
            shared_events=tuple(SharedEventSpec(**e) for e in spec.get("shared_events") or []),
        )


@dataclass
class Mission:
    """One crew, one mission.

    daily / events / episodes follow spacenormal.data.schema.
    truth (evaluation only): long table subject_id, study_day, vital,
        baseline, adaptation, events, illness, noise.
    provenance: {"adaptation": ..., "illness": ... | "NONE", "events": ...}.
    """

    mission_id: str
    scenario: str
    crew: list[str]
    daily: pd.DataFrame
    events: pd.DataFrame
    episodes: pd.DataFrame
    provenance: dict[str, str]
    truth: pd.DataFrame | None = field(default=None, repr=False)
    names: dict[str, str] = field(default_factory=dict)  # crew id -> display name (optional)
    # Optional finer-grained readings behind `daily`: subject_id, study_day, hour, <vitals>,
    # with each person's time-of-day pattern already removed. `daily` holds their daily means.
    hourly: pd.DataFrame | None = field(default=None, repr=False)


class MissionBuilder(Protocol):
    def __call__(self, crew: Sequence[str], scenario: Scenario, rng: np.random.Generator) -> Mission: ...
