# Space-Normal — film 30 s i pitch 3 min

Dla: Petro (pitch), Alex (film), Anna (napisy, montaż, AI-wideo).
Format: najpierw **film ≤ 30 s** w zgłoszeniu (EN lub napisy EN), potem **3 min pitchu na żywo bez slajdów**.
Wszystkie liczby: z `docs/claims.md` albo [`02-dowody-nasa.md`](02-dowody-nasa.md).

---

## 1. Film 30 s — decyzja: film, nie slajdy

Film to dobry wybór: wyróżnia nas, mamy designera, a wykres z uginającym się korytarzem **musi być zobaczony** — w pitchu bez slajdów jurorzy go nie zobaczą, więc film jest jedynym miejscem na ten obraz.

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
| 20–26 | **Nagranie dashboardu:** tętno Chena wypada z korytarza, ziemska norma milczy → karta OBSERVATION / CHECK NOW / ESCALATE IF | „It flags what adaptation can't explain — and tells you what to check.” |
| 26–30 | Liczba główna z `claims.md` + „Tested on NASA bed rest data (ground analog)” + nazwa | „Space-Normal. Your normal, for space.” |

## 2. Pitch 3 min (bez slajdów)

Cel: juror ma **zobaczyć w głowie** jeden obraz — siatkę centylową z kanałem, który ugina się w trakcie misji.

| Czas | Część | Treść (szkic, mówić własnymi słowami) |
|---|---|---|
| 0:00–0:20 | Haczyk | „Zdrowy astronauta po trzech miesiącach w kosmosie może mieć 38 stopni. Na Ziemi każdy lekarz powiedziałby: gorączka. W kosmosie to normalne.” |
| 0:20–0:55 | Problem słowami NASA | Droga na Marsa: do 22 min w jedną stronę, tygodnie ciszy, brak ewakuacji. NASA nie wymaga lekarza na pokładzie — dwóch przeszkolonych członków załogi. NASA sama napisała w celach Moon to Mars: monitorować zdrowie „throughout all mission phases… without terrestrial medical assistance”. |
| 0:55–1:40 | Pomysł | Siatka centylowa u pediatry: nie porównujesz dziecka z dorosłym, tylko z jego kanałem dla wieku. Space-Normal robi to samo: dzień misji zamiast wieku, korytarz każdego astronauty, który ugina się, bo ciało w kosmosie *powinno* się zmieniać. Ziemska norma krzyczy przy zdrowym; płaska norma sprzed lotu też. Korytarz milczy — i odzywa się, gdy ktoś wypada ze *swojego* kanału, nawet jeśli według Ziemi wszystko jest OK. Rano 3 linijki: co widzimy, co sprawdzić, kiedy eskalować. |
| 1:40–2:15 | Dowód | Prawdziwe dane NASA z bed rest — eksperymentów, w których ludzie leżą tygodniami głową w dół, tak jak NASA symuluje nieważkość. Dopasowanie na jednych osobach, test na innych, których model nigdy nie widział. Liczba główna z `claims.md`. Uczciwie: to analog naziemny — dokładnie taki krok walidacji NASA zapisała w celu HBS-2LM. |
| 2:15–2:45 | Różnica | „Google i NASA testują asystenta, który pomaga diagnozować, kiedy astronauta zgłosi objawy. To lekarz, do którego idziesz, kiedy boli. Space-Normal to codzienny przegląd, który mówi ci, że warto iść — zanim zaboli. Uzupełniamy się.” Osobisty baseline nie jest nowy (rosyjska szkoła Bajewskiego, koncepcja NASA) — nowy jest korytarz, który ugina się z misją. |
| 2:45–3:00 | Zamknięcie | „Na Marsie nie zapytasz lekarza. Ale możesz zapytać własne ciało, czy jest tam, gdzie powinno być.” |

## 3. Pytania jurorów — przygotowane odpowiedzi

| Pytanie | Odpowiedź (sedno) |
|---|---|
| „To tylko wykrywanie anomalii?” | Wykrywanie anomalii pyta „czy odbiega od normy”. My wiemy, **jak norma powinna się przesuwać** w kosmosie — dlatego nie alarmujemy przy zdrowej adaptacji i widzimy zmiany, które mieszczą się w ziemskiej normie. |
| „Czy macie dane z lotu?” | Nie. NASA bed rest, analog naziemny, wydzielony test. Temperatura w filmie to tryb oparty na publikacjach z lotów, oznaczony jako syntetyczny. Następny krok: dane z ISS (np. Bio-Monitor). |
| „Ile osób w teście?” | Podać uczciwie z `claims.md` (CFT70: 3 osoby; C3 G/H: 8). Małe, ale nigdy nieużyte do strojenia. |
| „Kto ustala progi eskalacji?” | Mentor medyczny / lekarze lotu; w prototypie to placeholdery. Twarde limity bezpieczeństwa działają niezależnie i personalizacja nie może ich poszerzyć. |
| „Czemu nie LLM?” | Decyzja o alarmie musi być wytłumaczalna i działać offline. LLM może najwyżej sformułować tekst; nie może wyciszyć alarmu. |
| „Czy NASA tego potrzebuje?” | Cytaty: TH-8LM, HBS-2LM, NASA-STD-3001 Rev C, luka HRP Medical-701, ADD Rev C 0405. |
| „Co z powierzchnią Marsa?” | Kolejna faza korytarza — roadmapa. Na razie walidujemy tylko tranzyt, bo bed rest to analog nieważkości. |
| „Przydatne na Ziemi?” | Ta sama idea dla ludzi w izolacji: stacje antarktyczne, praca offshore, długie misje wojskowe, pacjenci monitorowani zdalnie — wszędzie, gdzie „normalne” zmienia się z czasem, a lekarz jest daleko. (Hipoteza, nie wynik.) |
