# AGENTS.md — instrukcja dla wszystkich agentów (Space-Normal)

Ten plik obowiązuje każdego agenta AI w tym repo (Claude Code, Codex, Cursor i inne). `CLAUDE.md` tylko go importuje.

## 1. Projekt w 5 zdaniach

- **Space-Normal** to oprogramowanie na NASA Space Apps 2026, wyzwanie *„Create Health Monitoring Software for Astronauts on Space Missions”*.
- **Misja:** tranzyt załogowy na Marsa (faza mikrograwitacji). Opóźnienie łączności sięga 22 min w jedną stronę, przerwy w łączności trwają do ok. 2 tygodni, ewakuacji nie ma. Standard NASA nie wymaga lekarza na pokładzie.
- **Pomysł:** każdy astronauta ma **osobisty korytarz normy**, który zmienia się z dniem misji („siatka centylowa dla astronauty”). Alarm włącza się tylko wtedy, gdy parametr wychodzi poza korytarz, a nie tłumaczą tego zalogowane zdarzenia.
- **Użytkownicy:**
  1. astronauta — dostaje kartę: OBSERVATION → CHECK NOW → ESCALATE IF;
  2. Crew Medical Officer (nie lekarz) — widzi całą załogę;
  3. lekarz lotu na Ziemi — dostaje opóźniony pakiet.
- **Dane:** NASA bed rest (analog naziemny), z wydzielonym zbiorem testowym. Sygnatury chorób pochodzą z danych Stanford. Tryb „flight-like” jest syntetyczny i oparty na literaturze.

## 2. Kolejność czytania

1. [`docs/00-kontekst.md`](docs/00-kontekst.md) — **źródło prawdy.** Jeśli inny plik mu przeczy, wygrywa ten.
2. [`docs/05-stan-prac.md`](docs/05-stan-prac.md) — **co już działa, co następne, kto nad czym pracuje.** Nie zaczynaj zadania, które ma innego ownera, bez pytania.
3. Plik dla Twojego zadania (tabela w §3).
4. [`docs/README.md`](docs/README.md) — pełna mapa dokumentów.

Uwaga: [`PLAN.md`](PLAN.md) to specyfikacja sprzed researchu. Gdzie przeczy [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §4, wygrywa `01` §4.

**Nie używaj** [`docs/archiwum/`](docs/archiwum/) jako źródła decyzji. Są tam nieaktualne dane, np. „24 min” i „Kerremans i in.”.

## 3. Jakie zadanie → co przeczytać

| Zadanie | Czytaj |
|---|---|
| Kod: pipeline, model, detektory, ewaluacja | [`PLAN.md`](PLAN.md) (specyfikacja, EN) + **delta** w [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §4 + [`docs/data_notes.md`](docs/data_notes.md) |
| Kod: dashboard / UI (`web/`) | [`ZADANIA-VIKTOR-DASHBOARD.md`](ZADANIA-VIKTOR-DASHBOARD.md) + [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §1–2 i §4 + `web/src/contract.ts` |
| Deploy | [`README.md`](README.md) (uruchomienie) + [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §5 |
| Design ekranu, film 30 s | [`ZADANIA-ALEX-DESIGN.md`](ZADANIA-ALEX-DESIGN.md) + [`docs/03-pitch-i-film.md`](docs/03-pitch-i-film.md) §1 |
| Prezentacja pitchowa | [`pitch/index.html`](pitch/index.html) (jedyna aktualna) + [`pitch/SKRYPT.md`](pitch/SKRYPT.md) + [`docs/03-pitch-i-film.md`](docs/03-pitch-i-film.md) §2. `pitch/legacy/` jest wycofane — nie edytuj |
| Co robić teraz / stan faz P0–P8 | [`docs/05-stan-prac.md`](docs/05-stan-prac.md) |
| Teksty: pitch, film, strona zgłoszenia | [`docs/03-pitch-i-film.md`](docs/03-pitch-i-film.md) + [`docs/02-dowody-nasa.md`](docs/02-dowody-nasa.md) + [`docs/00-kontekst.md`](docs/00-kontekst.md) §10 |
| Pole References | [`docs/02-dowody-nasa.md`](docs/02-dowody-nasa.md) §4 |
| Organizacja pracy, terminy | [`docs/04-zespol-i-plan.md`](docs/04-zespol-i-plan.md) + [`docs/zrodla/judging-awards-guide-2026.pdf`](docs/zrodla/judging-awards-guide-2026.pdf) |

## 4. Research: które pytanie → który plik

| Pytanie | Plik |
|---|---|
| Czy ziemskie normy to realny problem? Co jest potwierdzone, co nie? | [`docs/research/raport-normy-ziemskie.md`](docs/research/raport-normy-ziemskie.md) |
| Czy dzisiejsze systemy (Astroskin, ISS, EVA, Artemis) mają alarmy na ziemskich progach? | [`docs/research/normy-ziemskie/systemy_i_alarmy.md`](docs/research/normy-ziemskie/systemy_i_alarmy.md) |
| Jak lekarze lotu oceniają dane (baseline sprzed lotu, PMC, SMOT)? | [`docs/research/normy-ziemskie/praktyka_lekarzy_lotu.md`](docs/research/normy-ziemskie/praktyka_lekarzy_lotu.md) |
| Które parametry zdrowego astronauty wychodzą poza ziemską normę? Czym różni się bed rest od lotu? | [`docs/research/normy-ziemskie/parametry_poza_norma.md`](docs/research/normy-ziemskie/parametry_poza_norma.md) |
| Literatura o osobistych zakresach i prior art (Bajewski/IBMP, Ferraro 2026, Scott 2023, CMO-DA) | [`docs/research/normy-ziemskie/literatura_i_prior_art.md`](docs/research/normy-ziemskie/literatura_i_prior_art.md) |
| Czy na Marsa leci lekarz? Czego wymaga NASA-STD-3001 i EIMO? Jakie jest opóźnienie łączności? | [`docs/research/misja-mars/zaloga_medyczna_mars.md`](docs/research/misja-mars/zaloga_medyczna_mars.md) |
| Co NASA zadeklarowała dla Marsa (cele Moon to Mars, ADD Rev C, luki HRP, CMO-DA)? | [`docs/research/misja-mars/cele_nasa_mars.md`](docs/research/misja-mars/cele_nasa_mars.md) |
| Ile realnie zmieniają się parametry w danych NASA bed rest? | [`docs/data_notes.md`](docs/data_notes.md) §5 |
| Gotowa mapa „wymaganie NASA → funkcja” z cytatami | [`docs/02-dowody-nasa.md`](docs/02-dowody-nasa.md) §1 |

W notatkach research każde twierdzenie ma tag ([FAKT]/[CZĘŚCIOWE]/[BRAK] albo [DANE]/[OPINIA]). Na zewnątrz cytuj tylko twierdzenia z tagiem [FAKT] lub [DANE]. Jeśli czegoś brakuje w researchu, napisz to wprost i nie zgaduj.

## 5. Zasady bezwzględne

1. **Język:** dokumenty projektu piszemy po polsku. Kod, komentarze, UI, strona zgłoszenia, film i napisy są po angielsku. Cytaty źródeł zostają w oryginale.
2. **Liczby:**
   - wyniki bierzemy tylko z [`docs/claims.md`](docs/claims.md), który wypełnia pipeline. **Dziś to stub bez wyników** — do tego czasu tylko placeholdery `{X}`;
   - nigdy nie dopisuj do `docs/claims.md` linii z hashem konfiguracji: loader odblokowuje wtedy zbiór testowy. Robi to wyłącznie `scripts/hash_config.py` w fazie P5;
   - fakty bierzemy tylko z [`docs/02-dowody-nasa.md`](docs/02-dowody-nasa.md) albo z notatek research z tagiem [FAKT];
   - nigdy nie wymyślaj liczb ani nie przepisuj ich ręcznie.
3. **Uczciwość danych:**
   - bed rest to analog naziemny, nie lot;
   - wszystko syntetyczne jest oznaczone `SYNTHETIC`;
   - dryfu tętna z bed rest nie przedstawiamy jako przewidywania dla lotu, bo w locie tętno spoczynkowe się nie zmienia.
4. **Czego nie twierdzić:** lista w [`docs/00-kontekst.md`](docs/00-kontekst.md) §10. Najważniejsze:
   - „obecne systemy na ISS fałszywie alarmują”;
   - „24 min”;
   - „nikt nie wpadł na osobisty baseline”;
   - „jesteśmy dokładniejsi niż CMO-DA”.
5. **Wydzielony test** (CFT70, Campaign 3 G/H) nigdy nie służy do strojenia. Loader blokuje go, dopóki w `docs/claims.md` nie ma hasha konfiguracji. Nie obchodź tej blokady.
6. **LLM nie decyduje o alarmie.** Może tylko sformułować tekst. Nie może alarmu wywołać, opóźnić ani obniżyć.
7. **Bez logo NASA** i bez stylizacji na oficjalny produkt NASA. Bez prawdziwych osób w materiałach generowanych przez AI (wideo, obrazy, głos). Wyjątek: imiona członków zespołu jako załoga w demo dashboardu — decyzja Petra z 2026-11-15.
8. **Każde zewnętrzne źródło, narzędzie i asset** (w tym narzędzia AI) dopisz do listy References.

## 6. Kod i polecenia

```bash
make setup            # Python 3.11 venv (uv), instalacja pakietu
make test             # pytest + hypothesis
make demo-synthetic   # misje syntetyczne -> web/public/cache/*.json + walidacja kontraktu
cd web && npm install && npm run dev   # dashboard
```

Układ kodu jest opisany w [`README.md`](README.md) (sekcja Layout). Kontrakt danych dashboardu to `web/src/contract.ts`, a jego lustro w pydantic to `src/spacenormal/contract.py`. Kontrakt zmieniamy po obu stronach naraz.

## 7. Git i praca zespołowa

- `main` to kod (PR-y Viktora i Davyda). `V2` to dokumenty Petra, które trafiają do `main` przez PR. Nie pushuj na cudzy branch.
- Commit message po angielsku, w stylu Conventional Commits (`feat:`, `fix:`, `docs:`).
- Zmianę kierunku produktu wprowadza tylko Petro, w `docs/00-kontekst.md`. Jeśli zadanie jej wymaga, zatrzymaj się i zapytaj.
- Role, harmonogram i zamrożenia (zakres na T+3h, funkcje na T+5h) są w [`docs/04-zespol-i-plan.md`](docs/04-zespol-i-plan.md).

## 8. Słowniczek

| Termin | Znaczenie |
|---|---|
| **Korytarz** | Pas wartości oczekiwanych u *tej osoby* w *tym dniu misji* (baza + oczekiwana adaptacja + zalogowane zdarzenia ± rozrzut). Ugina się z fazą misji |
| **Residual (reszta)** | Pomiar minus oczekiwanie; alarm liczymy tylko na reszcie |
| **CUSUM** | Detektor sumujący małe, uporczywe odchylenia reszty; daje żółty/czerwony alert |
| **Zakres sprzed lotu** (`frozen_baseline`) | Płaski osobisty zakres z dni przed misją/bed rest; koncepcja NASA CDSS (HRP-48033). W UI: „Pre-flight range” |
| **Ziemska norma** (`fixed_thresholds`) | Te same progi kliniczne dla wszystkich. W UI: „Earth normal” |
| **Rolling** (`rolling_14`) | „Normalne = ostatnie 14 dni”; silny baseline, uwzględniany w liczbie głównej |
| **CMO** | Crew Medical Officer: członek załogi z krótkim szkoleniem medycznym, nie lekarz |
| **Bed rest / HDT** | Naziemny analog nieważkości: tygodnie leżenia z głową 6° w dół |
| **C1, C3, CFT70** | Kampanie NASA bed rest: C1 + C3 A/C/D/E = dopasowanie; CFT70 i C3 G/H = wydzielony test |
| **Track A / B** | A: fałszywe alarmy na zdrowych danych (null); B: czułość i wyprzedzenie na przeszczepionych chorobach |
| **Flight-like** | Scenariusz syntetyczny z wielkościami zmian z publikacji z lotów (np. temperatura +1°C); zawsze `SYNTHETIC` |
| **Przeszczep (transplant)** | Wklejenie prawdziwej sygnatury choroby z danych Stanford w reszty z bed rest |

## 9. Definicja „gotowe”

- `make test` przechodzi; kontrakt jest zwalidowany (`make demo-synthetic`).
- Każda nowa liczba w UI lub tekście ma źródło (`docs/claims.md` albo `docs/02-dowody-nasa.md`).
- Etykiety pochodzenia danych są widoczne.
- Jeśli zmiana dotyczy dokumentów, `docs/README.md` jest aktualny.
