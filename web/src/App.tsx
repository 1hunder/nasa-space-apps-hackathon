import { useEffect, useState } from "react";
import { AlertPanel } from "./components/AlertPanel";
import { CrewList } from "./components/CrewList";
import { Figure } from "./components/Figure";
import { JournalStrip } from "./components/JournalStrip";
import { MethodCards } from "./components/MethodCards";
import { DEMO_VITALS, PROVENANCE_LABEL, VITAL_LABEL } from "./labels";
import { useReplay } from "./useReplay";

export function App() {
  const r = useReplay();
  const { mission, index } = r;
  const [detail, setDetail] = useState(false);
  // Journal entry open below the chart: -1 follows the replay (latest entry so far).
  const [entryIndex, setEntryIndex] = useState(-1);
  useEffect(() => setEntryIndex(-1), [r.dayIndex, r.crewId]);

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
    <div className="app" style={{ "--transit": (r.day - mission.days[0]) / (lastDay - mission.days[0]) } as React.CSSProperties}>
      {/* Backdrop: star field and Mars, which grows a little as the transit progresses. */}
      <div className="sky" aria-hidden="true"><div className="mars" /></div>

      <header className="top">
        <div className="brand">
          <svg className="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
            <ellipse cx="16" cy="16" rx="14" ry="6.2" transform="rotate(-24 16 16)" />
            <circle cx="16" cy="16" r="5.4" className="brand-core" />
            <circle cx="27.6" cy="10.4" r="1.9" className="brand-dot" />
          </svg>
          <h1>Space-Normal</h1>
        </div>
        <div className="mission">
          <span className="mission-name">Mars transit</span>
          <div className="clock">
            <span className="clock-day">Day {dayNow}</span>
            <span className="clock-of">of {lastDay}</span>
            {mission.samples_per_day > 1 && (
              <span className="clock-hour">{String(Math.min(23, Math.floor((r.day - Math.floor(r.day)) * 24))).padStart(2, "0")}:00</span>
            )}
          </div>
        </div>
        <button className="play" onClick={r.toggle}>
          <svg viewBox="0 0 12 12" aria-hidden="true">
            {r.playing ? <path d="M2 1h3v10H2zM7 1h3v10H7z" /> : <path d="M2.500 1l8 5-8 5z" />}
          </svg>
          {r.playing ? "Pause" : r.day >= lastDay ? "Replay" : r.day > mission.days[0] ? "Continue" : "Play"}
        </button>
      </header>

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
          detail={detail} reserve={outbreak ? 56 : 0} entryIndex={entryIndex} onPickEntry={setEntryIndex} onScrub={r.setDay} />

        <JournalStrip mission={mission} member={member} dayNow={dayNow} index={entryIndex} onIndex={setEntryIndex} />
        <MethodCards mission={mission} dayNow={dayNow} />

        {detail && (
          <p className="fineprint">
            Data in this replay: adaptation {PROVENANCE_LABEL[p.adaptation]}, illness {PROVENANCE_LABEL[p.illness]},
            events {PROVENANCE_LABEL[p.events]}; the journal readings are mocked and no language model runs.
            Keys: space plays or pauses, R restarts, the arrow keys step one day, D shows or hides details.
            Mars image: NASA/JPL/USGS.
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
