import type { Mission, State, Vital } from "../contract";

const ALERT_DAYS = 10; // how long a Space-Normal alert keeps a crew member marked
type System = "cardio" | "resp" | "thermo";
const SYSTEM_OF: Record<Vital, System> = { pulse: "cardio", sbp: "cardio", dbp: "cardio", resp_rate: "resp", temp_c: "thermo" };
const SYSTEMS: [System, string][] = [["cardio", "Heart"], ["resp", "Lungs"], ["thermo", "Temperature"]];

const SHORT: Record<State, string> = {
  expected: "As expected",
  event: "Explained by a logged event",
  unexplained: "Unexplained change",
  crew: "Crew-wide drift",
  not_monitored: "Not monitored",
};
const WORD: Record<State, string> = {
  expected: "as expected", event: "logged event", unexplained: "unexplained", crew: "crew-wide", not_monitored: "not monitored",
};
const ICON: Record<State, string> = { expected: "✓", event: "◆", unexplained: "!", crew: "≋", not_monitored: "–" };

/** Original front-view figure. Outline and glow = body temperature, lobes = lungs, heart = circulation. */
function BodyFigure({ cardio, resp, thermo }: Record<System, State>) {
  return (
    <svg viewBox="0 0 120 222" className="body" aria-hidden="true">
      <defs>
        <radialGradient id="body-glow" cx="50%" cy="42%" r="55%">
          <stop offset="0" stopColor="currentColor" stopOpacity="0.34" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0" />
        </radialGradient>
        <linearGradient id="body-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="currentColor" stopOpacity="0.22" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0.03" />
        </linearGradient>
      </defs>
      <g className={`sys sys-${thermo}`}>
        <ellipse cx="60" cy="96" rx="60" ry="100" fill="url(#body-glow)" />
        <circle cx="60" cy="21" r="15" className="outline" />
        <path className="outline" d="M53,37 C53,45 42,46 32,49 C21,52 16,62 15,76 L11,120 C10,129 21,131 23,122 L29,86 L30,118
          C29,130 30,140 31,150 L35,203 C36,213 49,213 49,203 L55,152 C56,147 58,146 60,146 C62,146 64,147 65,152 L71,203
          C71,213 84,213 85,203 L89,150 C90,140 91,130 90,118 L91,86 L97,122 C99,131 110,129 109,120 L105,76
          C104,62 99,52 88,49 C78,46 67,45 67,37 Z" />
      </g>
      <g className={`sys sys-${resp}`}>
        <path className="organ" d="M56,60 C47,60 40,70 40,84 L40,97 C40,102 45,103 49,100 L56,94 Z" />
        <path className="organ" d="M64,60 C73,60 80,70 80,84 L80,97 C80,102 75,103 71,100 L64,94 Z" />
      </g>
      <g className={`sys sys-${cardio}`}>
        <path className="organ heart" d="M65,75 c3,-4.500 11,-2 9.500,4.500 c-1.200,5 -9.500,10 -9.500,10 s-8.300,-5 -9.500,-10 c-1.500,-6.500 6.500,-9 9.500,-4.500 z" />
      </g>
    </svg>
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
        return (
          <div key={m.id} className={`crew-card state-${state}`} aria-current="true">
            <BodyFigure {...parts} />
            <div className="crew-card-text">
              <span className="crew-name">{m.name}</span>
              <span className="crew-state">{SHORT[state]}</span>
              <ul className="systems">
                {SYSTEMS.map(([key, label]) => (
                  <li key={key} className={`part part-${parts[key]}`}>
                    <span className="part-dot" aria-hidden="true" />
                    <span className="part-name">{label}</span>
                    <span className="part-state">{WORD[parts[key]]}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        );
      })}
    </div>
  );
}
