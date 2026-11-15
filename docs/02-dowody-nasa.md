# Space-Normal — dowody: wymagania NASA, fakty, źródła

Dla: Petro (pitch), Anna (pole References), agentów piszących teksty.
Każde zdanie w pitchu i filmie musi dać się podpiąć pod wiersz z tego pliku. Notatki źródłowe: [`research/`](research/).

---

## 1. Wymaganie NASA → odpowiedź Space-Normal

| # | NASA napisała (cytat) | Dokument | Space-Normal |
|---|---|---|---|
| N1 | „Develop systems that monitor and maintain crew health and performance **throughout all mission phases**, including during communication delays to Earth, and in an environment that does not allow emergency evacuation or terrestrial medical assistance.” | Moon to Mars Objectives, **TH-8LM** ([NPS 1001.104](https://nodis3.gsfc.nasa.gov/OPD_Docs/NPS_1001_104_.pdf)) | Korytarz zależny od fazy misji; działa offline |
| N2 | „Evaluate and validate progressively Earth-independent crew health & performance systems and operations with mission durations representative of Mars-class missions.” | Moon to Mars Objectives, **HBS-2LM** (jw.) | Walidacja na analogu naziemnym NASA z wydzielonym testem |
| N3 | CMOs „often are, but are not required, to be physicians”; min. dwóch CMO na pojazd; „monitoring, and trending vital signs”; „autonomous medical care” | **NASA-STD-3001 Vol 1 Rev C** ([PDF](https://standards.nasa.gov/sites/default/files/standards/NASA/C//nasa-std-3001-vol-1-rev-c-signature.pdf)) | Użytkownik nie-lekarz; codzienny trend parametrów; karta „co sprawdzić” |
| N4 | Wiedza medyczna „via a skilled medical practitioner and/or a highly functional CDSS”; załoga 4 os., ≥ 2 CMO | **EIMO**, AsMA 2023 ([PDF](https://ntrs.nasa.gov/api/citations/20230007863/downloads/EIMO.AsMA2023.Lemery.final.pdf)) | Moduł monitoringu dla takiego CDSS |
| N5 | „Mars missions will require advanced health and performance monitoring and response, both onboard and on the ground” | **ADD Rev C** (2025), RT-3 ([NTRS](https://ntrs.nasa.gov/citations/20250010956)) | Karta na pokładzie + pakiet dla lekarza na Ziemi |
| N6 | „…increasing the need for crew autonomy in initial diagnostic decision support…”; podluki 0405-05 (decision support), 0405-06 (crew health & performance integrated data architecture) | **ADD Rev C**, luka technologiczna 0405 | Wspomaganie pierwszej oceny; jeden format danych pomiar → karta |
| N7 | Luka obejmuje dawne „Med03: … personalized medicine…” i „Med10: … computed medical decision support during exploration missions” | **HRP Gap Medical-701** ([link](https://humanresearchroadmap.nasa.gov/Gaps/?i=716)) | Osobisty korytarz + automatyczne wspomaganie decyzji |
| N8 | System „executes baseline checks… within pre-flight determined reference ranges” | **CDSS ConOps HRP-48033** (2021) ([PDF](https://ntrs.nasa.gov/api/citations/20220017856/downloads/HRP-48033_ExMC_CDSS_ConOps.pdf)) | Rozwijamy: zakres nie jest płaski, ugina się z fazą |
| N9 | „Delays / lack of ground support = increased task demand, task switching & higher cognitive load” | **EIMO ConOps** 2024 ([NTRS](https://ntrs.nasa.gov/citations/20240001402)) | 3 linijki zamiast surowych danych |
| N10 | Opóźnienie do 22 min w jedną stronę; przerwy w łączności od dni do tygodni | ASCEND/NASA ([PDF](https://ntrs.nasa.gov/api/citations/20220013418/downloads/ASCEND-Communication%20Delays%2C%20Disruptions%2C%20and%20Blackouts%20for%20Crewed%20Mars%20Missions.pdf)); [2025 Architecture Update](https://www.nasa.gov/wp-content/uploads/2025/12/2025-architecture-update-for-publication.pdf) | Pełne działanie offline; pakiet w kolejce |

Nie powołujemy się na lukę **Med07** (zamknięta). Publicznych, ponumerowanych wymagań EIMO nie ma — EIMO to koncepcja/prezentacje.

## 2. Fakty fizjologiczne (zdrowy astronauta vs norma)

| Fakt | Liczby | Źródło | Status |
|---|---|---|---|
| Temperatura głęboka w spoczynku rośnie | ok. +1°C przez ~2,5 mies., do ok. 38°C; 11 astronautów | [Stahn i in. 2017, Sci Rep](https://doi.org/10.1038/s41598-017-15560-w) | potwierdzone |
| Anemia po lądowaniu | 5 z 13 wg kryteriów WHO; hemoliza +54% w locie | [Trudel i in. 2022, Nat Med](https://pmc.ncbi.nlm.nih.gov/articles/PMC8799460/) | potwierdzone |
| Ciśnienie i rzut serca w locie | 24 h BP 129/85 → 121/76; rzut serca +41%; tętno bez zmian; 8 astronautów | Norsk i in. 2015, J Physiol 593:573 (PMC: sprawdzić ręcznie 4324697 vs 4324706) | potwierdzone (zmiany w normie) |
| Bed rest ≠ lot | bed rest: tętno rośnie, temperatura bez zmian; lot: odwrotnie | [`data_notes.md`](data_notes.md) §5; [PMC4573436](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4573436/) | potwierdzone |
| Tętno rośnie przed objawami infekcji | kilka dni przed objawami w danych z wearables | Mishra i in. 2020, Nat Biomed Eng | potwierdzone (Ziemia) |
| Osobisty model lepszy od populacyjnego | EVA: indywidualny HR→metabolizm R² > 0,82 vs 0,40 | [NTRS 20210024317](https://ntrs.nasa.gov/api/citations/20210024317/downloads/EXTRAVEHICULAR%20ACTIVITY%20METABOLIC%20RATE%20MODEL%20METABOLIC%20RATE%20ESTIMATED%20FROM%20HEART%20RATE.pdf) | potwierdzone |
| Wyniki laboratoryjne zwykle w normie | „generally within the clinical normal ranges for a 6-month mission” (McMonigal, NASA) | [Clin Chem 2023](https://academic.oup.com/clinchem/article/69/5/442/7113323) | kontrargument — znać |
| Fałszywe alarmy z ziemskich progów na ISS | **brak udokumentowanych przypadków** | raport §1 | brak dowodów — nie twierdzić |

## 3. Prior art (wymieniamy, nie ukrywamy)

| Kto | Co robi | Czym się różnimy |
|---|---|---|
| Bajewski, IBMP (Rosja) — diagnostyka prenozologiczna | HRV → prawdopodobieństwo 4 stanów funkcjonalnych, uwzględnia typ regulacji kosmonauty ([PMID 25509871](https://pubmed.ncbi.nlm.nih.gov/25509871/), [PMID 17022467](https://pubmed.ncbi.nlm.nih.gov/17022467/)) | Oni klasyfikują stan; my pokazujemy jawny korytarz per osoba per dzień misji |
| NASA CDSS ConOps HRP-48033 | zakresy sprzed lotu | Nasz zakres ugina się z fazą |
| Ferraro i in. 2026, CCLM ([doi](https://doi.org/10.1515/cclm-2025-0526)) | postulat kosmicznych reference change values dla biomarkerów | My dla parametrów życiowych, działający prototyp |
| Scott i in. 2023, Nat Mach Intell ([link](https://www.nature.com/articles/s42256-023-00617-5)) | „the best baseline for an individual is oneself”, rekomendacje warsztatu NASA | Jw. — realizujemy ten postulat |
| Zheng i in. 2023, Front Physiol | 27 astronautów, zalecają osobisty baseline | Retrospektywnie; my prospektywnie, dziennie |
| CMO-DA, Google + NASA 2025 ([blog](https://cloud.google.com/blog/topics/public-sector/how-google-and-nasa-are-testing-ai-for-medical-care-in-space)) | diagnoza zgłoszonych objawów (reaktywna) | My proaktywnie, przed objawami; uzupełniamy |
| CSA Bio-Monitor / Astroskin | zbiera parametry, analiza na Ziemi | My interpretujemy na pokładzie |

**Korekta:** praca CCLM 2026 to **Ferraro i in.**, nie „Kerremans i in.” (błąd we wcześniejszych dokumentach).

## 4. Lista do pola References (zgłoszenie, EN)

Dane: NASA Life Sciences Portal — Bed Rest Case Report Form (nlsp.nasa.gov); Stanford COVID-19 Wearables (Mishra et al. 2020; Alavi et al. 2022).
Dokumenty NASA: N1–N10 powyżej.
Publikacje: Stahn 2017; Trudel 2022; Norsk 2015; Ferraro 2026; Scott 2023; Zheng 2023; Baevsky 2006/2013; Mishra 2020.
Narzędzia (kod): Python 3.11 z numpy, pandas, scipy, statsmodels, pydantic, PyYAML, requests, matplotlib, pyarrow, openpyxl, pytest, hypothesis, uv; dashboard: React, Vite, TypeScript, krój Archivo (pakiet `@fontsource-variable/archivo`, licencja SIL OFL); asystent kodowania AI: Claude Code (Anthropic). **Do uzupełnienia:** narzędzia AI do wideo/obrazów/głosu i muzyka (z licencją).
