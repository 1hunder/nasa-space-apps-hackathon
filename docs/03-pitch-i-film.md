# Space-Normal — film 30 s i pitch 3 min

Dla: pitchu, filmu, napisów i montażu.
Format: **film ≤ 30 s** w zgłoszeniu (EN lub napisy EN) + **pitch na żywo z deckiem**.
Deck: [`pitch/index.html`](../pitch/index.html) — jedyna aktualna prezentacja (wersja kinowa, jeden plik, PL, 2:30). Skrypt słowo w słowo: [`pitch/SKRYPT.md`](../pitch/SKRYPT.md).
Wszystkie liczby: z `docs/claims.md` albo [`02-dowody-nasa.md`](02-dowody-nasa.md).

---

## 1. Film 30 s do zgłoszenia — nie slajdy

W samym zgłoszeniu idzie film, nie zrzuty slajdów: wyróżnia nas, mamy designera, a wykres z uginającym się korytarzem **musi być zobaczony**. Na żywo ten sam obraz niesie slajd `chart` w decku.

Zasady:
- **Wykres w filmie = prawdziwe nagranie ekranu naszego dashboardu**, nie animacja AI. To dowód, że produkt działa (Validity). AI-wideo tylko na ujęcia klimatu (statek, astronauta, Mars).
- Limit 30 s jest twardy. Lepiej 28 s.
- Lektor po angielsku albo **napisy EN** obowiązkowe przy innym języku.
- Bez logo NASA, bez prawdziwych astronautów/osób, bez muzyki bez licencji. Wszystkie narzędzia AI i zasoby → pole References.
- Każdy kadr z danymi ma etykietę „NASA bed rest analog” lub „flight-like, literature-based, synthetic”.

### Storyboard

| s | Obraz | Tekst / lektor (EN) |
|---|---|---|
| 0–4 | AI: wnętrze statku w tranzycie, Mars daleko w oknie. Napis: „Mars transit · day 80” | „On the way to Mars, there's no doctor on call.” |
| 4–8 | Napisy jeden po drugim: „22 min one-way delay” · „2-week blackouts” · „no evacuation” | „Messages take up to 22 minutes. Sometimes weeks of silence.” |
| 8–12 | AI: astronautka mierzy temperaturę; na ekranie 37.7°C, czerwony alarm „FEVER?” | „And a healthy astronaut can run 38 degrees.” |
| 12–20 | **Nagranie dashboardu:** płaskie pasy (Earth normal, Pre-flight) migają alarmami; uginający się korytarz Space-Normal zostaje spokojny | „Space-Normal knows how *your* body should change on *this* day of the mission.” |
| 20–26 | **Nagranie dashboardu:** tętno Eleny wypada z korytarza, ziemska norma milczy → karta OBSERVATION / CHECK NOW / ESCALATE IF | „It flags what adaptation can't explain — and tells you what to check.” |
| 26–30 | Liczba główna z `claims.md` + „Tested on NASA bed rest data (ground analog)” + nazwa | „Space-Normal. Your normal, for space.” |

## 2. Pitch na żywo — deck

**Prezentacja:** [`pitch/index.html`](../pitch/index.html). Otwierasz plik w przeglądarce, działa offline (GSAP i filmy leżą w `pitch/vendor/` i `pitch/assets/`). Klawisze: `→` / spacja / klik dalej · `←` wstecz · `F` pełny ekran · `P` okno notatek prelegenta · `T` stoper 2:30 · `R` reset stopera · `1`–`8` skok do slajdu.

Pierwsze naciśnięcie odpala intro: dojazd do planet, przelot, portal otwiera się na astronautce. Potem dopiero slajd 1. Hash w adresie to `#slajd.klik`, np. `#3.2`, więc do próby wracasz tam, gdzie skończyłeś.

| # | Klucz | Kotwica | Klików |
|---|---|---|---|
| 1 | `hook` | Dzień 80 · 37,7 °C · „Gorączka?” | 1 |
| 2 | `problem` | Nie ma kogo zapytać (22 min · ~2 tyg. · 0 lekarzy) | 3 |
| 3 | `chart` | Jej norma się przesuwa | 5 |
| 4 | `product` | Trzy linijki | 1 |
| 5 | `proof` | Dane NASA (bed rest · 18 + 11 · Stanford) | 0 |
| 6 | `diff` | Warstwa przed diagnozą (vs CMO-DA) | 1 |
| 7 | `close` | Space-Normal · twoja norma · link do aplikacji | 1 |
| 8 | `sources` | Źródła — slajd zapasowy na Q&A | 0 |

Zasady przy edycji decku:
- Cały tekst siedzi w obiekcie `CONFIG` na górze `<script>` — slajdy generują się z niego. Nie dopisuj tekstu do HTML.
- Notatki (`notes:` w `CONFIG`) muszą zgadzać się ze [`pitch/SKRYPT.md`](../pitch/SKRYPT.md) — jeden `[klik]` = jeden `beat`.
- Link do aplikacji jest w jednym miejscu: stała `APP_URL`. Wyświetla się w rogu (dolny pas) i na slajdzie zamykającym.
- Żadnych liczb wyników, dopóki `docs/claims.md` jest stubem. Nie wstawiaj placeholderów `{X}` do slajdów — były, zostały usunięte.

### Wariant zapasowy: 3 min bez slajdów

Jeśli nie ma projektora. Cel: juror ma **zobaczyć w głowie** jeden obraz — siatkę centylową z kanałem, który ugina się w trakcie misji.

| Czas | Część | Treść (szkic, mówić własnymi słowami) |
|---|---|---|
| 0:00–0:20 | Haczyk | „Zdrowy astronauta po trzech miesiącach w kosmosie może mieć 38 stopni. Na Ziemi każdy lekarz powiedziałby: gorączka. W kosmosie to normalne.” |
| 0:20–0:55 | Problem słowami NASA | Droga na Marsa: do 22 min w jedną stronę, tygodnie ciszy, brak ewakuacji. NASA nie wymaga lekarza na pokładzie — dwóch przeszkolonych członków załogi. NASA sama napisała w celach Moon to Mars: monitorować zdrowie „throughout all mission phases… without terrestrial medical assistance”. |
| 0:55–1:40 | Pomysł | Siatka centylowa u pediatry: nie porównujesz dziecka z dorosłym, tylko z jego kanałem dla wieku. Space-Normal robi to samo: dzień misji zamiast wieku, korytarz każdego astronauty, który ugina się, bo ciało w kosmosie *powinno* się zmieniać. Ziemska norma krzyczy przy zdrowym; płaska norma sprzed lotu też. Korytarz milczy — i odzywa się, gdy ktoś wypada ze *swojego* kanału, nawet jeśli według Ziemi wszystko jest OK. Rano 3 linijki: co widzimy, co sprawdzić, kiedy eskalować. |
| 1:40–2:15 | Dowód | Prawdziwe dane NASA z bed rest — eksperymentów, w których ludzie leżą tygodniami głową w dół, tak jak NASA symuluje nieważkość. Dopasowanie na jednych osobach, test na innych, których model nigdy nie widział. Liczba główna z `claims.md`. Uczciwie: to analog naziemny — dokładnie taki krok walidacji NASA zapisała w celu HBS-2LM. |
| 2:15–2:45 | Różnica | „NASA już testuje asystenta CMO-DA — najpierw z Google, teraz offline z Red Hat. Pomaga diagnozować, kiedy astronauta zgłosi objawy: odpowiada na pytanie »co mi jest?«. Space-Normal odpowiada na pytanie wcześniejsze: »czy to jeszcze normalne u mnie, dziś?« — i przekazuje tę odpowiedź dalej. To lekarz, do którego idziesz, kiedy boli; my mówimy, że warto iść — zanim zaboli.” Osobisty baseline nie jest nowy (rosyjska szkoła Bajewskiego, koncepcja NASA) — nowy jest korytarz, który ugina się z misją. |
| 2:45–3:00 | Zamknięcie | „Na Marsie nie zapytasz lekarza. Ale możesz zapytać własne ciało, czy jest tam, gdzie powinno być.” |

## 3. Pytania jurorów — przygotowane odpowiedzi

| Pytanie | Odpowiedź (sedno) |
|---|---|
| „To tylko wykrywanie anomalii?” | Wykrywanie anomalii pyta „czy odbiega od normy”. My wiemy, **jak norma powinna się przesuwać** w kosmosie — dlatego nie alarmujemy przy zdrowej adaptacji i widzimy zmiany, które mieszczą się w ziemskiej normie. |
| „Czy macie dane z lotu?” | Nie. NASA bed rest, analog naziemny, wydzielony test. Temperatura w filmie to tryb oparty na publikacjach z lotów, oznaczony jako syntetyczny. Następny krok: dane z ISS (np. Bio-Monitor). |
| „Google/Red Hat dodadzą parametry życiowe do CMO-DA i będzie to samo.” | Same pomiary nic nie dadzą modelowi językowemu bez punktu odniesienia: co jest normalne u tej osoby w tym dniu misji. Korytarz to ten punkt odniesienia — dajemy asystentowi wejście, którego dziś publicznie nie ma. Decyzja o alarmie i tak nie powinna należeć do LLM (NASA: „digital hallucinations”, NTRS 20240000914). |
| „To funkcja, którą Google dopisze w tydzień.” | Wartość nie jest w kodzie, tylko w krzywych adaptacji dopasowanych na danych NASA, ewaluacji na wydzielonym teście i audytowalnej logice alarmu. Dlatego to osobna warstwa, nie kolejny prompt. |
| „Ile osób w teście?” | Podać uczciwie z `claims.md` (CFT70: 3 osoby; C3 G/H: 8). Małe, ale nigdy nieużyte do strojenia. |
| „Kto ustala progi eskalacji?” | Mentor medyczny / lekarze lotu; w prototypie to placeholdery. Twarde limity bezpieczeństwa działają niezależnie i personalizacja nie może ich poszerzyć. |
| „Czemu nie LLM?” | Decyzja o alarmie musi być wytłumaczalna i działać offline. LLM może najwyżej sformułować tekst; nie może wyciszyć alarmu. |
| „Czy NASA tego potrzebuje?” | Cytaty: TH-8LM, HBS-2LM, NASA-STD-3001 Rev C, luka HRP Medical-701, ADD Rev C 0405. |
| „Co z powierzchnią Marsa?” | Kolejna faza korytarza — roadmapa. Na razie walidujemy tylko tranzyt, bo bed rest to analog nieważkości. |
| „Przydatne na Ziemi?” | Ta sama idea dla ludzi w izolacji: stacje antarktyczne, praca offshore, długie misje wojskowe, pacjenci monitorowani zdalnie — wszędzie, gdzie „normalne” zmienia się z czasem, a lekarz jest daleko. (Hipoteza, nie wynik.) |
