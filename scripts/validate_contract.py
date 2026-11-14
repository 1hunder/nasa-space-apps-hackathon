"""Validate every dashboard cache file against the contract.

    python scripts/validate_contract.py web/public/cache

Exits non-zero on the first invalid file. Runs in CI.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

from spacenormal.contract import Mission, MissionIndex


def validate_dir(cache: Path) -> list[str]:
    errors: list[str] = []
    index_path = cache / "missions.json"
    files = sorted(cache.glob("mission_*.json"))
    if not index_path.exists():
        return [f"{index_path}: missing"]
    try:
        index = MissionIndex.model_validate_json(index_path.read_text(encoding="utf-8"))
    except ValidationError as exc:
        return [f"{index_path}: {exc}"]
    if sorted(e.file for e in index.missions) != [f.name for f in files]:
        errors.append("missions.json does not list exactly the mission_*.json files present")
    for path in files:
        try:
            Mission.model_validate_json(path.read_text(encoding="utf-8"))
        except ValidationError as exc:
            errors.append(f"{path}: {exc}")
    return errors


def main() -> None:
    cache = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("web/public/cache")
    errors = validate_dir(cache)
    for e in errors:
        print(f"INVALID {e}", file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print(f"contract OK: {len(list(cache.glob('mission_*.json')))} mission files in {cache}")


if __name__ == "__main__":
    main()
