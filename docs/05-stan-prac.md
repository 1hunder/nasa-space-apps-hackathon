# Space-Normal — stan prac i następne zadania

**Aktualizuje:** owner zadania po każdym ukończonym kroku (zmień wiersz + datę). **Ostatnia aktualizacja:** 2026-11-15, 00:05 (Petro; stan odczytany z repo — Viktor i Davyd potwierdzają).

Fazy według [`../PLAN.md`](../PLAN.md) §16. Priorytety według [`01-produkt-i-zakres.md`](01-produkt-i-zakres.md) §3–4.

## 1. Co już działa (na `main`)

| Faza | Co | Dowód w repo |
|---|---|---|
| P0 | Szkielet, schemat danych, generator syntetyczny, pipeline → JSON, kontrakt dashboardu, CI | `make demo-synthetic`, `web/src/contract.ts`, `.github/workflows/ci.yml` |
| P1 | Pobieranie i loader NASA bed rest (301 plików), loader Stanford, inwentaryzacja danych | `scripts/fetch_nlsp.py`, `src/spacenormal/data/nlsp.py`, `docs/data_notes.md` |
| P4 (częściowo) | Prosty model (baza + adaptacja × skala osobista + zdarzenia → residual), CUSUM, warstwa załogi, baseline'y (ziemskie progi, zakres sprzed lotu, rolling) | `src/spacenormal/model/simple.py`, `detect/`, `baselines.py` |
| P7 (częściowo) | Dashboard React z replayem 4 syntetycznych misji, korytarz temperatury, lista załogi, karta alertu | `web/src/` |
| Dokumenty | Kontekst, research, mapa wymagań NASA, pitch i film | `docs/` |

## 2. Czego jeszcze nie ma

| Faza | Brakuje | Plik docelowy |
|---|---|---|
| P2 | Dopasowanie krzywych adaptacji i rozrzutu między osobami na C1 + C3 (prawdziwe dane NASA); ekstrakcja sygnatur chorób ze Stanford (dane jeszcze niepobrane) | `src/spacenormal/priors/` (pusty), `priors_bedrest.json` |
| P3 | Pseudo-załogi z prawdziwych osób, przeszczep sygnatur chorób | `src/spacenormal/sim/` |
| P5 | Hash konfiguracji → ewaluacja na wydzielonym teście → liczba główna | `scripts/hash_config.py` (brak), `src/spacenormal/eval/` (pusty), `docs/claims.md` (stub) |
| — | Zmiany z `01` §4 (nazwy w UI, pasek misji, fazy na osi X) | `web/src/labels.ts`, `web/src/components/` |
| — | Publiczny deploy | — |
| — | Film 30 s, strona zgłoszenia, References | — |

## 3. Następne zadania (kolejność = priorytet)

| # | Zadanie | Owner | Gotowe, gdy |
|---|---|---|---|
| 1 | ~~Publiczny deploy obecnego dashboardu~~ **zrobione:** https://spacenormal.vercel.app/ | Davyd | Link otwiera replay; wpisany tutaj |
| 2 | P2: krzywe adaptacji z C1 + C3 dla tętna i ciśnienia | Viktor | Plik z priorami + krótki opis w `data_notes.md` |
| 3 | P5 minimum: hash konfiguracji → Track A na CFT70 i C3 G/H, porównanie z najlepszym baseline'em | Viktor | `docs/claims.md` z liczbą główną; jeśli Track B nie zdąży, piszemy tylko Track A |
| 4 | Odchudzenie i poprawki dashboardu wg [`../ZADANIA-VIKTOR-DASHBOARD.md`](../ZADANIA-VIKTOR-DASHBOARD.md) (A + B = P0; zawiera zmiany z `01` §4) | Viktor | Lista „Gotowe, gdy” z briefu; deploy zaktualizowany |
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
