# Przekazanie kontekstu — stan na 2026-11-14

Ten plik streszcza dwie rozmowy z Claude (aplikacja desktop): scalenie dwóch wersji pomysłu oraz sprawdzenie źródeł o ziemskich normach. Nowa sesja Claude Code powinna zacząć od przeczytania tego pliku.

## Zasady pracy

- **Branch roboczy: `V2`.** Każdą zmianę commitujemy i od razu pushujemy na `origin/V2`. Na `main` nie pushujemy; `V2` trafi do `main` później przez PR.
- Kolega pushuje bezpośrednio na `main` i ma osobny branch `p0-scaffold` (szkielet kodu, pipeline, kontrakt dashboardu). Tego kodu nie ma jeszcze na `V2`.
- **Dokumenty piszemy po polsku.** Tytuły i cytaty źródeł zostają w oryginale.

## Dokumenty: co jest aktualne

| Plik | Rola | Status |
|---|---|---|
| `space-normal-merged-concept.md` | **Główny, aktualny opis projektu.** Silnik Viktora (plan v2.1) + produkt Petra (brainstorm) | Propozycja do akceptacji przez zespół |
| `space-normal-dowody-normy-ziemskie.md` | Sprawdzenie źródeł: czy ziemskie normy nie pasują w kosmosie; poprawki do dokumentu merged | Gotowe |
| `space-normal-claude-code-plan.md` | Plan implementacji v2.1 (Viktor) | Do uzupełnienia po akceptacji merged (patrz niżej) |
| `space-normal-brainstorm-handoff.md` | Brainstorm Petra (po angielsku) | Źródło historyczne |
| `space-normal-summary.md` | Pierwsze streszczenie pomysłu | Do aktualizacji po akceptacji merged |

## Najważniejsze ustalenia

1. **Werdykt merged:** MVP = dzienny detektor adaptacji na danych NASA bed rest (C1+C3 do dopasowania, CFT70 jako nietknięty test). Scenariusz termiczny/treningowy = roadmapa, nie MVP. Główny użytkownik = astronauta (karta: obserwacja → sprawdź teraz → eskaluj, jeśli); lekarz lotu dostaje opóźniony pakiet.
2. **Ziemskie normy (dowody):**
   - Przyrządy mierzą poprawnie; problemem jest interpretacja przez populacyjne progi.
   - Nie ma dowodu, że na ISS działają automatyczne alarmy na ziemskich progach — dane interpretuje lekarz lotu na Ziemi. Nie twierdzić, że „obecne systemy alarmują bez przerwy”.
   - **Tętno spoczynkowe w locie się nie zmienia** (Norsk 2015). Spada ciśnienie (~−10 mmHg). Tętno w demo jest OK tylko jako analog bed rest.
   - Lepsze przykłady „zdrowy, ale poza normą”: temperatura głęboka ~38°C (Stahn 2017), anemia kosmiczna +54% niszczenia krwinek (Trudel 2022).
   - Osobisty punkt odniesienia wspierają: CCLM 2026 (reference change values — propozycja, nie standard), Zheng 2023, NASA ExMC/EIMO (pokładowe wsparcie decyzji, bo do Marsa do ~24 min opóźnienia).

## Otwarte decyzje (z merged §11)

1. Akceptacja werdyktu: dzienny detektor = MVP, termika = roadmapa.
2. Kwalifikacja: które źródło NASA jest w zakładce Resources wyzwania i czy nasze użycie się liczy.
3. Mentor medyczny: kto ustala limity niebezpieczeństwa i progi „eskaluj, jeśli”.
4. Dostęp do danych NLSP: inwentaryzacja; jeśli brak dziennych danych per osoba → fallback syntetyczny, uczciwie oznaczony.
5. Widoczność repo na potrzeby zgłoszenia.

## Następne kroki

- Wprowadzić do `space-normal-merged-concept.md` poprawki z `space-normal-dowody-normy-ziemskie.md` §5 (sformułowanie problemu w §2).
- Po akceptacji merged: zaktualizować `space-normal-summary.md` i uzupełnić plan v2.1 o kartę astronauty, warstwę limitów niebezpieczeństwa, 30-sekundowe demo i listę cięć.
- Zdecydować, czy i kiedy wciągnąć na `V2` kod z `p0-scaffold` / `main` kolegi.
