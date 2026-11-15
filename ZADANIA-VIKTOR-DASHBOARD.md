# Viktor — poprawki dashboardu przed demo

**Od:** Petro · **Data:** 2026-11-15 · **Dotyczy:** https://spacenormal.vercel.app/ (stan `origin/main` @ `7f53bbd`)

**Zasada:** jak najmniej funkcji, ale dopasowanych do jednej historii. Wszystko, czego nie pokażemy w filmie 30 s ani w pitchu 3 min, wylatuje z UI. Pipeline i ewaluacja zostają bez zmian. Track A (fałszywe alarmy na zdrowych danych) dalej liczymy, bo z niego idzie liczba główna. Usuwamy go tylko z ekranu.

**Kontrakt** (`web/src/contract.ts` ↔ `src/spacenormal/contract.py`) zostawiamy bez zmian. Wszystko poniżej da się zrobić w `web/`, `configs/` i przy przebudowie cache.

**Kolejność:** najpierw A + B (P0, ok. 1–1,5 h), potem C (P1, jeśli zostanie czas).

---

## A. Usuń z UI (P0)

| # | Co | Dlaczego | Gdzie |
|---|---|---|---|
| A1 | Scenariusz **„Healthy crew”** (`real_null`) | W „One crew member falls ill” widać już zdrowych kolegów i fałszywe alarmy innych metod w zdrowe dni. Osobny scenariusz to ten sam przekaz drugi raz | `configs/scenarios.yaml` (albo filtr w `scripts/build_demo_cache.py`), `web/src/labels.ts` → `SCENARIO_LABEL`, usunąć `web/public/cache/mission_synthetic_real_null.json` |
| A2 | Scenariusz **„Schedule change”** (`shared_event`) | Redundancja: słupek „logged schedule shift” jest już w „One crew member falls ill” | jw., `mission_synthetic_shared_event.json` |
| A3 | **Selektor parametrów → zostają tylko parametry z §D** | Film 30 s pokazuje jeden wykres. Pięć opcji w dropdownie to szum | `web/src/labels.ts`: dodać `DEMO_VITALS` i użyć go w `App.tsx` zamiast `VITALS`. Przy jednym parametrze usunąć dropdown. `VITALS` w kontrakcie **zostaje** (detektor waży pulse/temp/resp) |
| A4 | Organ **„Lungs”** w sylwetce i na liście załogi, jeśli oddech wypada w §D | Nie pokazujemy, czego nie mierzymy na ekranie | `web/src/components/CrewList.tsx` → `SYSTEMS` |
| A5 | Dropdown scenariusza, **jeśli zostanie jeden scenariusz** (patrz C1) | Jedna historia = zero wyboru | `App.tsx` (header) + skróty 1–9 |

Po zmianach: `make demo-synthetic` (walidacja kontraktu) i sprawdzić, czy `missions.json` ma tylko pozostałe scenariusze.

## B. Popraw (P0)

| # | Problem | Poprawka | Gdzie |
|---|---|---|---|
| B1 | **Prawdziwe imiona zespołu jako załoga** (Anna Uhalnik, Davyd Antoniuk, Petro Melnyk, Viktor Kulyk). Łamie AGENTS.md §5.7 („bez prawdziwych osób”) | Neutralne etykiety: `Crew A`, `Crew B`, `Crew C`, `Crew D`. Wymyślone imiona też są OK, ale sprawdź, czy nie należą do znanej osoby | `configs/default.yaml` → `mission.crew_names` |
| B2 | **Pomylone etykiety norm.** Szary pas „Earth normal / fixed before launch” to w rzeczywistości osobisty zakres sprzed lotu (`frozen_baseline`). Wiersz „Earth-normal monitor: Personal baseline…” jest opisany sprzecznie. Słowniczek (AGENTS.md §8): `frozen_baseline` = **„Pre-flight range”**, `fixed_thresholds` = **„Earth normal”** | `DETECTOR_LABEL.frozen_baseline` → `{ name: "Pre-flight range", how: "Personal range, fixed before launch" }`. `DETECTOR_LABEL.fixed_thresholds` → `{ name: "Earth normal", how: "Same clinical limits for everyone" }`. Szary pas na wykresie → „Pre-flight range”. „Earth baseline” w karcie alertu i tooltipie → „Pre-flight baseline” | `web/src/labels.ts`; `web/src/components/Figure.tsx` l. ~225–230, ~291, ~390; `AlertPanel.tsx` |
| B3 | **„Synthetic” widać tylko w drobnym tekście po kliknięciu „Show details”.** AGENTS.md §5.3: wszystko syntetyczne musi być oznaczone | Stała plakietka obok tytułu albo zegara: `SYNTHETIC · literature-based`, z `mission.provenance`. Widoczna zawsze, także w filmie | `App.tsx` (header), `styles.css` |
| B4 | `AlertPanel.tsx:55`: „The assistant can add context **or escalate**, never lower an alert”. AGENTS.md §5.6: LLM nie może alarmu wywołać, opóźnić ani obniżyć | „The detector sets the alert. The assistant only words it — it cannot raise, delay or lower it.” | `web/src/components/AlertPanel.tsx:55` |
| B5 | **Czerwone kropki poza korytarzem bez alarmu** (np. Crew D, dni 5–10, „Illness spreads”). Laik zapyta, czemu nie ma alarmu | W tooltipie i legendzie: „One day outside the range is watched, not alarmed. An alert needs a persistent shift.” Alternatywa: kropki pojedynczych dni bursztynowe zamiast czerwonych; czerwień tylko przy alarmie | `Figure.tsx` (tooltip ~l. 381–397, kolor kropek ~l. 244) |
| B6 | **Wielkość adaptacji temperatury.** W „Illness spreads” karta pokazuje „Expected adaptation +1.63 °C”, a literatura (Stahn 2017) daje ok. +1 °C. Komentarz w `default.yaml` mówi, że `scale_clip` trzyma dryf blisko średniej z publikacji | Sprawdzić, czy +1,63 to `amp × scale` czy doliczona korekta poziomu (`level_halflife_days`). W demo „expected adaptation” nie powinno przekraczać ok. +1,0–1,2 °C | `configs/default.yaml` → `synthetic.priors.temp_c`, `model.*` |

## C. Upraszczanie (P1 — rób po A + B)

| # | Propozycja | Po co |
|---|---|---|
| C1 | **Jeden scenariusz w UI: „One crew member falls ill”.** „Illness spreads” (alert załogowy) zostaje w pipeline, ale znika z ekranu. W pitchu mówimy o nim jednym zdaniem. **Czeka na decyzję Petra**, do tego czasu nie usuwaj | Film i pitch opowiadają jedną historię: adaptacja to nie alarm, choroba tak, i to dzień przed objawami |
| C2 | **Wiersze porównania metod:** w widoku głównym 3 wiersze: Earth normal, Pre-flight range, Space-Normal. „Rolling recalibration” tylko w „Show details” | Juror od razu widzi oba konkurencyjne podejścia. Rolling to argument do Q&A, nie do filmu |
| C3 | **Karta alertu w formacie 3 linii** OBSERVATION → CHECK NOW → ESCALATE IF, z istniejących danych (rozbicie + „Ask the crew member”). Bez nowego ekranu | Pierwszy użytkownik to astronauta (`00-kontekst.md` §6). Dziś karta jest pisana pod lekarza |
| C4 | „Note for the flight surgeon” → **„Handover note”** z podtytułem „for the flight surgeon or a diagnostic assistant” | Pozycjonowanie wobec CMO-DA (`00-kontekst.md` §8): oddajemy uporządkowany kontekst dalej. Nie nazywamy CMO-DA w UI |
| C5 | Skrócić `fineprint` w `App.tsx` do dwóch zdań: co jest syntetyczne + skróty klawiszowe | Mniej tekstu na ekranie |
| C6 | Pasek misji „Mars transit · day N · up to 22 min one-way delay” i fazy na osi X (`01` §4) | Już było w zadaniu #4 w `05-stan-prac.md`. Robić tylko, jeśli A–C5 są gotowe |

## D. Które parametry zostają w demo: **temperatura głęboka + tętno**

`DEMO_VITALS = ["temp_c", "pulse"]`. Domyślnie otwiera się **temperatura**. Oddech i ciśnienie znikają z selektora, ale zostają w kontrakcie i pipeline.

| Parametr | Rola w demo | Uzasadnienie NASA (szczegóły i URL: `docs/02-dowody-nasa.md` N11–N13) |
|---|---|---|
| **Temperatura głęboka** (domyślna) | Główny wątek filmu: zdrowa adaptacja wygląda jak gorączka, a korytarz to rozstrzyga | Wymieniona z nazwy w Mars ConOps HRP 48021 (lista vital signs z biosensorów). Fakt fizjologiczny: Stahn 2017, ok. +1 °C w ciągu ok. 2,5 mies. (ESA/DLR, nie NASA). **W bed rest temperatura prawie się nie zmienia**, więc ten wątek jest zawsze `SYNTHETIC`, flight-like |
| **Tętno** | Dowód na prawdziwych danych NASA bed rest (P2/P5). Sygnatury chorób ze Stanford to też HR | Jedyny parametr obecny we wszystkich źródłach: OCHMO-TB-033, HRP 48021 (scenariusz tranzytu: system „detects a change in … heart rate”, a flaga trafia do opiekuna), HRP-48033 (CDSS uruchamiany przez HR z urządzeń ubieralnych), CSA Bio-Monitor. **Dryfu tętna z bed rest nie pokazujemy jako prognozy lotu** (w locie HR się nie zmienia, Norsk 2015) |

Dlaczego bez oddechu i ciśnienia: oba są na listach NASA, ale żaden nie daje czytelnej historii w 30 s. Ciśnienie w locie spada w obrębie normy (Norsk 2015), a w urządzeniach ubieralnych jest estymowane. Oddech w danych bed rest się nie przesuwa.

## E. Gotowe, gdy

- `make test` przechodzi, `make demo-synthetic` waliduje kontrakt;
- na stronie: jeden lub dwa scenariusze, 1–2 parametry, plakietka SYNTHETIC widoczna bez klikania, brak prawdziwych imion, etykiety zgodne ze słowniczkiem;
- deploy na Vercel zaktualizowany, w `docs/05-stan-prac.md` zmieniony wiersz zadania #4 z datą.

Pytania do Petra na bieżąco. Jeśli coś z tej listy wymaga zmiany kontraktu, zatrzymaj się i daj znać.
