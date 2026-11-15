import type { Alert, Mission, Vital } from "../contract";
import { DEMO_VITALS, DIGITS, VITAL_LABEL, fixed, signed } from "../labels";

/** The astronaut's card: what we see, what to check now, when to escalate. Never a diagnosis. */
export function AlertPanel({ mission, alert, viewing }: { mission: Mission; alert: Alert | null; viewing: Vital }) {
  if (!alert) {
    return <p className="quiet"><span aria-hidden="true">✓</span> No unexplained change so far. No action needed today.</p>;
  }

  const member = mission.crew.find((c) => c.id === alert.crew_id)!;
  const i = mission.days.indexOf(alert.day);
  // Explain the vital on screen when it is also clearly off that day; otherwise the one that led the alert.
  // Only vitals the demo shows are ever explained; an alert led by any other falls back to temperature.
  const shown = (v: Vital) => DEMO_VITALS.includes(v);
  const led: Vital = shown(alert.vital) ? alert.vital : "temp_c";
  const vital = shown(viewing) && (member.vitals[viewing].z[i] ?? 0) > 2 ? viewing : led;
  const s = member.vitals[vital];
  const { name, unit } = VITAL_LABEL[vital];
  const dg = DIGITS[vital];
  const note = mission.notes[alert.id];
  const episode = mission.episodes.find((e) => e.crew_id === alert.crew_id);
  const lead = episode ? episode.onset_day - alert.day : null;
  const firstName = member.name.split(" ")[0];
  const rows: [string, string, string][] = [
    ["Pre-flight baseline", fixed(s.baseline[i], dg), ""],
    ["Expected adaptation", signed(s.adaptation[i], dg), "row-adapt"],
    ["Logged events", signed(s.events[i], dg), "row-event"],
    ["Unexplained", signed(s.residual[i] ?? 0, dg), "row-unexplained"],
  ];

  return (
    <section className="alert" key={alert.id} aria-live="polite">
      <p className="alert-kicker">Card for {firstName}, day {alert.day}</p>

      <h3 className="step">OBSERVATION</h3>
      <p className="step-text">
        {name} is <strong>{fixed(s.residual[i] ?? 0, dg)} {unit}</strong> above what is expected for you today.
        No logged event explains it.
      </p>

      <h3 className="step">CHECK NOW</h3>
      <p className="step-text">
        Repeat the reading at rest{note ? `, then answer ${note.questions.length} questions (about 1 minute).` : "."}
      </p>
      {note && (
        <details className="questions">
          <summary>Show the questions</summary>
          <ol className="step-list">{note.questions.map((q) => <li key={q}>{q}</li>)}</ol>
        </details>
      )}

      <h3 className="step">ESCALATE IF</h3>
      <p className="step-text">
        Still outside your range tomorrow, or a medical limit is crossed
        <span className="assumption"> (limits are placeholders)</span>.
        {note && <> Handover note ready, {note.bytes} bytes.</>}
      </p>

      <p className="not-dx">Not a diagnosis.</p>

      <details>
        <summary>Numbers and handover note</summary>
        <div className="sum">
          <div className="sum-total">
            <span>Daily mean</span>
            <strong>{fixed(s.y[i] ?? 0, dg)} <small>{unit}</small></strong>
          </div>
          {rows.map(([label, value, cls]) => (
            <div key={label} className={`sum-row ${cls}`}>
              <span>{label}</span><span className="num">{value}</span>
            </div>
          ))}
        </div>
        {lead !== null && lead > 0 && (
          <p className="lead">In this simulation the illness was planted: flagged {lead} {lead === 1 ? "day" : "days"} before its symptoms start.</p>
        )}
        {note && (
          <>
            <h3 className="handover-title">Handover note</h3>
            <p className="handover-sub">for the flight surgeon or a diagnostic assistant</p>
            <p className="note">{note.text.split("\n")[0]}</p>
            <p className="chips">
              <span className="chip">{note.numbers_verified ? "Numbers verified against data" : "Numbers not verified"}</span>
              <span className="chip">{note.bytes} bytes to downlink</span>
            </p>
            <p className="note muted">The detector alone raises and grades alerts. The assistant only words the note; it cannot raise, delay or lower an alert.</p>
            {note.context_items.length > 0 && (
              <>
                <h3>Possible contributors, unverified</h3>
                <ul>{note.context_items.map((c) => <li key={c.source_ref}>{c.text}</li>)}</ul>
              </>
            )}
          </>
        )}
      </details>
    </section>
  );
}
