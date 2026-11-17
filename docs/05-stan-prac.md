# Space-Normal — stan prac

**Ostatnia aktualizacja:** 2026-11-15.

Fazy według [`../PLAN.md`](../PLAN.md) §16. Priorytety według [`01-produkt-i-zakres.md`](01-produkt-i-zakres.md) §3–4.

## 1. Co już działa

| Faza | Co | Dowód w repo |
|---|---|---|
| P0 | Szkielet, schemat danych, generator syntetyczny, pipeline → JSON, kontrakt dashboardu, CI (testy Pythona, walidacja kontraktu i build `web/`; testy loadera na prawdziwych danych nie są w CI) | `make demo-synthetic`, `web/src/contract.ts`, `.github/workflows/ci.yml` |
| P1 | Pobieranie i loader NASA bed rest (301 plików), pobrane dane Stanford Phase 1 + etykiety + loader, inwentaryzacja danych | `scripts/fetch_nlsp.py`, `src/spacenormal/data/nlsp.py`, `scripts/build_stanford_labels.py`, `src/spacenormal/data/stanford.py`, `docs/data_notes.md` |
| P4 (częściowo) | Prosty model (baza + adaptacja × skala osobista + zdarzenia → residual), CUSUM, warstwa załogi, baseline'y (ziemskie progi, zakres sprzed lotu, rolling) | `src/spacenormal/model/simple.py`, `detect/`, `baselines.py` |
| P7 (częściowo) | Dashboard React z replayem 4 syntetycznych misji (90 dni): korytarz (domyślnie temperatura), linia „Earth normal” i pas „Pre-flight range”, odczyty godzinowe w tle i średnie dzienne, wiersz „Crew journal” (mock, bez LLM, nie wpływa na alarm), klikalne punkty i wpisy dziennika, replay zatrzymuje się na alarmie Space-Normal, lista załogi z sylwetką (regiony ciała + zgłoszenia bólu z dziennika), karta astronauty OBSERVATION / CHECK NOW / ESCALATE IF + „Not a diagnosis.”, pasek misji „Mars transit · day N”, link `?scenario=…&day=N` | `web/src/`, `configs/journal.yaml`, `web/src/contract.ts` |
| Dokumenty | Kontekst, research, mapa wymagań NASA, prezentacja i film | `docs/` |

Dashboard jest wdrożony pod https://spacenormal.vercel.app/ (statyczny build `web/`).

## 2. Czego jeszcze nie ma

| Faza | Brakuje | Plik docelowy |
|---|---|---|
| P2 | Dopasowanie krzywych adaptacji i rozrzutu między osobami na C1 + C3 (prawdziwe dane NASA); ekstrakcja sygnatur chorób ze Stanford (Phase 1 pobrana lokalnie i z etykietami — `data_notes.md` §3; Phase 2 niepobrana; sama ekstrakcja sygnatur jeszcze nie istnieje) | `src/spacenormal/priors/` (pusty), `priors_bedrest.json` |
| P3 | Pseudo-załogi z prawdziwych osób, przeszczep sygnatur chorób | `src/spacenormal/sim/` |
| P5 | Hash konfiguracji → ewaluacja na wydzielonym teście → liczba główna | `scripts/hash_config.py` (brak), `src/spacenormal/eval/` (pusty), `docs/claims.md` (stub) |
| — | Z `01` §4 zostało: fazy misji na osi X (brak ustalonych granic faz); plakietka `SYNTHETIC` w widoku głównym (dziś tylko w „Show details”); opóźnienie łączności na pasku misji | `web/src/components/Figure.tsx` |
| — | Film 30 s, strona zgłoszenia, References | — |

## 3. Następne kroki (kolejność = priorytet)

1. **P2:** krzywe adaptacji z C1 + C3 dla tętna i ciśnienia → plik z priorami + opis w `data_notes.md`.
2. **P5 minimum:** hash konfiguracji → Track A na CFT70 i C3 G/H, porównanie z najlepszym baseline'em → `docs/claims.md` z liczbą główną. Jeśli Track B nie zdąży, piszemy tylko Track A.
3. Film 30 s z napisami EN, strona zgłoszenia EN, lista References.

## 4. Znane rozbieżności do rozstrzygnięcia

1. Dashboard pokazuje odczyty godzinowe, a `00` §7 mówi „pomiar raz dziennie”.
2. Alarm w scenariuszu `single_illness` dotyczy temperatury (dzień 40, początek objawów dzień 41), nie tętna jak w storyboardzie `03` §1.
3. „Twarde limity bezpieczeństwa” z `00` §5 nie istnieją jeszcze w kodzie.

**Plan B, jeśli P2/P5 nie zdążą:** film i prezentacja na replayu syntetycznym z wyraźną etykietą „synthetic, literature-based”; mówimy wtedy, że ewaluacja na wydzielonych danych NASA jest przygotowana (loader, blokada testu) i jest następnym krokiem. Żadnych liczb wyników.
