# Space-Normal — produkt, ekrany i zakres

Dla: Alex (design), Viktor i Davyd (implementacja), agentów kodujących.
Kontekst i uzasadnienie: [`00-kontekst.md`](00-kontekst.md). Specyfikacja techniczna: [`../PLAN.md`](../PLAN.md) (EN, Viktor). Ten plik mówi, **co z PLAN.md zmienia się po researchu** i **co projektujemy**.

---

## 1. Jeden ekran, trzy warstwy

Dashboard już istnieje (`web/`, replay syntetycznych misji, ok. 15 s). Projektujemy **jeden główny ekran**, czytelny w 3 sekundy w filmie:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ MARS TRANSIT · DAY 80 · ONE-WAY DELAY 22 MIN · NO PHYSICIAN ON BOARD     │  ← pasek misji (założenia demo)
│ [ANALOG DATA: NASA bed rest]  [FLIGHT-LIKE: literature, synthetic]        │  ← etykiety pochodzenia, zawsze widoczne
├───────────────┬──────────────────────────────────────────────────────────┤
│ CREW          │  Anna · Core temperature                                 │
│ ● Anna   ok   │                                                          │
│ ● Ben    ok   │  ═══════ Earth normal (flat) ══════════════════════════  │
│ ● Chen   !    │        ╭───── Space-Normal corridor (bends) ─────╮       │
│ ● Dara   ok   │  ▓▓▓▓▓▓ Pre-flight range (flat, NASA CDSS idea) ▓▓▓▓▓▓   │
│               │  start   |adaptation|   steady state   |  day 80 ●       │  ← fazy misji na osi X
│               │                                                          │
│               │  Alarms:  Earth normal ███ ██ ████   Pre-flight ██████   │
│               │           Space-Normal  ·  ·  ·  (quiet)                 │
├───────────────┴──────────────────────────────────────────────────────────┤
│ CARD FOR CHEN                                                            │
│ OBSERVATION   Resting pulse +9 bpm above YOUR expected range for day 80. │
│               Not explained by logged exercise, sleep shift or cabin.    │
│ CHECK NOW     Take temperature · answer 3 questions (~1 min)             │
│ ESCALATE IF   [threshold – medical mentor] OR still high tomorrow        │
│               → flight-surgeon packet queued (arrives ~22 min after send)│
│               Not a diagnosis.                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

**Najważniejsza rzecz na ekranie:** różnica między **płaskimi pasami** (ziemska norma, zakres sprzed lotu) a **uginającym się korytarzem**. Jeśli juror zobaczy tylko to, wygraliśmy Creativity.

## 2. Zasady designu

- **Jeden wykres, trzy pasy, jedna kropka.** Reszta jest drugorzędna.
- **Kolory znaczeń:** ziemska norma i zakres sprzed lotu — neutralne/szare, ich alarmy czerwone; korytarz Space-Normal — jeden wyróżniony kolor (obecnie teal); alarm Space-Normal — bursztyn/czerwień tylko gdy reszta wychodzi poza korytarz.
- **Fazy misji na osi X** (adaptacja → stan ustalony → …): to wizualnie mówi „korytarz zależy od fazy”.
- **Karta po angielsku**, 3 nagłówki: OBSERVATION / CHECK NOW / ESCALATE IF. Zawsze „Not a diagnosis.”
- **Etykiety pochodzenia danych** zawsze widoczne (Validity + uczciwość).
- **Bez logo NASA** i bez stylizacji na oficjalny produkt NASA. Piszemy „NASA data”, „NASA bed rest”.
- Ekran musi być czytelny w filmie przy 1080p na telefonie: duże fonty, mało tekstu.

## 3. Zakres na hackathon

| Must (bez tego nie ma demo) | Should | Roadmapa (tylko w pitchu) |
|---|---|---|
| Ewaluacja na prawdziwych danych NASA: wydzielony test (CFT70, C3 G/H), fałszywe alarmy na osobo-miesiąc vs zakres sprzed lotu / ziemskie progi / rolling | Track D: prawdziwe zdarzenia z logów bed rest (przypadki) | Powierzchnia Marsa i powrót jako kolejne fazy korytarza |
| Przeszczepione sygnatury chorób (Stanford): czułość i ile dni wcześniej | Pytania samooceny (sen, nastrój, objawy) na karcie — dotyka „behavioral health” z wyzwania | Moduł termiczny w trakcie treningu (Stahn 2017) |
| Główny ekran z trzema pasami + karta + lista załogi | Pakiet dla lekarza (notatka) w widoku szczegółów | Więcej parametrów: SANS, kości, odporność |
| Pasek misji „Mars transit · day N · 22 min” + fazy na osi X | Alert wspólnego dryfu załogi w filmie | Integracja z CDSS (np. przekazanie kontekstu do asystenta diagnostycznego) |
| `docs/claims.md` z liczbami generowanymi przez pipeline | Deploy pod własną domeną | |
| Deploy publiczny (link w zgłoszeniu) | | |

Nigdy nie wycinamy: wydzielonego testu, porównania z zakresem sprzed lotu, etykiet pochodzenia, wykresu z korytarzem.

## 4. Zmiany względem PLAN.md i obecnego kodu (delta po researchu)

| Gdzie | Zmiana | Dlaczego |
|---|---|---|
| `web/src/labels.ts` | `frozen_baseline` nazwać **„Pre-flight range”** (how: „Personal range fixed before launch — NASA CDSS concept”) zamiast „Earth-normal monitor”. `fixed_thresholds` zostaje jako **„Earth normal”** | NASA planuje właśnie zakres sprzed lotu (HRP-48033); to nasz prawdziwy rywal, nie ziemska norma |
| Ewaluacja / claims | Główne porównanie: **Space-Normal vs zakres sprzed lotu** (przy wyrównanym budżecie fałszywych alarmów); ziemskie progi jako dodatkowa linia | Jw. |
| Dashboard | Pasek misji: „Mars transit · day N · one-way delay 22 min · no physician on board” (oznaczone jako założenie demo) | Zawężenie do misji na Marsa, NASA-STD-3001 Rev C |
| Dashboard | Fazy misji na osi X | NASA TH-8LM „throughout all mission phases” |
| Teksty, pitch, README | 22 min zamiast 24; dodać ~2 tygodnie bez łączności | Źródła NASA |
| Karta | Główny użytkownik = astronauta; CMO = widok załogi | Tekst wyzwania |
| Scenariusz temperatury | Zostaje jako **flight-like (literatura, syntetyczne)** — w bed rest temperatura się nie zmienia | `data_notes.md` §5 |
| Tętno z bed rest | Nie przedstawiać jako przewidywania dla lotu | W locie tętno spoczynkowe się nie zmienia (Norsk 2015) |

## 5. Definicja „gotowe” dla demo

- Dashboard publicznie dostępny pod linkiem, otwiera się na scenariuszu z filmu.
- Każda liczba na ekranie i w filmie ma źródło w `docs/claims.md` albo w [`02-dowody-nasa.md`](02-dowody-nasa.md).
- Etykiety „analog” / „synthetic” widoczne w każdym kadrze, gdzie są dane.
- Strona zgłoszenia po angielsku, pole References kompletne (lista w `02-dowody-nasa.md` §4).
