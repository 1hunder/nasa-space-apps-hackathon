"""Templated flight-surgeon note. Every number comes from the decomposition; fail closed.

P0 ships the template and the number check. The LLM that writes connecting prose (P6)
must pass `verify_numbers` or the raw template is sent instead.
"""

from __future__ import annotations

import json
import re
from typing import Any

from spacenormal.llm.checklists import CHECKLISTS

VITAL_LABEL = {
    "pulse": ("pulse", "bpm"), "temp_c": ("body temperature", "°C"),
    "resp_rate": ("respiratory rate", "breaths/min"),
    "sbp": ("systolic BP", "mmHg"), "dbp": ("diastolic BP", "mmHg"),
}
# A number is a digit run not glued to a letter or another digit (so "C3" is not a number).
_NUMBER = re.compile(r"(?<![A-Za-z\d.])[-+]?\d+(?:\.\d+)?")


def _fmt(x: float, signed: bool = False) -> str:
    return f"{x:+.1f}" if signed else f"{x:.1f}"


def verify_numbers(text: str, allowed: set[str]) -> bool:
    """True only if every number in `text` appears, as printed, in `allowed`."""
    canon = {a.lstrip("+") for a in allowed}
    return all(tok.lstrip("+") in canon for tok in _NUMBER.findall(text))


def template_note(crew_id: str, day: int, vital: str, d: dict[str, float]) -> tuple[str, set[str]]:
    """`d` holds y, baseline, adaptation, events, residual, z for that crew, vital and day."""
    label, unit = VITAL_LABEL[vital]
    nums = {
        "z": _fmt(d["z"], True), "day": str(day), "y": _fmt(d["y"]), "baseline": _fmt(d["baseline"]),
        "adaptation": _fmt(d["adaptation"], True), "events": _fmt(d["events"], True),
        "residual": _fmt(d["residual"], True),
    }
    text = (
        f"Unexplained residual {nums['z']}σ on {label}, {crew_id}, day {nums['day']}. Non-diagnostic.\n"
        f"Observed {nums['y']} {unit}. Personal baseline {nums['baseline']}; expected adaptation "
        f"{nums['adaptation']}; logged events {nums['events']}; unexplained {nums['residual']}.\n"
        "Severity is set by the detector and cannot be lowered by this note."
    )
    return text, set(nums.values())


def build_note(crew_id: str, day: int, vital: str, d: dict[str, float],
               context_items: list[dict[str, str]]) -> dict[str, Any]:
    text, allowed = template_note(crew_id, day, vital, d)
    packet = {"crew": crew_id, "day": day, "vital": vital, "text": text,
              "d": {k: round(v, 2) for k, v in d.items()}}
    return {
        "text": text,
        "numbers_verified": verify_numbers(text, allowed),
        "bytes": len(json.dumps(packet, separators=(",", ":"), ensure_ascii=False).encode("utf-8")),
        "context_items": context_items,
        "questions": list(CHECKLISTS[vital]),
    }
