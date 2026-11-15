# Credits and licences: pitch/deck

Everything the deck in this folder uses that the team did not make itself.
Entries are in English so they can be copied into the "References" field of the Space Apps submission.
No image carries a NASA logo or insignia, a real person, or a text overlay.
NASA does not endorse this project; using NASA imagery does not imply endorsement.

## Images

### assets/earth.jpg
- Title: The Blue Marble, "The Earth seen from Apollo 17" (NASA photo AS17-148-22727, 7 Dec 1972)
- Credit: NASA / Apollo 17 crew
- Licence: Public domain (work of the U.S. federal government, NASA)
- Source page: https://commons.wikimedia.org/wiki/File:The_Earth_seen_from_Apollo_17.jpg
- Change: downscaled to 1200 px (from `pitch/assets/free/earth-2400.jpg`), JPEG quality 85
- Used on: opening state, slide 1, slide 2

### assets/mars.jpg
- Title: Global Color Views of Mars, Valles Marineris hemisphere (Viking Orbiter mosaic), PIA00407
- Credit: NASA/JPL/USGS
- Licence: Public domain (NASA/JPL image; see the JPL image use policy)
- Source page: https://photojournal.jpl.nasa.gov/catalog/PIA00407 (also https://images.nasa.gov/details/PIA00407)
- Change: downscaled to 1800 px (from `pitch/assets/free/mars-2400.jpg`), JPEG quality 85
- Used on: opening state, slide 1, slide 7

### assets/dashboard-day44.png
- What: screenshot of the team's own Space-Normal dashboard (`web/`), day 44 of the demo scenario, captured with headless Chrome at 1440 x 810, scale 2
- Credit: Space-Normal team (own work)
- Contains: the same Mars image PIA00407 (NASA/JPL/USGS, public domain) as the dashboard background; the Archivo typeface
- Note: the crew and readings on that screen are a synthetic demo; the crew names are the team members' own names (team decision of 2026-11-15)
- Used on: slide 4

## Drawn in code (no external asset)

- The corridor chart (slide 3), the people and padlock diagram (slide 5), the timeline (slide 6), the corridor band (slide 7) and the star field behind every slide are SVG generated in `index.html`.
- The temperature scenario on the chart is illustrative and synthetic ("flight-like"), with the size of the change taken from the literature: Stahn et al. 2017, Scientific Reports, https://doi.org/10.1038/s41598-017-15560-w

## Typeface

### fonts/archivo-latin-wdth-normal.woff2, fonts/archivo-latin-ext-wdth-normal.woff2
- Name: Archivo (variable, weight and width axes)
- Credit: The Archivo Project Authors, Omnibus-Type (https://github.com/Omnibus-Type/Archivo)
- Licence: SIL Open Font License 1.1 (full text in `fonts/LICENSE-Archivo.txt`)
- Source: npm package `@fontsource-variable/archivo`, copied from `web/node_modules/`

## Software

### vendor/reveal/
- Name: reveal.js 5 (core, plus the speaker notes plugin)
- Credit: Hakim El Hattab and contributors, https://revealjs.com
- Licence: MIT
- Source: copied unchanged from `pitch/vendor/reveal/`

### Tools used to build the deck
- AI coding assistant: Claude Code (Anthropic)
- Google Chrome (headless) for the dashboard screenshot and the PDF export

## Not used

- The three AI video clips in `pitch/assets/` (`astro.mp4`, `planets.mp4`, `holo.mp4`) are not in this deck, so no AI video tool needs a credit for it.
- `stars.jpg` and `mars-surface.jpg` from `pitch/assets/free/` are not used.

## Sources of the facts on the slides

All facts come from `docs/00-kontekst.md` and `docs/02-dowody-nasa.md`; the full reference list is in `docs/02-dowody-nasa.md` §4.

- Up to 22 minutes one-way delay: ASCEND/NASA, "Communication Delays, Disruptions, and Blackouts for Crewed Mars Missions"; NASA 2025 Architecture Update
- About 2 weeks without communication at solar conjunction: HRP 48021, Medical System ConOps for Mars Exploration
- A physician is not required on board: NASA-STD-3001 Vol 1 Rev C
- Pre-flight reference ranges: CDSS ConOps HRP-48033 (2021)
- Resting core temperature of about 38 °C after about 2.5 months in flight: Stahn et al. 2017, Scientific Reports
- Data: NASA Life Sciences Portal, bed rest studies (18 people for fitting, 3 + 8 held out); Stanford COVID-19 Wearables (Mishra et al. 2020; Alavi et al. 2022)
- CMO-DA: Google Cloud blog (2025) and Red Hat blog (2026); these are company blogs, not NASA documents
