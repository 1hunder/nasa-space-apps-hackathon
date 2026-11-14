# Space-Normal — wersja połączona (plan v2.1 Viktora + brainstorm Petra)

**Status:** propozycja do akceptacji przez zespół. Łączy [space-normal-summary.md](space-normal-summary.md), [space-normal-claude-code-plan.md](space-normal-claude-code-plan.md) (Viktor) oraz [space-normal-brainstorm-handoff.md](space-normal-brainstorm-handoff.md) (Petro). Nic tu jeszcze nie zostało zmierzone: każda liczba poniżej jest albo cytowana, albo jest placeholderem, albo oznaczonym założeniem demo.

---

## 0. Werdykt w jednym akapicie

Zostawiamy **silnik Viktora** i opakowujemy go w **produkt Petra**. Plan Viktora ma najmocniejszy, obronny rdzeń: detektor świadomy adaptacji, zbudowany na prawdziwych danych NASA z bed rest, z nietkniętym zbiorem testowym, warstwą załogi i ograniczonym LLM. Brainstorm Petra dostarcza to, czego w planie brakuje: konkretny *powód istnienia* (transfer na Marsa, 4–24 min opóźnienia w jedną stronę, brak ewakuacji), *głównego użytkownika* (astronauta, nie tylko lekarz lotu), *krótki, wykonalny komunikat* (obserwacja → co sprawdzić → kiedy eskalować), *30-sekundowe demo*, *naukowe bezpieczniki* oraz *perspektywę kryteriów oceny i kwalifikacji*. Scenariusz termiczny/treningowy **nie** jest MVP: wymaga innej skali czasu i danych, których nie mamy. Staje się pierwszym modułem z roadmapy i warstwą „flight mode”, więc pomysł zostaje, a budowa nie jest zagrożona.

## 1. Co wnosi każda wersja

| Obszar | Viktor (summary + plan v2.1) | Petro (brainstorm handoff) | Wersja połączona |
|---|---|---|---|
| Rdzeń pomysłu | Rozkład sygnału: baza + oczekiwana adaptacja + zalogowane zdarzenia + residual; alarm tylko na residualu | Osobisty, zależny od fazy misji oczekiwany zakres | **Ten sam pomysł — zostaje jako rdzeń** |
| Dlaczego to ważne | Ewakuacja medyczna z ISS 2026, grypa na orbicie, „na Marsie nie ma ewakuacji” (jedno zdanie) | Transfer na Marsa, 4–24 min opóźnienia w jedną stronę, decyzja musi zapaść na pokładzie | **Framing Petra otwiera pitch** |
| Główny użytkownik | Lekarz lotu (notatka, dashboard) | Astronauta, krótki feedback | **Najpierw astronauta; lekarz dostaje zwięzły, opóźniony pakiet** |
| Wynik | Szuflada alertu, notatka dla lekarza, baner epidemii w załodze | Obserwacja → następne sprawdzenie → warunek eskalacji | **Karta dla astronauty w formacie Petra, wypełniona liczbami Viktora** |
| Dane | NASA bed rest NLSP (fit C1+C3, test CFT70), sygnatury chorób ze Stanford, OSDR | Te same źródła; nacisk na pochodzenie danych i kwalifikację (dane NASA) | **Plan danych Viktora + weryfikacja kwalifikacji Petra** |
| Sensory (narracja) | Dzienne pomiary punktowe; dane z wearables tylko do sygnatur chorób | Bez smartwatcha/iPhone'a; odzież pomiarowa (Bio-Monitor), instrumenty pokładowe, sprzęt treningowy | **Narracja sensorowa Petra; ziemskie dane z wearables zostają tylko danymi badawczymi** |
| Skala czasu | Dzienna | Ostrzeżenie: dzienne ≠ czas rzeczywisty; termika = w trakcie sesji | **Dzienny „poranny check”. Żadnych deklaracji czasu rzeczywistego** |
| Bezpieczeństwo | LLM nie może wyciszyć alarmu; severity = max(detektor, agent) | Bezwzględne limity bezpieczeństwa muszą przetrwać personalizację; wspólne pogorszenie może oznaczać problem z habitatem | **Dodajemy zawsze aktywną warstwę limitów niebezpieczeństwa; alert załogi brzmi „habitat lub epidemia”** |
| Deklaracje | „Nikt tego nie zaimplementował”; „residual znów wygląda jak na Ziemi” | Odrzuca obie jako niepotwierdzone | **Przeformułowane (§9)** |
| Demo | 3-minutowy replay dashboardu | 30-sekundowy film, jeden astronauta, jeden epizod | **30 s to zgłoszenie; 3 min to materiał dodatkowy** |
| Zakres | P0–P8, duży dashboard w React | „Bardzo mało funkcji” | **Podział must / should / later (§8)** |

## 2. Jedno zdanie i problem

**Jedno zdanie.** Space-Normal to pokładowa kontrola zdrowia załogi, która wie, jak zdrowe ciało *powinno* zmieniać się podczas długiej misji, i mówi astronaucie — w trzech linijkach, bez czekania na Ziemię — kiedy jego organizm schodzi z tej oczekiwanej ścieżki i co sprawdzić w następnej kolejności.

**Problem.**
- Lot kosmiczny z natury zmienia fizjologię (przesunięcie płynów, zmiany tętna i ciśnienia, anemia kosmiczna, wzrost temperatury głębokiej ciała). Ziemskie „normy” albo alarmują bez przerwy przy normalnej adaptacji, albo — po poluzowaniu — przeoczają prawdziwą chorobę.
- Na ISS lekarz lotu jest kilka minut stąd, a ewakuacja jest możliwa (pierwsza ewakuacja medyczna z ISS: styczeń 2026). W drodze na Marsa opóźnienie w jedną stronę wynosi **4–24 min** (w obie strony 8–48 min plus czas reakcji ludzi), a ewakuacji nie ma. Pierwsza ocena musi zapaść na pokładzie.
- Przegląd z chemii klinicznej z 2026 r. wzywa do stworzenia kosmicznych *reference change values* na podstawie podłużnych pomiarów na pokładzie (Kerremans i in.). Space-Normal przenosi tę ideę na rutynowo mierzone parametry życiowe.

## 3. Osadzenie w misji (Petro)

- Scenariusz: **transfer w stronę Marsa** w *referencyjnej* architekturze NASA Moon-to-Mars (koncepcja referencyjna Mars Transit Habitat, NTRS 2023). To nie jest zatwierdzona misja; żadnych wymyślonych dat startu.
- Założenia demo, oznaczone jako takie na ekranie: 4-osobowa załoga, ~41. dzień misji, **12 min opóźnienia w jedną stronę**.
- Analog naziemny jako dowód: 70-dniowy bed rest NASA z pochyleniem głową w dół (CFT70). Mówimy „analog”, nigdy „dane z lotu”.

## 4. Użytkownicy i wynik

**Główny: astronauta — karta porannego checku** (jeden ekran, tablet przy sprzęcie treningowym / w kwaterze):

```
OBSERWACJA      Tętno spoczynkowe +11 bpm powyżej Twojego oczekiwanego zakresu na dzień 41 (residual +3,2σ).
                Nie wyjaśniają tego zalogowany trening, przesunięcie snu ani klimat w kabinie.
SPRAWDŹ TERAZ   Zmierz temperaturę · odpowiedz na 3 pytania (≈1 min).
ESKALUJ, JEŚLI  [próg ustalony przez mentora medycznego] LUB nadal podwyższone jutro
                → pakiet dla lekarza gotowy (1,2 kB, dotrze ~12 min po wysłaniu).
                Nie jest to diagnoza.
```

Wszystkie liczby pochodzą z JSON-a z dekompozycją. Progi „sprawdź teraz” i „eskaluj, jeśli” to **placeholdery do czasu weryfikacji przez mentora medycznego** (zasada Petra).

**Drugorzędny: lekarz lotu — opóźniony pakiet.** Szablonowa notatka Viktora (najpierw residual, potem dekompozycja, kontekst z triage, odpowiedzi załogi), zoptymalizowana pod rozmiar dla łącza z opóźnieniem.

**Poziom załogi: alert wspólnego dryfu.** Gdy ≥2 członków załogi dryfuje razem, z przesuniętymi w czasie początkami, a żadne zalogowane zdarzenie tego nie wyjaśnia → „**Niewyjaśnione przesunięcie w całej załodze: sprawdź habitat ORAZ możliwą epidemię**”. Telemetria kabiny jest pokazywana jako kontekst.

## 5. Jak to działa (pipeline)

Wyłącznie skala dzienna.

1. **Wejścia.** Dzienne pomiary punktowe: tętno, temperatura ciała, częstość oddechów, ciśnienie skurczowe/rozkurczowe. Sensory w narracji: odzież/opaska typu Bio-Monitor, pokładowy zestaw medyczny, logi sprzętu treningowego. Kontekst: grafik/trening/sen, temperatura/wilgotność/CO2 w kabinie.
2. **Osobista baza.** Mediana + MAD sprzed lotu (sprzed bed rest), z korektą na małą próbę.
3. **Oczekiwana adaptacja.** Krzywe populacyjne + **rozrzut między osobami** dopasowane na kampaniach bed rest NASA C1 + C3. Skala indywidualna ograniczona do [0,3; 2], zamrożona po 21. dniu. Tryb „flight mode” dodaje cytowane warstwy z literatury (np. wzrost temperatury głębokiej, Stahn 2017; utrata snu; choroba lokomocyjna) — syntetyczne, oznaczone.
4. **Zalogowane zdarzenia.** Sesje treningowe, zmiany grafiku, klimat w kabinie; współczynniki ustalone przed testem. Trening jest *wyjaśniany*, a nie alarmowany (Petro: wysoki wysiłek to nie automatycznie problem).
5. **Detektor residualu.** Jednostronny CUSUM na residualu; żółty/czerwony; 3-dniowy burn-in; podwyższona czułość dla reszty załogi po alercie u jednej osoby.
6. **Warstwa limitów niebezpieczeństwa (nowość, od Petra).** Szerokie bezwzględne limity, których **żadna personalizacja nie może poszerzyć** (wartości od mentora medycznego). Działa niezależnie; raportowana osobno w ewaluacji, żeby nie zaburzać porównania fałszywych alarmów.
7. **Warstwa załogi.** Wspólny niewyjaśniony dryf → alert „habitat albo epidemia”. Nigdy nie odejmujemy mediany załogi.
8. **LLM (opcjonalny, nigdy nie decyduje).** Formułuje tekst karty i notatki dla lekarza z danych strukturalnych, wybiera pytania ze stałej checklisty, dodaje kontekst oznaczony „niezweryfikowany czynnik”. Nie może wywołać, opóźnić ani obniżyć alarmu. Kontrola zgodności liczb; przy błędzie wraca do surowego szablonu. Deterministyczny stub offline — demo nigdy nie sugeruje, że chmurowy LLM działa na pokładzie.

## 6. Dane i dowody (Viktor, z weryfikacją Petra)

| Źródło | Rola | Etykieta pochodzenia |
|---|---|---|
| NASA Life Sciences Portal, bed rest: C1 + C3 | Dopasowanie priorów adaptacji + rozrzutu | REAL_BEDREST |
| NASA bed rest CFT70 (kampania 11) | **Wydzielony test** — nigdy nie używany do dopasowania/strojenia | REAL_BEDREST |
| Stanford COVID-19 wearables P1 + P2 | Prawdziwe sygnatury chorób, przeszczepiane do tętna z bed rest | REAL_EARTH_ILLNESS (dane badawcze, nie proponowane urządzenie dla astronautów) |
| NASA OSDR Environmental Data App | Kontekst CO2/temperatury w kabinie; wspiera kwalifikację (dane NASA) | REAL_ISS_CONTEXT, bez zakładanego wpływu fizjologicznego |
| Tabela z literatury | Warstwy flight mode | SYNTHETIC (cytowane) |
| Homekit2020 | Opcjonalnie, tylko jeśli dostaniemy dostęp | — |

**Ewaluacja** (bez zmian względem v2.1): Track A — fałszywe alarmy na załogo-miesiąc na czystych danych CFT70 (główny wynik); Track B — czułość i wyprzedzenie dla przeszczepionych chorób przy wyrównanym budżecie fałszywych alarmów; baseline'y = ziemskie progi, zamrożona baza, rolling recalibration; hash konfiguracji zamrożony przed dotknięciem CFT70. Track C (ślepy generator) i D (prawdziwe zdarzenia z logów) to „should”, nie „must”.

**Deklaracja, którą wolno nam postawić:** „Na prawdziwych danych NASA z bed rest, nigdy nieużytych do dopasowania, Space-Normal wygenerował X fałszywych alarmów na załogo-miesiąc w okresie adaptacji wobec Y dla najlepszego rolling baseline'u i wykrył Z% przeszczepionych prawdziwych sygnatur chorób, z medianą L dni przed objawami. Analog naziemny; nie testowane na danych astronautów.”

## 7. Demo

**30-sekundowy film zgłoszeniowy** (format Petra, treść Viktora):

| Czas | Na ekranie |
|---|---|
| 0–5 s | „Transfer na Marsa · dzień 41 · 12 min opóźnienia w jedną stronę” (oznaczone założenie). 4 osoby w załodze, badge danych z analogu. |
| 5–12 s | Przyspieszony replay: ścieżki ziemskich progów i rolling baseline'u migają fałszywymi alarmami w trakcie adaptacji; Space-Normal zostaje zielono-niebieski (teal). |
| 12–20 s | Tętno jednej osoby wychodzi poza oczekiwany korytarz → karta astronauty: obserwacja → sprawdź teraz → eskaluj, jeśli. |
| 20–26 s | Astronauta odpowiada na 2 pytania; pakiet dla lekarza w kolejce „dotrze za ~12 min”; badge „severity zablokowane”. |
| 26–30 s | Główny wynik z `claims.json` + „NASA bed rest CFT70 (wydzielony test) · sygnatury chorób ze Stanford · analog naziemny”. |

**Wersja 3-minutowa** (dodatkowa): zakładki Viktora — burn-in, wspólne zdarzenie (wszystko bursztynowe, brak alarmu), choroba, epidemia, ekran Proof z „gdzie przegrywamy”.

## 8. Zakres na hackathon

| Must (bez tego demo nie istnieje) | Should | Later / roadmapa |
|---|---|---|
| Pobranie NLSP + inwentaryzacja (P1) — fallback syntetyczny, jeśli zablokowane | Track C, ślepy generator | Moduł termiczny/treningowy w trakcie sesji |
| Dopasowanie priorów C1+C3 (P2) | Track D, prawdziwe zdarzenia z logów medycznych | Wersja z filtrem Kalmana, ablacja LightGBM |
| Przeszczep + pseudo-załogi (P3) | Agent triage LLM (ponad szablonowy tekst) | Ciało 3D, rPPG z kamery, Homekit |
| Prosty model + CUSUM + warstwa załogi + baseline'y + warstwa limitów niebezpieczeństwa (P4) | Ekrany Proof + Data & Honesty (inaczej: slajdy) | Fazy po locie / powrotu |
| CFT70 Track A + B z zamrożonym hashem (P5) | Mapa ciała 2D | Szerszy zestaw sensorów (SANS, kości, odporność) |
| Szablonowa karta + notatka dla lekarza + stub offline | | |
| Jeden ekran: pasek załogi, wykres korytarza, ścieżki alarmów, karta astronauty | | |
| 30-sekundowy film | | |

Nigdy nie wycinamy: wydzielonego CFT70, Track A, rolling baseline'u, porównania przy wyrównanym budżecie, etykiet pochodzenia danych, wykresu korytarza.

## 9. Deklaracje — poprawione sformułowania

| Oryginał (summary) | Zamiast tego |
|---|---|
| „Według naszej wiedzy nikt tego nie zaimplementował.” | „Nie znaleźliśmy publicznej implementacji kosmicznych oczekiwanych trajektorii dla rutynowych parametrów życiowych.” |
| „Po usunięciu wpływu kosmosu i środowiska residual znów wygląda jak na Ziemi, więc ziemskie detektory działają na orbicie.” | „**Hipoteza, którą testujemy:** po usunięciu oczekiwanej adaptacji i zalogowanych zdarzeń residuale zachowują się jak ziemskie. Track B mierzy, jak dobrze odzyskujemy przeszczepione ziemskie sygnatury chorób.” |
| Wspólny czynnik załogi szacowany ze współruchu załogi + CO2 | Odejmujemy tylko zalogowane zmienne; współruch załogi to **alert**, a nie korekta. Bez zakładanego wpływu CO2. |
| LightGBM / 1D-CNN na residualu | CUSUM; ML tylko jako opcjonalna ablacja. |
| HRV jako cecha | Usunięte: brak w dostępnych zbiorach danych. |
| LLM zamienia teksty załogi na słabe etykiety | Wycięte. |
| „Niska hemoglobina → zjedz batonik”, „wysokie tętno → zwolnij”, przewidywanie naciągnięcia mięśnia | Nie deklarujemy. Pulsoksymetria ≠ hemoglobina; trening ≠ problem; brak przewidywania urazów. |

## 10. Pomysł termiczny/treningowy — gdzie trafia

Scenariusz termiczny Petra jest naukowo sensowny (Stahn 2017: szybszy/wyższy wzrost temperatury głębokiej podczas treningu w kosmosie), ale wymaga ciągłych danych w trakcie sesji i osobnej ewaluacji; dzienne dane z bed rest go nie zwalidują. Wchodzi do wersji połączonej dwukrotnie, nie blokując budowy:

1. **Warstwa flight mode:** wzrost temperatury głębokiej w locie jest już cytowanym priorem w syntetycznym scenariuszu flight mode.
2. **Slajd z roadmapą:** „Ta sama dekompozycja, krótsza skala czasu: oczekiwana odpowiedź termiczna dla tego obciążenia, tej osoby, tego dnia misji → alert na niewyjaśnione nagrzewanie lub wolną regenerację.” Pokazywany jako następny moduł, nie jako działająca funkcja.

## 11. Otwarte decyzje (potrzebne tak/nie od zespołu)

1. **Akceptacja werdyktu:** dzienny detektor adaptacji = MVP; termika = roadmapa. (Rekomendowane.)
2. **Kwalifikacja:** potwierdzić, które źródło NASA jest w zakładce Resources tego wyzwania (OSDR? NLSP?) i że nasze użycie się liczy.
3. **Mentor medyczny:** kto ustala limity niebezpieczeństwa i progi „eskaluj, jeśli” na karcie.
4. **Dostęp do NLSP:** najpierw inwentaryzacja; jeśli dzienne parametry per osoba nie dają się pobrać, w ciągu pierwszych godzin decydujemy o fallbacku (dane syntetyczne + literatura, uczciwie oznaczone).
5. **Widoczność repo** na potrzeby zgłoszenia — osobna decyzja.

Po akceptacji: zaktualizować `space-normal-summary.md` do tego ujęcia i uzupełnić plan v2.1 o §4 (karta astronauty), §5.6 (warstwa limitów niebezpieczeństwa), §7 (30-sekundowe demo) i §8 (lista cięć).
