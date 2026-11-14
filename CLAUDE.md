# Instrukcja dla agentów — Space-Normal (NASA Space Apps 2026)

Projekt: oprogramowanie do monitoringu zdrowia astronautów w tranzycie na Marsa. Osobisty korytarz normy parametrów życiowych, zależny od dnia misji; alarm tylko na tym, czego nie tłumaczy oczekiwana adaptacja.

## Zanim zaczniesz

1. Przeczytaj [`docs/00-kontekst.md`](docs/00-kontekst.md) — źródło prawdy. Jeśli coś mu przeczy, wygrywa on.
2. Mapa dokumentów: [`docs/README.md`](docs/README.md).
3. Kod: [`README.md`](README.md) (uruchomienie) i [`PLAN.md`](PLAN.md) (specyfikacja) + delta w [`docs/01-produkt-i-zakres.md`](docs/01-produkt-i-zakres.md) §4.

## Zasady

- **Dokumenty projektu piszemy po polsku.** Kod, komentarze w kodzie, UI, strona zgłoszenia i film — po angielsku.
- **Uczciwość danych:** bed rest to analog naziemny, nie lot. Dane syntetyczne zawsze oznaczone. Żadnych liczb wymyślonych ani przepisanych ręcznie — liczby wyników tylko z `docs/claims.md` (generuje pipeline), fakty tylko z [`docs/02-dowody-nasa.md`](docs/02-dowody-nasa.md).
- **Czego nie twierdzić:** lista w `docs/00-kontekst.md` §10 (np. „obecne systemy na ISS fałszywie alarmują”, „24 min”, „zdrowy astronauta ma w kosmosie wyższe tętno”).
- **Wydzielony zbiór testowy** (CFT70, Campaign 3 G/H) nigdy do strojenia — loader blokuje go do czasu zapisania hasha konfiguracji.
- **LLM nie decyduje** o alarmie (nie wywołuje, nie opóźnia, nie obniża).
- **Git:** `main` = kod (PR-y), `V2` = dokumenty Petra → PR do `main`. Nie pushuj bezpośrednio na cudzy branch.
