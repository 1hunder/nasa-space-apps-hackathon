# Space-Normal

Crew health monitoring that knows how a body under microgravity is *expected* to change, and alarms only on what is left over after removing the personal baseline, the expected adaptation for that day, and the effects of logged events. NASA Space Apps hackathon prototype.

- Spec: [`PLAN.md`](PLAN.md) · Kontekst projektu (PL): [`docs/README.md`](docs/README.md)
- **Status:** pipeline, NASA bed rest loader and demo dashboard work. The dashboard replays synthetic missions; every output so far is labelled `SYNTHETIC` and is not a result.

## Run

```bash
make setup            # Python 3.11 venv via uv, installs the package
make test             # pytest + hypothesis
make demo-synthetic   # synthetic missions -> model -> detectors -> web/public/cache/*.json, then validates them
```

## Dashboard

Live: https://spacenormal.vercel.app. Every push to `main` redeploys it (`.github/workflows/deploy-vercel.yml`, needs the `VERCEL_TOKEN` repo secret); manual deploy: `cd web && npx vercel deploy --prod`.

```bash
make demo-synthetic          # writes the JSON the dashboard reads
cd web && npm install && npm run dev
```

Open the printed URL and press space. One replay takes about 15 seconds: core temperature drifts out of the flat "Earth normal" band while the Earth-calibrated monitor collects false alarms, stays inside the moving Space-Normal range, then leaves it when illness starts. Readings are hourly; ranges and monitors work on daily means. The size of each drift follows published spaceflight findings (`docs/data_notes.md`, section 5).

- The default view shows only the chart, the two monitors and the crew list. "Show details" (or D) adds the other two monitors and the per-day breakdown; the alert card expands to the flight-surgeon note.
- The "Crew journal" row holds free-text entries (`configs/journal.yaml`). Click a mark to read the entry and how the assistant read it. The readings are mocked: no language model runs in the demo, and entries never raise or lower an alert.
- Keys: space play/pause, R restart, D details, arrow keys step one day, 1–4 switch scenario. Click a point for that day's breakdown; drag on the chart to scrub. The replay stops when Space-Normal raises an alert; Play continues.
- `?scenario=transplant_outbreak&day=40` opens a specific moment.
- The four cached missions are synthetic, with seeds picked by hand for a clean replay (`configs/scenarios.yaml`). They illustrate the idea; they are not results.

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
