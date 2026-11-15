import { DETECTORS, type Detector, type Mission } from "../contract";
import { DETECTOR_LABEL } from "../labels";

// Our own method first, then the ones it is compared with.
const ORDER: Detector[] = ["space_normal", "frozen_baseline", "fixed_thresholds", "rolling_14"];
const NOISY = 3; // with this many false alarms, a matching alarm cannot be told apart from the rest
const WINDOW_DAYS = 3; // a method has missed an illness once this many days have passed since symptoms began

/** An expandable list, one row per way of judging the readings: how often it cried wolf, and whether it caught the illness. */
export function MethodCards({ mission, dayNow }: { mission: Mission; dayNow: number }) {
  const first = mission.days[0];
  const span = mission.days[mission.days.length - 1] - first;
  const pct = (day: number) => `${((day - first) / span) * 100}%`;
  const started = mission.episodes.filter((e) => e.onset_day <= dayNow);
  const closed = new Set(mission.episodes.filter((e) => e.onset_day + WINDOW_DAYS < dayNow).map((e) => e.crew_id));

  return (
    <details className="methods">
      <summary>
        <span className="methods-title">Compare monitoring methods</span>
        <span className="methods-sub">false alarms and missed illness so far, for {ORDER.length} ways of judging the same readings</span>
      </summary>
      <ul className="method-list">
      {ORDER.filter((d) => (DETECTORS as readonly string[]).includes(d)).map((det) => {
        const seen = mission.alerts.filter((a) => a.level === "red" && a.detector === det && a.day <= dayNow);
        const falseAlarms = seen.filter((a) => a.truth === "false_alarm");
        const hits = seen.filter((a) => a.truth === "hit");
        const caught = new Set(hits.map((a) => a.crew_id));
        const known = new Set([...started.map((e) => e.crew_id), ...caught]);
        const pending = started.some((e) => !caught.has(e.crew_id) && !closed.has(e.crew_id));
        // Days between this method's first matching alert and the start of symptoms, for a single illness.
        const episode = mission.episodes.length === 1 ? mission.episodes[0] : null;
        const firstHit = episode ? hits.filter((a) => a.crew_id === episode.crew_id).sort((a, b) => a.day - b.day)[0] : undefined;
        const lead = episode && firstHit ? episode.onset_day - firstHit.day : 0;

        let verdict: { tone: "none" | "good" | "wait" | "bad"; icon: string; text: string };
        if (known.size === 0) verdict = { tone: "none", icon: "–", text: "No illness so far" };
        else if (known.size > 1) verdict = { tone: caught.size === known.size ? "good" : caught.size ? "wait" : "bad",
          icon: caught.size ? "✓" : "✕", text: `Caught ${caught.size} of ${known.size} illnesses` };
        // An alarm near the illness is no use if it looks like all the false ones around it.
        else if (caught.size && falseAlarms.length >= NOISY) verdict = { tone: "wait", icon: "?",
          text: `Illness alarm lost among ${falseAlarms.length} false ones` };
        else if (caught.size) verdict = { tone: "good", icon: "✓",
          text: lead > 0 ? `Caught ${lead} ${lead === 1 ? "day" : "days"} before symptoms` : "Caught the illness" };
        else if (pending) verdict = { tone: "wait", icon: "…", text: "Illness not flagged yet" };
        else verdict = { tone: "bad", icon: "✕", text: "Missed the illness" };

        return (
          <li key={det} className={det === "space_normal" ? "method method-ours" : "method"}>
            <div className="method-name">
              <h3>{DETECTOR_LABEL[det].name}</h3>
              <p className="method-how">{DETECTOR_LABEL[det].how}</p>
            </div>
            <p className={falseAlarms.length ? "method-count is-bad" : "method-count is-good"}>
              <strong>{falseAlarms.length}</strong> false {falseAlarms.length === 1 ? "alarm" : "alarms"}
            </p>
            <div className="method-strip" aria-hidden="true">
              <span className="strip-done" style={{ width: pct(dayNow) }} />
              {seen.map((a) => (
                <span key={a.id} className={a.truth === "hit" ? "strip-hit" : a.truth === "false_alarm" ? "strip-false" : "strip-near"}
                  style={{ left: pct(a.day) }} />
              ))}
            </div>
            <p className={`method-verdict tone-${verdict.tone}`}>
              <span className="verdict-icon" aria-hidden="true">{verdict.icon}</span>{verdict.text}
            </p>
          </li>
        );
      })}
      </ul>
    </details>
  );
}
