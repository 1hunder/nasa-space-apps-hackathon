# Ujęcia AI do prezentacji pitchu — brief dla osoby generującej

**Narzędzie:** Higgsfield (web), wewnątrz: obraz → Nano Banana Pro albo GPT Image; wideo → Kling 3.0 (taniej) albo Veo 3.1 Fast (najlepsza jakość). Płatny tier (bez watermarku), ok. 10 USD kredytów.
**Format:** 16:9, 1080p, 5–8 s, bez dźwięku. Pliki wrzuć tutaj (`pitch/assets/`) pod nazwami z tabeli — prezentacja podmieni je automatycznie.

**Zasady (AGENTS.md §5.7–8):** fikcyjna osoba, bez podobieństwa do prawdziwych ludzi, **nigdy** nie wgrywaj prawdziwego zdjęcia jako referencji. Bez logo NASA, naszywek, flag, napisów. Każde użyte narzędzie (Higgsfield + konkretny model) → pole References.

**Ta sama astronautka we wszystkich ujęciach:** najpierw ujęcie 1 (still), potem każde wideo jako image-to-video z tym stillem jako pierwszą klatką. Pętla: ostatnia klatka = pierwsza.

Do każdego promptu dopisz na końcu:
`cinematic, 16:9, 1080p, photorealistic, slow camera move, no text, no logos, no insignia, no flags, fictional person`

| # | Plik | Typ | Prompt |
|---|---|---|---|
| 1 | `hero.jpg` | obraz | Portrait of a fictional female astronaut in a plain white EVA helmet, gold visor half-raised, calm expression, soft teal rim light, deep space background, unbranded suit with no patches |
| 2 | `helmet.mp4` | I2V z #1 | Very slow dolly push-in on the astronaut's helmet, Earth reflected and drifting in the visor, subtle breathing, faint teal HUD glow |
| 3 | `planets.mp4` | wideo | Earth in the foreground and Mars far away in black space, thin atmosphere limb glow, distant stars, very slow push toward Mars |
| 4 | `hologram.mp4` | wideo | Translucent teal holographic human body scan rotating slowly above a dark console, heart and lungs glowing, scanning line moving top to bottom, seamless loop |
| 5 | `habitat.mp4` | wideo | Inflatable Mars habitat module on red dunes at sunset, blue Martian sunset sky, dust drifting, slow lateral crane move, warm window light |

Kolejność ważności: 1 → 2 → 3. Ujęcia 4–5 tylko jeśli starczy czasu.
