import json
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from spacenormal.contract import DETECTORS, Mission
from spacenormal.pipeline import run_pipeline

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def single(make, cfg):
    return make("transplant_single", 1), run_pipeline(make("transplant_single", 1), cfg)


def test_pipeline_output_matches_contract(single):
    _, out = single
    assert out.days == list(range(1, 71))
    assert [c.id for c in out.crew] == ["C1", "C2", "C3", "C4"]
    assert set(a.detector for a in out.alerts) <= set(DETECTORS)
    assert out.provenance.adaptation == "SYNTHETIC"


def test_no_space_normal_red_during_burn_in(make, cfg):
    for seed in range(5):
        out = run_pipeline(make("real_null", seed), cfg)
        assert not [a for a in out.alerts if a.detector == "space_normal" and a.level == "red" and a.day <= 3]


def test_missing_days_become_null_not_numbers(single):
    mission, out = single
    gaps = int(mission.daily.query("phase == 'in'")["pulse"].isna().sum())
    nulls = sum(v is None for c in out.crew for v in c.vitals["pulse"].y)
    assert nulls == gaps > 0


def test_every_red_space_normal_alert_has_a_verified_note(single):
    _, out = single
    reds = [a for a in out.alerts if a.detector == "space_normal" and a.level == "red"]
    assert set(out.notes) == {a.id for a in reds}
    assert all(n.numbers_verified for n in out.notes.values())


def test_planted_illness_is_flagged_on_most_seeds(make, cfg):
    """Smoke check on SYNTHETIC data only: the ill crew member goes red near onset."""
    hits = 0
    for seed in range(10):
        m = make("transplant_single", seed)
        ep = m.episodes.iloc[0]
        out = run_pipeline(m, cfg)
        hits += any(
            a.detector == "space_normal" and a.level == "red" and a.crew_id == ep.subject_id
            and ep.onset_day - 7 <= a.day <= ep.onset_day + 3
            for a in out.alerts
        )
    assert hits >= 8


def test_outbreak_scenario_raises_a_crew_alert_on_most_seeds(make, cfg):
    fired = sum(bool(run_pipeline(make("transplant_outbreak", s), cfg).crew_alerts) for s in range(10))
    assert fired >= 8


def test_contract_rejects_broken_files(single):
    _, out = single
    good = json.loads(out.model_dump_json())
    Mission.model_validate(good)

    for mutate in (
        lambda m: m["crew"][0]["vitals"]["pulse"]["baseline"].pop(),
        lambda m: m["crew"][0]["vitals"].pop("dbp"),
        lambda m: m["alerts"].append({**m["alerts"][0], "id": "x", "crew_id": "nobody"}),
        lambda m: m["notes"].update({"missing-alert": next(iter(m["notes"].values()))}),
        lambda m: m.update({"extra_number": 42}),
        lambda m: m["provenance"].update({"adaptation": "REAL_ASTRONAUT"}),
    ):
        bad = json.loads(json.dumps(good))
        mutate(bad)
        with pytest.raises(ValidationError):
            Mission.model_validate(bad)


def test_demo_cache_builds_and_validates(tmp_path):
    py = sys.executable
    subprocess.run([py, "scripts/build_demo_cache.py", "--synthetic", "--out", str(tmp_path)],
                   cwd=REPO, check=True, capture_output=True)
    result = subprocess.run([py, "scripts/validate_contract.py", str(tmp_path)],
                            cwd=REPO, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

    (tmp_path / "mission_synthetic_real_null.json").write_text("{}")
    result = subprocess.run([py, "scripts/validate_contract.py", str(tmp_path)],
                            cwd=REPO, capture_output=True, text=True)
    assert result.returncode == 1
