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
