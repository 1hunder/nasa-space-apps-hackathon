# Ziemskie normy referencyjne w monitoringu astronautów — literatura i prior art

Stan na 14.11.2026. Cytaty dosłowne w oryginale (EN). Oznaczenia: **[DANE]** = wniosek oparty na danych empirycznych; **[OPINIA/PROPOZYCJA]** = review, stanowisko, wizja, rekomendacja warsztatowa bez własnych danych.

Ważna korekta do briefu: praca CCLM o DOI 10.1515/cclm-2025-0526 **nie jest autorstwa „Kerremans et al.”**. Autorzy to Ferraro S, Sengupta S, Shaw J, Dave A, Cheli M, Colon R, Zuccotti G, Mason CE, Marcovina S. Ukazała się w Clin Chem Lab Med 2026;64(3):570–581 (PMID 41140086), typ: Review — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1515/cclm-2025-0526&resultType=core&format=json).

---

## 1. Ferraro et al. (CCLM 2026): co dokładnie mówią o ziemskich normach i RCV w kosmosie

### Takeaway
To jedyna znaleziona publikacja z medycyny laboratoryjnej, która wprost i jednym zdaniem przeciwstawia „tradycyjne cut-offy ustalone w stabilnych warunkach ziemskich” wartościom RCV (reference change values) wyliczanym na pokładzie z pomiarów podłużnych. To jednak **propozycja w review**, bez własnych danych i bez wyliczonych RCV dla żadnego analitu.

### Cited Findings
- Dosłowny cytat z abstraktu: "Furthermore, the development and use of reference change values (RCV) in space environment, derived from biomarkers measured longitudinally in real-time onboard, will be crucial to differentiate clinically relevant changes in biomarkers levels from alterations induced by microgravity. This approach may overcome the use of traditional cut-off values which are assessed and generally applied under stable terrestrial conditions." **[OPINIA/PROPOZYCJA, review, 2026]** — [Europe PMC, abstrakt](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1515/cclm-2025-0526&resultType=core&format=json); [DOI](https://doi.org/10.1515/cclm-2025-0526)
- Kontekst z abstraktu: "Microgravity disrupts biochemical and hormonal regulation, leading to reversible homeostatic dysregulation across multiple organ systems in astronauts during spaceflight in LEO." Oraz: "Clinical laboratory capabilities on the ISS are currently minimal." — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1515/cclm-2025-0526&resultType=core&format=json)
- Autorzy wskazują hs-cTnI w POCT jako kluczowy biomarker: "The recent implementation of high-sensitivity cardiac troponin I on POCT will be essential for early identifying myocardial injury and facilitating telemedicine support." — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1515/cclm-2025-0526&resultType=core&format=json)
- Pełny tekst jest za paywallem. W repozytorium Uniwersytetu Mediolańskiego ma status „restricted” — [AIR UniMi](https://air.unimi.it/handle/2434/1244758); strona wydawcy zwraca 405 dla automatów — [De Gruyter](https://www.degruyterbrill.com/document/doi/10.1515/cclm-2025-0526/html)

### Inferences
- Zdanie Ferraro et al. jest najmocniejszym „cytowalnym” uzasadnieniem dla pomysłu hackathonowego. Uwaga: dotyczy **biomarkerów laboratoryjnych (POCT)**, a nie parametrów życiowych (HR, BP, SpO2). Przeniesienie tej logiki na vitals to nasza ekstrapolacja.
- Formuła „may overcome” to hipoteza. W abstrakcie nie ma liczbowej walidacji.

### Gaps
- Nie udało się przeczytać pełnego tekstu. Nie wiadomo, czy autorzy podają przykładowe RCV, wartości CV_I/CV_A ani konkretne analizy (poza hs-cTnI). Nie wiadomo też, czy cytują Markin 2013 (zob. pkt 3).

---

## 2. Zheng et al. 2023 (Frontiers in Physiology): co dokładnie rekomendują

### Takeaway
To **praca empiryczna** (n=27 astronautów NASA, dane LSAH/LSDA, długie misje na ISS). Autorzy wprost postulują monitoring zindywidualizowany: baseline każdego członka załogi i wykrywanie odchyleń od niego. **Nie używają jednak terminów „reference range/interval”** i nie krytykują wprost ziemskich norm. Argument dotyczy self-baseline, a nie niedopasowania populacyjnych norm.

### Cited Findings
- Metadane: Zheng M, Charvat J, Zwart SR, Mehta SK, Crucian BE, Smith SM, He J, Piermarocchi C, Mias GI. "Time-resolved molecular measurements reveal changes in astronauts during spaceflight", Front Physiol 2023;14:1219221, Original Research **[DANE]** — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/)
- Główna rekomendacja (Wstęp): "The next steps must enable monitoring of data from multiple astronauts during long-duration space missions, and should include the implementation of a personalized approach that can establish baseline characteristics in each crew member, detect deviations therefrom, and detect potentially adverse medical events." — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/)
- "In this investigation, we implemented the first (to our knowledge) multi-astronaut individual-focused monitoring in long-duration spaceflight." — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/)
- "Our findings identify significant metabolite and immunological modifications during spaceflight, and suggest that individual-focused monitoring must be implemented to identify the onset of these changes in order to also address them in a timely manner with personalized countermeasures." — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/)
- "The approach allowed the identification of sets of measurements that display time-resolved deviations from an astronaut's baseline." Wniosek końcowy: "We have implemented an individual-focused approach to investigate personalized astronaut monitoring and detecting deviations from a wellness baseline." — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/)
- Metoda: analiza szeregów czasowych w PyIOmica (normalizacja szeregu, autokorelacje, hierarchiczne klastrowanie trendów) per astronauta. To **retrospektywna analiza trendów, nie system alarmowy w czasie rzeczywistym** — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/)
- Rekomendacje praktyczne z Wniosków (wg streszczenia strony): dodatkowe countermeasures przeciw osteoporozie, kamicy nerkowej i reaktywacji wirusów, w tym wzbogacone racje żywnościowe, suplementacja i leki immunologiczne na pokładzie. Brak dosłownego zdania „we recommend” — [Frontiers](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2023.1219221/full)

### Inferences
- Zheng et al. to dobry dowód empiryczny, że **zmiany wewnątrzosobnicze są wykrywalne i istotne**. Nie dowodzi jednak wprost, że ziemskie normy dają fałszywe alarmy lub przegapienia. Nie należy im przypisywać takiej tezy.

### Gaps
- Nie sprawdzono, ile z wykrytych odchyleń mieściło się w klinicznych normach laboratorium. Autorzy tego nie raportują (brak fraz „reference range/normal range” w tekście).

---

## 3. Medycyna laboratoryjna: zakresy referencyjne specyficzne dla astronautów/kosmonautów

### Takeaway
Istnieje **jedna empiryczna praca wyznaczająca zakresy referencyjne dla kosmonautów** (Markin et al. 2013, IBMP, n=28). Pokazała, że dla 15 z 40 parametrów biochemicznych zakresy są węższe niż ogólnie przyjęte, a górne granice części enzymów są przesunięte. Poza nią temat pojawia się tylko jako pytanie lub lista problemów (Clinical Chemistry 2023) i jako propozycja RCV (Ferraro 2026). Inspiration4 (Nature 2024) mówi wprost, że zakresy referencyjne dla lotów dopiero *mogą* powstać.

### Cited Findings
- **Markin AA, Zhuravleva OA, Morukov BV, Kuzichkin DS, Zabolotskaia IV, Vostrikova LV. „[Reference values of Russian cosmonauts blood biochemical indices]”, Fiziol Cheloveka 2013;39(2):79–84; PMID 23789387; Human Physiology DOI 10.1134/S0362119713020084 [DANE]**:
  - "Within the period of 2000 to 2012 the values of 40 diagnostically significant biochemical indices in venous blood were being determined during the pre-flight clinical and physiological examination of 28 Russian cosmonauts aged 35 to 54 [...]"
  - "It was found that reference interval boundaries for 15 indices were narrower as compared to the generally accepted ranges. The upper boundaries of activity reference ranges of a number of enzymes, as well as of concentration of some metabolites of energy and plasticity metabolism were raised relative to mean population values."
  - "Thus, it was found that Russian cosmonauts being a specific professional team featured inherent reference values which differed from mean population values in a number of blood biochemical indices. It is conditioned by peculiarities of selection, physical training and psychic and emotional status of crew members during a pre-flight period." — [Europe PMC / PubMed 23789387](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:23789387%20AND%20SRC:MED&resultType=core&format=json); [Springer](https://link.springer.com/article/10.1134/S0362119713020084)
  - Uwaga: zakresy dotyczą **okresu przedlotowego** (45–30 dni przed startem), nie lotu.
- **Wiencek JR, Das S, Beheshti A, Crucian BE, Karouia F, Trudel G, McMonigal KA. „Lab Medicine in Space”, Clin Chem 2023;69(5):442 (Q&A), DOI 10.1093/clinchem/hvad035 [OPINIA eksperckiej]**:
  - K. McMonigal (NASA): "Generally, laboratory profiles are within the clinical normal ranges for a 6-month mission." Specjaliści mają "a keen sense of what is 'normal' for a population". Dalsze postępowanie zaczyna się, gdy "a slight deviation from normal or from an individual's prior laboratory results is seen". Dane: "all pre- and post-flight laboratory data is preserved in a longitudinal database." — [OUP](https://academic.oup.com/clinchem/article/69/5/442/7113323)
  - Według zapowiedzi podcastu Q&A porusza pytanie "Are reference intervals different in space?". W transkrypcji podcastu brak odpowiedzi — [ADLM podcast](https://www.myadlm.org/science-and-research/clinical-chemistry/clinical-chemistry-podcasts/2023/lab-medicine-in-space)
- **Jones CW et al. „Molecular and physiological changes in the SpaceX Inspiration4 civilian crew”, Nature 2024 [DANE + opinia w dyskusji]**: "Nonetheless, the Inspiration4 data, along with data from other civilian spaceflight missions, may contribute to the development of reference ranges and pre-flight preparatory tasks [...] that can help guide future crew selection and mission planning." Ponadto: "most metrics (for example, IJV size, heart rate, complete blood count metrics, gene expression and cytokines) were either stable or quickly reverted to pre-flight levels (baseline) after landing on Earth." Zmiany HR/HRV analizowano względem baseline przedlotowego per astronauta (Apple Watch). — [PMC11357997](https://pmc.ncbi.nlm.nih.gov/articles/PMC11357997/)
- **Balali P et al. „Evidence of effective cardiovascular countermeasures during spaceflights: insights from wearable monitoring”, npj Microgravity 2025 (n=17 kosmonautów) [DANE]**: "Our results showed that the evolution of cardiac time intervals, blood pressure, stroke volume, and cardiac systolic kinetic energy depended on the chosen baseline position. After five months in space, heart rate increased compared to the supine baseline on Earth (p = 0.013, d = 0.86) but not to the sitting position." — [PMC12484674](https://www.nature.com/articles/s41526-025-00522-8)
- Wyszukiwanie w Europe PMC (astronaut/cosmonaut/spaceflight × "personalized reference" / "reference change value" / "population-based reference") dało 23 trafienia. Żadne nie dotyczy zakresów referencyjnych u astronautów (szum tematyczny) — [Europe PMC search](https://www.ebi.ac.uk/europepmc/)

### Inferences
- Markin 2013 to **twardy argument empiryczny**, że populacyjne normy nie pasują do astronautów już na Ziemi, z powodu selekcji i treningu. Węższe przedziały oznaczają, że wynik „w normie populacyjnej” może być nietypowy dla tej grupy.
- Wypowiedź McMonigal ("within the clinical normal ranges") pokazuje, jak NASA obecnie interpretuje wyniki: wg norm klinicznych, z nieformalnym porównaniem do wcześniejszych wyników osoby. Implikacja (nasza): istotne zmiany wewnątrzosobnicze mogą mieścić się w normie populacyjnej i nie generować flagi.
- Balali 2025 pokazuje problem „która ziemska referencja”: wniosek (HR wzrósł / nie wzrósł) zależy od wybranej pozycji baseline. To argument za referencją zależną od kontekstu, a nie jedną liczbą.

### Gaps
- Nie znaleziono pracy z IFCC, J Appl Lab Med ani Clinical Chemistry, która wyznaczałaby **przedziały referencyjne w trakcie lotu**.
- Nie znaleziono publicznego dokumentu NASA (np. NASA-STD-3001, Medical Operations Requirements) opisującego, jakie zakresy referencyjne stosuje się do wyników lotniczych.
- Nie zweryfikowano wzmianki o artykule z Clinical Chemistry z 1993 r. o „reference values” w mikrograwitacji (pojawił się tylko w podsumowaniu wyszukiwarki, bez źródła).

---

## 4. Medycyna spersonalizowana/precyzyjna dla astronautów (NASA, SOMA, Twins, Schmidt & Goodwin)

### Takeaway
Postulat personalizacji jest powszechny i stary: od Schmidt & Goodwin 2013 przez Scott et al. 2021/2023 („the best baseline for an individual is oneself”) do SOMA/Mason 2024 („precision aerospace medicine”). Prawie wszystko to **opinie, wizje i rekomendacje warsztatowe**. Dotyczą głównie omiki i countermeasures, rzadko vitals, i nie formułują wprost tezy „ziemskie normy dają błędne alarmy”.

### Cited Findings
- **Schmidt MA, Goodwin TJ. „Personalized medicine in human space flight: using Omics based analyses to develop individualized countermeasures that enhance astronaut safety and performance”, Metabolomics 2013 [OPINIA/REVIEW]**: wg streszczenia, ze względu na małą liczbę osób, wysokie ryzyko i ekstremalne obciążenia lot załogowy jest "among the most obvious environments for personalized medicine" — [PMC3825629](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3825629/)
- **Scott RT et al. (preprint arXiv 2112.12554, 2021; opublikowane jako „Biomonitoring and precision health in deep space supported by artificial intelligence”, Nat Mach Intell 2023;5:196–207, DOI 10.1038/s42256-023-00617-5) [OPINIA — rekomendacje warsztatu NASA 2021]**. Cytaty z preprintu (wersja opublikowana może się różnić redakcyjnie):
  - "As the NASA Twins study showed, even comparing an astronaut to their twin on earth is limited: the best baseline for an individual is oneself."
  - "Such approaches can first establish baselines of various biomarkers for each astronaut individually on Earth."
  - "AI methods for time-series analysis, particularly utilizing changepoint or anomaly detection, can be used to identify potentially adverse medical events through monitoring deviations from a healthy baseline using longitudinal data."
  - "Further, the development of AI-driven models capable of individualized interpretation of biomarkers will allow further acceptance and establishment of monitoring thresholds on a personalized basis."
  - "When digital twin technology is mature, having a digital twin of each astronaut (rather than a biological twin) would aid predictive power."
  - W tabeli wyzwań ML: "Adapting a model trained using terrestrial electrocardiogram data to 'new normal' of electrocardiogram readings from astronauts whose heart physiology has changed in spaceflight." — **to najbliższe znalezione sformułowanie problemu „ziemska norma vs kosmiczna norma” dla vitals**
  - "Paired with an AI-assisted biological knowledge base including expected baselines and biomarkers, such non-invasive approaches could assist in predicting adverse health outcomes and identifying preventive actions." — [arXiv 2112.12554](https://arxiv.org/abs/2112.12554); [Nature MI](https://www.nature.com/articles/s42256-023-00617-5)
  - W opublikowanej wersji abstrakt: "maximally automated, autonomous and intelligent Precision Space Health system, to monitor, aggregate and assess biomedical statuses" — [Nature MI](https://www.nature.com/articles/s42256-023-00617-5)
- **Overbey EG et al. „The Space Omics and Medical Atlas (SOMA) and international astronaut biobank”, Nature 2024 [zasób danych + opinia]**: "Yet current frameworks for aerospace medicine are nascent and lag far behind advancements in precision medicine on Earth [...]" oraz "these accessible data — when profiled and aggregated at scale — will enable the development of both personalized and general medical guidance for astronauts." — [PMC11357981](https://pmc.ncbi.nlm.nih.gov/articles/PMC11357981/)
- **Mason CE et al. „A second space age spanning omics, platforms and medicine across orbits”, Nature 2024 (Perspective) [OPINIA]**: abstrakt mówi o "precision aerospace medicine for the crews" i "personalized risk profiles tailored for astronauts" — [Europe PMC, PMID 38862027](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22second%20space%20age%22&resultType=core&format=json)
- **Garrett-Bakelman FE et al. „The NASA Twins Study”, Science 2019 [DANE, n=1+1]**: "Longitudinal assessments identified spaceflight-specific changes [...]". Większość parametrów wróciła "to near preflight levels within 6 months after return to Earth". Projekt podłużny, oparty na porównaniu z własnym baseline i z bliźniakiem — [PMC7580864 / PubMed 30975860](https://www.science.org/doi/10.1126/science.aau8650)
- **Afshinnekoo E et al. „Fundamental Biological Features of Spaceflight”, Cell 2020 [REVIEW]**: abstrakt opisuje 6 cech biologicznych (stres oksydacyjny, uszkodzenia DNA, mitochondria, epigenetyka, telomery, mikrobiom). W abstrakcie brak odniesienia do zakresów referencyjnych — [Europe PMC, PMID 33242416](https://doi.org/10.1016/j.cell.2020.10.050)

### Inferences
- Literatura „precision space health” daje solidne wsparcie dla tezy „baseline = sam astronauta” (Scott: „the best baseline for an individual is oneself”). Projekt hackathonowy może się na tym oprzeć.
- Żadna z tych prac nie formalizuje **zależności baseline od fazy misji** (pre-flight → launch → early adaptation → steady state → landing → readaptation) jako oczekiwanego korytarza. Mówią o „deviations from a healthy baseline”, czyli implicite o baseline ziemskim.

### Gaps
- Pełnego tekstu Afshinnekoo 2020 i opublikowanej wersji Scott 2023 (paywall/brak w Europe PMC) nie przeszukano pod kątem „reference range”. Sanders et al. 2023 (Nat Mach Intell, „Biological research and self-driving labs in deep space”) nie udało się wyekstrahować (uszkodzony PDF). Nie wiadomo, czy wspominają o normach.

---

## 5. AI/ML, wykrywanie anomalii i CDSS dla autonomii medycznej: czy wspominają o niedopasowaniu ziemskich norm / fałszywych alarmach?

### Takeaway
NASA (EIMO, CMO Digital Assistant z Google) planuje CDSS z pasywnym monitoringiem i wczesnymi ostrzeżeniami. **Nie znaleziono dokumentu, który kwantyfikowałby fałszywe alarmy wynikające z ziemskich norm.** Problem „new normal” jest nazwany tylko u Scott et al. (adaptacja modeli EKG trenowanych na danych ziemskich).

### Cited Findings
- EIMO (NASA): CDSS ma wspierać CMO "in response to medical contingencies when terrestrial support is delayed or otherwise unavailable". Zaawansowane funkcje mogą obejmować "passive monitoring to identify early warning signs of behavioral or medical anomalies" (wg streszczenia wyszukiwarki dokumentu NTRS) **[OPINIA/PLAN]** — [NTRS EIMO overview](https://ntrs.nasa.gov/api/citations/20230016189/downloads/EIMO_OVERVIEW_IWS24.docx); [NTRS 20230014228](https://ntrs.nasa.gov/citations/20230014228)
- Abstrakt NASA zauważa, że obecne multimodalne AI "remain unreliable and are subject to 'digital hallucinations'" (wg podsumowania wyszukiwarki) — [NTRS 20240000914](https://ntrs.nasa.gov/citations/20240000914)
- Google + NASA, Crew Medical Officer Digital Assistant (CMO-DA): plan rozbudowy o dane z urządzeń medycznych i trening modelu na "space-specific conditions" (materiał prasowy, nie peer-review) — [Google Public Sector](https://publicsector.google/ai/how-google-and-nasa-are-testing-ai-for-medical-care-in-space/)
- Scott et al.: "Adapting a model trained using terrestrial electrocardiogram data to 'new normal' of electrocardiogram readings from astronauts whose heart physiology has changed in spaceflight." **[OPINIA]** — [arXiv 2112.12554](https://arxiv.org/abs/2112.12554)
- W przeglądzie (ogólnym, nie kosmicznym) human digital twin opisano budowę baseline z historii danej osoby zamiast norm populacyjnych (wg podsumowania wyszukiwarki) — [arXiv 2508.13138](https://arxiv.org/abs/2508.13138)

### Inferences
- Luka „fałszywe alarmy z powodu ziemskich norm” jest w literaturze kosmicznej **niezbadana ilościowo**. Projekt hackathonowy może ją pokazać na danych symulowanych, uczciwie oznaczając je jako ilustrację, a nie dowód.

### Gaps
- Nie znaleziono publikacji z liczbą lub odsetkiem fałszywych alarmów (ani przegapień) monitoringu fizjologicznego astronautów przy progach ziemskich.
- Nie zweryfikowano pełnych dokumentów EIMO (pobrano tylko podsumowania).

---

## 6. Analogie ziemskie (sportowcy, Antarktyda/Concordia, wojsko) używane w literaturze kosmicznej

### Takeaway
Metodologia spersonalizowanych przedziałów referencyjnych i RCV jest dojrzała w chemii klinicznej. W literaturze kosmicznej **nie znaleziono jednak jawnego odwołania do Athlete Biological Passport** ani do spersonalizowanych zakresów z analogów (Concordia, HERA, Mars-500). Najbliższe są dane Markina (selekcja i trening zmieniają normy) oraz Baevsky'ego (analogi: Mars-500, praca operatorska).

### Cited Findings
- Metodologia ziemska: „A Parametric Empirical Bayes Approach to Personalized Reference Intervals and Reference Change Values” (Clinical Chemistry 2025). Personalizowany RI używa wielu punktów do ustalenia baseline pacjenta, a RCV ocenia zmianę między dwoma pomiarami (wg podsumowania wyszukiwarki) — [PMC12582661](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12582661/)
- Concordia/CHOICE: monitoring immunologiczny i kortyzolu raportowany na poziomie grupy, bez indywidualnych przedziałów (wg podsumowania wyszukiwarki dokumentów NTRS) — [NTRS 20140002723](https://ntrs.nasa.gov/citations/20140002723); [NTRS Palmer pilot](https://ntrs.nasa.gov/citations/20230004257)
- HERA (analog NASA) z Astroskin/Bio-Monitor: baseline przed i po misji, każdy to 1 doba ciągłego monitoringu 24 h (wg podsumowania wyszukiwarki) — [NTRS 20190000238](https://ntrs.nasa.gov/api/citations/20190000238/downloads/20190000238.pdf)
- Baevsky et al., Mars-500: "a slight tendency to increase the probability of prenosological states" (wg podsumowania wyszukiwarki abstraktu IAC 2012) — [IAC-12 A1.2](https://iafastro.directory/iac/archive/browse/IAC-12/A1/2/14835/)

### Inferences
- Athlete Biological Passport (bayesowski indywidualny profil z adaptacyjnymi progami) to bardzo bliska koncepcyjnie analogia dla „osobistego korytarza”. Jej użycie w projekcie byłoby **naszym oryginalnym transferem**, nieudokumentowanym w literaturze kosmicznej.

### Gaps
- Nie znaleziono pracy o personalizowanych przedziałach referencyjnych dla wysokogórskich lub wojskowych populacji, która byłaby cytowana w kontekście kosmicznym. Nie znaleziono wyników CARDICORTEX (Concordia) z indywidualnymi baseline.

---

## 7. Prior art: czy ktoś zbudował „osobisty, zależny od fazy misji oczekiwany korytarz” dla vitals astronautów? (ocena nowości)

### Takeaway
**Najbliższym i bardzo istotnym prior art jest rosyjska (IBMP) diagnostyka prenozologiczna R.M. Baevsky'ego.** Od lat 2000 na ISS (eksperymenty „Pulse”, „Pneumocard”) na podstawie HRV oceniano prawdopodobieństwo czterech stanów funkcjonalnych („adaptation risk”), uwzględniano indywidualny typ regulacji autonomicznej i etapy adaptacji. To jest koncepcyjnie „osobista ocena zależna od fazy”, ale oparta na klasyfikacji stanów (normy grupowe i dyskryminacja), a nie na jawnym, ciągłym korytarzu oczekiwanych wartości per osoba i faza. Nie znaleziono systemu zachodniego (NASA, ESA, CSA Bio-Monitor), który publicznie robi to, co proponuje hackathon. Bio-Monitor przesyła dane na Ziemię, a publicznie nie opisano analityki baseline.

### Cited Findings
- **Baevsky RM, Luchitskaia ES, Funtova II, Chernikova AG. „[Researches of autonomic regulation of blood circulation in the condition of long-term space flight]”, Fiziol Cheloveka 2013 (PMID 25509871) [DANE + model]**: "We described probabilistic approach created on the basis of HRV analysis to an estimation of risk of pathology development in the conditions of long space flight. The individual type of autonomic regulation had essential value during the analysis of results. It is shown that the type of regulation, which is inherent in every cosmonaut in the conditions of weightlessness, remains even during following flights." Oraz: "staying in weightlessness is connected with changeover of regulatory systems and with transition in a zone of prenosological states." — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=prenosological%20AND%20(cosmonaut*%20OR%20%22space%20flight%22)&resultType=core&format=json)
- **Baevsky RM, Chernikova AG. „[Assessment of adaptation risk in the individual prenosological control]”, Ross Fiziol Zh Im I M Sechenova 2014 (PMID 25697025) [model + dane]**: "Trends in the development of modern ideas about health as the ability to adapt require personalization and preventive orientation in evaluating and predicting individual health. It can be realized only on the basis of prenosological approach, which is necessary [...] in the aviation and space medicine." Autorzy deklarują: "the developed methods for individual prenosological control have high diagnostic efficiency." — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=prenosological%20AND%20(cosmonaut*%20OR%20%22space%20flight%22)&resultType=core&format=json)
- **Baevsky RM 2006, „[Estimation and prediction of functional changes in organisms in space flight]”, Usp Fiziol Nauk (PMID 17022467)**: "Changes of organism functional state at different stages of adaptation to conditions of long weightlessness are described. The mathematical model of functional states is submitted. Four types of the vegetative regulation, differing on the adaptive reactions in conditions of space flight are allocated." Ten element zależny od faz najbliżej przypomina „mission-phase-dependent” — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=prenosological%20AND%20(cosmonaut*%20OR%20%22space%20flight%22)&resultType=core&format=json)
- IAC 2012 (Baevsky et al., 26 członków rosyjskich załóg): oblicza się prawdopodobieństwo (%) każdego z 4 stanów jako miarę ryzyka. Średnie grupowe w locie "do not go beyond normal (probability of physiological normal state varies from 63 to 74%)" (wg podsumowania wyszukiwarki) — [IAC-12 A1.2 14827](https://iafastro.directory/iac/archive/browse/IAC-12/A1/2/14827/)
- IAC 2015 (IBMP) przyznaje trudność: interpretacja jest utrudniona "particularly when evaluating the individual dynamics because of strong interindividual differences" (wg podsumowania wyszukiwarki) — [IAC-15 A1 IP 29341](https://iafastro.directory/iac/archive/browse/IAC-15/A1/IP/29341/)
- Baevsky 2011 (Acta Astronautica): klasyfikacja dyskryminacyjna (4 klasy) indywidualnej adaptacji na podstawie HRV. U poszczególnych kosmonautów widać odmienne wzorce zależne od stanu przedlotowego (wg podsumowania wyszukiwarki) — [ScienceDirect S0094576511002189](https://www.sciencedirect.com/science/article/abs/pii/S0094576511002189)
- Ushakov, Orlov, Baevsky et al. 2013, „[Conception of health: space-earth]”: koncepcja przeniesiona na sportowców, pilotów, kierowców i operatorów, czyli ziemskie zastosowania prenozologii — [Europe PMC, PMID 23789380](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=prenosological%20AND%20(cosmonaut*%20OR%20%22space%20flight%22)&resultType=core&format=json)
- CSA Bio-Monitor (Astroskin, Carré Technologies/Hexoskin) na ISS od 2019: mierzy tętno, EKG, ciśnienie krwi i inne parametry, "sends information to the ground" do monitoringu całodobowego. Brak publicznego opisu indywidualnych baseline ani analityki alarmowej — [CSA](https://www.asc-csa.gc.ca/eng/sciences/astroskin.asp)
- Zheng 2023 i Scott 2021/2023 (pkt 2 i 4) to retrospektywna analiza lub wizja, nie działający system korytarzy — [PMC10376710](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376710/); [arXiv 2112.12554](https://arxiv.org/abs/2112.12554)
- Propozycje „digital twin astronauty” istnieją w roadmapach, np. EBRC 2024: tworzenie AI-generated twins astronautów przed misjami (dokument planistyczny, wg podsumowania wyszukiwarki) — [EBRC roadmap 2024](https://roadmap.ebrc.org/wp-content/uploads/2024/10/Engineering-Biology-for-Space-Health_EBRC-28Oct2024.pdf)

### Inferences
- **Ocena nowości pomysłu hackathonowego:** sam postulat „osobisty baseline zamiast ziemskiej normy” **nie jest nowy** (Baevsky od lat 90./2000., Schmidt & Goodwin 2013, Scott 2021/2023, Zheng 2023, Ferraro 2026). **Nowa może być konkretna operacjonalizacja**: jawny korytarz oczekiwanych wartości vitals per osoba **i** per faza misji (np. baseline ziemski × oczekiwany dryf adaptacyjny dla fazy), z wizualnym porównaniem „alarm wg normy ziemskiej vs alarm wg korytarza”. W publicznej literaturze nie znaleziono takiego działającego systemu.
- Uczciwe pozycjonowanie: „rozwijamy kierunek wskazany przez NASA (Precision Space Health), laboratoryjników (RCV, Ferraro 2026) i IBMP (prenozologia), dodając jawny model zależny od fazy misji”. Pomijanie Baevsky'ego w prezentacji byłoby błędem merytorycznym, bo to bezpośredni poprzednik.
- Dane Markina 2013 i Balali 2025 można użyć jako argumentu, że „norma” zależy od populacji (astronauci ≠ populacja ogólna) i od kontekstu pomiaru (pozycja ciała).

### Gaps
- Nie znaleziono pełnych tekstów prac Baevsky'ego (rosyjskie czasopisma, abstrakty IAC). Nie wiadomo, czy system „Pneumocard” operacyjnie generował alerty dla lekarzy w czasie rzeczywistym, czy służył tylko badaniom.
- Nie znaleziono publicznych informacji o analityce danych Bio-Monitor ani o tym, czy ESA, JAXA albo prywatni operatorzy (Axiom, SpaceX/Polaris) stosują indywidualne progi.
- Nie przeszukano patentów (Google Patents) pod kątem „personalized physiological baseline astronaut”.
- Nie znaleziono prac z 2026 r. (poza Ferraro et al.) wprost o spersonalizowanych zakresach referencyjnych w kosmosie. Wyszukiwanie mogło nie objąć najnowszych preprintów.
