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
2. Plik dla Twojego zadania (tabela w §3).
3. [`docs/README.md`](docs/README.md) — pełna mapa dokumentów.

**Nie używaj** [`docs/archiwum/`](docs/archiwum/) jako źródła decyzji. Są tam nieaktualne dane, np. „24 min” i „Kerremans i in.”.

## 3. Jakie zadanie → co przeczytać

| Zadanie | Czytaj |
|---|---|
| Kod: pipeline, model, detektory, ewaluacja | [`PLAN.md`](PLAN.md) (specyfikacja, EN) + **delta** w [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §4 + [`docs/data_notes.md`](docs/data_notes.md) |
| Kod: dashboard / UI (`web/`) | [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §1–2 i §4 + `web/src/contract.ts` |
| Deploy | [`README.md`](README.md) (uruchomienie) + [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §5 |
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
   - wyniki bierzemy tylko z `docs/claims.md`, który generuje pipeline;
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
7. **Bez logo NASA** i bez stylizacji na oficjalny produkt NASA. Bez prawdziwych osób w materiałach AI.
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

## 8. Definicja „gotowe”

- `make test` przechodzi; kontrakt jest zwalidowany (`make demo-synthetic`).
- Każda nowa liczba w UI lub tekście ma źródło (`docs/claims.md` albo `docs/02-dowody-nasa.md`).
- Etykiety pochodzenia danych są widoczne.
- Jeśli zmiana dotyczy dokumentów, `docs/README.md` jest aktualny.
