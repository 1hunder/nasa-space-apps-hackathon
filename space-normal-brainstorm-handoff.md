# Space-Normal — brainstorm handoff from Petro's ChatGPT discussion

**Date:** 2026-11-14 (Europe/Warsaw)  
**Purpose:** Preserve the product discussion, scientific corrections, proposed demo and open decisions for teammates and agents continuing this repository.  
**Status:** Research and product handoff. No software implementation, measurements, benchmark results or clinical validation were produced in this chat.

Read alongside:

- [Existing concept summary](space-normal-summary.md)
- [Existing implementation plan v2.1](space-normal-claude-code-plan.md)

This document supplements those files. It does not replace their implementation plan or authorize a product pivot. In particular, **thermal/exercise monitoring was the assistant's latest recommendation; Petro has not explicitly selected it as the final MVP.**

## 1. What the team is trying to build

Challenge: **Create Health Monitoring Software for Astronauts on Space Missions**.

The original idea was an onboard assistant that consumes physiological and environmental sensor data, detects meaningful deviations, and gives the astronaut a short explanation and next step without waiting for Earth.

Three ideas emerged:

1. **Autonomous onboard feedback:** make the first assessment locally despite delayed or unavailable Earth communication.
2. **Adaptation-aware interpretation:** compare each person with a personal baseline and an expected trajectory for the relevant mission phase.
3. **Environmental context:** use measured habitat conditions and known activities to interpret changes.

These can be layers of one product rather than three separate applications. The smallest useful interaction is:

**Measurements → context-aware assessment → concise explanation → appropriate check or escalation.**

The astronaut is the primary user in this discussion. A report for a flight surgeon is a secondary output. The team wants very few features and a compelling demonstration of no more than 30 seconds.

## 2. Explicit user preferences and constraints

| Item | Status from this conversation |
|---|---|
| Frame the problem around future crewed Mars missions | Petro explicitly accepted this direction. |
| Smartwatch/iPhone-led hardware concept | Explicitly excluded by Petro. Do not reintroduce it as the product's sensing hardware. |
| Sensor inputs | Prefer established technologies used for astronaut physiology and habitat measurements: garments, headbands, onboard instruments and exercise equipment. |
| Hardware development | The discussion favors software using existing measurement technologies, not inventing another wearable. |
| Number of features | Keep it minimal; fewer functions are better for the demo. |
| Output | Short, actionable feedback rather than a long chat response. |
| Scientific claims | Petro invited strong criticism to reach a defensible core idea. |
| Submission | Design toward judging criteria and the required short demo. |
| Thermal/exercise scenario | Assistant recommendation, still awaiting a team choice. |
| Final thresholds, clinical actions, exact model and dataset | Not agreed or validated in this chat. |

**Important distinction:** excluding smartwatch hardware does not automatically exclude retrospective Earth wearable datasets as research inputs. If retained, explain their research role and limitations. The current repository plan uses Stanford data for illness signatures, not a proposed astronaut smartwatch.

## 3. Mission framing: use a real reference architecture, label assumptions

### Communication correction

The initial assumption of 10–15 minutes of delay for all space missions was incorrect.

- ISS operations can involve practically real-time communication with Earth; the Mars delay should not be attributed to the ISS.
- NASA describes Earth–Mars communication as approximately **4–24 minutes one way**, depending on geometry.
- That is approximately **8–48 minutes for a message and response**, before medical analysis, scheduling and other operational delays.
- A demo value such as **12 minutes one way / 24 minutes round trip** is an illustrative scenario assumption, not a fixed property of every mission.

Source: [NASA — Space Communications: 7 Things You Need to Know](https://www.nasa.gov/missions/tech-demonstration/space-communications-7-things-you-need-to-know/).

### Reference to use

NASA planning distinguishes strategic objectives, an evolving architecture, conceptual reference missions and specific operational missions. Do not invent an approved mission such as “NASA Mars 2036.”

Useful references:

- [NASA — Moon to Mars Architecture Definition](https://www.nasa.gov/architecture-definition/)
- [NASA — Planning, Architecture & Analysis](https://www.nasa.gov/reference/jsc-planning-architecture-analysis/)
- [NASA NTRS — Mars Transit Habitat Refinement Point of Departure Design, 2023](https://ntrs.nasa.gov/citations/20230002033)

The Transit Habitat document describes a **reference concept**, including long-duration microgravity habitation, autonomy, life support and crew-health needs. It is not proof of a final flight configuration or launch date.

For a focused product narrative, choose the **outbound transit phase**: a crew in a closed habitat, exercising routinely, with limited access to immediate Earth expertise. A day such as “mission day 90,” the crew count and communication delay should be marked as demo assumptions unless taken from a chosen mission study.

Operational phases to distinguish:

| Phase | Relevance |
|---|---|
| Preflight | Establish personal baselines and measurement protocols. |
| Outbound transit | Main proposed MVP setting: microgravity, exercise, closed habitat and communication latency. |
| Mars arrival/surface | Different gravity and operational conditions; outside the smallest MVP. |
| Return transit and postflight | Further context changes; possible later extension. |

## 4. Scientific corrections and rejected shortcuts

### Existing onboard capabilities

Onboard monitoring and autonomous medical support already exist in research and operational tools. Therefore “we analyze locally” alone is insufficient as a novelty claim.

Examples:

- [NASA — Astronaut Exercise](https://www.nasa.gov/general/astronaut-exercise/): CEVIS displays workout parameters and heart rate.
- [NASA NTRS — Autonomous Medical Officer Support demonstrations](https://ntrs.nasa.gov/citations/20240012964): autonomous procedure guidance has been demonstrated on the ISS.

The proposed contribution is the interpretation of personal dynamics and context, plus a clear local next step. Its benefit still needs to be measured.

### Do not merge different biomarkers

A conventional pulse oximeter estimates oxygen saturation and pulse rate. It does not provide hemoglobin concentration or iron stores. Do not show a normal consumer sensor detecting low hemoglobin or iron without an appropriate separate measurement.

Sources:

- [FDA — Pulse Oximeters](https://www.fda.gov/medical-devices/products-and-medical-procedures/pulse-oximeters)
- [NASA — Medical Examination Requirements](https://www.nasa.gov/directorates/esdmd/hhp/treat/medical-examination-requirements-mer-for-former-astronauts/)

“Low hemoglobin → eat a bar” was an illustrative brainstorm example, **not an accepted medical recommendation**. Space anemia should not be equated automatically with iron deficiency.

Source: [NASA NTRS — Red blood cell and iron metabolism during space flight](https://ntrs.nasa.gov/search.jsp?R=20040088075&hterms=anemia).

### High exertion is not automatically a problem

“High pulse → slow down” is inadequate during planned exercise. Likewise, burning calories does not by itself justify stopping a workout. Exercise is an important countermeasure against muscle and bone loss.

A meaningful assessment needs activity/load context, personal response, trends and signal quality.

Source: [NASA — Counteracting Bone and Muscle Loss in Microgravity](https://www.nasa.gov/humans-in-space/counteracting-bone-and-muscle-loss-in-microgravity/).

### Muscle-injury prediction remains unsupported

Petro mentioned an unclear muscle metric transcribed as “KSI.” No specific sensor or validated mapping from this metric to injury risk was established.

The scenario “the person has been inactive, wants to move suddenly, and will strain a muscle” should not be claimed as a capability. Neither future intent nor an impending strain follows from the described measurements.

An upcoming activity can instead be known from a schedule, a selected workout mode or a user check-in. No mind-reading is needed to detect an observable physiological issue.

### Correlation is not a causal diagnosis

The intended explanation must distinguish:

1. what was measured;
2. what was unusual relative to the model;
3. possible contributors;
4. what must be checked next.

Do not convert correlated pulse/temperature/environment changes into a definitive diagnosis of dehydration, infection or injury. Label possible contributors as hypotheses.

## 5. Reconciliation with the original Space-Normal idea

The strongest reusable idea is **a personal, mission-context-dependent expected range**, rather than a universal fixed normal.

A reviewed clinical chemistry paper discusses space-specific reference change values for biochemical markers. This motivates individualized longitudinal interpretation, but does **not** validate a particular wearable model, pulse threshold or exercise-alert algorithm:

[Point of care testing of biochemical markers for monitoring astronauts during long duration missions in deep space](https://www.degruyterbrill.com/document/doi/10.1515/cclm-2025-0526/html).

Corrections to the original summary:

- **Individual residuals cannot be the only alert route.** Shared deterioration may reflect a habitat problem or a crew-wide illness.
- **Removing estimated adaptation/environment effects does not establish Earth-to-space model transfer.** That remains a hypothesis needing evaluation.
- **Do not claim “nobody has implemented this.”** No exhaustive novelty assessment was completed.
- **A model's expected adaptation is not automatically clinically safe.** Absolute safety rules and acute-event checks must not disappear after personalization.
- **Daily trends and live signals are different timescales.** Daily sleep/resting pulse cannot support claims of second-by-second detection of an acute training event.

The repository's **v2.1 plan already addresses several initial concerns**: it avoids subtracting a crew median, separates crew alerts, constrains the LLM and distinguishes bed rest from flight. Do not treat those improvements as missing merely because the older summary says otherwise.

## 6. Latest proposed MVP: thermal strain during exercise

**Recommendation made by the assistant, not a final team decision.**

### Why this candidate is stronger than the calorie/injury examples

Thermal response during exercise is observable and space-relevant. Thermolab research found faster/higher core-temperature increases during exercise in space compared with preflight measurements.

Primary research:

[Stahn et al., 2017 — Increased core body temperature in astronauts during long-duration space missions](https://doi.org/10.1038/s41598-017-15560-w)

NASA explanations:

- [Heat Safety in Space Keeps Infants and Patients Safe on Earth](https://www.nasa.gov/missions/station/heat-safety-in-space-keeps-infants-and-patients-safe-on-earth/)
- [Wearable Tech for Space Station Research](https://www.nasa.gov/humans-in-space/wearable-tech-for-space-station-research/)

The study involved **11 astronauts**. Its findings support investigating the problem; they do not supply validated operational alarm thresholds for this prototype.

### Inputs and interface

| Source | Proposed role | Qualification |
|---|---|---|
| Bio-Monitor garment/headband system | Heart/pulse, respiration and activity channels | Real ISS technology; no live connection was established in this chat. |
| Specialized Thermolab/T-Mini-type instrumentation | Estimate core temperature | Skin temperature and estimated core temperature must not be substituted silently. |
| Exercise equipment or workout log | Workload, mode and duration | The feed and available fields must be verified. |
| Habitat temperature/humidity | Environmental context | An observed correlation is not a validated causal coefficient. |
| Tablet near exercise equipment | Short alert, explanation and check-in | Suitable demo interface; a new vibrating device is unnecessary. |

[Canadian Space Agency — Bio-Monitor](https://www.csa-asc.gc.ca/eng/sciences/bio-monitor.asp) describes a smart garment system and tablet application, including activity selection and viewing vital signs during exercise.

ISS use of an instrument does not qualify the proposed software or combined system for Mars. Live access, interfaces, reliability and flight qualification remain separate engineering tasks.

### Smallest interaction

1. Observe pulse, core-temperature estimate and known exercise load.
2. Detect an unusual trajectory or recovery pattern relative to an explicitly defined personal/contextual expectation.
3. Show a concise reason and open a short, reviewed check or escalation workflow.

The alert should contain **observation → next check → escalation condition**. Clinical instructions and thresholds require an appropriate expert/protocol; none were finalized here.

Keep slow adaptation and acute thermal limits separate. A shifted baseline cannot justify unlimited heating during a workout.

### LLM role

- Optional explanation and question phrasing from structured evidence.
- Never invent sensor values or establish a causal diagnosis.
- Detection and essential local feedback must work without a cloud response.
- Use a deterministic fallback; an offline replay must not be presented as proof that an external LLM runs onboard.

## 7. Important difference from the repository's current implementation plan

| Current v2.1 plan | Thermal/exercise candidate |
|---|---|
| Daily bed-rest spot vitals | Continuous or sufficiently frequent exercise measurements |
| Adaptation over days/weeks | Within-session dynamics and recovery |
| CFT70 held-out evaluation and transplanted illness signatures | Needs an appropriate exercise/temperature dataset or an honestly labelled simulation |
| Crew/individual anomaly research | A single astronaut-facing training alert |
| No real-time hardware integration | Also can use replay; a live hardware claim would need separate proof |

**Daily bed-rest data cannot validate acute thermal-strain detection.** Do not rename the existing daily pipeline “real-time exercise monitoring” without changing inputs, temporal resolution and evaluation.

Two coherent paths remain open:

- Continue the existing adaptation/illness research plan and use Mars transit as its operational narrative.
- Deliberately choose the thermal scenario, narrow the build and obtain appropriate data.

The handoff does not choose between these on the team's behalf. If time or data are insufficient for a thermal pivot, preserve the existing research pipeline and label thermal monitoring as a future use case.

## 8. Data provenance and evaluation

Discussed data options:

- **Homekit2020:** real Earth Fitbit observations and laboratory influenza labels. Access and applicable terms still need verification.
- **Stanford COVID-19 wearables:** Earth illness signatures; use the repository plan's participant splits and provenance rules if retained.
- **NASA OSDR Environmental Data App:** historical ISS cabin environmental/radiation records.
- **NASA bed-rest campaigns:** introduced in the repository's v2.1 plan, not independently downloaded or audited in this chat.
- **Published adaptation findings:** possible research priors, with assumptions and uncertainty made explicit.

References:

- [Homekit2020 research paper](https://proceedings.mlr.press/v209/merrill23b.html)
- [NASA OSDR Environmental Data App](https://visualization.osdr.nasa.gov/eda/)

Combining Earth illness data, ISS cabin records and assumed adaptation produces a **semi-synthetic scenario**. These sources do not constitute synchronized astronaut health-and-habitat measurements.

For any chosen MVP:

- Record source, units, sample frequency, gaps and real/synthetic status per channel.
- Compare with a credible simple baseline.
- Keep fit/tuning and evaluation separate.
- Test expected behavior, an anomaly and missing/poor-quality measurements.
- Preserve an alert path for dangerous shared environmental signals.
- Report observed results, including ties or failures.
- Do not claim a real reduction in injuries, diagnoses or false alarms before measuring it.

## 9. Judging and submission implications

The reviewed 2026 Space Apps materials list **Impact, Creativity, Validity, Relevance and Presentation**. Universal numeric weights were not verified.

| Criterion | Evidence the project should provide |
|---|---|
| Impact | A specific astronaut decision supported despite Earth latency. |
| Creativity | A demonstrated improvement from personal and mission context, beyond displaying sensor values. |
| Validity | Realistic inputs, scientific basis, honest assumptions and measured comparison. |
| Relevance | A complete path from health indicators to assessment and a next step. |
| Presentation | One memorable event and a visible software response. |

Sources:

- [Official Space Apps 2026 event page listing criteria](https://www.spaceappschallenge.org/2026/local-events/ajmer/)
- [Project Submission Guide](https://www.spaceappschallenge.org/resources/project-submission-guide/)
- [Judging & Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide/)

**Verification limitation:** the two guide pages returned access/server errors during this chat. Their full contents and exact required submission fields were not read. Recheck them before submission; the suggested written structure below is a working outline.

The **30-second video or up-to-seven-slide alternative** was corroborated in current Space Apps materials, including:

[Official Stalowa Wola event page](https://www.spaceappschallenge.org/2026/local-events/stalowa-wola/?tab=details).

A Global Organizing Team response states that Global Awards eligibility requires at least one NASA data source included in the chosen challenge's Resources:

[Space Apps discussion #1849](https://github.com/nasa/spaceapps/discussions/1849).

**Open eligibility task:** verify the exact resource in this challenge's Resources tab and show how it is used. Do not assume that a NASA mission reference, photo, generic citation or synthetic-only replay satisfies the requirement.

Working submission outline:

1. High-level problem, user and solution.
2. Public demo link and final project/code link.
3. Method, sensor assumptions and mission framing.
4. NASA/partner data use and exact provenance.
5. Evaluation results and limitations.
6. AI tools and their roles.
7. References, dependencies and asset attribution.

The repository was private when inspected. Public-access requirements for the final submission need a separate delivery decision; **this handoff does not authorize changing repository visibility**.

## 10. Proposed 30-second thermal demo

This is a storyboard proposal, not a recording already produced.

| Time | On screen |
|---|---|
| 0–5 s | Simulated outbound Mars transit; 12-minute one-way communication delay. |
| 5–11 s | Exercise replay with pulse, core-temperature estimate and workload. |
| 11–19 s | An unusual thermal trajectory triggers a short explanation. |
| 19–26 s | Astronaut acknowledges; a short check opens locally. |
| 26–30 s | Project name, actual NASA source used and simulation/provenance label. |

Use a clearly marked accelerated replay if the simulated event takes minutes. Do not imply that physiological heating or recovery occurred in a few seconds.

Show one screen, one astronaut and one episode. Keep model details, extra scenarios and research plots in the project documentation or longer supporting demo.

The existing implementation plan proposes a three-minute recording. That can be supplementary material; it does not replace the required short submission demo.

## 11. Open decisions for the next agents and team

Prioritize:

1. **Choose the evidence-backed MVP:** keep the current daily adaptation detector or deliberately select the thermal/exercise scenario.
2. **Inventory actual available data before promising capabilities.** Preserve CFT70 holdout discipline if following v2.1.
3. **Verify challenge resource eligibility and current submission rules.**
4. **Define the event, signals, timescale, baseline and success metric together.**
5. **Review alert thresholds and next steps with an appropriate mentor.** Keep prototype assumptions explicit.
6. **Build the smallest complete replay and record the 30-second version.**
7. **Reconcile documents after a real team decision.** Update the older concept summary only when the selected scope is settled.

No final name change, hardware integration, clinical protocol, launch date, measured performance claim or acceptance of the thermal pivot was agreed in this chat.
