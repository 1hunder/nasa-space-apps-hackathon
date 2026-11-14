# Space-Normal: adaptation-aware health monitoring for astronauts

**One-liner.** A crew health monitor that knows how a healthy body is supposed to change in space, and raises an alarm only when someone deviates from that expected path.

## Problem

Onboard alarm thresholds are calibrated to Earth physiology, but spaceflight shifts the body by design. Heart rate and blood pressure drop during the first weeks of spaceflight and then stay near the preflight supine level for up to 6 months. Astronauts lose about 10% of the fluid in their blood vessels, and in one study 5 of 13 astronauts were clinically anemic at landing.

A generic detector fails either way. It fires constantly on normal adaptation, or it gets recalibrated and then misses real illness. A 2026 clinical chemistry review calls for space-specific "reference change values", derived from biomarkers measured longitudinally onboard, to separate clinically relevant changes from microgravity effects. To our knowledge, nobody has implemented this.

## Why now

In January 2026 NASA carried out the first medical evacuation in ISS history. NASA's chief medical officer cited a "lingering question as to what that diagnosis is", and NASA's models expect a medical evacuation roughly every three years. A 2026 NASA paper documents influenza reaching crew in orbit after an asymptomatic crew launched following exposure. On Mars there is no evacuation, so telling adaptation from illness onboard becomes critical.

## What is new

Some pieces already exist on Earth:

- Smartwatch systems detect infection against a personal baseline. One alerted on about 80% of infected people, a median of 3 days before symptoms.
- A patent describes flagging clusters of physiological change caused by contagion or shared environmental stress.

What is missing is a model that treats "normal" in spaceflight as a moving, expected trajectory. Space-Normal splits each crew signal into four parts: personal baseline, expected adaptation for that flight day, a factor shared by the whole crew and habitat, and an individual residual. Only the residual can trigger an alarm.

**Core claim:** once "space" and "environment" are removed from the signal, what remains looks Earth-like again, so detectors trained on Earth data can work in orbit.

## How it works

1. **Features.** Daily resting heart rate, sleep, activity and HRV, aligned to flight day, with a personal baseline built from preflight weeks.
2. **Adaptation priors.** Taken from the literature. An LLM extracts effect sizes and time constants with citations, and a human checks every number.
3. **Signal decomposition.** A state-space (Kalman) or Bayesian model. The shared crew factor is estimated from cross-crew co-movement plus cabin CO2.
4. **ML detector on the residual.** LightGBM or a 1D-CNN trained on PCR-labelled Earth data, plus CUSUM. When one crew member alerts, sensitivity rises for the others.
5. **LLM triage agent.** Looks for benign explanations in schedules and logs, asks the crew 2–3 targeted questions, turns crew text into weak labels, and drafts a compact note for the flight surgeon. The LLM never decides whether an alarm fires.

## Data (all public)

- **Stanford COVID-19 Wearables**: heart rate, steps and sleep, 32 infected participants. https://medrxiv.org/content/10.1101/2020.07.06.20147512v1
- **Homekit2020**: 592,000 days of minute-level Fitbit data (sleep, heart rate, steps) from 5,196 participants, with PCR-confirmed influenza results. https://github.com/behavioral-data/Homekit2020
- **NASA OSDR Environmental Data App**: ISS cabin temperature, humidity, CO2 and radiation telemetry. https://visualization.osdr.nasa.gov/eda
- **Published spaceflight adaptation curves** for heart rate, plasma volume and hemoglobin (see references).
- **Optional live input**: webcam heart rate via rPPG. https://github.com/ubicomplab/rPPG-Toolbox

## Evaluation and demo

We build semi-synthetic missions:

- four real people from the wearable datasets, one with a confirmed infection;
- spaceflight adaptation curves, with individual variation, applied after "launch";
- a real ISS CO2 series as the shared factor.

We compare three detectors: Earth thresholds, personal baseline, and Space-Normal. Metrics are false alarms per crew-month, sensitivity, and lead time in days before symptom onset.

In the demo, the baseline detectors flood with false alarms, while Space-Normal flags only the infected crew member, days early, and explains why.

## Assumptions and limitations

- The illness signals and noise are real.
- The adaptation curves and the effect size of CO2 on physiology are assumptions taken from the literature. They come from small studies with large individual variation.
- Group curves serve only as a starting prior that is updated per person.
- This is a decision-support prototype, not a diagnostic device.

## Scope

Buildable in 24–48 hours with Python (pandas, filterpy/statsmodels, LightGBM), FastAPI, and a Streamlit dashboard.

## Key references

- First ISS medical evacuation (The Register, Jan 2026): https://www.theregister.com/2026/01/09/nasa_crew_11_iss/
- Point-of-care testing and reference change values in space (CCLM 2026): https://www.degruyterbrill.com/document/doi/10.1515/cclm-2025-0526/html
- NASA Health Stabilization Program outcomes (npj Microgravity 2026): https://www.nature.com/articles/s41526-026-00593-1
- Real-time wearable alerting for COVID-19 (Nature Medicine): https://www.nature.com/articles/s41591-021-01593-2
- Personalized baseline deviation for infection detection (2026): https://doi.org/10.1177/20552076261477919
- Heart rate and blood pressure up to 6 months in space (J Appl Physiol): https://journals.physiology.org/doi/full/10.1152/japplphysiol.00883.2009
- Space anemia (Ottawa Hospital Research Institute): https://ohri.ca/newsroom/story/view/1428?l=en
- Homekit2020 (CHIL 2023): https://proceedings.mlr.press/v209/merrill23b.html
