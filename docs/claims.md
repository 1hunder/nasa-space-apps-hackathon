# Claims — wyniki do cytowania

**Stan: BRAK WYNIKÓW.** Ewaluacja na wydzielonym teście (faza P5 z `PLAN.md`) jeszcze się nie odbyła. Do tego czasu w filmie, prezentacji i na stronie zgłoszenia używamy tylko placeholderów `{X}`, `{Y}`, `{S}` — **nie wpisujemy żadnych liczb wyników**.

## Jak ten plik powstaje

1. Przed pierwszym dotknięciem zbioru testowego `scripts/hash_config.py` dopisuje tu hash zamrożonej konfiguracji. Dopiero wtedy loader (`src/spacenormal/data/nlsp.py`) odblokowuje splity testowe.
   **Uwaga dla agentów:** nie wpisuj tu ręcznie żadnego hasha ani linii w formacie klucza hasha — to odblokowałoby test bez zamrożenia konfiguracji.
2. Pipeline ewaluacji (P5) dopisuje liczbę główną z przedziałami ufności, Track A (fałszywe alarmy na prawdziwym null), Track B (czułość i wyprzedzenie na przeszczepionych chorobach).
3. Dashboard czyta te same liczby z `claims.json` (wersja maszynowa, generowana razem z tym plikiem). Ten plik jest wersją dla ludzi i tekstów.

## Szablon liczby głównej (z `PLAN.md` §12)

> On real NASA bed rest data never used for fitting, Space-Normal produced {X} false alarms per crew-month during adaptation, against {Y} for the best baseline, and detected {S}% of transplanted real illness signatures, a median {L} days before symptom onset. Bed rest is a ground analog; this has not been tested on astronaut data.

Porównanie „best baseline” = najlepszy z: ziemskie progi, zakres sprzed lotu, rolling recalibration — przy wyrównanym budżecie fałszywych alarmów. Patrz `docs/01-produkt-i-zakres.md` §4.
