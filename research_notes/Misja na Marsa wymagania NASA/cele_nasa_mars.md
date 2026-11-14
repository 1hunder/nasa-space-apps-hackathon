# Co NASA oficjalnie zadeklarowała dla załogowej misji na Marsa — zdrowie załogi i autonomia medyczna

Data researchu: 2026-11-14. Cel: zakotwiczyć nasz produkt (osobisty, zależny od fazy misji zakres oczekiwany dla codziennych parametrów życiowych + karta „obserwuj → sprawdź teraz → eskaluj, jeśli…”) w dokumentach NASA.

Tagi: **[FAKT]** = cytat zweryfikowany w pierwotnym dokumencie NASA (pobrany i przeczytany), **[CZĘŚCIOWE]** = źródło wtórne / streszczenie / niepełna weryfikacja, **[BRAK]** = nie znaleziono oficjalnej informacji.

---

## 1. Moon to Mars Objectives (NPS 1001.104, wrzesień 2022)

Źródła (identyczny tekst):
- https://nodis3.gsfc.nasa.gov/OPD_Docs/NPS_1001_104_.pdf
- https://www.nasa.gov/wp-content/uploads/2022/09/m2m-objectives-exec-summary.pdf

Kluczowe cele (dosłownie):

- **TH-8LM** (Transportation & Habitation) [FAKT] — najmocniejsze zakotwiczenie dla nas:
  > "TH-8LM: Develop systems that monitor and maintain crew health and performance throughout all mission phases, including during communication delays to Earth, and in an environment that does not allow emergency evacuation or terrestrial medical assistance."
  - Uwaga: „throughout all mission phases” = bezpośrednie uzasadnienie zakresów zależnych od fazy misji.
- **HBS-2LM** (Human and Biological Science) [FAKT]:
  > "HBS-2LM: Evaluate and validate progressively Earth-independent crew health & performance systems and operations with mission durations representative of Mars-class missions."
- **HBS-1LM** [FAKT]:
  > "HBS-1LM: Understand the effects of short- and long-duration exposure to the environments of the Moon, Mars, and deep space on biological systems and health, using humans, model organisms, systems of human physiology, and plants."
- **HBS-3LM** [FAKT]:
  > "HBS-3LM: Characterize and evaluate how the interaction of exploration systems and the deep space environment affect human health, performance, and space human factors to inform future exploration-class missions"
- **OP-7LM** (Operations) [FAKT]:
  > "OP-7LM: Validate readiness of systems and operations to support crew health and performance for the initial human Mars exploration campaign."
- **OP-6L** [FAKT]:
  > "OP-6L: Evaluate, understand, and mitigate the impacts on crew health and performance of a long deep space orbital mission, followed by partial gravity surface operations on the Moon."
- **OP-2LM** [FAKT]:
  > "OP-2LM: Optimize operations, training and interaction between the team on Earth, crew members on orbit, and a Martian surface team considering communication delays, autonomy level, and time required for an early return to the Earth."
- **Recurring Tenets** [FAKT]:
  > "RT-3: Crew Return: return crews safely to Earth while mitigating adverse impacts to crew health."
  > "RT-4: Crew Time: maximize crew time available for science and engineering activities within planned mission durations."
  > "RT-5: Maintainability and Reuse: ... increase Earth independence."
  - RT-4 (czas załogi) uzasadnia „krótką kartę” zamiast długich raportów.

Późniejsza rewizja celów: [CZĘŚCIOWE] Nie znalazłem nowej wersji tekstu celów. ADD Rev C (grudzień 2025) nadal się do nich odwołuje (np. "OP-1, OP-2, OP-4, OP-5, OP-6, OP-7"), a RT-3 cytuje w lekko zmienionym brzmieniu: "RT-3: Return crew safely to Earth while mitigating adverse impact to crew health." Wniosek: cele 2022 są nadal obowiązujące.

Dodatkowo [FAKT]: zespół HRP ExMC w prezentacji EIMO ConOps (2024, slajd 2) cytuje właśnie TH-8 / HBS-2 / OP-7 jako cele, z których wywodzi się EIMO — czyli sama NASA łączy te cele z autonomią medyczną.

---

## 2. Moon to Mars Architecture Definition Document — Revision C (ESDMD-001, grudzień 2025)

Źródło: https://ntrs.nasa.gov/citations/20250010956
PDF: https://ntrs.nasa.gov/api/citations/20250010956/downloads/ADD%20Revision%20C%20-%2020260115.pdf
Uzupełnienie: „2025 Architecture Update” https://www.nasa.gov/wp-content/uploads/2025/12/2025-architecture-update-for-publication.pdf

### Parametry misji
- **Liczebność załogi (decyzja MD-05, ACR 2025)** [FAKT]:
  > "At the 2025 Architecture Concept Review, the agency determined that the initial Humans to Mars segment will target no fewer than four (4) crew to the surface, with consideration for no fewer than six (6) crew to enhance mission capability and/or provide risk reduction."
  > "NASA found that crew health and performance and mission and operational risk were the main drivers for this decision. There is stakeholder community consensus that fewer than four crew would present unacceptable crew risk." (Appendix C.2.2.7)
  - 2025 Architecture Update: "...with consideration for up to six crew..." oraz "the agency could choose to send additional astronauts to remain in Mars orbit" (czyli możliwa dzielona załoga: powierzchnia + orbita).
- **Opóźnienie komunikacji** [FAKT] (2025 Architecture Update, „Operations and Earth Independence”):
  > "missions to Mars will need to account for a one-way time delay of up to 22 minutes. This delay means astronauts cannot rely on real-time advice or guidance from mission controllers and must operate with significant autonomy and independence from Earth."
  > "This Earth independence means delayed support from experts on the ground, such that the crew must quickly respond to critical events using their expertise and local systems."
  - [CZĘŚCIOWE] Zakres ogólnie znany: ok. 4–22 min w jedną stronę, do tego okres koniunkcji słonecznej (blackout ~2 tyg.) — ADD wspomina "blackouts", ale liczby dni nie podaje.
- **Czas trwania misji** [FAKT] — ADD (wielokrotnie w Appendix D, luki technologiczne zdrowia):
  > "Mars In addition, support mission durations on the order of 2-3 years."
  - Całkowity czas misji to nadal **otwarte zadanie definicyjne** ("total mission duration, transit habitation strategy, mission mode operation" — gap 1104) [FAKT].
- **Czas tranzytu** [BRAK w obowiązującej architekturze]. ADD Rev C nie podaje liczby dni tranzytu. Referencyjnie [CZĘŚCIOWE, źródło historyczne, nie aktualna architektura]: Design Reference Architecture 5.0 (2009) — misja koniunkcyjna: ok. 174 dni w jedną stronę, 201 dni powrót, 539 dni na Marsie, łącznie ~914 dni. Prezentacja HRP EIMO ConOps 2024 [FAKT] podaje dla misji eksploracyjnej: "650-day to > 900-day mission duration".
- **Habitat tranzytowy** [FAKT] (glosariusz ADD): "Deep Space Transport ... the assembled Mars transit vehicle stack ... in the crew variant, the cargo will consist of a transit habitat that may or may not be a separate free-flyer". [CZĘŚCIOWE] Nazwa „Mars Transit Habitat” pojawia się w materiałach NASA, ale konkretny projekt nie jest wybrany.
- **Harmonogram** [CZĘŚCIOWE]: brak oficjalnej daty misji na Marsa. Administrator Jared Isaacman (wywiad, połowa 2026): misje załogowe na Marsa „before 2040”, jeśli najpierw powstanie stała obecność na Księżycu (Sinclair/KUTV: https://kutv.com/news/nation-world/exclusive-nasa-leader-jared-isaacman-on-next-steps-for-artemis-lunar-base-space-race-earth-crew-lunar-astronauts-mars-president-donald-trump-rocket).

### Zdrowie załogi i operacje niezależne od Ziemi (ADD Rev C)
- Sekcja 3.5.3 RT-3 Crew Return — wyzwania dla Marsa [FAKT]:
  > "Mars missions will need to operate with more independence from Earth to account for communications latency and time-to-effect events"
  > "Mars missions will require advanced health and performance monitoring and response, both onboard and on the ground"
  > "To enable safe crew return and survival capabilities in the event of long-duration loss of communications, including required onboard planning capabilities, trajectory execution, and medical support, requirements should include validated onboard autonomy and crew procedures"
- Sekcja RT-4 Crew Time [FAKT]:
  > "For Mars exploration, distribution of time critical system responses to essentially co-located assets (e.g., surface autonomy/crew or crew remaining on transit vehicle) and non-time critical responses to MCC enables more surface crew time for exploration and mission objectives."
  - To idealnie pasuje do naszej karty: decyzje pilne lokalnie, niepilne → eskalacja do MCC z opóźnieniem.
- **Technology Gap 0405 „Exploration Medical Capabilities for Deep Space Missions”** (Appendix D) [FAKT]:
  > "As missions become more Earth-independent (increased duration, communications delays, limited abort or resupply), improvements are required across the spectrum of medical capabilities to enable deep space human habitability. There is a need for improved capabilities to allow for prevention, early diagnosis, and treatment options for a wider range of medical conditions ... In addition, we cannot fully rely on ground support to address time-critical treatments, increasing the need for crew autonomy in initial diagnostic decision support and guidance in the use of treatments for medical care."
  - Child gaps: "0405-05 Medical imaging, diagnostics, and decision support", "0405-06 Crew health & performance integrated data architecture", "0405-03 Probabilistic risk models and simulations for crew health".
  - Stan obecny: "The scope of ISS medical capabilities is predicated on real-time communication and ground support, evacuation for definitive care of significant medical events, frequent and reliable resupply, and mission durations less than one year."
  - Cel dla Marsa: "Medical systems and ConOps to reduce risk of adverse crew health outcomes with communication delay, limited abort capability, and limited diagnostic and treatment resources."
- **Use cases / funkcje Mars (Appendix B)** [FAKT]:
  > "UC-X-107 M Deployment and operation of crew health monitoring assets in deep space and/or Mars vicinity"
  > "UC-X-108 M Deployment and operation of crew health monitoring assets on the Martian surface"
  > "FN-X-101 M Manage crew health and performance (medical, physiological, psychological, environmental, task support, etc.) for extended duration (year+) crew mission(s) in deep space and/or Mars vicinity"
  > "FN-X-102 M Manage crew health and performance for mid-duration (month+) crew mission(s) on the Martian surface"
  > "FN-X-107 M Deploy crew health monitoring assets for extended duration (year+) in deep space and/or Mars vicinity"
  - Rozróżnienie „deep space/transit” vs „Martian surface” = oficjalny podział na fazy misji.
- Gap 0401 (ćwiczenia) [FAKT]: "assessment tools are needed for crew to accurately maintain and monitor physical health and performance during exploration missions"; "the communication delay will introduce new issues, and will force crew to be more self-reliant."

---

## 3. HRP Human Research Roadmap — ryzyko „Medical Conditions” i luki

Ryzyko [FAKT]: "Risk of Adverse Health Outcomes and Decrements in Performance Due to Medical Conditions that occur in Mission, as well as Long Term Health Outcomes Due to Mission Exposures"
https://humanresearchroadmap.nasa.gov/risks/risk.aspx?i=95

Obecny układ luk: stare luki ExMC „Med01–Med13” zostały **scalone** w nowe luki „Medical-101…701” [FAKT].

- **Medical-701** (najważniejsza dla nas) [FAKT] — https://humanresearchroadmap.nasa.gov/Gaps/?i=716
  > "Medical-701: We need to increase inflight medical capabilities and identify new capabilities that (a) maximize benefit and/or (b) reduce “costs” on human system/mission/vehicle resources."
  - Scalone z niej m.in.:
    - "Med03: We do not know how to apply personalized medicine effectively to reduce health risk for a selected crew." ← uzasadnienie dla **osobistych** zakresów
    - "Med05: We do not know how to train crew for medical decision making and medical skills to enable extended mission or autonomous operations."
    - "Med10: We do not have the capability to provide computed medical decision support during exploration missions."
  - Z opisu: "This new approach will require highly functional and easy to use medical technology that has a reduced resource footprint, tools and training that enable astronauts to perform medical functions autonomously..."
  - Podejście: "Development of technology prototypes and operational protocols that enable astronauts to provide medical care in a progressively Earth independent fashion (e.g. medical decision-making support tools)"
  - Cel zamknięcia: "NASA acceptance of the Medical Risk as determined by high confidence in the ability of an exploration medical system to maintain astronaut health necessary for a successful human Mars mission"
- **Medical-501** [FAKT] — https://humanresearchroadmap.nasa.gov/Gaps/?i=714
  > "Medical-501: We need to develop integrated exploration medical system models for the Moon and Mars." (scalona z "Med01: We do not have a concept of operations for medical care during exploration missions.")
  - Podejście: "Derive necessary additional requirements that enable system utility (e.g. medical data architecture, medical workstation)."
- **Medical-401** [FAKT] — scalona z "Med09: We do not have the capability to predict estimated medical risk posture during exploration missions based on current crew health and resources." (https://humanresearchroadmap.nasa.gov/Gaps/?i=641)
- **Med07** [FAKT] — "We do not have the capability to comprehensively process medically-relevant information to support medical operations during exploration missions." — status: **Closed** (https://humanresearchroadmap.nasa.gov/Gaps/?i=639). Nie powoływać się na nią jako otwartą lukę.
- Medical-101 [FAKT]: "We need to characterize the medical conditions that can occur during exploration missions and their relevant associated end states, management options, and the capabilities necessary to manage them..."

---

## 4. EIMO — Earth-Independent Medical Operations ConOps (HRP ExMC, 13 lutego 2024)

Źródło: https://ntrs.nasa.gov/citations/20240001402 (PDF: https://ntrs.nasa.gov/api/citations/20240001402/downloads/2024_IWS_EIMO_ConOps_FINAL.pdf) — to prezentacja z HRP IWS, nie formalny dokument wymagań. Pełny model ConOps (MBSE) jest dostępny tylko na wniosek [FAKT].

- Definicja [FAKT]:
  > "EIMO – The gradual transition of medical care and decision making from terrestrial to space-based assets, enabling support of astronaut health and performance and reducing overall mission risk"
- Porównanie ISS vs misja eksploracyjna [FAKT]: ISS "Real-time communications", "Emergency evacuations possible", "Limited onboard medical care (Earth-reliant)" vs misja eksploracyjna "650-day to > 900-day mission duration", "No real-time communications + blackouts", "No evacuations possible", "Expanded onboard medical care (crew/vehicle-reliant)"; "As Distance from Earth ↑, Medical Risk ↑".
- 5 komponentów EIMO [FAKT]: Pre-Mission Planning; Acute & Emergent Management Decision Making; Prolonged Medical Decision Making; Supplies & Resource Management; Task Load Management.
- Kluczowe punkty [FAKT]:
  > "Non-emergent medical condition management less dependent on real time ground support"
  > "KSA with on-board Clinical Decision Support System (CDSS)"
  > "Delays / lack of ground support = increased task demand, task switching & higher cognitive load (all shown to impair decision making)"
  > "Identification of tasks that can be automated to reduce cognitive load demands"
  > "EIMO utilizes data streams from multiple sources to assess Crew Health & Performance and makes recommendations using AI-supported natural language processing and machine learning techniques"
  - CHP-IDA: "Crew Health and Performance – Integrated Data Architecture (CHP-IDA) system as a platform to enable the amalgamation of a variety of crew-relevant data sources and applications."
  - AMO: "Autonomous Medical Operations (AMO) project is developing an on-board software-based Medical Decision Support System (MDSS) which will enable astronauts to diagnose and treat emergent conditions in a timely manner."
- Status [FAKT]: "We have begun requirements development for L2,3, & 4 baseline delivery" — czyli formalne wymagania EIMO są w trakcie tworzenia (brak publicznego dokumentu wymagań) → [BRAK] publicznych, numerowanych wymagań EIMO.
- Uzupełnienie (HRP IWS 2023, „Architectural Framework for Conceptualizing Exploration Class Medical Missions”, https://ntrs.nasa.gov/api/citations/20240001379/downloads/2024%20IWS%20SoSA%20FINAL.pdf) [FAKT]: proponowany framework: "Prevention: Crew Environment Monitoring / Crew Preventive Health Monitoring / Crew Performance Monitoring → Diagnosis → Treatment → Support", zgodny z NASA-STD-3001. Nasz produkt mieści się w „Crew Preventive Health Monitoring”.
- „Crew-centric” — [CZĘŚCIOWE] to nasza interpretacja; dokumenty mówią o "crew and system autonomy", nie używają słowa „crew-centric”.

---

## 5. Aktualności 2025–2026

- **CMO-DA (Google + NASA), 8 sierpnia 2025** [FAKT, źródło: blog Google Cloud, nie nasa.gov] — https://cloud.google.com/blog/topics/public-sector/how-google-and-nasa-are-testing-ai-for-medical-care-in-space
  > "Google and NASA collaborated on an innovative proof-of-concept for an automated Clinical Decision Support System (CDSS) known as the "Crew Medical Officer Digital Assistant" (CMO-DA)."
  > "The CMO-DA tool could help astronauts autonomously diagnose and treat symptoms when crews are not in direct contact with Earth-based medical experts."
  > "Early results showed promise for reliable diagnoses based on reported symptoms."
  - [CZĘŚCIOWE] Media (TechCrunch, Space.com) podają: scenariusze testowe – uraz kostki, ból w boku, ból ucha; ~88% trafności dla kostki; plan testów na ISS. Niezweryfikowane w źródle pierwotnym.
  - Wniosek dla nas: CMO-DA zajmuje się **diagnozą objawów zgłaszanych przez załogę** (reaktywnie). Nasz produkt jest **proaktywny** (trend codziennych parametrów vs osobisty zakres zależny od fazy) — komplementarny, nie konkurencyjny.
- **Artemis II** [CZĘŚCIOWE, źródła prasowe] — załogowy przelot wokół Księżyca, wodowanie 10 kwietnia 2026 (Wiseman, Glover, Koch, Hansen), ~10 dni.
- **Artemis III** [CZĘŚCIOWE] — wg wywiadu z Isaacmanem cel: połowa 2027, przekształcona w test dokowania z lądownikami na orbicie okołoziemskiej; Artemis IV (2028) — powrót na powierzchnię Księżyca.
- **2025 Architecture Update** [FAKT]: na 2026 NASA zapowiada m.in. "examining the communications and navigation needs of crewed Mars missions".

---

## Szybkie podsumowanie parametrów misji (do slajdu)

| Parametr | Wartość | Status |
|---|---|---|
| Załoga na powierzchni Marsa | ≥4, rozważane do 6 (MD-05, ACR 2025) | [FAKT] |
| Dodatkowa załoga na orbicie | możliwa („split crew”), nierozstrzygnięte | [FAKT] |
| Opóźnienie komunikacji | do 22 min w jedną stronę + blackouty | [FAKT] |
| Całkowity czas misji | „on the order of 2-3 years” (ADD); 650–>900 dni (HRP EIMO) | [FAKT] |
| Tranzyt w jedną stronę | brak decyzji; historycznie ~6–7 mies. (DRA 5.0: 174/201 dni) | [CZĘŚCIOWE] |
| Pobyt na powierzchni | brak decyzji; DRA 5.0: ~500+ dni (koniunkcja) | [CZĘŚCIOWE] |
| Ewakuacja medyczna | niemożliwa | [FAKT] |
| Data misji | brak oficjalnej; „przed 2040” (Isaacman, 2026) | [CZĘŚCIOWE] |
