"""Build the static JSON the dashboard reads.

    python scripts/build_demo_cache.py --synthetic --out web/public/cache

Only the synthetic fallback exists so far; real-data caches arrive with P5.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path

import numpy as np

from spacenormal.config import load_config, load_scenarios
from spacenormal.contract import DETECTORS
from spacenormal.data import synthetic
from spacenormal.pipeline import run_pipeline
from spacenormal.sim.interface import Scenario


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic", action="store_true", help="use the synthetic fallback")
    parser.add_argument("--out", type=Path, default=Path("web/public/cache"))
    args = parser.parse_args()
    if not args.synthetic:
        raise SystemExit("Only --synthetic is available until real data is loaded (P1) and evaluated (P5).")

    cfg = copy.deepcopy(load_config())
    cfg["synthetic"]["gap_rate"] = 0.0  # the replay shows every day; missing readings are covered by the tests
    crew = [f"C{i + 1}" for i in range(cfg["mission"]["crew_size"])]
    args.out.mkdir(parents=True, exist_ok=True)

    index, rows = [], []
    for name, spec in load_scenarios().items():
        scenario = Scenario.from_dict(name, spec)
        rng = np.random.default_rng(spec["demo_seed"])
        raw = synthetic.make_mission(crew, scenario, rng, cfg)
        raw.names = dict(zip(crew, cfg["mission"]["crew_names"]))
        mission = run_pipeline(raw, cfg)
        file = f"mission_{mission.mission_id}.json"
        (args.out / file).write_text(mission.model_dump_json(), encoding="utf-8")
        index.append({"file": file, "mission_id": mission.mission_id, "scenario": mission.scenario,
                      "provenance": mission.provenance.model_dump()})
        red = Counter(a.detector for a in mission.alerts if a.level == "red")
        rows.append((name, [red.get(d, 0) for d in DETECTORS], len(mission.crew_alerts), len(mission.notes)))

    (args.out / "missions.json").write_text(json.dumps({"missions": index}, indent=2), encoding="utf-8")

    print("SYNTHETIC — illustrative missions with hand-picked seeds, not a result. Red alerts per detector:")
    print(f"{'scenario':<22}" + "".join(f"{d:>18}" for d in DETECTORS) + f"{'crew alerts':>13}{'notes':>7}")
    for name, counts, n_crew, n_notes in rows:
        print(f"{name:<22}" + "".join(f"{c:>18}" for c in counts) + f"{n_crew:>13}{n_notes:>7}")
    print(f"wrote {len(index)} missions + missions.json to {args.out}")


if __name__ == "__main__":
    main()
