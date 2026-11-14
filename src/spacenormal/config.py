"""Config loading. All experiment settings live in configs/*.yaml."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "configs"


def _load(name: str) -> dict[str, Any]:
    with open(CONFIG_DIR / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=None)
def load_config() -> dict[str, Any]:
    return _load("default.yaml")


@lru_cache(maxsize=None)
def load_scenarios() -> dict[str, Any]:
    return _load("scenarios.yaml")


@lru_cache(maxsize=None)
def load_eval_config() -> dict[str, Any]:
    return _load("eval.yaml")
