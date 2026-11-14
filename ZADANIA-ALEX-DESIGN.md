# Alex — zadania designu Space-Normal

**Od:** Petro (team lead) · **Data:** 2026-11-14 · **Pytania:** pisz do Petra na bieżąco, nie czekaj.

Ten plik ma Ci dać dwie rzeczy: **zrozumienie, co aplikacja robi**, i **kolejność pracy**, żeby z tego powstał ekran, film 30 s i slajdy. Zakres jest zamknięty — możesz projektować bez czekania na kolejne decyzje.

---

## 0. Space-Normal w 60 sekund

- **Wyzwanie NASA:** „Create Health Monitoring Software for Astronauts on Space Missions”. Kluczowe zdanie z opisu: *astronauts carry much of the responsibility for spotting these changes in themselves… enable astronauts to evaluate and act on the status of their health.*
- **Problem:** w kosmosie zdrowe ciało zmienia się w normalny sposób (np. temperatura w spoczynku rośnie do ok. 38°C, ciśnienie spada). Ziemska norma albo stały zakres sprzed lotu biorą taką adaptację za chorobę albo — po poluzowaniu — przeoczają prawdziwą chorobę. Dziś różnicę ocenia lekarz na Ziemi. W drodze na Marsa lekarz jest do 24 min opóźnienia dalej.
- **Nasze rozwiązanie:** każdy członek załogi ma **korytarz normy** — pasmo wartości, których *oczekujemy* u tej osoby w tym dniu misji. Korytarz przesuwa się razem z fazą misji. Alarm jest tylko wtedy, gdy pomiar wychodzi poza korytarz i nie tłumaczy go żadne zapisane zdarzenie (trening, zmiana grafiku, klimat w kabinie).
- **Główny użytkownik:** astronauta. Dostaje krótką kartę: **co widzimy → co sprawdzić teraz → kiedy eskalować**. Lekarz na Ziemi dostaje zwięzły pakiet, który dotrze z opóźnieniem.
- **Dane:** prawdziwe dzienne pomiary z badań NASA bed rest (ludzie leżą tygodniami z głową lekko w dół — naziemny analog lotu). Zawsze mówimy „ground analog”, nigdy „dane z lotu”.

---

## 1. Co przeczytać (ok. 40 min, w tej kolejności)

Repo: https://github.com/1hunder/nasa-space-apps-hackathon

| # | Plik | Branch | Co z niego wyciągnąć | Czas |
|---|---|---|---|---|
| 1 | `space-normal-merged-concept.md` — **§0, §2, §4, §7, §8** | `V2` | Idea, użytkownicy, **karta astronauty (§4)**, scenariusz 30-sekundowego demo (§7), co jest w zakresie (§8) | 15 min |
| 2 | `reports/Ziemskie normy w monitoringu astronautów.md` — tylko sekcja **„Werdykt dla pitchu”** (tabela „Wolno powiedzieć / Nie mówić”) | `V2` | Czego nie wolno pisać na ekranie i slajdach | 5 min |
| 3 | `README.md` | `p0-scaffold` | Jak działa silnik Viktora, krótko | 3 min |
| 4 | `web/src/contract.ts` | `p0-scaffold` | **Najważniejsze dla Ciebie:** jakie dane dostanie ekran. Tłumaczenie w §2 poniżej | 10 min |
| 5 | `web/public/cache/mission_synthetic_transplant_single.json` (otwórz w przeglądarce / VS Code, przewiń) | `p0-scaffold` | Jak wyglądają prawdziwe dane, które Davyd podłączy | 5 min |
| 6 | `Space-Normal-architecture.png` | `V2` | Obraz całości | 2 min |

**Zasada nadrzędna z kontraktu:** *the UI shows no number that is not in this JSON.* Nie projektuj liczb, których silnik nie liczy.

---

## 2. Funkcjonalność → elementy ekranu (słownik dla designera)

To jest tłumaczenie `contract.ts` na język ekranu. Każdy element, który projektujesz, powinien mieć tu swoje źródło.

### 2.1 Misja i scenariusze

Jeden plik JSON = jedna **misja** (`Mission`). Mamy 4 scenariusze — to są gotowe „historie” do demo:

| Scenariusz (`scenario`) | Co się dzieje | Rola w demo |
|---|---|---|
| `real_null` | Nikt nie choruje, tylko normalna adaptacja | „Spokojny dzień”: inne metody alarmują, Space-Normal milczy |
| `shared_event` | Cała załoga przesuwa grafik (dzień 30) | Wszyscy zmieniają się razem, ale to **wyjaśnione** → brak alarmu |
| `transplant_single` | Jedna osoba zaczyna chorować w dniu 41 | **Główny kadr:** wyjście z korytarza → karta astronauty |
| `transplant_outbreak` | 3 osoby chorują po kolei (dni 38–42) | Alert załogi: „sprawdź habitat ORAZ możliwą epidemię” |

Załoga ma **3–4 osoby** (`crew[]`, identyfikatory `id`). Projektuj tak, żeby działało dla obu liczb.

### 2.2 Parametry życiowe (`Vital`)

`pulse` (tętno), `temp_c` (temperatura), `resp_rate` (oddechy/min), `sbp` / `dbp` (ciśnienie skurczowe/rozkurczowe). Jeden pomiar dziennie. `null` = brak pomiaru tego dnia → pokaż lukę, nie zero.

### 2.3 Wykres korytarza (`VitalSeries`) — serce ekranu

Dla każdej osoby i każdego parametru, dzień po dniu:

| Pole | Po ludzku | Jak pokazać |
|---|---|---|
| `y` | Zmierzona wartość | Linia / punkty |
| `band_low`, `band_high` | **Korytarz normy** (dolna i górna granica) | Półprzezroczyste pasmo — najważniejszy element wizualny |
| `baseline` | Osobista norma sprzed misji | Opcjonalnie cienka linia |
| `adaptation` | Oczekiwana zmiana od kosmosu w tym dniu | Opcjonalnie (widok „rozłóż sygnał”) |
| `events` | Wpływ zapisanych zdarzeń (trening, grafik) | Opcjonalnie |
| `residual`, `z` | To, czego nic nie tłumaczy, i jak bardzo | Raczej nie na wykresie głównym; może w tooltipie |

Idea do pokazania: **oczekiwane = baseline + adaptation + events**, a alarm patrzy tylko na resztę. Wystarczy, że wykres to sugeruje — nie rób z tego wzoru na ekranie.

### 2.4 Cztery metody alarmowania (`DETECTORS`) — dowód, że jesteśmy lepsi

| Pole | Nazwa na ekranie (propozycja) | Co to jest |
|---|---|---|
| `fixed_thresholds` | **Earth thresholds** | Ziemskie progi kliniczne |
| `frozen_baseline` | **Static pre-flight range** | Stały zakres sprzed lotu — tak dziś planuje NASA w swojej koncepcji pokładowego wsparcia decyzji |
| `rolling_14` | **Rolling 14-day baseline** | Średnia z ostatnich 14 dni |
| `space_normal` | **Space-Normal** | Nasz korytarz |

Alarmy (`alerts[]`) mają: kto (`crew_id`), dzień (`day`), poziom `yellow`/`red`, parametr (`vital`). Pokaż je jako **ścieżki pod wykresem**: jeden wiersz na metodę, znacznik w dniu alarmu, licznik po prawej. Historia, którą ekran ma opowiadać: *trzy stare metody migają przy zdrowej adaptacji, Space-Normal reaguje tylko na prawdziwą chorobę.*

### 2.5 Stan układów (`SystemsDay`)

Na każdy dzień 4 układy: `cardio`, `resp`, `thermo`, `fluids`. Każdy ma stan:

| Stan | Znaczenie | Sugerowany kolor |
|---|---|---|
| `expected` | Zgodnie z oczekiwaniem | teal / zielony |
| `event` | Zmiana, ale wyjaśniona zdarzeniem | bursztynowy, spokojny |
| `unexplained` | Niewyjaśnione odchylenie | czerwony |
| `crew` | Część wspólnego dryfu załogi | fiolet / osobny kolor |
| `not_monitored` | Brak danych | szary |

Dobry pomysł na kompaktowy **pasek statusu załogi** (wiersz = osoba, 4 kropki = układy) albo mini-oś czasu.

### 2.6 Alert załogi (`crew_alerts`) i zdarzenia (`events`)

- `crew_alerts`: kilka osób dryfuje razem bez wyjaśnienia → baner **„Unexplained crew-wide shift: check habitat AND possible outbreak”**.
- `events`: zapisane zdarzenia (np. `schedule_shift`) → małe znaczniki na osi czasu.

### 2.7 Karta astronauty i pakiet dla lekarza (`notes`)

Dla czerwonych alarmów Space-Normal jest `Note`:

| Pole | Gdzie trafia |
|---|---|
| `text` | Treść karty / notatki |
| `questions` | Pytania „sprawdź teraz” (2–3 pytania, odpowiedź jednym tapnięciem) |
| `bytes` | „Packet 1.2 kB” w pakiecie dla lekarza |
| `context_items` | Kontekst ze źródłem — małym drukiem |
| `numbers_verified` | Mały znacznik „numbers verified” |

Format karty (z merged §4):

```
OBSERVATION   Resting heart rate +[X] bpm above your expected range for day 41.
              Not explained by logged exercise, sleep shift or cabin climate.
CHECK NOW     Measure temperature · answer 3 questions (~1 min)        [Start]
ESCALATE IF   [threshold from medical mentor] OR still elevated tomorrow
              → flight surgeon packet ready (1.2 kB, arrives ~12 min after send)
              Not a diagnosis.
```

### 2.8 Pochodzenie danych (`provenance`)

Każda misja ma etykiety: `REAL_BEDREST` (prawdziwe NASA bed rest), `REAL_EARTH_ILLNESS` (prawdziwe ziemskie sygnatury choroby), `SYNTHETIC`. **Zawsze widoczne** jako małe badge — to nasza uczciwość i punkty za „Validity”.

---

## 3. Zadania

Czas liczony od Twojego startu. Po każdym zadaniu wyślij Petrowi zrzut/link — odpowiem w 10 min.

### Zadanie 1 — Zrozumienie (0:00–0:45)

**Cel:** projektujesz funkcję, nie dekorację.

1. Przeczytaj pliki z §1.
2. Napisz Petrowi 4–5 zdań własnymi słowami: kim jest użytkownik, co widzi rano, czym różni się korytarz od stałego zakresu, co dzieje się przy alarmie.
3. Zapisz pytania, jeśli coś jest niejasne.

**Gotowe, gdy:** Petro potwierdzi, że rozumiesz tak samo jak my.

### Zadanie 2 — Mapa ekranu (0:45–1:15)

**Cel:** każdy element ma źródło w danych.

1. Zrób listę komponentów ekranu, przy każdym pole z §2, z którego bierze dane (np. „Wykres korytarza ← `y`, `band_low`, `band_high`”).
2. Zaznacz, co jest **must** (bez tego demo nie działa) a co **nice-to-have**.

Must według nas: header misji, pasek załogi, oś faz, wykres korytarza z zakładkami parametrów, ścieżki 4 metod alarmowania, karta astronauty, pakiet dla lekarza, badge pochodzenia danych, baner alertu załogi.

**Gotowe, gdy:** lista jest u Petra i Davyda.

### Zadanie 3 — Szkic low-fi (1:15–1:45)

**Cel:** szybko ustalić układ, zanim zaczniesz kolory.

Jeden ekran desktop 1440×900, bez nawigacji i podstron. Punkt wyjścia (możesz zmienić):

```
┌──────────────────────────────────────────────────────────────┐
│ Space-Normal · Mars transit (scenario) · Day 41 · Delay 12min │
│                                   [Ground analog: NASA bed rest]│
├──────────────┬───────────────────────────────────────────────┤
│ CREW         │ PHASE BAR: Baseline | Adaptation | Steady |   │
│ A ● ● ● ●    │            Readaptation           ▲ today     │
│ B ● ● ● ●    ├───────────────────────────────────────────────┤
│ C ● ● ● ●    │ [Pulse] [Temp] [BP] [Resp]                    │
│ (cardio/resp/│ CORRIDOR CHART: points + band + event marks    │
│ thermo/fluids│                                               │
│              ├───────────────────────────────────────────────┤
│              │ Earth thresholds       ▮ ▮▮ ▮▮▮        [N]    │
│              │ Static pre-flight      ▮▮ ▮▮▮▮         [N]    │
│              │ Rolling 14-day           ▮   ▮▮        [N]    │
│              │ Space-Normal                     ▮     [N]    │
├──────────────┴──────────────────────┬────────────────────────┤
│ ASTRONAUT CARD                      │ FLIGHT SURGEON PACKET   │
│ OBSERVATION / CHECK NOW / ESCALATE  │ Queued · 1.2 kB · ~12min│
└─────────────────────────────────────┴────────────────────────┘
```

**Gotowe, gdy:** Petro i Davyd zaakceptują układ.

### Zadanie 4 — Hi-fi + 4 stany ekranu (1:45–3:15)

**Cel:** te stany to dokładnie klatki filmu.

Zaprojektuj ekran w 4 stanach, jeden na scenariusz z §2.1:

| Stan | Scenariusz | Co widać |
|---|---|---|
| A. Calm adaptation | `real_null` | Korytarz się przesuwa, punkty w środku. Earth/Static/Rolling mają alarmy, Space-Normal — zero. Karta: „No action needed today.” |
| B. Explained shift | `shared_event` | Wszyscy bursztynowi (`event`), znacznik „schedule shift” na osi, brak alarmu Space-Normal |
| C. Real deviation | `transplant_single` | Jedna osoba wychodzi poza pasmo w dniu 41, czerwony stan, **karta astronauty wypełniona**, pakiet w kolejce |
| D. Crew alert | `transplant_outbreak` | Baner „check habitat AND possible outbreak”, kilka osób na czerwono z przesuniętym startem |

Plus mini-ekran **„Check now”**: 3 pytania (np. *Do you feel feverish? · Sleep last night? · Any new symptoms?*), odpowiedź jednym tapnięciem, przycisk „Send to flight surgeon packet”.

Wymagania:
- Teksty po angielsku.
- Kolory statusów rozróżnialne przy daltonizmie (kolor + kształt lub etykieta).
- Korytarz musi być czytelny na pierwszy rzut oka — to on „sprzedaje” pomysł.
- Liczby to `[X]` dopóki Viktor nie da prawdziwych.

**Gotowe, gdy:** 4 stany + ekran „Check now” są w Figmie.

### Zadanie 5 — Przekazanie Davydowi (3:15–3:45)

**Cel:** Davyd koduje bez zgadywania.

1. Link do Figmy z nazwanymi komponentami. **Nazywaj warstwy jak pola z kontraktu** (`band_low`, `alerts.space_normal`, `systems.cardio`…).
2. Tokeny: kolory hex (tło, tekst, 5 stanów z §2.5, 4 metody alarmowania, pasmo korytarza), font, rozmiary, odstępy.
3. 15 min rozmowy z Davydem: co jest statyczne, co z JSON.

**Gotowe, gdy:** Davyd potwierdzi, że ma wszystko.

### Zadanie 6 — Storyboard filmu 30 s (3:45–4:30)

**Cel:** film to nasze główne demo w zgłoszeniu (limit 30 s, angielskie napisy obowiązkowe).

Format 1920×1080, margines bezpieczeństwa u dołu na napisy. Kadry pochodzą ze stanów z Zadania 4:

| Czas | Kadr | Napis (EN, propozycja — Petro dopracuje) |
|---|---|---|
| 0–5 s | Header: Mars transit · day 41 · 12 min delay | *On the way to Mars, the doctor is 12 minutes away.* |
| 5–12 s | Stan A: trzy stare metody migają, Space-Normal spokojny | *A healthy body changes in space. Fixed limits call it illness.* |
| 12–20 s | Stan C: wyjście z korytarza → karta astronauty | *Space-Normal knows what's expected for you, today — and flags what isn't.* |
| 20–26 s | „Check now” → pakiet „arrives ~12 min” | *Check now. Escalate if needed. The doctor gets a short packet.* |
| 26–30 s | Karta końcowa: wynik `[X]` + „Real NASA bed rest data · ground analog” | *[headline result]* |

Najlepiej nagrać **działającą aplikację Davyda** (screen recording). Plan B: klikany prototyp z Figmy.

**Gotowe, gdy:** storyboard (klatki + napisy) jest u Petra.

### Zadanie 7 — 7 slajdów (4:30–6:00)

**Cel:** zapasowe demo i tło do pitchu. Limit **7 slajdów razem z tytułowym**, po angielsku. Teksty da Petro — Ty robisz układ i diagramy.

1. **Title** — Space-Normal + jedno zdanie + zespół.
2. **Problem** — zdrowy astronauta „wygląda na chorego” według ziemskich norm (ok. 38°C w spoczynku; 5 z 13 z anemią po lądowaniu); na Marsie brak lekarza w pętli.
3. **Gap** — dziś odróżnia to lekarz na Ziemi; planowane systemy NASA porównują ze stałym zakresem sprzed lotu, bez zmiany w fazach misji.
4. **Solution** — **diagram korytarza**: baseline + oczekiwana adaptacja + zdarzenia → alarm tylko na resztę. Najważniejszy diagram całej prezentacji.
5. **Demo** — zrzut stanu C.
6. **Results** — 3 duże liczby `[X]` od Viktora, podpis „ground analog, held-out test”.
7. **Honesty + roadmap** — co prawdziwe, co syntetyczne; następne moduły.

**Gotowe, gdy:** 7 slajdów z placeholderami jest u Petra.

---

## 4. Zasady (nie łam ich)

- **Język:** wszystko w UI, filmie i slajdach po angielsku.
- **Bez logo NASA** ani innych agencji. Możemy pisać „NASA bed rest data”, ale nie używamy ich znaków graficznych.
- **Zawsze „ground analog”**, nigdy „flight data”. Badge pochodzenia danych widoczny na każdym ekranie.
- **Nie piszemy:** „current ISS devices raise false alarms”, „healthy astronauts have higher heart rate in space”, „nobody has done personal baselines before”. Szczegóły w raporcie, tabela „Nie mówić”.
- **Karta to nie diagnoza** — zawsze „Not a diagnosis”.
- **Nie projektujemy:** aplikacji mobilnej, logowania, ciała 3D, chatbota, wielu podstron.

## 5. Checkpointy

| Kiedy | Co wysyłasz | Komu |
|---|---|---|
| T+0:45 | 4–5 zdań zrozumienia | Petro |
| T+1:15 | Mapa ekranu | Petro, Davyd |
| T+1:45 | Szkic low-fi | Petro, Davyd |
| T+3:15 | Hi-fi, 4 stany + „Check now” | Petro, Davyd |
| T+3:45 | Przekazanie (Figma + tokeny) | Davyd |
| T+4:30 | Storyboard filmu | Petro |
| T+6:00 | 7 slajdów | Petro |
