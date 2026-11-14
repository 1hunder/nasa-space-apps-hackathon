# Space-Normal — czy ziemskie normy naprawdę „nie pasują” w kosmosie? Sprawdzenie źródeł

**Data:** 2026-11-14
**Cel:** sprawdzić tezę z pitchu: „zdrowy astronauta ma w kosmosie np. wyższe tętno, a obecne przyrządy fałszywie alarmują”.
**Uzupełnia:** `space-normal-merged-concept.md` (§2 Problem, §7 Demo) oraz `space-normal-brainstorm-handoff.md` (§5).

## 1. Wynik w skrócie

Teza jest **w połowie prawdziwa**.

- **Przyrządy mierzą poprawnie.** Problem leży w interpretacji: populacyjne normy referencyjne ustalono w stabilnych warunkach ziemskich i nie pasują do zdrowego, zaadaptowanego astronauty.
- **Nie znaleźliśmy dowodu, że na ISS działają automatyczne alarmy oparte na ziemskich progach.** Dane interpretują lekarze lotu na Ziemi i porównują je z wynikami sprzed lotu. Zdanie „stary system alarmuje prawie cały czas” jest więc niepotwierdzone dla dzisiejszego ISS.
- **Tętno spoczynkowe w locie to zły przykład** (patrz §2).

## 2. Tętno: korekta

U 8 astronautów na długich misjach na ISS (24-godzinny pomiar, 85.–192. dzień lotu):

- tętno spoczynkowe **bez zmian**,
- średnie ciśnienie tętnicze z 24 h **niższe o ok. 10 mmHg** (skurczowe −8, rozkurczowe −9),
- rzut serca **wyższy o ok. 41%**, opór naczyń obwodowych **niższy o ok. 39%**.

Źródło: [Norsk i in., 2015, J Physiol](https://pmc.ncbi.nlm.nih.gov/articles/PMC4324697).

**Wpływ na dokument merged:** karta astronauty (§4) i demo (§7) pokazują tętno wychodzące z korytarza. To jest w porządku, **jeśli mówimy o analogu bed rest**, a nie o locie. Do sprawdzenia na danych C1/C3/CFT70, czy i jak tętno spoczynkowe dryfuje w bed rest. W narracji „lot na Marsa” nie twierdzimy, że zdrowy astronauta ma wyższe tętno. Wykres „ziemska norma vs korytarz” lepiej zilustrować temperaturą (§3).

## 3. Lepsze przykłady „zdrowy, ale poza ziemską normą”

| Parametr | Zmiana u zdrowych astronautów | Źródło |
|---|---|---|
| Temperatura głęboka ciała w spoczynku | Stopniowy wzrost przez ok. 2,5 miesiąca do **ok. 38°C** (na Ziemi stan podgorączkowy); 11 astronautów | [Stahn i in., 2017, Scientific Reports](https://doi.org/10.1038/s41598-017-15560-w) |
| Niszczenie czerwonych krwinek | O **54% więcej** niż na Ziemi („anemia kosmiczna”); 14 astronautów; rok po powrocie nadal o ok. 30% powyżej poziomu sprzed lotu | [Trudel i in., 2022, Nature Medicine — omówienie OHRI](https://ohri.ca/newsroom/story/view/1428?l=en) |
| Ciśnienie krwi | Niższe skurczowe, rozkurczowe i średnie z 24 h | Norsk i in., 2015 (§2) |

## 4. Czy ktoś już to rozwiązał? Nie w pełni

- **CCLM 2026** ([Point of care testing of biochemical markers…](https://www.degruyterbrill.com/document/doi/10.1515/cclm-2025-0526/html)): tradycyjne progi pochodzą ze stabilnych warunków ziemskich. Autorzy proponują kosmiczne **reference change values** liczone z podłużnych pomiarów każdego astronauty. To **propozycja, nie standard**. Artykuł podaje też, że laboratorium kliniczne na ISS jest minimalne.
- **Zheng i in., 2023** ([Frontiers in Physiology](https://www.frontiersin.org/articles/10.3389/fphys.2023.1219221/full)): 27 astronautów, misje średnio ok. 165 dni. Autorzy zalecają osobisty punkt odniesienia dla każdego członka załogi i wykrywanie odchyleń od niego. To bezpośrednio wspiera ideę „osobistego korytarza”.
- **NASA ExMC / EIMO**: NASA buduje pokładowy system wspomagania decyzji medycznych, bo przy misji na Marsa opóźnienie w jedną stronę sięga ok. 24 min i nie da się na bieżąco konsultować z Ziemią. Źródła: [EIMO ConOps 2024 (NTRS)](https://ntrs.nasa.gov/api/citations/20240001402/downloads/2024_IWS_EIMO_ConOps_FINAL.pdf), [NTRS 20220017869](https://ntrs.nasa.gov/citations/20220017869).
- **Astroskin / Bio-Monitor** (Kanadyjska Agencja Kosmiczna, na ISS od Ekspedycji 58 w 2018) zbiera parametry życiowe. Nie znaleźliśmy źródła, że stosuje kosmiczne zakresy norm. Źródła: [CSA](https://www.canada.ca/en/space-agency/news/2016/10/new-advances-innovative-health-technology-tested-space.html), [Space.com](https://www.space.com/43228-astroskin-smart-space-jersey-for-astronauts.html).

## 5. Bezpieczne sformułowanie do pitchu

Zamiast „obecne przyrządy fałszywie alarmują”:

> Dziś normalną adaptację od choroby odróżnia lekarz lotu na Ziemi. W drodze na Marsa ten lekarz jest kilkanaście minut stąd, a ziemskie progi nie pasują (np. ok. 38°C w spoczynku u zdrowego astronauty). Pokładowy system potrzebuje osobistego, zależnego od fazy misji korytarza normy.

Proponowana zmiana w `space-normal-merged-concept.md` §2, punkt 1: zamiast „Ziemskie normy albo alarmują bez przerwy przy normalnej adaptacji…” napisać „Ziemskie normy nie pasują do normalnej adaptacji: sztywny próg albo **alarmowałby** przy zdrowym astronaucie, albo — po poluzowaniu — przeoczy chorobę. Dziś ten problem rozwiązuje lekarz na Ziemi; na Marsie go nie będzie.”

## 6. Czego nie sprawdzono

- Dokładnych procedur i progów stosowanych przez lekarzy lotu NASA.
- Wyników dokładności Astroskin i jego obecnego statusu operacyjnego.
- Jak tętno spoczynkowe zachowuje się w danych bed rest C1/C3/CFT70.
