# Space-Normal — kontekst projektu (źródło prawdy)

**Stan na:** 2026-11-14 · **Właściciel:** Petro · **Status:** kierunek zaakceptowany przez team leada.
Jeśli inny dokument mówi coś innego niż ten, **wygrywa ten**. Zmiany kierunku wpisujemy tutaj.

---

## 1. Jedno zdanie

**Space-Normal to „siatka centylowa” dla astronauty w drodze na Marsa:** każdego ranka sprawdza, czy parametry życiowe każdego członka załogi mieszczą się w jego **osobistym korytarzu normy na dany dzień misji**, i mówi astronaucie w trzech linijkach, co sprawdzić, zanim ktokolwiek poczuje się źle — bez lekarza na pokładzie i bez łączności z Ziemią.

## 2. Wyzwanie (NASA Space Apps 2026)

**Create Health Monitoring Software for Astronauts on Space Missions**

> Long-duration missions expose astronauts to space radiation, isolation and confinement, altered gravity, and a hostile closed environment, which can bring immune changes, bone loss, cardiovascular events, and behavioral health problems. On long missions, astronauts carry much of the responsibility for spotting these changes in themselves. Your challenge is to build a health monitoring software that gathers health indicators and enables astronauts to evaluate and act on the status of their health.

Kluczowe słowa wyzwania, na które odpowiadamy: **„spotting these changes in themselves”**, **„evaluate and act”**.

## 3. Misja, do której się zawężamy

**Tranzyt załogowy na Marsa, faza mikrograwitacji** (lot Ziemia → Mars). Powierzchnia Marsa i powrót = roadmapa.

| Parametr | Wartość | Źródło |
|---|---|---|
| Data misji | Brak oficjalnej; administrator NASA: „before 2040” | wywiad Isaacman 2026 (prasa) |
| Czas całej misji | ok. 2–3 lata | NASA ADD Rev C (2025) |
| Załoga | ≥ 4 osoby (rozważane do 6) | ADD Rev C, EIMO 2023 |
| Opóźnienie łączności | **do 22 min w jedną stronę** (nie 24!) | ASCEND/NASA, 2025 Architecture Update |
| Przerwy w łączności | **ok. 2 tygodnie** przy koniunkcji Słońca | HRP 48021 (2019) |
| Ewakuacja | brak | NASA TH-8LM |
| Lekarz na pokładzie | **nie jest wymagany** | NASA-STD-3001 Vol 1 Rev C |

Dlaczego tranzyt: dane NASA z bed rest to analog **mikrograwitacji**, nie grawitacji Marsa (3/8 g). Uczciwie walidują tylko tę fazę. NASA sama dzieli misję na fazy (ADD: UC-X-107 przestrzeń kosmiczna / okolice Marsa vs UC-X-108 powierzchnia).

Odpowiedź na „to dopiero za 15 lat”: NASA w celu **HBS-2LM** wymaga, by systemy zdrowia niezależne od Ziemi były walidowane **stopniowo, już teraz** (analogi, ISS, Księżyc). Test na analogu naziemnym to dokładnie ten krok. Baza księżycowa (Artemis) też będzie miała opóźnienia i dni do ewakuacji.

## 4. Problem (wersja dowodowa)

1. **Na pokładzie nie będzie lekarza w pętli.** NASA-STD-3001 Rev C: Crew Medical Officerzy (min. 2 na pojazd) „often are, but are not required, to be physicians”. Standard wymaga „monitoring, and trending vital signs” i „autonomous medical care”. EIMO 2023: wiedza medyczna „via a skilled medical practitioner **and/or a highly functional CDSS**”.
2. **Lekarz na Ziemi jest za daleko:** do 44 min na pytanie i odpowiedź, 2 tygodnie ciszy przy koniunkcji, brak ewakuacji.
3. **Ziemskie normy nie pasują do zdrowego astronauty.** Zdrowy astronauta po ~2,5 mies. ma ok. **38°C** w spoczynku (Stahn 2017); **5 z 13** spełnia kryteria anemii WHO po lądowaniu (Trudel 2022). Działa to też w drugą stronę: ciśnienie spada ~10 mmHg, rzut serca rośnie 41% — i wszystko **mieści się w normie**, więc ziemska norma tego nie zobaczy (Norsk 2015).
4. **Płaska norma osobista też nie wystarcza.** Koncepcja NASA (CDSS ConOps HRP-48033, 2021) sprawdza wyniki „within pre-flight determined reference ranges” — czyli względem płaskiego zakresu sprzed lotu. A ciało w kosmosie **powinno** się zmieniać.

**Uczciwie:** nie znaleźliśmy dowodu, że dzisiejsze systemy na ISS fałszywie alarmują — dziś dane interpretuje lekarz na Ziemi. Problem dotyczy **przyszłego automatu**, który ma tego lekarza zastąpić. Szczegóły: [`research/raport-normy-ziemskie.md`](research/raport-normy-ziemskie.md).

## 5. Rozwiązanie: korytarz

**Korytarz = pas na wykresie, w którym parametr *tej osoby* powinien być *w tym dniu misji*.** Analogia: siatka centylowa u pediatry — dziecko porównujemy z oczekiwanym wzrostem dla jego wieku i pilnujemy, czy trzyma się swojego kanału.

```
Temperatura
 38.0 ┤                                  ╭──────────── KORYTARZ Space-Normal (ugina się z misją)
      │                        ╭─────────╯   ●  dzień 80: 37,7°C
 37.5 ┤═══════════════════════════════════════════════ ZIEMSKA NORMA (płaska, dla wszystkich)
      │              ╭─────────╯
 37.0 ┤    ╭─────────╯
      │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ZAKRES SPRZED LOTU (płaski, osobisty; koncepcja NASA)
 36.5 ┤▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
      └────┬─────────┬─────────┬─────────┬──────────
         start     dz.30     dz.60     dz.90      dzień misji
```

| Sposób oceny pomiaru 37,7°C w dniu 80 | Wynik | Słusznie? |
|---|---|---|
| Ziemska norma | „stan podgorączkowy” | ❌ fałszywy alarm |
| Zakres sprzed lotu (NASA CDSS) | „daleko poza normą” | ❌ fałszywy alarm |
| Korytarz Space-Normal | „tak powinno być u Ciebie w dniu 80” | ✅ |

I odwrotnie: 37,0°C w dniu 80 → ziemska norma i zakres sprzed lotu mówią „OK”, korytarz mówi „nietypowo jak na ten etap” → **wyłapujemy przeoczenia**.

Jak to działa technicznie (szczegóły: [`../PLAN.md`](../PLAN.md)): pomiar = osobista baza sprzed lotu + oczekiwana adaptacja na dany dzień (dopasowana na danych NASA) + efekt zalogowanych zdarzeń (trening, sen, klimat w kabinie) + **reszta**. Alarm tylko na reszcie (CUSUM). Do tego: twarde limity bezpieczeństwa, których personalizacja nie może poszerzyć, oraz alert załogowy („kilka osób dryfuje naraz → sprawdź habitat albo epidemię”).

## 6. Użytkownicy (kolejność ważności)

1. **Każdy astronauta** — rano karta w 3 linijkach: **OBSERWACJA → SPRAWDŹ TERAZ → ESKALUJ, JEŚLI**. Odpowiada na „spotting changes in themselves… evaluate and act”.
2. **Crew Medical Officer** (członek załogi z kilkunasto–kilkudziesięciogodzinnym szkoleniem, nie lekarz) — widok całej załogi: kto w korytarzu, kto wypada, alert wspólnego dryfu.
3. **Lekarz lotu na Ziemi** — mały pakiet tylko gdy coś wypadło z korytarza; po przerwie w łączności uporządkowana historia zamiast 2 tygodni surowych danych.

## 7. Czym to NIE jest

- **Nie diagnoza.** Mówimy „wypadłeś z korytarza, sprawdź X”, nie „masz grypę”.
- **Nie czas rzeczywisty.** Pomiar raz dziennie, rano.
- **Nie dane z lotu.** Analog naziemny (bed rest) + literatura, zawsze tak oznaczone.
- **Nie konkurencja dla CMO-DA** (Google + NASA, 2025) — uzupełnienie (sekcja 8).
- **Nie LLM, który decyduje.** Tekst może formułować LLM, ale nie może wywołać, opóźnić ani obniżyć alarmu. Rdzeń to przejrzysta statystyka, działa offline.

## 8. Przewaga i nowość

**Wobec CMO-DA** („Crew Medical Officer Digital Assistant”, Google + NASA, sierpień 2025 — proof-of-concept CDSS, diagnozuje na podstawie „reported symptoms”):

| | CMO-DA | Space-Normal |
|---|---|---|
| Kiedy działa | gdy astronauta już źle się czuje | każdego ranka, zanim ktoś coś poczuje |
| Na czym | słowa astronauty + ogólna wiedza medyczna | codzienne pomiary + jak ciało *tej osoby* powinno się zmieniać *w tym dniu* |
| Wynik | „prawdopodobnie X, leczenie Y” | „wypadłeś ze swojego korytarza, sprawdź temperaturę, eskaluj, jeśli…” |
| Adaptacja do kosmosu | publicznie nic o tym | rdzeń produktu |
| Technologia | duży model językowy | przejrzysta statystyka, każda liczba wytłumaczalna, offline |

Zdanie na scenę: *„CMO-DA to lekarz, do którego idziesz, kiedy boli. Space-Normal to codzienny przegląd, który mówi ci, że warto iść — zanim zaboli.”*
Nie mówimy: „jesteśmy dokładniejsi od CMO-DA”; nie cytujemy procentów trafności CMO-DA (tylko prasa).

**Nowość (Creativity):** osobisty baseline sam w sobie **nie jest nowy** — mówimy to wprost i wymieniamy poprzedników: rosyjska diagnostyka prenozologiczna Bajewskiego (IBMP, HRV), koncepcja CDSS NASA (zakresy sprzed lotu), RCV w medycynie laboratoryjnej (Ferraro i in. 2026). **Nowe** jest to, że korytarz **ugina się z fazą misji** i jest jawny, wizualny, per osoba. Takiego działającego systemu nie znaleźliśmy w publicznej literaturze.

## 9. Dane i jak uczciwie o nich mówić

| Źródło | Rola | Etykieta |
|---|---|---|
| NASA Life Sciences Portal, bed rest (Campaign 1 + 3 A/C/D/E, 18 osób) | dopasowanie bazy i krzywych adaptacji | `REAL_BEDREST` |
| NASA bed rest CFT70 (3 osoby) + Campaign 3 G/H (8 osób) | wydzielony test, nigdy do strojenia | `REAL_BEDREST` |
| Stanford COVID-19 wearables | prawdziwe sygnatury chorób, przeszczepiane | `REAL_EARTH_ILLNESS` |
| Literatura lotów (Stahn 2017, Norsk 2015) | tryb „flight-like” w demo | `SYNTHETIC` (cytowane) |

**Ważne ograniczenie (z [`data_notes.md`](data_notes.md) §5):** w bed rest **temperatura prawie się nie zmienia** (+0,1°C), a tętno rośnie o medianę +4,5 bpm (mniej niż 1 SD dziennej zmienności). W locie odwrotnie: temperatura +1°C, tętno bez zmian. Wniosek:
- historia o 38°C w filmie = **tryb flight-like oparty na literaturze**, oznaczony jako syntetyczny;
- dowód na prawdziwych danych NASA = korytarz tętna/ciśnienia i liczba fałszywych alarmów oraz wykrytych chorób na wydzielonym teście;
- nigdy nie przedstawiamy dryfu tętna z bed rest jako przewidywania dla lotu.

## 10. Co wolno, a czego nie wolno mówić

| Wolno | Nie wolno |
|---|---|
| Zdrowy astronauta może mieć ok. 38°C w spoczynku; ~4 na 10 spełnia ziemskie kryteria anemii po lądowaniu | „Obecne urządzenia na ISS ciągle fałszywie alarmują” |
| Dziś adaptację od choroby odróżnia lekarz na Ziemi; w drodze na Marsa go nie będzie w pętli | „NASA używa ziemskich norm i się myli” |
| NASA nie wymaga lekarza na pokładzie (STD-3001 Rev C) | „Na Marsa poleci bez lekarza” (to nie jest przesądzone) |
| Do 22 min w jedną stronę, ~2 tygodnie bez łączności | „24 min” |
| Osobisty baseline postulują badacze i NASA; my dodajemy zależność od fazy misji | „Nikt wcześniej nie wpadł na osobisty baseline” |
| Wyniki na danych NASA z bed rest, analog naziemny | Liczby z demo syntetycznego jako wyniki; „zdrowy astronauta ma w kosmosie wyższe tętno” |

Każda liczba w filmie i pitchu musi pochodzić z `docs/claims.md` generowanego przez pipeline albo z cytowanego źródła w [`02-dowody-nasa.md`](02-dowody-nasa.md).

## 11. Otwarte decyzje

1. **Liczba główna** (headline): po ewaluacji CFT70 — Viktor podaje, Petro akceptuje treść zdania.
2. **Limity bezpieczeństwa i progi „eskaluj, jeśli”** — bez mentora medycznego oznaczamy jako placeholdery.
3. **Format zgłoszenia:** film 30 s (rekomendowany) — patrz [`03-pitch-i-film.md`](03-pitch-i-film.md).
