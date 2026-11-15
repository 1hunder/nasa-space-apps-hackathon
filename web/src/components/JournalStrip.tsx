import type { CrewMember, Mission } from "../contract";

/** The crew journal as one readable entry at a time: the crew member's own words, then how it was read. */
export function JournalStrip({ mission, member, dayNow, index, onIndex }: {
  mission: Mission; member: CrewMember; dayNow: number; index: number; onIndex: (i: number) => void;
}) {
  const entries = mission.journal.filter((j) => j.crew_ids.includes(member.id) && j.day <= dayNow);
  if (!entries.length) {
    return (
      <section className="journal journal-empty">
        <h3>Crew journal</h3>
        <p>No entries yet. Notes written by the crew appear here as the mission goes on.</p>
      </section>
    );
  }
  const k = index >= 0 && index < entries.length ? index : entries.length - 1;
  const j = entries[k];
  const who = j.crew_ids.length > 1 ? "whole crew" : member.name.split(" ")[0];
  return (
    <section className="journal">
      <div className="journal-head">
        <h3>Crew journal</h3>
        <p className="journal-when">Day {j.day}, {String(j.hour).padStart(2, "0")}:00, {who}</p>
        <div className="journal-nav">
          <button type="button" onClick={() => onIndex(k - 1)} disabled={k === 0} aria-label="Earlier entry">‹</button>
          <span>{k + 1} of {entries.length}</span>
          <button type="button" onClick={() => onIndex(k + 1)} disabled={k === entries.length - 1} aria-label="Later entry">›</button>
        </div>
      </div>
      <p className="journal-quote">“{j.text}”</p>
      <p className="journal-read">
        <span className={j.accounted ? "journal-tag is-accounted" : "journal-tag"}>{j.category}</span>
        {j.effect}
        <span className="journal-mock">Reading mocked in this demo.</span>
      </p>
    </section>
  );
}
