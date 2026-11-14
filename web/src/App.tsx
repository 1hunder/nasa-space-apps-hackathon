import { useEffect, useState } from "react";
import { VITALS, type Vital } from "./contract";
import { AlertPanel } from "./components/AlertPanel";
import { CrewList } from "./components/CrewList";
import { Figure } from "./components/Figure";
import { PROVENANCE_LABEL, SCENARIO_LABEL, VITAL_LABEL } from "./labels";
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
      else if (index && /^[1-9]$/.test(e.key)) {
        const entry = index.missions[Number(e.key) - 1];
        if (entry) r.setScenario(entry.scenario);
      }
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
        <label className="pick">
          <span className="sr">Scenario</span>
          <select value={mission.scenario} onChange={(e) => r.setScenario(e.target.value)}>
            {index.missions.map((m) => (
              <option key={m.scenario} value={m.scenario}>{SCENARIO_LABEL[m.scenario] ?? m.scenario}</option>
            ))}
          </select>
        </label>
        <div className="clock">
          <span className="clock-day">Day {dayNow}</span>
          <span className="clock-of">of {lastDay}</span>
          {mission.samples_per_day > 1 && (
            <span className="clock-hour">{String(Math.min(23, Math.floor((r.day - Math.floor(r.day)) * 24))).padStart(2, "0")}:00</span>
          )}
        </div>
        <button className="play" onClick={r.toggle}>
          {r.playing ? "Pause" : r.day >= lastDay ? "Replay" : "Play"}
        </button>
      </header>

      <main className="stage">
        <div className="stage-head">
          <h2>{member.name}</h2>
          <label className="pick">
            <span className="sr">Vital sign</span>
            <select value={r.vital} onChange={(e) => r.setVital(e.target.value as Vital)}>
              {VITALS.map((v) => <option key={v} value={v}>{VITAL_LABEL[v].name}, {VITAL_LABEL[v].unit}</option>)}
            </select>
          </label>
          <button className="more" onClick={() => setDetail((d) => !d)} aria-expanded={detail}>
            {detail ? "Hide details" : "Show details"}
          </button>
        </div>

        {outbreak && (
          <div className="outbreak" role="status">
            <strong>Crew-wide drift.</strong>{" "}
            {outbreak.crew_ids.map((id, i) => `${first(id)} from day ${outbreak.onsets[i]}`).join(", ")}.
            No logged event explains it.
          </div>
        )}

        <Figure mission={mission} member={member} vital={r.vital} day={r.day} dayIndex={r.dayIndex}
          detail={detail} reserve={outbreak ? 56 : 0} onScrub={r.setDay} />

        {detail && (
          <p className="fineprint">
            Adaptation: {PROVENANCE_LABEL[p.adaptation]}. Illness: {PROVENANCE_LABEL[p.illness]}. Events:{" "}
            {PROVENANCE_LABEL[p.events]}. Heart, lungs and body temperature are tracked; eyes, bone, muscle and immune
            function are not monitored yet. The faint line is the hourly readings with each person's time-of-day pattern
            removed; the bold line is the daily mean, which the ranges and monitors use. Keys: space to play, R to restart, arrows to step, D for details.
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
