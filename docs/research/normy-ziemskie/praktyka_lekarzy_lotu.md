# Praktyka lekarzy lotu (flight surgeons): jak interpretuje się dane zdrowotne astronautów — normy ziemskie vs. indywidualny baseline przedlotowy

Stan wiedzy na listopad 2026. Notatki robocze dla autora raportu. Cytaty zostawiam w oryginale (EN), komentarz po polsku.
Oznaczenia poziomu dowodu: **[FAKT]** = udokumentowane w źródle pierwotnym; **[CZĘŚCIOWE]** = pośrednie, ze streszczeń lub z doniesień medialnych; **[BRAK]** = nie znaleziono źródła.

Uwaga metodologiczna: pełne teksty kilku kluczowych źródeł były niedostępne (paywall Springer i Nature, PDF-y z NTRS i nasa.gov w formie nieczytelnej dla narzędzia). Dotyczy to podręcznika Barratt & Pool, pracy Markina i wsp. 2013, Trudel i wsp. 2022 oraz briefu OCHMO o SAS. Tam, gdzie opieram się na streszczeniu albo wyniku wyszukiwarki, zaznaczam to.

---

## 1. Jak NASA Medical Operations przegląda dane w locie (PMC, SMOT, MORD, NASA-STD-3001): jak często i według jakich kryteriów?

### Takeaway
Rytm przeglądu jest dobrze udokumentowany. PMC (Private Medical Conference) to cotygodniowa rozmowa 1:1 z każdym członkiem załogi ISS. Dane są też omawiane co tydzień na międzynarodowym zespole SMOT, a raz w miesiącu odbywa się przegląd prognostyczny. W żadnym publicznym dokumencie nie znalazłem natomiast **kryteriów** interpretacji, czyli progów, zakresów referencyjnych ani reguły „baseline vs. norma”. Publiczny NASA-STD-3001 odsyła do MORD (dokument programowy, niepubliczny) i nie podaje progów.

### Cited Findings
- **[FAKT]** NASA-STD-3001 Vol. 1, §6.2.1 [V1 6002]: "Private medical communications shall be scheduled on a routine basis, as determined by the Flight Surgeon", z częstotliwością "dictated for short- or long-duration missions". Uzasadnienie [V1 6003]: "This private communication provides for privacy of medical information between the crewmembers and the appropriate health and medical personnel." — [NASA-STD-3001, 6.0 Medical Operations](https://www.nasa.gov/reference/6-0-medical-operations/)
- **[FAKT]** Ten sam dokument, §6.5.2: "Medical Operations Requirements Document (MORD) details the medical technical requirements for the program." [V1 6009] każe programowi opracować dokument wymagań medycznych "based on the concepts outlined in the program-specific crew health operations concept (CHOC) document." Strona **nie opisuje**, jak przeglądać dane w locie ani jakich kryteriów (baseline, zakresy) używać. — [NASA-STD-3001, 6.0](https://www.nasa.gov/reference/6-0-medical-operations/)
- **[FAKT]** Przy kwalifikacji do EVA: "Flight Surgeon on ground evaluates available data from recent medical evaluations, fitness sessions" i na tej podstawie ocenia "readiness for EVA". Jest to ocena ekspercka, bez opisanego algorytmu. — [NASA-STD-3001, 6.0](https://www.nasa.gov/reference/6-0-medical-operations/)
- **[FAKT]** Will Fernandez (flight surgeon NASA, podcast NASA) o PMC: "it's a weekly check in with all of our crew members in the ISS, one at a time"; zakres to sen, jedzenie i samopoczucie ("making sure they're sleeping, okay, eating, okay, how they're feeling"); podkreśla też: "it's not just, you know, checking vital signs". — [NASA, Houston We Have a Podcast: Mission Control Crew Health Consoles](https://www.nasa.gov/podcasts/houston-we-have-a-podcast/mission-control-crew-health-consoles)
- **[FAKT]** Nancy Bansbach (BME, Biomedical Engineer) w tym samym podcaście o decyzjach w niejasnych sytuacjach: "I'm allowed to make educated decisions and recommendations based on experience"; przypadki niepewne ("ever a question of uncertainty, or we're in uncharted territory") trafiają do eskalacji. W transkrypcji nie pada ani słowo o zakresach referencyjnych czy progach. — [NASA podcast](https://www.nasa.gov/podcasts/houston-we-have-a-podcast/mission-control-crew-health-consoles)
- **[CZĘŚCIOWE]** Według dokumentów NTRS (wynik wyszukiwania, pełny PDF nieprzeczytany) dane z codziennych aktywności "presented weekly at the Space Medicine Operations Team (SMOT)", gdzie międzynarodowa grupa lekarzy omawia znane i potencjalne problemy. Odbywa się też comiesięczny przegląd z prognozą zdrowia załogi na kolejny miesiąc. Lista tematów PMC według wymagań: dane z ćwiczeń, dane środowiskowe, sen, obciążenie pracą, wsparcie rodziny. — [NTRS 20080010877](https://ntrs.nasa.gov/citations/20080010877)
- **[FAKT]** Rozdzielenie „baseline przedlotowy” → „w locie” → „R+0” to standardowy schemat zbierania danych w NASA. Każdy astronauta przechodzi testy wymagane medycznie (MR, medical requirement), które ustalają "a preflight baseline for physiologic functions" (dokument NASA o rekondycjonowaniu, cytowany w wyniku wyszukiwania). — [NTRS 20110020318](https://ntrs.nasa.gov/api/citations/20110020318/downloads/20110020318.pdf)
- **[FAKT, kontekst 2026]** W styczniu 2026 r. NASA przeprowadziła pierwszą w 25-letniej historii ISS ewakuację medyczną (Crew-11 wróciła ok. miesiąc wcześniej). NASA nie ujawniła ani diagnozy, ani tożsamości astronauty; Jared Isaacman: "it was a serious medical condition". Według Space Review słuchacze kanału audio ISS usłyszeli, że Kimiya Yui (JAXA) prosi o PMC. Nie jest to oficjalne potwierdzenie, że chodziło o niego. — [Space Review](https://thespacereview.com/article/5136/1); [NPR](https://www.npr.org/2026/01/15/nx-s1-5677647/nasa-spacex-crew-11-splashdown-return); [Scientific American](https://www.scientificamerican.com/article/evacuated-iss-astronauts-return-to-earth-as-nasa-prepares-for-artemis-moon/)

### Inferences
- Interpretacja danych w locie przez NASA to **ocena kliniczna lekarza lotu w pętli z Ziemią** (PMC co tydzień, SMOT co tydzień, przegląd miesięczny). Nie jest to automatyczne porównanie z progami. Dane są zbierane względem baseline'u przedlotowego, ale publicznie nie da się ustalić, czy w ocenie dominuje baseline, czy laboratoryjny zakres referencyjny.
- Ewakuacja Crew-11 (2026) pokazuje, że przy niejasnym problemie medycznym bazowa strategia ISS to „zejść na Ziemię”. Na misji marsjańskiej tej opcji nie będzie.

### Gaps
- **[BRAK]** Treść MORD (ISS MORD, SSP 50260) i dokumentów MED (Medical Evaluation Documents, np. Volume B) nie jest publiczna. Nie znalazłem w nich publicznego fragmentu z regułami interpretacji wyników (np. „porównaj z baseline'em ±X%”).
- **[BRAK]** Nie znalazłem publicznego opisu, jak LSAH (Lifetime Surveillance of Astronaut Health) analizuje dane względem norm. Brief OCHMO „Longitudinal Health Surveillance” istnieje ([PDF](https://www.nasa.gov/wp-content/uploads/2023/03/longitudinal-health-surveillance-technical-brief-ochmo.pdf)), ale go nie przeczytałem.
- **[BRAK]** ESA, JAXA, CSA: nie znalazłem publicznych opisów ich własnych kryteriów interpretacji. Wszystkie te agencje uczestniczą w SMOT (wspólny zespół ISS), co sugeruje wspólną praktykę, ale nie mam na to bezpośredniego cytatu.

---

## 2. Czy dokumenty NASA (MORD, CPG, NASA-STD-3001) określają kosmiczne zakresy referencyjne (Hb, IOP, BP, temperatura, wapń w moczu)?

### Takeaway
W publicznych dokumentach NASA **nie znalazłem żadnych „spaceflight-specific reference ranges”**. Najbliżej tej idei jest Rosja: badania IBMP (Markin i wsp. 2013 i późniejsze) wyznaczyły **zakresy referencyjne dla kosmonautów jako grupy zawodowej** na podstawie danych przedlotowych. Część z nich jest węższa niż ogólnopopulacyjna. Są to jednak normy dla zdrowej populacji kosmonautów **na Ziemi**, a nie normy na czas lotu.

### Cited Findings
- **[FAKT – streszczenie]** Markin i wsp., "Reference values of blood biochemical indices in Russian cosmonauts", *Human Physiology* 2013; 39:178–183. Przebadano 40 wskaźników biochemicznych u 28 kosmonautów (35–54 lata) w badaniach przedlotowych z lat 2000–2012. Dla 15 wskaźników "reference interval boundaries ... were narrower as compared to the generally accepted ranges". Wniosek autorów: wartości referencyjne kosmonautów jako odrębnej grupy zawodowej różnią się dla kilku wskaźników od norm populacyjnych. — [Springer, abstrakt](https://link.springer.com/article/10.1134/S0362119713020084) (pełny tekst niedostępny; nazw 15 wskaźników nie znam)
- **[CZĘŚCIOWE]** Praca IBMP z 2017 r. o hemostazie u kosmonautów: zakresy referencyjne parametrów pro- i antykoagulacyjnych oraz fibrynolitycznych "were somewhat narrowed and close to the boundaries of general population ranges". — [Human Physiology / RCSI](https://journals.rcsi.science/0362-1197/article/view/177121)
- **[CZĘŚCIOWE]** Według wyniku wyszukiwania badanie z 1993 r. na 24 kosmonautach nie wykazało istotnych odchyleń od standardów populacyjnych, z wyjątkiem parametrów związanych z metabolizmem energetycznym (źródło: streszczenie w wynikach, pełnego tekstu nie widziałem).
- **[FAKT]** Rozdział NASA-STD-3001 o operacjach medycznych nie podaje zakresów referencyjnych dla żadnego parametru. — [NASA-STD-3001, 6.0](https://www.nasa.gov/reference/6-0-medical-operations/)
- **[FAKT]** Przegląd Bizzarri, Prudente i Angeloni (*J Lab Precis Med* 2026) **nie definiuje** kosmicznych zakresów referencyjnych. Wzywa jedynie ogólnie: "Optimal Performance should be adequately quantitated and identified for spaceflight missions" oraz "multiple baseline levels established early in the astronaut's training are warranted." — [JLPM 2026](https://jlpm.amegroups.org/article/view/11439/html)
- **[CZĘŚCIOWE]** Przy badaniu pierwszej w pełni cywilnej misji na ISS (najpewniej Axiom-1, 2022; Mayo Clinic Proceedings 2024, "Plasma Biomarkers of First All-Civilian Space Flight to the ISS") wyniki porównywano ze **standardowymi** klinicznymi zakresami referencyjnymi. Według streszczenia wyszukiwarki Na, Cl i Ca pozostały w zakresie, a jako „low/high” klasyfikowano wartości >5% poza zakresem. Pełny tekst zwrócił 403, więc nie zweryfikowałem tego. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0025619624002726)
- **[CZĘŚCIOWE]** Rozdział wprowadzający podręcznika *Principles of Clinical Medicine for Space Flight* (Barratt & Pool, Springer 2008) według streszczenia obejmuje "laboratory values and test results deemed important for understanding the clinical norms associated with space flight". Pełnego tekstu nie widziałem (paywall). — [Springer, rozdz. 2](https://link.springer.com/chapter/10.1007/978-0-387-68164-1_2)

### Inferences
- Dziś istnieją dwa „poziomy” odniesienia: (a) **standardowe zakresy laboratoryjne**, używane w publikacjach, np. przy cywilnych misjach, oraz (b) **indywidualny baseline przedlotowy**, używany w badaniach NASA i wspomniany w NASA-STD-3001. Trzeci poziom, **normy dla populacji astronautów**, jest udokumentowany tylko dla Rosji i tylko jako normy przedlotowe. Kategoria „normal for spaceflight”, czyli zakresy oczekiwane w danym tygodniu lotu, nie jest publicznie skodyfikowana przez żadną agencję.

### Gaps
- **[BRAK]** Kosmicznych zakresów dla IOP, BP, temperatury ciała ani wapnia w moczu nie znalazłem w żadnym publicznym dokumencie NASA, ESA, JAXA ani CSA.
- **[BRAK]** Nie udało się sprawdzić, czy Clinical Practice Guidelines (ISS Medical Checklist / CPG) zawierają skorygowane progi. Dokumenty są niepubliczne.
- Wynik w De Gruyter *CCLM* 2025 ([cclm-2025-0526](https://www.degruyterbrill.com/document/doi/10.1515/cclm-2025-0526/html)) wygląda na tematyczny (medycyna laboratoryjna w kosmosie), ale go nie przeczytałem.

---

## 3. Czy lekarze lotu i podręczniki wprost mówią, że normy ziemskie są nieadekwatne lub mylące u astronautów?

### Takeaway
**Nie znalazłem bezpośredniego cytatu** lekarza lotu NASA ani fragmentu podręcznika (Barratt & Pool, *Fundamentals of Aerospace Medicine*, Nicogossian), który dosłownie mówiłby „normy ziemskie są nieadekwatne”. Istnieją wypowiedzi bliskie tej tezie: (a) przegląd z 2026 r. o tym, że odchylenie nie oznacza choroby, (b) rosyjskie dane o odrębnych normach kosmonautów, (c) nazewnictwo „space anemia” i „physiologic atrophy” sugerujące, że część wyników „poza normą” to adaptacja.

### Cited Findings
- **[FAKT]** Bizzarri i wsp. 2026: "Variance does not mean disease." oraz "a dynamic parameter—usually neglected/underrated on terrestrial condition—can help in assigning a «physiological» value". — [JLPM 2026](https://jlpm.amegroups.org/article/view/11439/html)
- **[CZĘŚCIOWE]** Przegląd „Human Health during Space Travel: State-of-the-Art Review” (PMC9818606) opisuje anemię kosmiczną jako "perhaps due to a normal physiologic adaptation of newly released blood cells and iron metabolism to microgravity", a zmiany sercowo-naczyniowe jako możliwe "physiologic atrophy", która wraca do baseline'u po locie (cytaty ze streszczenia wyszukiwarki). — [PMC9818606](https://pmc.ncbi.nlm.nih.gov/articles/PMC9818606/)
- **[FAKT – streszczenie]** Markin i wsp. 2013: normy kosmonautów różnią się od populacyjnych dla kilku wskaźników (patrz pkt 2). Jest to empiryczny argument, że ogólnopopulacyjne zakresy są mniej czułe dla tej grupy. — [Springer](https://link.springer.com/article/10.1134/S0362119713020084)

### Inferences
- Teza „normy ziemskie są mylące” ma u astronautów silne **pośrednie** poparcie: wartości przesunięte w locie u zdrowych osób (Hb, temperatura, wit. D) oraz węższe normy przedlotowe. Nie jest jednak publicznie sformułowana jako stanowisko agencji. W pitchu należy ją przedstawiać jako wniosek z danych, a nie jako cytat z NASA.

### Gaps
- **[BRAK]** Dosłownych cytatów z Barratt & Pool, *Fundamentals of Aerospace Medicine* (Davis i wsp.) ani Nicogossian *Space Physiology and Medicine* nie udało się zdobyć (paywall, brak snippetów Google Books w wynikach).
- **[BRAK]** Nie znalazłem wywiadu ani artykułu, w którym konkretny flight surgeon NASA lub ESA mówi o nieadekwatności norm ziemskich.

---

## 4. NASA Biochemical Profile / Nutritional Status Assessment (Smith, Zwart): jak interpretowane są wyniki i czy u zdrowej załogi pojawiały się wartości poza zakresami klinicznymi?

### Takeaway
Badania zespołu Smith/Zwart (NASA Nutritional Biochemistry Lab) interpretują wyniki głównie **względem indywidualnego baseline'u przedlotowego** (pre/in/post) i opisują systematyczne zmiany u zdrowych astronautów: spadek witaminy D, folianów, wit. K i E, wzrost markerów resorpcji kości i stresu oksydacyjnego, zmiany żelaza i Zn. Nie udało mi się zweryfikować w pełnym tekście, **jaki odsetek** wartości wypadał poza kliniczne zakresy referencyjne.

### Cited Findings
- **[CZĘŚCIOWE]** Smith i wsp. 2009 (*J Nutr*, 11 astronautów, loty 128–195 dni): "bone loss, compromised vitamin D status, and oxidative damage are among critical nutritional concerns for long-duration space travelers"; opisano też spadek statusu wit. D, folianów, wit. K i E oraz wzrost markerów resorpcji kości i uszkodzeń oksydacyjnych (streszczenie wyszukiwarki). — [NASA, Studying the Role of Nutrition in Spaceflight](https://www.nasa.gov/?p=209742); [NASA, Nutritional Biochemistry of Space Flight (PDF)](https://www.nasa.gov/wp-content/uploads/2023/04/nutritional-biochemistry-of-space-flight.pdf)
- **[FAKT]** NASA opisuje Biochemical Profile jako panel obejmujący białka, witaminy, minerały, markery kostne, hormony, metabolity, funkcje immunologiczne, antyoksydanty i chemię ogólną; oceny biochemiczne wykonuje się przed lotem i po locie. — [NASA](https://www.nasa.gov/?p=209742)
- **[FAKT]** Zheng, Charvat, Zwart, Mehta, Crucian, Smith i wsp., *Frontiers in Physiology* 2023 (dane 27 astronautów, śr. lot ok. 165 dni): intensywności liczono "relative to the pre-flight timepoint (−45 days)", a autorzy proponują podejście "detecting deviations from a wellness baseline". Wyniki: "25-OH Vitamin D measurements are decreased across 19 astronauts"; cynk w surowicy "is elevated during flight, and returns to low levels after return to Earth"; żelazo w surowicy: "there is a marked decrease post return to Earth". Praca **nie porównuje** wyników z klinicznymi zakresami referencyjnymi. Objawy kliniczne pochodziły z raportów IMM ("were provided to our team as IMM reports"). — [Frontiers in Physiology 2023](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2023.1219221/full)
- **[CZĘŚCIOWE]** Zwart (NASA) o żelazie: wcześniejsze badania sugerują, że astronauci "need less iron during long-duration missions due to changes in the body's production of red blood cells". Oznacza to, że ziemskie zalecenia i interpretacja ferrytyny i żelaza nie przenoszą się 1:1. — [News-Medical 2015](https://www.news-medical.net/news/20150804/Researchers-explore-key-factors-to-improve-astronauts-nutrition-needs-during-space-missions.aspx)

### Inferences
- W badaniach NASA standardem analitycznym jest **baseline osobniczy** (pre-flight → in-flight → R+0 → R+n), a nie pojedynczy zakres populacyjny. Wspiera to koncepcję „personalnego baseline'u + oczekiwanej trajektorii lotu”.

### Gaps
- **[BRAK]** Nie zweryfikowałem w pełnym tekście, ilu zdrowych astronautów miało w locie wartości poza klinicznymi zakresami referencyjnymi (np. wit. D < próg kliniczny, ferrytyna, Ca w moczu powyżej progu ryzyka kamicy). Takie dane są prawdopodobnie w Smith i wsp. 2005 (*J Nutr* 135:437) i 2009 oraz w książce „Nutritional Biochemistry of Space Flight”, ale ich nie przeczytałem.

---

## 5. Autonomia na Marsa: ryzyko HRP „Inflight Medical Conditions”, luki ExMC, opóźnienie komunikacji; czy pada „normal for spaceflight”?

### Takeaway
HRP i ExMC wprost uznają potrzebę **autonomicznego wsparcia decyzji i pokładowych zasobów wiedzy** przy dużym opóźnieniu łączności. W żadnym przeczytanym dokumencie nie znalazłem jednak frazy „normal for spaceflight” ani „spaceflight-adjusted normals”. Ta luka koncepcyjna istnieje, ale nie jest nazwana.

### Cited Findings
- **[FAKT]** Raport dowodowy HRP (Antonsen, 2017) „Risk of Adverse Health Outcomes and Decrements in Performance due to Inflight Medical Conditions” w ocenie National Academies (2018) omawia "the need for autonomous decision support and for onboard knowledge resources" w kontekście "missions affected by long communications latency". Komitet zaleca opisanie "decision-support principles for making diagnoses of health conditions in space", "particularly in settings of long communications latency or lost communications". — [National Academies, Review of NASA's Evidence Reports 2017 Letter Report (2018)](https://www.nationalacademies.org/read/24953/chapter/9)
- **[FAKT]** Raport kończy się listą 13 luk badawczych. National Academies krytykuje: "The steps needed for the resolution of these 13 existing gaps are not articulated" oraz "the gaps as currently worded may be worded too broadly". Przykład luki Med02: "We do not have the capability to provide a safe and effective pharmacy for exploration missions". — [National Academies 2018](https://www.nationalacademies.org/read/24953/chapter/9)
- **[FAKT]** Strona National Academies **nie porusza** zmienionej prezentacji chorób ani zmienionych norm fizjologicznych. Najbliższe zdanie to: "the nature of the health risks in a number of areas is reasonably well understood in microgravity". — [National Academies 2018](https://www.nationalacademies.org/read/24953/chapter/9)
- **[CZĘŚCIOWE]** Powiązane dokumenty ExMC: NASA/TM-2022-220299 „Development of an Accepted Medical Condition List for Exploration Medical Capability Scoping” (Antonsen, Blue, Nusbaum, 2022) oraz HRP-48044 „Exploration Medical Capability Medical Scenarios” (baseline z 10/2021). Ich treści nie przeczytałem. — [NTRS 20220003136](https://ntrs.nasa.gov/api/citations/20220003136/downloads/NASA-T_1.pdf); [NTRS 20230006550](https://ntrs.nasa.gov/api/citations/20230006550/downloads/Medical%20Scenarios.pdf); [NTRS 20170004604](https://ntrs.nasa.gov/citations/20170004604)
- **[FAKT]** Możliwości laboratoryjne na pokładzie są ograniczone. iSTAT w wersji lotnej "was able in measuring six analytes"; "the rHEALTH-One analyzer was launched in February 2022"; HemoCue ma ograniczenia: "limited shelf life of 6 months, refrigeration needs and data reliability issues". — [Bizzarri i wsp. 2026, JLPM](https://jlpm.amegroups.org/article/view/11439/html)

### Inferences
- Koncepcja „autonomicznej interpretacji z normami skorygowanymi o lot” wypełnia lukę, którą NASA sama zgłasza (decision support przy opóźnieniu łączności). Nie powinniśmy jednak twierdzić, że NASA już nazwała potrzebę „spaceflight-adjusted normals”, bo tego nie znalazłem.

### Gaps
- **[BRAK]** Nie przeczytałem aktualnej (po 2020) wersji Evidence Report o Inflight Medical Conditions ani aktualnej listy luk ExMC na humanresearchroadmap.nasa.gov. Nie wiem, czy nowsze wersje zawierają sformułowanie o normach dostosowanych do lotu.
- **[BRAK]** Zero trafień dla „normal for spaceflight” / „spaceflight-adjusted normal” w przeszukanych źródłach.

---

## 6. Adaptacja do lotu maskuje lub naśladuje chorobę (fluid shift, gorączka przy podwyższonej temperaturze rdzeniowej, anemia)

### Takeaway
Są mocne dowody, że **zdrowi astronauci w locie mają wartości, które na Ziemi zostałyby uznane za nieprawidłowe**: temperatura rdzeniowa wyższa o ok. 1 °C oraz anemia przy lądowaniu u 5 z 13 osób. Ogólnie uznaje się też, że diagnoza w kosmosie jest trudniejsza z powodu zmienionej fizjologii. Nie znalazłem natomiast publikacji, która opisywałaby konkretny przypadek **przeoczonej lub błędnie rozpoznanej choroby** z powodu nałożenia się na adaptację.

### Cited Findings
- **[FAKT]** Stahn i wsp., *Scientific Reports* 2017: "At rest CBT was increased by about 1.01 °C on the ISS compared to baseline". Wzrost narastał stopniowo przez ok. 2,5 miesiąca i towarzyszył mu wzrost IL-1ra (antagonisty receptora interleukiny 1); w czasie wysiłku temperatura rdzeniowa "rises higher and faster in space than on Earth". Autorzy nie nazywają tego gorączką. — [Stahn i wsp. 2017 (PDF)](https://air.unimi.it/bitstream/2434/533558/2/ScientificReports_IncreasedCoreBodyTemperature_2017.pdf); [DLR elib](https://elib.dlr.de/116228)
- **[FAKT]** Trudel i wsp., *Nature Medicine* 2022 ("Hemolysis contributes to anemia during long-duration space flight"): u 14 astronautów niszczenie erytrocytów było o ok. 54% większe niż na Ziemi; "five out of 13 astronauts were clinically anemic when they landed"; rok po locie hemoliza "was still 30 percent above preflight levels". Kryterium „clinically anemic” nie jest podane w komunikacie, choć najpewniej chodzi o standardowy próg kliniczny. — [ScienceDaily 2022](https://www.sciencedaily.com/releases/2022/01/220114115708.htm); [Nature Medicine (DOI 10.1038/s41591-021-01637-7)](https://www.nature.com/articles/s41591-021-01637-7) (pełny tekst niedostępny – paywall)
- **[FAKT]** Ten sam komunikat: odkrycie "supports screening astronauts or space tourists for existing blood or health conditions that are affected by anemia"; Trudel: anemia "affecting your energy, endurance, and strength can threaten mission objectives"; "the longer the space mission, the worse the anemia". — [ScienceDaily 2022](https://www.sciencedaily.com/releases/2022/01/220114115708.htm)
- **[CZĘŚCIOWE]** NASA (dane z czasów Apollo) opisuje krótkotrwałą rozcieńczeniową "Space Flight Anemia" i powrót objętości osocza do normy w ciągu 24–48 h po lądowaniu; zmiany WBC i rozmazu były "transient and reverted to normal within 24 to 48 hours after flight" (streszczenie wyszukiwarki, NASA SP-368 i slajdy NTRS). — [SP-368 Biomedical Results of Apollo](https://corpora.tika.apache.org/base/docs/govdocs1/773/773844.html); [NTRS 20150022859](https://ntrs.nasa.gov/api/citations/20150022859/downloads/20150022859.pdf)
- **[CZĘŚCIOWE]** NASA o układzie immunologicznym: dane "are typically captured before flight to establish baseline values, during flight (when possible), and on landing day (R+0) to establish spaceflight associated changes" (streszczenie wyszukiwarki; PDF nieczytelny dla narzędzia). — [NTRS 20200001703](https://ntrs.nasa.gov/api/citations/20200001703/downloads/20200001703.pdf)
- **[CZĘŚCIOWE]** Przegląd (IntechOpen, „Beyond the Algorithm”) stwierdza, że diagnozę w kosmosie komplikują "limited diagnostic tools, environmental influences on physiology, and the possibility of unfamiliar disease presentations". Jest to źródło o niższej wadze (rozdział IntechOpen). — [IntechOpen](https://www.intechopen.com/chapters/1220645)
- **[CZĘŚCIOWE]** Bed rest (analog lotu): "the physiological changes recorded during space flight and bed rest mimic those observed in some diseases and in the aging process". — [ClinicalTrials.gov NCT00311571](https://clinicaltrials.gov/study/NCT00311571)
- **[CZĘŚCIOWE]** SANS (zespół neurooczny związany z lotem): konsensus ekspertów z 2026 r. (*Eye*) uzasadnia publiczny przewodnik tym, że "would be instructive to flight surgeons who manage SANS". Pokazuje to, że nawet dla dobrze znanej adaptacji kryteria diagnostyczne dopiero się standaryzuje. — [Eye 2026](https://www.nature.com/articles/s41433-026-04651-6)

### Inferences
- Przykłady, gdzie ziemski próg dałby fałszywy alarm albo maskowanie: (1) **temperatura** – baseline w locie ok. +1 °C, więc ziemski próg gorączki 38 °C traci część marginesu i interpretacja „podgorączki” jest niejednoznaczna (wniosek, brak bezpośredniego cytatu NASA); (2) **Hb/Hct** – spadek po adaptacji i po lądowaniu u zdrowych, więc przy ziemskim zakresie spada swoistość wykrywania krwawienia lub hemolizy patologicznej (wniosek); (3) **wit. D, Fe, Zn** – przewidywalne trajektorie w locie (Frontiers 2023).
- Najmocniejszy argument dla projektu: **interpretacja względem osobniczego baseline'u i oczekiwanej trajektorii lotu** jest zgodna z praktyką badawczą NASA (pre/in/R+0). Nie jest to jednak opisana publicznie praktyka kliniczna z twardymi progami.

### Gaps
- **[BRAK]** Nie znalazłem udokumentowanego przypadku klinicznego, w którym adaptacja do lotu zamaskowała chorobę (np. przeoczona infekcja z powodu wyższej temperatury bazowej).
- **[BRAK]** Treści briefu OCHMO-MTB-004 „Space Adaptation Sickness” ([PDF](https://www.nasa.gov/wp-content/uploads/2025/09/ochmo-mtb-004-space-adaptation-sickness-sas.pdf)) nie odczytałem (PDF nieczytelny dla narzędzia). Brief może zawierać diagnostykę różnicową SAS vs. inne przyczyny nudności.
- **[BRAK]** Roscosmos/IBMP: poza pracami o normach przedlotowych nie znalazłem publicznego opisu, jak rosyjscy lekarze interpretują dane w locie (np. system „Sonokard” i inne). ESA/DLR: znalazłem tylko pracę Stahna (Charité/DLR), żadnego dokumentu operacyjnego ESA o interpretacji wyników.
