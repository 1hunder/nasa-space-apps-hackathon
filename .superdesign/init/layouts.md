# Layouts

Single-screen app, no router. `App.tsx` is the shell: header (title, day clock, play button), mission strip, main stage (crew name, vital control, details toggle, chart), side column (crew list, alert card). `useReplay.ts` holds the replay state.

### `web/src/App.tsx`

```tsx
import { useEffect, useState } from "react";
import { AlertPanel } from "./components/AlertPanel";
import { CrewList } from "./components/CrewList";
import { Figure } from "./components/Figure";
import { DEMO_VITALS, PROVENANCE_LABEL, VITAL_LABEL } from "./labels";
import { useReplay } from "./useReplay";

export function App() {
  const r = useReplay();
  const { mission, index } = r;
  const [detail, setDetail] = useState(false);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLElement && ["INPUT", "SELECT", "TEXTAREA"].includes(e.target.tagName)) return;
      if (e.code === "Space") { e.preventDefault(); r.toggle(); }
      else if (e.key === "r" || e.key === "R") r.restart();
      else if (e.key === "d" || e.key === "D") setDetail((d) => !d);
      else if (e.key === "ArrowRight") r.setDay(Math.floor(r.day) + 1);
      else if (e.key === "ArrowLeft") r.setDay(Math.ceil(r.day) - 1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  if (r.error) return <main className="empty"><h1>Space-Normal</h1><p>{r.error}</p></main>;
  if (!mission || !index) return <main className="empty"><h1>Space-Normal</h1><p>Loading the mission…</p></main>;

  const member = mission.crew.find((c) => c.id === r.crewId) ?? mission.crew[0];
  const dayNow = mission.days[r.dayIndex];
  const lastDay = mission.days[mission.days.length - 1];
  const outbreak = mission.crew_alerts.find((c) => c.day <= dayNow);
  const first = (id: string) => (mission.crew.find((c) => c.id === id)?.name ?? id).split(" ")[0];
  const p = mission.provenance;

  return (
    <div className="app">
      <header className="top">
        <h1>Space-Normal</h1>
        <div className="clock">
          <span className="clock-day">Day {dayNow}</span>
          <span className="clock-of">of {lastDay}</span>
          {mission.samples_per_day > 1 && (
            <span className="clock-hour">{String(Math.min(23, Math.floor((r.day - Math.floor(r.day)) * 24))).padStart(2, "0")}:00</span>
          )}
        </div>
        <button className="play" onClick={r.toggle}>
          {r.playing ? "Pause" : r.day >= lastDay ? "Replay" : r.day > mission.days[0] ? "Continue" : "Play"}
        </button>
      </header>

      <p className="strip">
        <span>Mars transit</span>
        <span>day {dayNow}</span>
      </p>

      <main className="stage">
        <div className="stage-head">
          <h2>{member.name}</h2>
          <div className="seg" role="group" aria-label="Vital sign">
            {DEMO_VITALS.map((v) => (
              <button key={v} type="button" className="seg-opt" aria-pressed={r.vital === v} onClick={() => r.setVital(v)}>
                {VITAL_LABEL[v].name} <span className="seg-unit">{VITAL_LABEL[v].unit}</span>
              </button>
            ))}
          </div>
          <button className="more" onClick={() => setDetail((d) => !d)} aria-expanded={detail}>
            {detail ? "Hide details" : "Show details"}
          </button>
        </div>

        {outbreak && (
          <div className="outbreak" role="status">
            <strong>Unexplained crew-wide shift: check the habitat and a possible outbreak.</strong>{" "}
            {outbreak.crew_ids.map((id, i) => [id, outbreak.onsets[i]] as const).filter(([, d]) => d <= dayNow)
              .map(([id, d]) => `${first(id)} from day ${d}`).join(", ")}. No logged event explains it.
          </div>
        )}

        <Figure mission={mission} member={member} vital={r.vital} day={r.day} dayIndex={r.dayIndex}
          detail={detail} reserve={outbreak ? 56 : 0} onScrub={r.setDay} />

        {detail && (
          <p className="fineprint">
            Data in this replay: adaptation {PROVENANCE_LABEL[p.adaptation]}, illness {PROVENANCE_LABEL[p.illness]},
            events {PROVENANCE_LABEL[p.events]}; the journal readings are mocked and no language model runs.
            Keys: space plays or pauses, R restarts, the arrow keys step one day, D shows or hides details.
          </p>
        )}
      </main>

      <aside className="side">
        <CrewList mission={mission} dayIndex={r.dayIndex} crewId={member.id} onSelect={r.setCrewId} />
        <AlertPanel mission={mission} alert={r.activeAlert} viewing={r.vital} />
      </aside>
    </div>
  );
}

```
### `web/src/main.tsx`

```tsx
import "@fontsource-variable/archivo/standard.css";
import "./styles.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

```
### `web/src/useReplay.ts`

```ts
import { useCallback, useEffect, useRef, useState } from "react";
import type { Alert, Mission, MissionIndex, Vital } from "./contract";
import { DEMO_VITALS } from "./labels";

const FULL_REPLAY_SECONDS = 13; // one mission at 1x

export interface Replay {
  index: MissionIndex | null;
  mission: Mission | null;
  error: string | null;
  scenario: string;
  setScenario: (s: string) => void;
  day: number; // fractional mission day
  dayIndex: number; // index of the last fully revealed day
  setDay: (d: number) => void;
  playing: boolean;
  toggle: () => void;
  restart: () => void;
  speed: number;
  setSpeed: (s: number) => void;
  crewId: string;
  setCrewId: (id: string) => void;
  vital: Vital;
  setVital: (v: Vital) => void;
  activeAlert: Alert | null; // latest Space-Normal red alert at or before the playhead
}

export function useReplay(): Replay {
  const [index, setIndex] = useState<MissionIndex | null>(null);
  const [mission, setMission] = useState<Mission | null>(null);
  const [error, setError] = useState<string | null>(null);
  // ?day=40 opens a specific moment (used for bookmarks and screenshots). ?scenario= still works,
  // but the demo cache holds one mission; an unknown scenario falls back to the first one listed.
  const params = useRef(new URLSearchParams(window.location.search));
  const [scenario, setScenario] = useState(params.current.get("scenario") ?? "single_illness");
  const [day, setDayState] = useState(1);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [crewId, setCrewId] = useState("");
  const [vital, setVital] = useState<Vital>("temp_c");
  const dayRef = useRef(1);

  useEffect(() => {
    fetch("./cache/missions.json")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`missions.json: HTTP ${r.status}`))))
      .then(setIndex)
      .catch((e) => setError(`Could not load the mission cache. Run "make demo-synthetic" first. (${e.message})`));
  }, []);

  useEffect(() => {
    if (!index) return;
    const entry = index.missions.find((m) => m.scenario === scenario) ?? index.missions[0];
    if (!entry) return;
    setPlaying(false);
    fetch(`./cache/${entry.file}`)
      .then((r) => r.json())
      .then((m: Mission) => {
        const firstAlert = m.alerts.find((a) => a.detector === "space_normal" && a.level === "red");
        setMission(m);
        setCrewId(firstAlert?.crew_id ?? m.episodes[0]?.crew_id ?? m.crew[0].id);
        setVital("temp_c");
        const asked = Number(params.current.get("day"));
        params.current.delete("day"); // only for the first mission loaded
        const start = asked >= m.days[0] && asked <= m.days[m.days.length - 1] ? asked : m.days[0];
        dayRef.current = start;
        setDayState(start);
      })
      .catch((e) => setError(`Could not load ${entry.file}. (${e.message})`));
  }, [index, scenario]);

  const setDay = useCallback(
    (d: number) => {
      if (!mission) return;
      const clamped = Math.min(mission.days[mission.days.length - 1], Math.max(mission.days[0], d));
      dayRef.current = clamped;
      setDayState(clamped);
    },
    [mission],
  );

  useEffect(() => {
    if (!playing || !mission) return;
    const first = mission.days[0];
    const last = mission.days[mission.days.length - 1];
    const rate = ((last - first) / FULL_REPLAY_SECONDS) * speed; // days per second
    const reds = mission.alerts.filter((a) => a.detector === "space_normal" && a.level === "red");
    let frame = 0;
    let prev = performance.now();
    const tick = (now: number) => {
      // A frame's timestamp can precede the moment the loop started; never step backwards.
      const dt = Math.max(0, Math.min(0.1, (now - prev) / 1000));
      prev = now;
      {
        const before = dayRef.current;
        let next = Math.min(last, before + dt * rate);
        const crossed = reds.find((a) => a.day > before && a.day <= next);
        if (crossed) {
          // An alert stops the replay on that day; Play continues from there.
          next = crossed.day;
          setCrewId(crossed.crew_id);
          // Stay on the vital being watched if it is also clearly off; otherwise show the one that led the alert.
          const i = mission.days.indexOf(crossed.day);
          const member = mission.crew.find((c) => c.id === crossed.crew_id);
          // Only the vitals the demo offers can be shown; anything else falls back to temperature.
          const lead: Vital = DEMO_VITALS.includes(crossed.vital) ? crossed.vital : "temp_c";
          setVital((v) => ((member?.vitals[v].z[i] ?? 0) > 2 ? v : lead));
        }
        dayRef.current = next;
        setDayState(next);
        if (crossed || next >= last) {
          setPlaying(false);
          return;
        }
      }
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing, mission, speed]);

  const toggle = useCallback(() => {
    if (!mission) return;
    if (dayRef.current >= mission.days[mission.days.length - 1]) setDay(mission.days[0]);
    setPlaying((p) => !p);
  }, [mission, setDay]);

  const restart = useCallback(() => {
    if (!mission) return;
    setDay(mission.days[0]);
    setPlaying(true);
  }, [mission, setDay]);

  const dayIndex = mission ? Math.max(0, Math.floor(day) - mission.days[0]) : 0;
  const activeAlert =
    mission?.alerts
      .filter((a) => a.detector === "space_normal" && a.level === "red" && a.day <= Math.floor(day))
      .sort((a, b) => b.day - a.day || (a.crew_id === crewId ? -1 : 1))[0] ?? null;

  return {
    index, mission, error, scenario, setScenario, day, dayIndex, setDay, playing, toggle, restart,
    speed, setSpeed, crewId, setCrewId, vital, setVital, activeAlert,
  };
}

```
### `web/index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Space-Normal: crew health monitoring that knows how the body is expected to change in microgravity. NASA Space Apps prototype." />
    <title>Space-Normal</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>

```
