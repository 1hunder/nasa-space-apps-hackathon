# Routes

No router. One page at `/` rendered by `web/src/App.tsx`.

- `/` — Mission dashboard: replays a 90-day crew-health mission. URL parameters: `?day=N` opens a specific day; `?scenario=` is accepted but only one mission exists.

The page shows, for the selected crew member, a chart of a vital sign (core temperature or pulse) against three references: the Earth-normal clinical limit (same for everyone), the personal flat pre-flight range, and the Space-Normal range that moves with expected adaptation. Below the chart: a crew journal row and three monitor lanes with false-alarm counts. Right column: crew list with a body figure for the selected member, and an alert card when Space-Normal raises an alert. The replay stops on an alert.
