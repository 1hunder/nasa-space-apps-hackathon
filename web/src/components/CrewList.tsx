import { useState } from "react";
import type { Mission, State, Vital } from "../contract";
import { BodyFigure, activeReports, describe, type PainReport, type System } from "./BodyFigure";

const ALERT_DAYS = 10; // how long a Space-Normal alert keeps a crew member marked
const SYSTEM_OF: Record<Vital, System> = { pulse: "cardio", sbp: "cardio", dbp: "cardio", resp_rate: "resp", temp_c: "thermo" };

const SHORT: Record<State, string> = {
  expected: "As expected",
  event: "Explained by a logged event",
  unexplained: "Unexplained change",
  crew: "Crew-wide drift",
  not_monitored: "Not monitored",
};
const ICON: Record<State, string> = { expected: "✓", event: "◆", unexplained: "!", crew: "≋", not_monitored: "–" };

/** The selected crew member: the body map carries the system states and journal reports, no text list. */
function CrewCard({ name, state, parts, reports }: {
  name: string; state: State; parts: Record<System, State>; reports: PainReport[];
}) {
  const [inspected, setInspected] = useState<string | null>(null);
  const readout = describe(inspected, parts, reports);
  return (
    <div className={`crew-card state-${state}`} aria-current="true">
      <BodyFigure parts={parts} reports={reports} onInspect={setInspected} />
      <div className="crew-card-text">
        <span className="crew-name">{name}</span>
        <span className="crew-state">{SHORT[state]}</span>
        {/* Says what the hovered or focused part of the figure means. Empty otherwise. */}
        <div className={`readout ${readout?.state ? `readout-${readout.state}` : "readout-report"}`} aria-hidden="true">
          {readout && (
            <>
              <span className="readout-title">{readout.title}</span>
              {readout.quotes.map((q) => (
                <span key={`${q.day} ${q.text}`} className="readout-quote">
                  “{q.text}” <span className="readout-day">Reported day {q.day}</span>
                </span>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export function CrewList({ mission, dayIndex, crewId, onSelect }: {
  mission: Mission; dayIndex: number; crewId: string; onSelect: (id: string) => void;
}) {
  const dayNow = mission.days[dayIndex];
  return (
    <div className="crew" role="group" aria-label="Crew">
      {mission.crew.map((m) => {
        // A single noisy day should not turn a name red: status follows Space-Normal's own
        // alerts (shown for ALERT_DAYS after they fire), then the crew layer, then logged events.
        const sys = m.systems[dayIndex];
        const alerts = mission.alerts.filter((a) => a.detector === "space_normal" && a.level === "red"
          && a.crew_id === m.id && a.day <= dayNow && dayNow - a.day <= ALERT_DAYS);
        const inOutbreak = mission.crew_alerts.some((c) => c.day <= dayNow && c.crew_ids.includes(m.id));
        const flagged: State = inOutbreak ? "crew" : "unexplained";
        const systemState = (name: System): State =>
          alerts.length && (alerts.some((a) => SYSTEM_OF[a.vital] === name) || sys[name] === "unexplained" || sys[name] === "crew")
            ? flagged : sys[name] === "event" ? "event" : "expected";
        const parts = { cardio: systemState("cardio"), resp: systemState("resp"), thermo: systemState("thermo") };
        const states = Object.values(parts);
        const state: State = alerts.length ? flagged : states.includes("event") ? "event" : "expected";
        const selected = m.id === crewId;

        if (!selected) {
          return (
            <button key={m.id} className={`crew-row state-${state}`} onClick={() => onSelect(m.id)} aria-pressed={false}>
              <span className="crew-mark" aria-hidden="true">{ICON[state]}</span>
              <span className="crew-name">{m.name}</span>
              <span className="crew-state">{SHORT[state]}</span>
            </button>
          );
        }
        return <CrewCard key={m.id} name={m.name} state={state} parts={parts}
          reports={activeReports(mission.journal, m.id, dayNow)} />;
      })}
    </div>
  );
}
