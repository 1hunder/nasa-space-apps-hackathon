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

Open the printed URL and press space. One replay takes about 13 seconds and stops when Space-Normal raises an alert: core temperature drifts above the "Earth normal" limit and out of the flat personal pre-flight range, both of which collect false alarms in this simulation, while it stays inside the moving Space-Normal range until illness starts. Readings are hourly; ranges and monitors work on daily means. The temperature and blood-pressure drifts follow published spaceflight findings; pulse is unchanged, as in flight. Time constants, illness sizes and event effects are assumptions (`docs/data_notes.md`, section 5).

- The default view shows only the chart, the two monitors and the crew list. "Show details" (or D) adds the other two monitors and the per-day breakdown; the alert card expands to the flight-surgeon note.
- The "Crew journal" row holds free-text entries (`configs/journal.yaml`). Click a mark to read the entry and how the assistant read it. The readings are mocked: no language model runs in the demo, and entries never raise or lower an alert.
- Keys: space play/pause, R restart, D details, arrow keys step one day. Two vitals are offered, core temperature (default) and pulse; the other three stay in the data and the detector. Click a point for that day's breakdown; drag on the chart to scrub. The replay stops when Space-Normal raises an alert; Play continues.
- The dashboard shows one scenario, `single_illness` ("One crew member falls ill"); there is no scenario picker. `?day=40` opens a specific day.
- `configs/scenarios.yaml` also defines `healthy_crew`, `outbreak` and `shared_event` for the pipeline and the tests. Only scenarios marked `demo: true` there are built into `web/public/cache/`.
- The cached mission is synthetic, with a seed picked by hand for a clean replay (`configs/scenarios.yaml`). It illustrates the idea; it is not a result.

### Credits

The Mars image behind the dashboard is "Global Color Views of Mars" (PIA00407), a Viking Orbiter mosaic, credit NASA/JPL/USGS. Its use does not imply NASA endorsement. The star field is generated in code. Typeface: Archivo (SIL Open Font License).

## Layout

```
configs/            default.yaml (model, detector, synthetic mock) · scenarios.yaml · journal.yaml · eval.yaml (splits) · priors_literature.yaml
src/spacenormal/
  config.py         YAML loading
  data/             schema.py · nlsp.py (NASA bed rest loader, test-set lock) · stanford.py (illness signatures) · synthetic.py (mock generator)
  sim/interface.py  Mission + make_mission interface
  model/simple.py   baseline + adaptation prior x per-person scale + logged events -> residual z
  detect/           cusum.py (individual) · crew.py (outbreak)
  baselines.py      Earth normal (fixed limits) · pre-flight range · rolling recalibration
  llm/              templated note with number verification · fixed checklists (no language model runs yet)
  priors/ eval/     empty so far (P2, P5)
  pipeline.py       mission -> contract JSON
  contract.py       pydantic mirror of web/src/contract.ts
scripts/            fetch_nlsp.py · build_stanford_labels.py · build_demo_cache.py · validate_contract.py
tests/              pytest + hypothesis
data/manifests/     what was fetched (raw data is never committed)
web/                React dashboard; web/src/contract.ts is its data contract, web/public/cache/ the JSON it replays
```

## Data splits (fixed before any test data is read)

| Set | Subjects | Use |
|---|---|---|
| NASA bed rest Campaign 1 + Campaign 3 blocks A/C/D/E | 18 | Fit priors, event coefficients, thresholds |
| CFT70 (Campaign 11) | 3 with public daily vitals | Headline test, one crew of 3 |
| Campaign 3 blocks G + H | 8 | Second held-out test, two crews of 4 |

## Honesty

Bed rest is a ground analog, not spaceflight. Illness signatures come from Earth wearable data. Nothing here is validated on astronaut data, and this is decision support, not diagnosis. See `PLAN.md` section 17.
