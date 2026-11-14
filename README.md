# Space-Normal

Crew health monitoring that knows how a body under microgravity is *expected* to change, and alarms only on what is left over after removing the personal baseline, the expected adaptation for that day, and the effects of logged events. NASA Space Apps hackathon prototype.

- Spec: [`PLAN.md`](PLAN.md) · Summary: [`space-normal-summary.md`](space-normal-summary.md)
- **Status:** P0 (scaffold + synthetic fallback). No real data is loaded yet; every output so far is labelled `SYNTHETIC` and is not a result.

## Run

```bash
make setup            # Python 3.11 venv via uv, installs the package
make test             # pytest + hypothesis
make demo-synthetic   # synthetic missions -> model -> detectors -> web/public/cache/*.json, then validates them
```

## Layout

```
configs/            default.yaml (model, detector, synthetic priors) · scenarios.yaml · eval.yaml (splits) · priors_literature.yaml
src/spacenormal/
  data/             schema.py (daily / events / episodes tables) · synthetic.py (fallback generator)
  sim/interface.py  Mission + make_mission interface
  model/simple.py   baseline + adaptation prior x per-person scale + logged events -> residual z
  detect/           cusum.py (individual) · crew.py (outbreak)
  baselines.py      fixed thresholds · frozen baseline · rolling recalibration
  llm/              templated note with number verification · fixed checklists
  pipeline.py       mission -> contract JSON
  contract.py       pydantic mirror of web/src/contract.ts
scripts/            build_demo_cache.py · validate_contract.py
web/src/contract.ts the dashboard's data contract; web/public/cache/ holds the JSON it reads
```

## Data splits (fixed before any test data is read)

| Set | Subjects | Use |
|---|---|---|
| NASA bed rest Campaign 1 + Campaign 3 blocks A/C/D/E | 18 | Fit priors, event coefficients, thresholds |
| CFT70 (Campaign 11) | 3 with public daily vitals | Headline test, one crew of 3 |
| Campaign 3 blocks G + H | 8 | Second held-out test, two crews of 4 |

## Honesty

Bed rest is a ground analog, not spaceflight. Illness signatures come from Earth wearable data. Nothing here is validated on astronaut data, and this is decision support, not diagnosis. See `PLAN.md` section 17.
