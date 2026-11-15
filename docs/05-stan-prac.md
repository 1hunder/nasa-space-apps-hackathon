# Space-Normal — stan prac i następne zadania

**Aktualizuje:** owner zadania po każdym ukończonym kroku (zmień wiersz + datę). **Ostatnia aktualizacja:** 2026-11-15 (Viktor, po przeglądzie spójności aplikacji z dokumentami; wiersze P0, P1, P2, P7 i wiersz o zmianach z `01` §4).

Fazy według [`../PLAN.md`](../PLAN.md) §16. Priorytety według [`01-produkt-i-zakres.md`](01-produkt-i-zakres.md) §3–4.

## 1. Co już działa (na `main`)

| Faza | Co | Dowód w repo |
|---|---|---|
| P0 | Szkielet, schemat danych, generator syntetyczny, pipeline → JSON, kontrakt dashboardu, CI (testy Pythona, walidacja kontraktu i build `web/`; testy loadera na prawdziwych danych nie są w CI) | `make demo-synthetic`, `web/src/contract.ts`, `.github/workflows/ci.yml` |
| P1 | Pobieranie i loader NASA bed rest (301 plików), pobrane dane Stanford Phase 1 + etykiety + loader, inwentaryzacja danych | `scripts/fetch_nlsp.py`, `src/spacenormal/data/nlsp.py`, `scripts/build_stanford_labels.py`, `src/spacenormal/data/stanford.py`, `docs/data_notes.md` |
| P4 (częściowo) | Prosty model (baza + adaptacja × skala osobista + zdarzenia → residual), CUSUM, warstwa załogi, baseline'y (ziemskie progi, zakres sprzed lotu, rolling) | `src/spacenormal/model/simple.py`, `detect/`, `baselines.py` |
| P7 (częściowo) | Dashboard React z replayem 4 syntetycznych misji (90 dni): korytarz (domyślnie temperatura), linia „Earth normal” i pas „Pre-flight range”, odczyty godzinowe w tle i średnie dzienne, wiersz „Crew journal” (mock, bez LLM, nie wpływa na alarm), klikalne punkty i wpisy dziennika, replay zatrzymuje się na alarmie Space-Normal, lista załogi z sylwetką (regiony ciała + zgłoszenia bólu z dziennika), karta astronauty OBSERVATION / CHECK NOW / ESCALATE IF + „Not a diagnosis.”, pasek misji „Mars transit · day N · up to 22 min · no physician” ze stałą etykietą SYNTHETIC, link `?scenario=…&day=N` | `web/src/`, `configs/journal.yaml`, `web/src/contract.ts` |
| Dokumenty | Kontekst, research, mapa wymagań NASA, pitch i film | `docs/` |

## 2. Czego jeszcze nie ma

| Faza | Brakuje | Plik docelowy |
|---|---|---|
| P2 | Dopasowanie krzywych adaptacji i rozrzutu między osobami na C1 + C3 (prawdziwe dane NASA); ekstrakcja sygnatur chorób ze Stanford (Phase 1 pobrana lokalnie i z etykietami — `data_notes.md` §3; Phase 2 niepobrana; sama ekstrakcja sygnatur jeszcze nie istnieje) | `src/spacenormal/priors/` (pusty), `priors_bedrest.json` |
| P3 | Pseudo-załogi z prawdziwych osób, przeszczep sygnatur chorób | `src/spacenormal/sim/` |
| P5 | Hash konfiguracji → ewaluacja na wydzielonym teście → liczba główna | `scripts/hash_config.py` (brak), `src/spacenormal/eval/` (pusty), `docs/claims.md` (stub) |
| — | Z `01` §4 zostało: fazy misji na osi X (brak ustalonych granic faz). Zrobione: nazwy w UI, pasek misji, linia „Earth normal” + pas „Pre-flight range”, karta astronauty. **Do decyzji Petra:** (1) załoga w demo ma imiona i nazwiska zespołu (`configs/default.yaml` → `crew_names`), storyboard używa fikcyjnych; (2) dashboard pokazuje odczyty godzinowe, a `00` §7 mówi „pomiar raz dziennie”; (3) alarm w scenariuszu `single_illness` dotyczy temperatury (dzień 40, początek objawów dzień 41), nie tętna jak w storyboardzie `03` §1; (4) „twarde limity bezpieczeństwa” z `00` §5 nie istnieją w kodzie. | `web/src/components/Figure.tsx` |
| — | Publiczny deploy | — |
| — | Film 30 s, strona zgłoszenia, References | — |

## 3. Następne zadania (kolejność = priorytet)

| # | Zadanie | Owner | Gotowe, gdy |
|---|---|---|---|
| 1 | Publiczny deploy obecnego dashboardu | Davyd | Link otwiera replay; wpisany tutaj |
| 2 | P2: krzywe adaptacji z C1 + C3 dla tętna i ciśnienia | Viktor | Plik z priorami + krótki opis w `data_notes.md` |
| 3 | P5 minimum: hash konfiguracji → Track A na CFT70 i C3 G/H, porównanie z najlepszym baseline'em | Viktor | `docs/claims.md` z liczbą główną; jeśli Track B nie zdąży, piszemy tylko Track A |
| 4 | Zmiany z `01` §4 w UI | Viktor lub Davyd (po deployu) | Etykieta „Pre-flight range”, pasek „Mars transit · day N · 22 min”, fazy na osi X |
| 5 | Ekran wg makiety Alexa | Davyd | Kadry 12–26 s filmu nagrane z prawdziwego dashboardu |
| 6 | Film 30 s | Alex + Anna | Plik ≤ 30 s, napisy EN |
| 7 | Pitch 3 min + strona zgłoszenia EN + References | Petro + Anna | Próba na stoperze < 3:00; formularz wypełniony |

**Plan B, jeśli P2/P5 nie zdążą do checkpointu T+5:00:** film i pitch na replayu syntetycznym z wyraźną etykietą „synthetic, literature-based”; w pitchu mówimy, że ewaluacja na wydzielonych danych NASA jest przygotowana (loader, blokada testu) i jest następnym krokiem. Żadnych liczb wyników.

## 4. Kto nad czym pracuje teraz

| Osoba | Teraz | Brief |
|---|---|---|
| Viktor | core: P2 → P5 | `01` §4, `PLAN.md` |
| Davyd | deploy + domena | `01` §1, §5 |
| Alex | ekran + film | [`../ZADANIA-ALEX-DESIGN.md`](../ZADANIA-ALEX-DESIGN.md) |
| Anna | References, AI-ujęcia, napisy | `02` §4, `03` |
| Petro | pitch, kontrola prawdy, koordynacja | `00`, `03` |
