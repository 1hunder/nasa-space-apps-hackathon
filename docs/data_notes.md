# Data notes (P1 inventory)

Accessed 2026-11-14. Reproduce with `python scripts/fetch_nlsp.py` (idempotent; hashes in `data/manifests/nlsp.json`). Numbers below come from `spacenormal.data.nlsp.inventory()` and `load_logs()`.

The §5 table, the reading-hour share, the symptom keyword counts and the Stanford usable-episode counts were computed ad hoc; no script in the repo reproduces them yet.

**Test-set discipline.** For the two test splits this inventory reports structure only: subject counts, day ranges, missingness and log keyword counts. No test vital values or log texts were read. `load_daily()` refuses test splits until `docs/claims.md` carries a config hash.

## 1. NASA bed rest (NASA Life Sciences Portal)

- Source: `https://nlsp.nasa.gov/api/v1`, experiment "Case Report Form" (`eeb9bd34-bdd4-5115-b139-adf2c9927962`). Open download, no account or terms.
- 301 files, 7.3 MB, 25 folders: daily vitals, water intake, urine collection, meals, symptoms, medication, protocol deviations, stretch log, bowel movements.
- Facility: Flight Analogs Research Unit, UTMB Galveston. All campaigns are 6° head-down tilt.
- Campaign 5 has no vitals folder on the portal.

### Subjects with daily vitals

| Split | Campaign / blocks | Years | Subjects | Pre days | In-bed days per subject | In-bed subject-days |
|---|---|---|---|---|---|---|
| fit | Campaign 1 | 2004 | 3 | 10 | 60 | 180 |
| fit | Campaign 3 blocks A, C, D, E | 2005–2008 | 15 | 11–16 | 85–91 | 1,343 |
| test_power | Campaign 3 blocks G, H | 2009–2010 | 8 | 13–16 | 60 | 480 |
| test_headline | CFT70 (Campaign 11) | 2013 | 3 | 13, 21, 21 | 42, 63, 70 | 175 |

- Fit total: 18 subjects, 1,523 in-bed subject-days (1,076 within the first 60 days).
- CFT70: 25 subjects appear in the campaign medication log, but only 3 have public daily vitals. Two of the three left before day 70.
- Post-bed-rest days (0–14 per subject) are loaded but not used.

### Variables and units

One reading per day, taken in the 06:00 hour for 96% of fit-set readings: pulse (bpm), systolic and diastolic BP (mmHg), respiratory rate (per min), body temperature (°C; °F in some older files), weight (kg), ambient temperature (°F) and humidity (%). Measurement method and posture are not stated in the files.

### Missingness on in-bed days (mean % of days per subject)

| Variable | fit | test_power | test_headline |
|---|---|---|---|
| pulse | 0.5 | 0 | 0 |
| body temperature | 9.8 | 0 | 0 |
| respiratory rate | 0.3 | 0 | 0 |
| SBP / DBP | 0 | 0 | 0 |
| weight | 1.4 | 0 | 0 |
| room temperature | 54.0 | 0.2 | 0 |
| room humidity | 54.8 | 0 | 0 |

- **Room climate** is usable (≥50% of days) for 8 of 18 fit subjects: Campaign 1 (3), block A (4) and one block E subject. Blocks C and D have almost none. Both test sets have complete room climate.
- **Body temperature** is missing on 53–67% of in-bed days and 80–90% of pre days for the three Campaign 1 subjects; the 15 Campaign 3 fit subjects are complete except for one day (C3A_0446).

### What the loader does (`src/spacenormal/data/nlsp.py`)

- The 29 subject files use 13 header layouts; columns are matched by alias.
- `study_day`: pre days are negative (`BR_Day` counts down to the last day before tilt), in-bed days are 1..N, post days continue from N+1.
- Fahrenheit is converted to Celsius. Values outside wide physiological limits become missing: 4 values across all files.
- Several readings on one day: the earliest is kept. This affects C3D_3985 (1 row) and C3D_7984 (5 rows).
- Known oddities, left as they are: C3D_3985 has 91 readings with day numbers up to 92; C1_0001 and C1_0002 carry some dates in 2001 although the campaign ran in 2004 (day numbering is intact); C3D_7984 has 85 readings over 90 in-bed days.
- `group` holds the block label, because the treatment arm is not in the vitals files.

## 2. Symptom, medication and issue logs

| Split | Symptom entries | Medication entries | Issue entries |
|---|---|---|---|
| fit | 633 (15 subjects; Campaign 1 has none) | 4,790 | 491 |
| test_power | 288 | 3,004 | 367 |
| test_headline | 132 | 576 | 50 |

Keyword scan for illness-like entries on in-bed days (all three logs together):

| Split | Fever/chills | Upper respiratory | Gastrointestinal | Infection / antibiotic | Cold medication | Subject-days with any hit | Subjects |
|---|---|---|---|---|---|---|---|
| fit | 1 | 42 | 25 | 10 | 4 | 50 | 12 of 18 |
| test_power | 0 | 115 | 13 | 1 | 0 | 52 | 6 of 8 |
| test_headline | 0 | 2 | 5 | 6 | 0 | 9 | 3 of 3 |

Reading of the fit-set entries:

- Most upper-respiratory entries are nasal or head congestion treated with a decongestant spray. Congestion is a known effect of head-down tilt, so these are not evidence of infection.
- There is one fever/chills entry in the fit set and no laboratory-confirmed infection anywhere in the logs.
- Of 633 fit-set symptom entries, 431 mention pain, soreness or aches and 180 mention headache; 25 mention upper-respiratory terms.

**Consequence:** the logs give real, dated symptom events, enough for Track D case studies. They do not give confirmed illness labels, so sensitivity still has to come from transplanted signatures.

## 3. Stanford COVID-19 wearables (illness signatures)

**Phase 1 — downloaded 2026-11-14.**

- Archive: `https://storage.googleapis.com/gbsc-gcp-project-ipop_public/COVID-19/COVID-19-Wearables.zip` (378 MB, SHA-256 `52ca976e…e380f4`), unpacked into `data/raw/stanford_p1/`. Public, no terms.
- 120 hr/steps file pairs for 118 participants (one participant, AA0HAI1, is split into three episode files) with minute-level heart rate and steps; 32 also have sleep. Four participants have extra `*_longterm.csv` files, which the loader does not read.
- Labels: Mishra et al. 2020 (Nat Biomed Eng, doi 10.1038/s41551-020-00640-6), Supplementary Table 3, saved as `mishra2020_MOESM3.xlsx`. `scripts/build_stanford_labels.py` turns it into `labels.csv`: 30 COVID-19 episodes (30 participants) and 17 other-illness episodes, all with files in the archive.
- Dates are shifted per participant, so only day offsets are usable.
- Loader: `src/spacenormal/data/stanford.py`. Night resting HR = mean HR 00:00–06:00 on zero-step minutes, at least 30 such minutes per night.
- **Usable episodes:** requiring at least 14 of the 28 baseline nights (days −42 to −15) and at least 25 of the 36 nights in the signature window (days −14 to +21) leaves 19 COVID-19 and 5 other-illness episodes. The thresholds are a first choice, to be fixed in P2 before any tuning.

**Phase 2 — not downloaded.** `https://storage.googleapis.com/gbsc-gcp-project-ipop_public/COVID-19-Phase2/COVID-19-Phase2-Wearables.zip` is 5.5 GB (36 GB unpacked, 2,123 participants). Its labels are in the supplementary tables of Alavi et al. 2022 (Nat Med) and have not been located yet. The loader handles its layout but has only been tested on hand-written files.

## 4. What this changes for later phases

Status 2026-11-15: items 1–4 and 7 are not implemented for real data yet; the pipeline currently requires equal-length crews and at least 7 valid baseline days per vital.

1. **CFT70 crew is 3, with unequal lengths** (42, 63, 70 days). Missions built on it need missing days after dropout; the contract already allows nulls.
2. **Room-climate coefficients** can be fitted on 8 subjects only. If they are unstable, the event term falls back to zero for room climate and says so.
3. **Campaign 1 cannot contribute to the temperature prior**; it rests on the 15 Campaign 3 subjects.
4. **No per-session exercise log** exists in these folders. CFT70 arm can be inferred from the pre-bed-rest length stated by NASA (21 days = exercise: 5160, 8072; 13 days = control: 8936), but "real exercise-session events" from the spec are not available. Exercise enters as a group label, and session events stay synthetic.
5. **Treatment arms for Campaign 3 blocks** are not in the vitals files and are not yet identified.
6. **Baselines are short** (10–16 pre days, 21 for two CFT70 subjects), and the pre phase is ambulatory while the in-bed phase is tilted. The first in-bed days mix a posture change with adaptation.
7. **Track D** is feasible as case studies on logged symptoms; there are no confirmed infections.

## 5. How big the expected shifts are

Checked on 2026-11-14 to size the synthetic demo, after the first mock used a pulse drift of +10 to +12 bpm.

**NASA bed rest, our 18 fit subjects** (change from each person's pre-bed-rest median; morning spot readings):

| Vital | Days 4–10 | Days 11–21 | Days 22–40 | Days 41–60 | Day-to-day SD in bed |
|---|---|---|---|---|---|
| Pulse, bpm | +0.25 | +0.75 | +4.25 | +4.5 (IQR −1.3 to +7.9) | 7.0 |
| Body temperature, °C (15 subjects) | 0.00 | +0.05 | 0.00 | +0.10 | 0.24 |
| Respiratory rate, /min | 0 | 0 | 0 | 0 | 1.4 (whole-number readings) |
| Systolic BP, mmHg | +0.5 | +0.75 | +0.25 | +2.0 | 7.6 |
| Diastolic BP, mmHg | +0.25 | +2.0 | +2.25 | +3.0 | 6.7 |

Values are medians across subjects; the last column is the within-subject SD of in-bed readings, median across subjects. The pulse shift is well under one day-to-day SD (7 bpm), and individuals range from −5 to +13.5 bpm at days 41–60. (An earlier version of this column used an unscaled measure and was too low; corrected 2026-11-15.)

**Published spaceflight findings:**

- Resting core temperature rises by about 1 °C, gradually over 2.5 months, reaching roughly 38 °C (Stahn et al. 2017, Sci Rep 7:16180, 11 astronauts, forehead heat-flux sensor).
- 24-hour ambulatory blood pressure falls by 8–10 mmHg; heart rate does not change (Norsk et al. 2015, J Physiol 593:573, 8 astronauts, 85–192 days on the ISS).
- Bed rest and flight differ: bed rest raises resting pulse and barely moves temperature, flight leaves pulse alone and raises temperature.

**What the mock now uses** (`configs/default.yaml`, flight-like, hourly readings, 90 mission days): core temperature from a 36.8 °C mean baseline, +1.0 °C asymptote with a 25-day time constant (about +0.95 °C by day 80); systolic −8 and diastolic −9 mmHg (15-day time constant); pulse unchanged, because the bed rest drift is not a flight prediction (Norsk 2015); respiratory rate unchanged. Per-person scale is N(1, 0.15) clipped to 0.7–1.2. Synthetic illness peaks at +7 bpm, +0.8 °C and +2 breaths/min. The "Earth normal" temperature limit is 37.5 °C, following `00-kontekst.md` §5; it and the other fixed limits are placeholders. Every time constant, the person-to-person spread, the illness sizes, the logged-event effects and the noise levels are assumptions with no source.
