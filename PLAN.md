# Space-Normal — implementation plan for Claude Code (v2.1: NASA bed rest data + dashboard spec)

> **Update 2026-11-15 (read first):** product direction and priorities changed after research. Mission framing = crewed Mars transit (22 min one-way delay, not 24); primary user = astronaut, then Crew Medical Officer. Headline comparison stays vs the best baseline. UI priority = frames for the 30 s video + public link; Proof screen and 3-minute dashboard demo are optional (the live talk has no screen). See `AGENTS.md` and `docs/01-produkt-i-zakres.md` §4 (Polish) for the full delta; `docs/05-stan-prac.md` for current status.

## Kickoff prompt (paste this into Claude Code)

> Read `PLAN.md` (this file) fully before writing code. Implement Space-Normal phase by phase, in the order given in "Phases". At the end of each phase, run the tests, show me the acceptance-criteria results, and wait for my go-ahead before the next phase.
> Ground rules:
> - Never invent data or results. If a dataset is missing, use the synthetic fallback and label every output "SYNTHETIC".
> - Don't download gated datasets or accept terms on my behalf. Tell me what access is needed.
> - Keep CFT70 (Campaign 11) as the test set: never use it for fitting priors or tuning thresholds.
> - Write the blind synthetic generator (Phase 5) in a fresh session or subagent that sees only the generator interface. It must never see the model code.
> - Keep everything reproducible: seeded RNG, configs in YAML, one command per experiment.

---

## 1. Goal

Build a prototype of **Space-Normal**: crew health monitoring that knows how a body under microgravity is *expected* to change. It alarms only on what is left over after removing:

1. the person's baseline,
2. the expected adaptation for that day,
3. effects of logged events.

It also raises a separate **crew-wide outbreak alert** when several crew drift together and no logged event explains it.

**What changed in v2:** adaptation now comes from **real NASA head-down-tilt bed rest data** (daily vitals from the NASA Life Sciences Portal), not only literature. The model is fitted on bed rest Campaigns 1 and 3 and tested on CFT70 (Campaign 11), which it never sees. Illness signatures still come from real Earth wearable data (Stanford), because bed rest subjects are screened-healthy volunteers.

**Deliverables:** a Python package, an evaluation harness with 4 evaluation tracks, a templated LLM flight-surgeon note and context-only triage agent, and a Streamlit demo on cached results.

**Non-goals:** diagnosis, any claim of validation on astronaut data, real-time hardware integration.

**Claim we are allowed to make:** "On real NASA bed rest data never used for fitting, Space-Normal produced X false alarms per crew-month during adaptation, against Y for the best rolling baseline, and detected Z% of transplanted real illness signatures. Bed rest is a ground analog; this has not been tested on astronaut data."

## 2. Frozen design decisions (from independent review — do not change without asking)

| Area | Decision |
|---|---|
| Core signals | Daily spot vitals from bed rest: pulse, body temperature, respiratory rate, systolic/diastolic BP. Weight and fluid balance are context. |
| Wearable signals | Stanford night resting HR, steps and sleep are used only to extract real illness signatures (and in an optional stretch "wearable mode"). HRV is dropped: no reachable dataset has it. |
| Shared / event factor | ONLY logged covariates: room temperature/humidity (real, from bed rest), exercise-group sessions (real, CFT70), and schedule events (synthetic). Coefficients are fixed before the test period. **Never** subtract a crew median, because it masks outbreaks. A leave-one-out crew median is a diagnostic only. |
| Per-person adaptation scale | Prior N(1, 0.4²), bounded [0.3, 2]. Fitted only on days 4–21, excluding flagged days. Frozen from day 21. Score on the pre-update residual. |
| Burn-in | First 3 days of head-down tilt (acute fluid shift; in flight, motion sickness): no red alerts, reported separately. |
| Detector | One-sided CUSUM. No neural nets; LightGBM appears only as an optional ablation. |
| LLM | Never fires, delays or lowers an alarm. Final severity = max(detector, agent), enforced in types and code. The note is templated, with every number from data. Priors are fitted from data plus a hand-checked literature table. Weak labels: cut. |
| Evaluation | Fit on Campaigns 1 + 3, test on CFT70. Real-null false alarms (no injection) are the headline. Transplanted real illness signatures give sensitivity. A blind synthetic generator handles robustness. Fair baselines include rolling recalibration. Every detector is compared at a matched false-alarm budget. |

## 3. Stack

- Python 3.11: pandas, numpy, scipy, statsmodels, pydantic v2, pyyaml, requests, matplotlib (static report plots), pytest, hypothesis.
- UI: React 18 + Vite + TypeScript, Tailwind, visx (or Recharts) for charts, Framer Motion for replay transitions. It reads static JSON exported by `scripts/build_demo_cache.py`, so no backend is needed for the demo; FastAPI is optional. Stretch only: react-three-fiber for a 3D body.
- Optional: filterpy (Kalman stretch goal), lightgbm (ablation), anthropic SDK (LLM layer). The model comes from env var `SN_LLM_MODEL`. An offline stub runs when `ANTHROPIC_API_KEY` is absent.

## 4. Repo layout

```
space-normal/
  README.md  PLAN.md  pyproject.toml  Makefile
  configs/ default.yaml  priors_literature.yaml  scenarios.yaml  eval.yaml
  data/ (gitignored) raw/{nlsp,stanford_p1,stanford_p2,homekit,osdr}  processed/  cache/  manifests/
  docs/ data_notes.md  model_card.md  claims.md
  src/spacenormal/
    data/      schema.py  nlsp.py  stanford.py  homekit.py  osdr.py  radlab.py  synthetic.py
    features.py
    priors/    fit_bedrest.py  literature.py
    sim/       interface.py  transplant.py  crews.py  generator_dev.py  generator_blind.py  scenarios.py
    model/     baseline.py  adaptation.py  events.py  simple.py  kalman.py
    detect/    cusum.py  crew.py
    baselines.py
    eval/      tracks.py  metrics.py  plots.py  ablations.py
    llm/       schemas.py  checklists.py  triage.py  note.py  stub.py
  web/       (React app)
    src/ contract.ts  state/  components/{CrewStrip,BodyMap,CorridorChart,DecompositionBars,AlarmLanes,EventTimeline,AlertDrawer,OutbreakBanner,ReplayBar,ProvenanceBadge}  screens/{MissionControl,Proof,DataHonesty}
    public/cache/  (mission_*.json, eval.json, claims.json, datasets.json)
  scripts/ fetch_nlsp.py  run_eval.py  build_demo_cache.py  hash_config.py  validate_contract.py
  tests/
```

## 5. Data layer

**Common schema** (`data/schema.py`): one daily table:

```
subject_id, campaign, phase (pre|in|post), study_day (BR-day or flight day),
pulse, temp_c, resp_rate, sbp, dbp, weight_kg, room_temp_c, room_rh,
group (control|exercise|exercise_testosterone|...), source
```

plus an `events` table:

```
subject_id, study_day, event_type, value
```

and an `episodes` table:

```
subject_id, onset_day, label_type, pathogen, source
```

### Sources

1. **NASA bed rest via the NASA Life Sciences Portal (primary for adaptation).**
   - Campaigns 1 and 3 (and 5 if released): fitting set.
   - CFT70 (Campaign 11, 70-day 6° head-down tilt): test set.
   - Target files: per-subject daily vitals ("Medical Status and Vitals": BP, respiratory rate, pulse, body temperature, weight, plus daily room temperature and humidity), water intake/output, CFT70 medical and medication logs (`CRF_CFT70_MEDLOG_*`, `CRF_CFT70_FARUMEDLOGS_FINAL`), meals, and group assignment.
   - **Access:** the portal is JavaScript-rendered. Per-subject CSVs are reported to be unauthenticated downloads behind a JSON API (see the open project `MiladBahariQaragoz/BedrestToMars`, which has an NLSP fetcher). Write `scripts/fetch_nlsp.py`:
     1. discover the API calls (inspect the portal's network requests, or reuse that project's approach);
     2. download into `data/raw/nlsp/`;
     3. write `data/manifests/nlsp.json` with each file's UUID and SHA-256.
     If the API can't be reached from your environment, stop and ask me to download manually.
   - **First task: inventory.** Before any modelling, list which campaigns actually have daily vitals, how many subjects each has, the BR-day range, missingness, and units. Read the medical/medication logs and record whether they contain symptom or illness events. Put it all in `docs/data_notes.md` and **show me before Phase 2**.
2. **Stanford COVID-19 Wearables, Phase 1 + Phase 2** (illness signatures). Raw HR, steps, sleep, self-reported symptom dates; 32 + 84 positives. Get the URLs from the papers' data availability statements; I download them manually into `data/raw/stanford_p*/`.
3. **Homekit2020 (optional).** PCR-confirmed flu. Synapse access requires identity verification and may not arrive. Use only if present.
4. **Literature priors** (`configs/priors_literature.yaml`): hand-checked, cited rows for what bed rest cannot provide: in-flight core temperature rise ("space fever"), sleep loss, motion sickness. Used only in "flight mode" synthetic scenarios.
5. **ISS context (optional):** OSDR Environmental Data App (manual CSV export of cabin CO2) and the RadLab API (`https://visualization.osdr.nasa.gov/radlab/api`, CSV/JSON). Dashboard context only; no assumed physiological effect.
6. **Synthetic fallback** (`data/synthetic.py`): bed-rest-like daily vitals plus illness bumps, so the pipeline runs with zero real data. Everything it produces is labelled SYNTHETIC.

### Splits

- **Fit:** NLSP Campaigns 1, 3 (and 5).
- **Test:** CFT70, never used for fitting or tuning.
- **Illness signatures:** Stanford positives split by participant into tune / eval / demo.

## 6. Features (`features.py`)

- **Bed rest, daily:** pulse, temp_c, resp_rate, sbp, dbp. Weight and fluid balance are context only.
- **Baseline:** the pre-bed-rest days (median and MAD; at least 7 valid days). The baseline is short (~10–13 days), so inflate σ with a small-sample correction.
- **Stanford, for illness signature extraction:** night resting HR (mean HR 00:00–06:00 on zero-step minutes), each person's 28-day causal median baseline, and the deviation series ΔHR(d) for d = −14…+21 days around symptom onset. Save the signatures as `data/processed/illness_signatures.parquet`.

## 7. Adaptation priors (`priors/`)

**`fit_bedrest.py`**: for each vital, on Campaigns 1 + 3 only:
1. Compute each subject's change from baseline by BR-day.
2. Fit a population curve g_f(day): try exponential approach, two-phase and piecewise-linear, and choose by leave-one-subject-out error.
3. Estimate the between-person spread of amplitude and τ. **This is the person-to-person SD that no flight paper reports.**
4. Write `data/processed/priors_bedrest.json`, with plots in `docs/`.

**Flight vs analog:** bed rest is not flight. Note known differences in `docs/model_card.md` (in-flight resting HR is roughly unchanged vs preflight supine; core temperature rises ~1 °C in flight per Stahn 2017; bed rest has no motion sickness). **Analog mode** uses bed rest priors. **Flight mode** (synthetic only) layers the literature rows on top.

## 8. Mission builder (`sim/`)

`sim/interface.py` defines `make_mission(crew, scenario, rng) -> Mission`. A `Mission` holds per-person daily vitals, the true components (evaluation only), event logs and ground-truth episodes.

- **`crews.py`:** pseudo-crews of 4 bed rest subjects from the same campaign, aligned by BR-day. They were not physically co-located, so shared schedule events are synthetic and logged. Room climate is real, per subject.
- **`transplant.py`:** add a real Stanford ΔHR illness signature to a bed rest subject's daily pulse at a random in-bed onset day (after the burn-in), scaled by the ratio of the subjects' baseline SDs.
  - Temperature and respiratory-rate illness bumps come from cited literature and are labelled synthetic. Stanford has neither.
  - Also run a **pulse-only track**, so one result uses no synthetic illness component.
- **`generator_dev.py`:** fully synthetic missions for robustness, drawing adaptation curves around the bed rest priors with heavy-tailed noise and gaps.
- **`generator_blind.py`:** written in Phase 5 by a session that never sees model code. It uses different shapes (logistic, overshoot, two-phase), per-person scale 0.5–2×, and different noise.
- **Scenarios** (`configs/scenarios.yaml`):

  | Scenario | What it tests |
  |---|---|
  | `real_null` | Real CFT70, nothing injected. |
  | `transplant_single` | 1 of 4 crew gets an illness. |
  | `transplant_outbreak` | 2–3 crew get illnesses, onsets staggered 1–4 days. |
  | `shared_event` | Synthetic schedule shift for all 4 crew; must not alert. |
  | `misspec_sweep` | Amplitude 0–2×, τ ⅓–3×, plus a wrong-sign case. |
  | `flight_mode` | Literature space-fever, sleep and motion-sickness layers. |

## 9. Model — Space-Normal (simple version first)

For each person and vital *f*:

1. **Baseline:** pre-bed-rest median and MAD.
2. **Adaptation:** prior g_f(day) from `priors_bedrest.json`.
3. **Per-person scale** ŝ_f: Huber fit on days 4–21, excluding days with |z|>2. Shrink toward 1, bound to [0.3, 2], freeze after day 21.
4. **Event term** βᵀe_t: room temperature/humidity, exercise sessions and logged schedule events. β is fitted on the fit campaigns, then fixed.
5. **Residual:** z_t = (y_t − baseline − ŝ·g(day) − βᵀe_t) / σ_t, where σ_t is the baseline MAD × 1.4826, inflated by the prior spread in early days.
6. **Output per day:** `{baseline, adaptation, events, residual, z, band_low, band_high}`.

**Stretch** (`model/kalman.py`): the same model as a Kalman filter with state [ℓ, s], a gated update (skip it when z>2 in the illness direction), and innovation z. Same interface as `simple.py`.

## 10. Detection

**Individual** (`detect/cusum.py`):

- S_t = max(0, S_{t−1} + z̃_t − k), with k = 0.5.
- z̃_t is a signature-weighted sum of z over pulse (main), temperature and respiratory rate.
- **Yellow** at S ≥ 3. **Red** at S ≥ h (default 5).
- No red alerts in the first 3 days.
- Calibrate h on the fit campaigns plus the Stanford tune set to **≤1 red false alarm per crew-month**.

**Crew layer** (`detect/crew.py`):

- **Outbreak alert** when ≥2 crew have residual z>1.5 within 4 days of each other, the onsets are not all on the same day, and no logged event explains the shift.
- **Contagion boost:** when one person goes red, lower crewmates' h by 1 for 7 days.

## 11. Baselines (`baselines.py`) — same CUSUM machinery, matched false-alarm budget

1. **Fixed clinical thresholds.**
2. **Frozen pre-bed-rest baseline**, no adaptation model.
3. **Rolling recalibration**, windows W = 7, 14, 28 days.
4. **Space-Normal without the crew layer** (ablation).

## 12. Evaluation (`eval/tracks.py`) — all on CFT70 unless stated

| Track | Data | Measures |
|---|---|---|
| **A: real null (headline)** | Real CFT70 adaptation, nothing injected | Red false alarms per crew-month for every detector, overall and by BR-day |
| **B: transplant** | CFT70 + real Stanford illness signatures, ≥200 Monte Carlo missions | Episode sensitivity, lead time, sensitivity at matched false-alarm budget; pulse-only sub-track |
| **C: robustness** | Blind synthetic generator + misspec sweep + outbreak + shared event + flight mode | Where Space-Normal degrades (crossover point) |
| **D: real events (if any)** | Symptom/medication events found in the CFT70 medical logs | Case studies: what each detector would have flagged. No statistics if the count is tiny. |

**Scoring rules:**

- **Hit:** ≥1 red alert in [onset − 7, onset + 3]. Lead time = onset − first red alert.
- **False alarm:** a red alert >21 days from any episode, normalized per crew-month.
- **CIs:** bootstrap 95% by subject. Report chance-level sensitivity for the window size.

**Plots:**

- **A:** false alarms by BR-day on the real null (Track A).
- **B:** sensitivity vs false alarms per crew-month (Track B).
- **C:** false alarms at 80% sensitivity vs prior error (Track C).
- **D:** ablation table (no adaptation / no events / no crew layer).

**Headline number:** Track A real-null false alarms per crew-month for Space-Normal vs the best rolling baseline, quoted with Track B sensitivity at that budget.

**Freeze:** `scripts/hash_config.py` writes the hash of configs + model code into `docs/claims.md` **before** any CFT70 run.

## 13. LLM layer (`llm/`) — unchanged from v1

**Flight-surgeon note** (`note.py`):

- A template whose numbers all come from the decomposition JSON; the LLM writes only connecting prose.
- The first line is "Unexplained residual Xσ on <vital>, <person>, day N. Non-diagnostic."
- A regex check verifies every number against the source JSON. Fail closed: if it fails, send the raw template.

**Triage agent** (`triage.py`):

- Runs **in parallel**; the alert is delivered whether or not the agent finishes.
- Tools: read the event log, room climate and notes.
- Output schema: `{context_items:[{text, source_ref, label:"unverified contributor"}], escalate: bool, questions:[str]}`. There is no field that can lower severity. Final severity = max(detector, agent).
- Questions come from a fixed per-vital checklist; the LLM only phrases them.

**Tests:**

- 50 planted illness cases, each with a same-day benign cause. **False suppression must be 0/50**.
- Dismissal-rate rubric.
- 100% number fidelity.

**Offline stub** (`stub.py`): deterministic outputs for runs without an API key.

## 14. Dashboard UI — designed to show our strongest points

### 14.1 Principle

The UI is the demo engine. Every screen must prove one of our six strongest points, using numbers read from data:

| # | Strong point | Where the UI proves it |
|---|---|---|
| 1 | Real NASA data (bed rest CFT70, never used in fitting) + real illness signatures | Provenance badges on every chart; Data & Honesty screen; config hash |
| 2 | The core idea: expected-adaptation corridor and decomposition | Corridor chart + decomposition bars (hero of Mission Control) |
| 3 | Crew as each other's control: environment vs individual vs outbreak | Crew strip of 4 body maps + outbreak banner |
| 4 | Fewer false alarms than fair baselines, at matched sensitivity | Alarm lanes during replay + Proof screen |
| 5 | Safe-by-design LLM (cannot suppress; 0/50; number fidelity) | Alert drawer: severity lock, test badges, templated note |
| 6 | Honesty: what we don't monitor, where we lose | Grey "not monitored" systems; Proof screen shows the crossover plot |

### 14.2 Screens

**A. Mission Control** (the main demo screen, 16:9, one view, no scrolling at 1440×900):

1. **Top bar.**
   - Mission clock "Day 41 / 70" with replay controls: play/pause, 1×/4×/16× speed, scrubber, and bookmark chips for key moments (burn-in, shared event, illness onset −3, outbreak).
   - Scenario picker: real_null, transplant_single, transplant_outbreak, shared_event, flight_mode.
   - Mode chip: "ANALOG · NASA bed rest CFT70" or "FLIGHT MODE · synthetic layers".
2. **Crew strip.** Four crew cards, each showing:
   - a small 2D body systems map, colored per system for the current day;
   - a status ring;
   - a 14-day residual sparkline;
   - a group tag (exercise/control).
3. **Alarm lanes.** One row per detector (Fixed thresholds, Frozen baseline, Rolling 14 d, Space-Normal), with alarm ticks across mission days. A live counter shows "red false alarms so far: {a} / {b} / {c} / {d}" (computed live from the JSON) during replay. This is the head-to-head moment.
4. **Selected astronaut panel** (click a crew card):
   - **Body map (large)**, with clickable systems.
   - **Corridor chart (hero):** the actual vital against the expected corridor (baseline + adaptation ± uncertainty band). The unexplained part is shaded red, logged-event effects amber.
   - **Decomposition bars:** stacked per day (adaptation / events / residual) for the selected vital.
   - **Event timeline** under the charts: exercise sessions, sleep shifts, EVA prep, room-climate excursions.
5. **Alert drawer** (opens on click of any red tick):
   - **Header:** residual first, e.g. "Unexplained residual +{z}σ on pulse, C3, day {n}. Non-diagnostic."
   - **Lock badge:** "Severity locked ≥ detector". The tooltip explains that the LLM can only add context or escalate.
   - **Decomposition numbers.**
   - **Templated flight-surgeon note** with a "numbers verified ✓" chip, and a "Mars delay packet: {bytes}" chip.
   - **Triage context items,** each labelled "unverified contributor".
   - **Checklist questions.**
6. **Outbreak banner** (purple, spans the crew strip) when the crew layer fires. It shows which crew, the staggered onset days, and "no logged event explains this shift".

**B. Proof** (for judges):

- **Headline card,** read from `claims.json`, never hard-coded: "Real CFT70 adaptation: {X} vs {Y} false alarms per crew-month (Space-Normal vs best rolling baseline) at {S}% sensitivity on transplanted real illness." (placeholders filled from claims.json; never type numbers here) Shown with 95% CIs, the config hash and a "CFT70 untouched during development" badge.
- **The four plots:**
  - A: false alarms by bed-rest day;
  - B: sensitivity vs false alarms;
  - C: degradation vs prior error, with the crossover point visible ("where we lose");
  - D: ablation table.

**C. Data & Honesty:**

- Dataset cards (source, link, subjects, what is real or synthetic, splits).
- The limitations list from section 17.
- Kerremans et al. 2026 cited as "the call this answers".

### 14.3 Body systems map

- **Rendering:** original 2D SVG with one path group per system. No copyrighted figures. Front view only; neutral, minimal and consistent across all 4 crew.

| System (body region) | Vitals | Notes |
|---|---|---|
| Cardiovascular (heart + vessels) | pulse, SBP/DBP | |
| Respiratory (lungs) | resp_rate | |
| Thermoregulation (whole-body outline glow) | temp_c | |
| Fluids / renal (kidneys) | weight, fluid in/out | Context only, never alarms |
| Not monitored (eyes/SANS, bone, muscle, immune) | — | Grey, with a "future sensor" tooltip; doubles as the roadmap |

- **Color states** (colorblind-safe, each paired with an icon or pattern):

  | State | Look | Meaning |
  |---|---|---|
  | Expected adaptation | teal | Within the corridor |
  | Event-explained | amber | Deviation matched by a logged event |
  | Unexplained | red, pulsing | Residual alert |
  | Crew-wide | purple outline | Outbreak or shared, unexplained |
  | Not monitored | grey, hatched | No sensor |

- **State rule per system per day:** red if any mapped vital has a red alert or unexplained z > 2. Otherwise amber if |events term| > |residual| and the deviation is > 1σ. Otherwise teal.
- **3D (stretch, P8):** a react-three-fiber body with the same system IDs and the same state contract, toggled with "2D | 3D". Only with a license-checked model (BodyParts3D and Z-Anatomy are CC BY-SA: check attribution and share-alike) and only if a teammate already knows Three.js.

### 14.4 Data contract (`web/src/contract.ts`, mirrored by pydantic in `scripts/validate_contract.py`)

```ts
type Provenance = "REAL_BEDREST" | "REAL_EARTH_ILLNESS" | "SYNTHETIC";
interface VitalSeries { y: number[]; baseline: number[]; adaptation: number[]; events: number[];
  residual: number[]; z: number[]; band_low: number[]; band_high: number[] }
interface CrewMember { id: string; group: string;
  vitals: Record<"pulse"|"temp_c"|"resp_rate"|"sbp"|"dbp", VitalSeries>;
  systems: { day: number; cardio: State; resp: State; thermo: State; fluids: State }[] }
type State = "expected" | "event" | "unexplained" | "crew" | "not_monitored";
interface Alert { id: string; detector: string; crew_id: string; day: number;
  level: "yellow"|"red"; vital: string; z: number }
interface Mission { mission_id: string; scenario: string; days: number[];
  provenance: { adaptation: Provenance; illness: Provenance | "NONE"; events: Provenance };
  crew: CrewMember[]; events: { day: number; type: string; crew_ids: string[] }[];
  alerts: Alert[]; crew_alerts: { day: number; crew_ids: string[]; onsets: number[] }[];
  notes: Record<string, { text: string; numbers_verified: boolean; bytes: number;
    context_items: { text: string; source_ref: string }[]; questions: string[] }> }
```

Rule: the UI shows **no number that is not in the JSON**. `validate_contract.py` runs in CI against every cache file.

### 14.5 Demo bookmarks (maps to the 3-minute script)

| Bookmark | What it shows |
|---|---|
| Day 1–3 | Burn-in: old detectors already flash; Space-Normal holds (teal) |
| Shared event | All 4 bodies turn amber together; no alarm; alarm lanes show baselines firing |
| Onset −3 | One heart turns red; drawer opens: residual first, locked severity, note, packet size |
| Outbreak scenario | Purple banner across 2–3 crew with staggered onsets |
| Proof | Headline number, then plot C ("where we lose") |

### 14.6 UI acceptance criteria

- Loads offline in <3 s from static JSON. A 70-day replay at 16× runs smoothly (≥50 fps on a laptop).
- Every chart carries a provenance badge. Every number comes from the JSON (contract validator passes).
- Keyboard shortcuts for the demo: space (play/pause), 1–5 (bookmarks), D (drawer).
- Readable from the back of a room: minimum 14 px text, high-contrast dark theme, color plus icon for every state.
- A recorded 3-minute video of the demo exists as a fallback.

## 15. Starter `priors_literature.yaml` (flight-mode only; extend only with cited rows)

```yaml
core_temp_c:
  shape: exponential
  amplitude: {mean: 1.0, sd: 0.4}
  tau_days: {log_mean: 3.22, log_sd: 0.5}   # ~25 d, plateau after ~75 d
  sources: [Stahn 2017, Sci Rep (n=11; forehead core-temp sensor)]
sleep_min:
  shape: step
  in_flight_mean_min: 363      # ~6.0-6.1 h vs 8.5 h scheduled
  sd_min: 45                   # assumption
  sources: [Barger 2014, Lancet Neurol]
night_rhr_flight:
  shape: zero_mean             # in-flight resting HR ~ unchanged vs preflight supine
  amplitude_pct: {mean: 0.0, sd: 5.0}   # assumption
  sources: [Norsk 2015, Hughson 2012, Otsuka 2018]
motion_sickness:
  incidence: [0.6, 0.8]
  duration_hours: [8, 72]
excluded:
  hrv: conflicting evidence; absent from datasets
  plasma_volume_hb: context only (plasma -10 to -17%; Hb rises in flight; anemia at landing)
  co2_on_vitals: no evidence at ISS levels -> no assumed effect
```

## 16. Phases, acceptance criteria and cut lines

| Phase | Build | Acceptance |
|---|---|---|
| P0 | Scaffold, schema, synthetic fallback, Makefile, CI | `make demo-synthetic` runs end to end |
| P1 | `fetch_nlsp.py` + NLSP loader + Stanford loaders + `docs/data_notes.md` inventory | Inventory shown to me: campaigns with daily vitals, subjects, BR-days, missingness, medical-log contents. **Stop for review.** |
| P2 | Bed rest prior fitting (C1 + C3) + illness signature extraction | `priors_bedrest.json` with between-person spread; signature plots; leave-one-subject-out curve error |
| P3 | Pseudo-crews, transplant, dev generator, scenarios | Property tests: null → no episodes; outbreak → staggered onsets; transplant preserves the signature shape |
| P4 | Simple model + CUSUM + crew layer + baselines | On the fit campaigns: real null ≤ budget; outbreak → crew alert |
| P5 | Config hash → CFT70 Tracks A, B, D → blind generator (separate session) → Track C | `docs/claims.md` with hash, headline numbers and CIs |
| P6 | LLM note + triage + 50-case suppression test | 0/50 false suppression; 100% number fidelity; stub mode passes |
| P7 | React dashboard (section 14) + `build_demo_cache.py` + contract validator + recorded demo video | All section 14.6 criteria pass |
| P8 (stretch) | 3D body toggle; Kalman version; wearable mode (night RHR on Stanford); Homekit; LightGBM ablation; webcam rPPG | Same interfaces / same contract |

- **UI runs in parallel from hour 0.** The front-end person builds against `contract.ts` with synthetic mission JSON from P0. Real cache files drop in at P5 with no UI changes.
- **Cut order if behind:** P8 items → flight-mode scenario → Data & Honesty screen (move to slides) → alarm-lane animations (keep static ticks).
- **Never cut:** CFT70 as the untouched test set, Track A real null, the rolling baseline, the matched-budget comparison, provenance badges, the corridor chart, the crew strip.

## 17. Honesty checklist (README and presentation)

- Adaptation comes from real NASA head-down-tilt bed rest, a ground analog, not spaceflight. Flight-mode results are synthetic layers on top.
- Illness signatures are real Earth wearable data (COVID), transplanted. Temperature/RR illness bumps are synthetic.
- No public astronaut vital-sign streams exist to validate in flight.
- The common in-flight case (asymptomatic herpesvirus reactivation) is not covered.
- Show where Space-Normal loses or ties (Track C crossover, any late-period false alarms).
- Cite Kerremans et al. 2026 (Frontiers in Space Technologies) as the call this prototype answers.
