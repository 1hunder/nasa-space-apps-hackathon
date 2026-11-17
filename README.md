# Space-Normal

Crew health monitoring that knows how a body under microgravity is *expected* to change, and alarms only on what is left over after removing the personal baseline, the expected adaptation for that day, and the effects of logged events. NASA Space Apps hackathon prototype.

- Spec: [`PLAN.md`](PLAN.md) · Kontekst projektu (PL): [`docs/README.md`](docs/README.md) · Diagram: [`Space-Normal-architecture.png`](Space-Normal-architecture.png)
- **Status:** pipeline, NASA bed rest loader and demo dashboard work. The dashboard replays synthetic missions; every output so far is labelled `SYNTHETIC` and is not a result.

## Why Earth norms do not work in space

A healthy astronaut does not stay inside clinical reference ranges. After about two and a half
months in orbit, resting core temperature rises by roughly 1 °C and can approach 38 °C
([Stahn et al. 2017](https://doi.org/10.1038/s41598-017-15560-w), 11 astronauts). After landing,
5 of 13 astronauts met the WHO criteria for anemia
([Trudel et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8799460/)). Blood pressure drops,
cardiac output rises by about 41 % and resting pulse barely moves
(Norsk et al. 2015, J Physiol 593:573, 8 astronauts). None of this is illness.

A monitor built on hospital thresholds therefore fails in both directions: it fires on healthy
adaptation, and it stays quiet while a real change hides inside a range that is wrong for this
person on this day.

On a Mars transit that matters more than in low Earth orbit. A message takes up to 22 minutes one
way, the link can go silent for around two weeks near solar conjunction, there is no evacuation,
and NASA-STD-3001 does not require a physician on board. The crew has to make the first call
itself.

## The idea: a corridor instead of a line

A growth chart does not compare a child to the average adult. It compares the child to where that
child is expected to be at that age. Space-Normal does the same for an astronaut: a personal
corridor of expected values that bends with the day of the mission.

For every vital sign and every day, the model builds the expectation from four parts:

1. the person's own pre-flight baseline,
2. the adaptation expected on that mission day, scaled to how strongly this person adapts,
3. the logged events of the day — the workout, the shifted sleep schedule, the cabin CO2,
4. the spread that is normal between people.

What is left after subtracting all of it is the **residual**. The detector only ever looks at the
residual, so planned exercise is *explained* rather than alarmed. A CUSUM accumulates small
persistent deviations into an amber or red alert, and a crew layer raises a separate alert when
several crew members drift together with no logged event to explain it.

The dashboard shows the corridor next to the two baselines it competes with: `Earth normal` (the
same clinical thresholds for everyone) and `Pre-flight range` (a flat personal band from the days
before the mission, the idea behind NASA's own CDSS concept). Both are flat. Only the corridor
bends.

## What each user gets

- **The astronaut** gets a card with three lines: OBSERVATION (what we see, in their own numbers),
  CHECK NOW (a one-minute action), ESCALATE IF (the condition that sends it further). It always
  ends with "Not a diagnosis."
- **The Crew Medical Officer** — a crew member with short medical training, not a physician — sees
  the whole crew and the outbreak layer.
- **The flight surgeon on Earth** gets a small queued packet, and only when someone actually leaves
  their corridor.

## Two rules the code enforces

**No language model raises an alarm.** Severity comes from a deterministic statistic that runs
offline. A model may only phrase the sentence, and every number it writes is verified against the
data before the note is sent; if verification fails, the plain template goes out instead. A model
can never raise, lower or delay an alert.

**The held-out test set is locked in code.** `src/spacenormal/data/nlsp.py` raises `TestSetLocked`
for CFT70 and Campaign 3 blocks G/H until `docs/claims.md` contains a configuration hash, which
only the evaluation step writes. Tuning on the test set is not a matter of discipline here; the
loader refuses.

## Run

```bash
make setup            # Python 3.11 venv via uv, installs the package
make test             # pytest + hypothesis
make demo-synthetic   # synthetic missions -> model -> detectors -> web/public/cache/*.json, then validates them
```

## Dashboard

Live: https://spacenormal.vercel.app. The dashboard is a static Vite build (`cd web && npm run build` writes `web/dist/`), so any static host will serve it.

```bash
make demo-synthetic          # writes the JSON the dashboard reads
cd web && npm install && npm run dev
```

## Pitch deck

[`pitch/index.html`](pitch/index.html) is the deck we present — one self-contained cinematic file, fully offline (GSAP and the clips live in `pitch/vendor/` and `pitch/assets/`). Open it in a browser; no build step.

```bash
open pitch/index.html
```

Keys: `→` / space / click next · `←` back · `F` fullscreen · `P` presenter notes window · `T` rehearsal timer · `R` reset it · `1`–`8` jump to a slide. The first press plays the intro; the address hash is `#slide.beat`, so a rehearsal resumes where it stopped.

Every slide's text lives in the `CONFIG` object at the top of the script, speaker notes included — edit there, not in the markup. The app link shown in the corner and on the closing slide comes from the single `APP_URL` constant. Spoken script, synced click by click: [`pitch/SKRYPT.md`](pitch/SKRYPT.md). Slide list and editing rules: [`docs/03-pitch-i-film.md`](docs/03-pitch-i-film.md) section 2.


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
