# Data notes (P1 inventory)

Accessed 2026-11-14. Reproduce with `python scripts/fetch_nlsp.py` (idempotent; hashes in `data/manifests/nlsp.json`). Numbers below come from `spacenormal.data.nlsp.inventory()` and `load_logs()`.

**Test-set discipline.** For the two test splits this inventory reports structure only: subject counts, day ranges, missingness and log keyword counts. No test vital values or log texts were read. `load_daily()` refuses test splits until `docs/claims.md` carries a config hash.

## 1. NASA bed rest (NASA Life Sciences Portal)

- Source: `https://nlsp.nasa.gov/api/v1`, experiment "Case Report Form" (`eeb9bd34-bdd4-5115-b139-adf2c9927962`). Open download, no account or terms.
- 301 files, 7.2 MB, 25 folders: daily vitals, water intake, urine collection, meals, symptoms, medication, protocol deviations, stretch log, bowel movements.
- Facility: Flight Analogs Research Unit, UTMB Galveston. All campaigns are 6° head-down tilt.
- Campaign 5 has no vitals folder on the portal.

### Subjects with daily vitals

| Split | Campaign / blocks | Years | Subjects | Pre days | In-bed days per subject | In-bed subject-days |
|---|---|---|---|---|---|---|
| fit | Campaign 1 | 2004 | 3 | 10 | 60 | 180 |
| fit | Campaign 3 blocks A, C, D, E | 2005–2008 | 15 | 11–16 | 85–91 | 1,343 |
| test_power | Campaign 3 blocks G, H | 2009–2010 | 8 | 13–16 | 60 | 480 |
| test_headline | CFT70 (Campaign 11) | 2013 | 3 | 13, 21, 21 | 42, 63, 70 | 175 |

- Fit total: 18 subjects, 1,523 in-bed subject-days (1,080 within the first 60 days).
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
- **Body temperature** is missing on 53–67% of in-bed days and 80–90% of pre days for the three Campaign 1 subjects; the 15 Campaign 3 fit subjects are complete.

### What the loader does (`src/spacenormal/data/nlsp.py`)

- The 30 subject files use 13 header layouts; columns are matched by alias.
- `study_day`: pre days are negative (`BR_Day` counts down to the last day before tilt), in-bed days are 1..N, post days continue from N+1.
- Fahrenheit is converted to Celsius. Values outside wide physiological limits become missing: 4 values across all files.
- Several readings on one day: the earliest is kept. This affects C3D_3985 (1 row) and C3D_7984 (5 rows).
- Known oddities, left as they are: C1_0001 and C1_0002 carry some dates in 2001 although the campaign ran in 2004 (day numbering is intact); C3D_7984 has 85 readings over 90 in-bed days.
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

## 3. Stanford COVID-19 wearables (illness signatures) — not downloaded yet

| | Phase 1 | Phase 2 |
|---|---|---|
| Archive | `https://storage.googleapis.com/gbsc-gcp-project-ipop_public/COVID-19/COVID-19-Wearables.zip` | `https://storage.googleapis.com/gbsc-gcp-project-ipop_public/COVID-19-Phase2/COVID-19-Phase2-Wearables.zip` |
| Size | 378 MB (3.6 GB unpacked) | 5.5 GB (36 GB unpacked) |
| Participants | 117 with heart rate and steps, 32 with sleep | 2,123 |
| Unpack into | `data/raw/stanford_p1/` | `data/raw/stanford_p2/` |

- Both URLs respond publicly; the file layouts were read from the archive directory and the first lines of one file per type. Nothing else was downloaded.
- Dates are shifted per participant, so only day offsets are usable.
- **Symptom-onset dates are not in the archives.** They are in the papers' supplementary tables (Mishra et al. 2020, Nat Biomed Eng; Alavi et al. 2022, Nat Med). Save them as `labels.csv` beside the data with columns `participant_id, symptom_onset_date`.
- Loader: `src/spacenormal/data/stanford.py` (night resting HR = mean HR 00:00–06:00 on zero-step minutes). Tested on hand-written files in the real layouts only.

## 4. What this changes for later phases

1. **CFT70 crew is 3, with unequal lengths** (42, 63, 70 days). Missions built on it need missing days after dropout; the contract already allows nulls.
2. **Room-climate coefficients** can be fitted on 8 subjects only. If they are unstable, the event term falls back to zero for room climate and says so.
3. **Campaign 1 cannot contribute to the temperature prior**; it rests on the 15 Campaign 3 subjects.
4. **No per-session exercise log** exists in these folders. CFT70 arm can be inferred from the pre-bed-rest length stated by NASA (21 days = exercise: 5160, 8072; 13 days = control: 8936), but "real exercise-session events" from the spec are not available. Exercise enters as a group label, and session events stay synthetic.
5. **Treatment arms for Campaign 3 blocks** are not in the vitals files and are not yet identified.
6. **Baselines are short** (10–16 pre days, 21 for two CFT70 subjects), and the pre phase is ambulatory while the in-bed phase is tilted. The first in-bed days mix a posture change with adaptation.
7. **Track D** is feasible as case studies on logged symptoms; there are no confirmed infections.
