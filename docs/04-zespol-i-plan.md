# Space-Normal — zespół, plan i sposób pracy

Stan na 2026-11-14. Budżet: **8 h pracy** do zgłoszenia (oficjalny termin: niedziela 15.11, 23:59 czasu lokalnego — patrz [`zrodla/judging-awards-guide-2026.pdf`](zrodla/judging-awards-guide-2026.pdf)).

## 1. Role

| Osoba | Rola | Odpowiada za (owner) | Czyta najpierw |
|---|---|---|---|
| **Petro** | team lead, AI dev, pitch | kierunek i [`00-kontekst.md`](00-kontekst.md); akceptacja każdej liczby i zdania w filmie/zgłoszeniu; pitch 3 min; lektor | wszystko |
| **Viktor** | AI dev — core | pipeline, ewaluacja na prawdziwych danych NASA, `docs/claims.md`, zmiany z [`01`](01-produkt-i-zakres.md) §4 | `00`, `01` §4, `../PLAN.md` |
| **Davyd** | AI dev — deploy | publiczny deploy dashboardu (statyczny Vite z `web/`), domena, potem nagrania ekranu do filmu, strona zgłoszenia | `00` §1, `01` §1 i §5 |
| **Alex** | design | główny ekran (3 pasy + karta + załoga), storyboard i montaż filmu, styl napisów | `00` §1–5, `01` §1–2, `03` §1 |
| **Anna** | asystentka | pole References, teksty formularza EN (szkic), AI-ujęcia do filmu wg storyboardu, napisy, pilnowanie czasu, próby pitchu z Petro | `02` §4, `03` |

## 2. Harmonogram (T = start po odpoczynku)

| Kiedy | Kto | Co | Wynik |
|---|---|---|---|
| T+0:00–0:15 | wszyscy | Kick-off: każdy czyta `00-kontekst.md` (10 min), Petro odpowiada na pytania | wspólny obraz |
| T+0:15–3:00 | Viktor | Ewaluacja na wydzielonym teście + zmiany z `01` §4 | `docs/claims.md` z liczbą główną |
| T+0:15–2:00 | Davyd | Deploy obecnego dashboardu pod linkiem; domena opcjonalnie | działający link |
| T+0:15–2:30 | Alex | Projekt głównego ekranu + karta (Figma/makieta) → przekazanie do Viktora/Davyda | makieta |
| T+0:15–3:00 | Anna | AI-ujęcia 0–12 s filmu, lista References, szkic tekstów formularza | materiały |
| T+0:15–3:00 | Petro | Scenariusz pitchu słowo w słowo, lektor filmu, przegląd tekstów | scenariusz |
| **T+3:00** | wszyscy | **Checkpoint 1 (15 min):** liczba główna znana? makieta przyjęta? link działa? | **zamrożenie zakresu** |
| T+3:00–5:00 | Viktor + Davyd | Wdrożenie makiety Alexa do dashboardu, scenariusz demo do nagrania | ekran do filmu |
| T+3:00–5:00 | Alex + Anna | Montaż filmu z placeholderem na nagranie ekranu | wersja 0 filmu |
| **T+5:00** | wszyscy | **Checkpoint 2:** nagranie ekranu → film. **Zamrożenie funkcji** — od teraz tylko poprawki | wersja 1 filmu |
| T+5:00–6:30 | Petro + Anna | Próby pitchu (min. 3 razy na stoperze), strona zgłoszenia EN | pitch < 3:00 |
| T+5:00–6:30 | Alex | Szlif filmu, napisy EN | film finalny |
| T+6:30–7:00 | Petro | **Bramka prawdy:** każda liczba i zdanie vs `claims.md` / `02-dowody-nasa.md` | zgoda na wysyłkę |
| T+7:00 | Davyd/Petro | **Zgłoszenie** (wszyscy w zakładce Members!) | wysłane |
| T+7:00–8:00 | — | bufor na awarie | — |

## 3. Zasady iteracji

- **Jedno źródło prawdy:** `00-kontekst.md`. Zmiana kierunku = edycja tego pliku przez Petro + wiadomość na kanale.
- **Krótkie synchronizacje co ~90 min** (5 min, na stojąco): co zrobione, co blokuje, czy liczby się zmieniły.
- **Liczby płyną w jedną stronę:** pipeline → `docs/claims.md` → dashboard / film / pitch. Nikt nie wpisuje liczb ręcznie do filmu.
- **Zamrożenia:** zakres na T+3:00, funkcje na T+5:00. Po T+5:00 tylko poprawki błędów i tekstu.
- **Blokady:** jeśli coś stoi > 30 min, eskaluj do Petro; plan B zawsze gotowy (np. film na samym syntetycznym replayu z uczciwą etykietą).
- **Agenci AI:** każdy agent zaczyna od `CLAUDE.md` → `docs/README.md` → `00-kontekst.md`; dostaje zadanie z jednym plikiem wynikowym.

## 4. Git

- `main` — kod Viktora i Davyda (PR-y). `V2` — dokumenty Petra; trafia do `main` przez PR.
- Kod demo i dokumenty nie powinny edytować tych samych plików jednocześnie; README edytuje Viktor.
