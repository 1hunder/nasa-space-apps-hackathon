import type { Alert, Mission, Vital } from "../contract";
import { DIGITS, VITAL_LABEL, fixed, signed } from "../labels";

export function AlertPanel({ mission, alert, viewing }: { mission: Mission; alert: Alert | null; viewing: Vital }) {
  if (!alert) {
    return <p className="quiet"><span aria-hidden="true">✓</span> No unexplained change so far.</p>;
  }

  const member = mission.crew.find((c) => c.id === alert.crew_id)!;
  const i = mission.days.indexOf(alert.day);
  // Explain the vital on screen when it is also clearly off that day; otherwise the one that led the alert.
  const vital = (member.vitals[viewing].z[i] ?? 0) > 2 ? viewing : alert.vital;
  const s = member.vitals[vital];
  const { name, unit } = VITAL_LABEL[vital];
  const dg = DIGITS[vital];
  const note = mission.notes[alert.id];
  const episode = mission.episodes.find((e) => e.crew_id === alert.crew_id);
  const lead = episode ? episode.onset_day - alert.day : null;
  const rows: [string, string, string][] = [
    ["Earth baseline", fixed(s.baseline[i], dg), ""],
    ["Expected adaptation", signed(s.adaptation[i], dg), "row-adapt"],
    ["Logged events", signed(s.events[i], dg), "row-event"],
    ["Unexplained", signed(s.residual[i] ?? 0, dg), "row-unexplained"],
  ];

  return (
    <section className="alert" key={alert.id} aria-live="polite">
      <p className="alert-kicker">Day {alert.day}</p>
      <h2>{member.name}: unexplained rise in {name.toLowerCase()}</h2>

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
        <p className="lead">Flagged {lead} {lead === 1 ? "day" : "days"} before symptoms start.</p>
      )}

      {note && (
        <details>
          <summary>Note for the flight surgeon</summary>
          <p className="note">{note.text.split("\n")[0]}</p>
          <p className="chips">
            <span className="chip">{note.numbers_verified ? "Numbers verified against data" : "Numbers not verified"}</span>
            <span className="chip">{note.bytes} bytes to downlink</span>
          </p>
          <p className="note muted">The detector sets the severity. The assistant can add context or escalate, never lower an alert.</p>
          {note.context_items.length > 0 && (
            <>
              <h3>Possible contributors, unverified</h3>
              <ul>{note.context_items.map((c) => <li key={c.source_ref}>{c.text}</li>)}</ul>
            </>
          )}
          <h3>Ask the crew member</h3>
          <ol>{note.questions.map((q) => <li key={q}>{q}</li>)}</ol>
        </details>
      )}
    </section>
  );
}
