import type { BodyRegion, JournalEntry, State } from "../contract";

export type System = "cardio" | "thermo";

/** A self-reported pain or symptom stays fully lit this many days after the journal entry... */
export const PAIN_VISIBLE_DAYS = 4;
/** ...then fades over this many more days before it disappears. */
export const PAIN_FADE_DAYS = 2;

export interface PainReport {
  entry: JournalEntry;
  /** 1 while fresh, falling towards 0 during the fade-out days. */
  strength: number;
}

/** Journal entries about a body area that this crew member has written by `dayNow` and that are still recent. */
export function activeReports(journal: JournalEntry[], crewId: string, dayNow: number): PainReport[] {
  return journal
    .filter((j) => j.region !== null && j.crew_ids.includes(crewId) && j.day <= dayNow
      && dayNow - j.day <= PAIN_VISIBLE_DAYS + PAIN_FADE_DAYS)
    .map((entry) => {
      const late = dayNow - entry.day - PAIN_VISIBLE_DAYS;
      return { entry, strength: late <= 0 ? 1 : 1 - late / (PAIN_FADE_DAYS + 1) };
    });
}

const SYSTEM_NAME: Record<System, string> = { cardio: "Heart", thermo: "Body temperature" };
const STATE_WORD: Record<State, string> = {
  expected: "as expected", event: "explained by a logged event", unexplained: "unexplained change",
  crew: "crew-wide drift", not_monitored: "not monitored",
};

const SINGULAR: Partial<Record<BodyRegion, string>> = {
  shoulders: "shoulder", upper_arms: "upper arm", forearms: "forearm", hands: "hand",
  thighs: "thigh", knees: "knee", calves: "calf", feet: "foot",
};
const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

function regionLabel(region: BodyRegion, side: JournalEntry["side"]): string {
  const plural = region.replace("_", " ");
  const one = SINGULAR[region];
  if (!one) return cap(plural);
  if (side === "left" || side === "right") return `${cap(side)} ${one}`;
  return side === "both" ? `Both ${plural}` : cap(plural);
}

type ShapeSide = "left" | "right" | "mid";
interface Shape { id: string; region: BodyRegion; side: ShapeSide }

const W = 132; // viewBox width; the figure is symmetric about x = W / 2
const H = 260;

/**
 * Original stylised front view, drawn as separate plates. Paired plates are drawn once for the
 * person's right side (the viewer's left, as on a medical chart) and mirrored for the left.
 * `at` is where the report marker sits.
 */
const MID: { region: BodyRegion; d: string; at: [number, number] }[] = [
  { region: "head", at: [66, 17], d: "M66,3 C75,3 79,10 79,18 C79,27 73,35 66,35 C59,35 53,27 53,18 C53,10 57,3 66,3 Z" },
  { region: "neck", at: [66, 42.2], d: "M60.5,37.6 H71.5 L73.6,47 H58.4 Z" },
  { region: "chest", at: [66, 55], d: "M48,49.5 H84 C89,53 92.5,60 93,70 L91.5,97 H40.5 L39,70 C39.500,60 43,53 48,49.5 Z" },
  { region: "abdomen", at: [66, 133], d: "M40.8,99.5 H91.2 L90.5,112 C90.5,122 92,130 94,137 L68.5,149 H63.5 L38,137 C40,130 41.5,122 41.5,112 Z" },
];
const PAIRED: { region: BodyRegion; d: string; at: [number, number] }[] = [
  { region: "shoulders", at: [32.5, 60], d: "M45,49.300 C35,49 27,55 25.2,67 L24.5,72 L36.3,69 C37,61 40,54.5 45,49.300 Z" },
  { region: "upper_arms", at: [29, 90], d: "M24,74.600 L36.4,71.600 C37,82 36,95 34,106.5 L21,108.5 C21,97 22,85 24,74.600 Z" },
  { region: "forearms", at: [24.5, 128], d: "M20.6,111 L33.6,109 C33,122 29,136 25,147 L15.5,145 C16,133 18,121 20.6,111 Z" },
  { region: "hands", at: [17, 160], d: "M14.8,147.600 L24.3,149.600 C24.5,157 22,166 17.5,170.5 C13,172 9.500,168 10.5,161 C11,156 13,151 14.8,147.600 Z" },
  { region: "thighs", at: [50, 168], d: "M37,140.5 L63.8,153 C64,165 62,178 60.5,188 H40 C37.5,175 35.5,158 37,140.5 Z" },
  { region: "knees", at: [50.3, 196.800], d: "M40.3,190.5 H60.2 C60,195 59.5,199 58.8,203 H42 C41,199 40.5,195 40.3,190.5 Z" },
  { region: "calves", at: [50, 221], d: "M42.3,205.5 H58.5 C59.5,215 57.5,228 55.5,240 H46 C42,229 40.5,216 42.3,205.5 Z" },
  { region: "feet", at: [48.5, 250], d: "M45.5,242.5 H55.8 L56.5,250 C56.5,254 54,256 50,256 H41 C37,256 37,251 41,249.5 L45,247.5 Z" },
];
/** "back" has no front-view plate: it is the spine, a column of vertebrae down the midline. */
const SPINE_Y = [52, 60.5, 69, 77.5, 86, 94.5, 103, 111.5, 120, 128.5, 137];
const SPINE_AT: [number, number] = [66, 114];

/** The only organ drawn: pulse is the one organ-level sign on screen. Sits on the person's left of the spine. */
const HEART = "M71.5,68.5 c3.6,-5.4 13.2,-2.4 11.4,5.4 c-1.44,6 -11.4,12 -11.4,12 s-9.96,-6 -11.4,-12 c-1.8,-7.8 7.8,-10.8 11.4,-5.4 z";
const MIRROR = `matrix(-1 0 0 1 ${W} 0)`;

const covering = (shape: Shape, reports: PainReport[]) =>
  reports.filter(({ entry }) => entry.region === shape.region
    && (shape.side === "mid" || entry.side === null || entry.side === "both" || entry.side === shape.side));

const tipText = (reports: PainReport[]) =>
  reports.map(({ entry }) => `${regionLabel(entry.region!, entry.side)}: "${entry.text}" reported day ${entry.day}`).join("\n");

export interface Readout { title: string; state?: State; quotes: { text: string; day: number }[] }

/** What the hovered or focused part of the figure means, for the card's readout. */
export function describe(key: string | null, parts: Record<System, State>, reports: PainReport[]): Readout | null {
  if (!key) return null;
  if (key.startsWith("sys:")) {
    const name = key.slice(4) as System;
    return { title: `${SYSTEM_NAME[name]}: ${STATE_WORD[parts[name]]}`, state: parts[name], quotes: [] };
  }
  const [region, side] = key.split(":") as [BodyRegion, ShapeSide];
  const hits = covering({ id: key, region, side }, reports);
  if (!hits.length) return null;
  const newest = hits[hits.length - 1].entry;
  return { title: regionLabel(newest.region!, newest.side), quotes: hits.map(({ entry }) => ({ text: entry.text, day: entry.day })) };
}

/**
 * Body map. Detector states: plate outlines and glow = body temperature, heart = pulse.
 * Self-reports from the crew journal: dotted pale plate with a ringed dot, never the alarm colour.
 */
export function BodyFigure({ parts, reports, onInspect }: {
  parts: Record<System, State>; reports: PainReport[]; onInspect: (key: string | null) => void;
}) {
  const { cardio, thermo } = parts;
  const watch = (key: string) => ({ onMouseEnter: () => onInspect(key), onMouseLeave: () => onInspect(null) });
  const sysTip = (name: System) => `${SYSTEM_NAME[name]}: ${STATE_WORD[parts[name]]}`;
  const markers: { key: string; x: number; y: number; strength: number }[] = [];

  /** One plate (or the spine). With a current report it becomes a focusable, dotted, pale shape. */
  const plate = (shape: Shape, at: [number, number], mirrored: boolean, draw: (cls: string) => JSX.Element) => {
    const hits = covering(shape, reports);
    if (!hits.length) return <g key={shape.id} {...watch("sys:thermo")}>{draw("")}</g>;
    const strength = Math.max(...hits.map((h) => h.strength));
    markers.push({ key: shape.id, x: mirrored ? W - at[0] : at[0], y: at[1], strength });
    const tip = tipText(hits);
    return (
      <g key={shape.id} className="region" tabIndex={0} role="img" aria-label={tip} {...watch(shape.id)}
        onFocus={() => onInspect(shape.id)} onBlur={() => onInspect(null)}>
        <title>{tip}</title>
        {draw("")}
        <g style={{ opacity: strength }}>{draw("reported")}</g>
      </g>
    );
  };
  const path = (d: string) => (cls: string) => <path className={`plate ${cls}`} d={d} />;
  const spine = (cls: string) => (
    <g className={`spine ${cls}`}>
      {/* wide transparent strip so the thin spine is easy to point at */}
      <rect x={61} y={50} width={10} height={95} fill="transparent" stroke="none" />
      {SPINE_Y.map((y) => <rect key={y} className="vertebra" x={63.2} y={y} width={5.6} height={5.4} rx={1.6} />)}
    </g>
  );

  const summary = [
    ...(["cardio", "thermo"] as System[]).map(sysTip),
    ...reports.map((r) => tipText([r])),
  ].join(". ");

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="body" role="group" aria-label={`Body map. ${summary}`}>
      <defs>
        <radialGradient id="bf-glow" cx="50%" cy="40%" r="55%">
          <stop offset="0" stopColor="currentColor" stopOpacity="0.36" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0" />
        </radialGradient>
        <pattern id="bf-dots" width="5" height="5" patternUnits="userSpaceOnUse">
          <rect width="5" height="5" className="pat-report-bg" />
          <circle cx="1.25" cy="1.25" r="0.95" className="pat-report" />
          <circle cx="3.75" cy="3.75" r="0.95" className="pat-report" />
        </pattern>
        <pattern id="bf-hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="4" height="4" className="pat-event-bg" />
          <rect width="1.7" height="4" className="pat-event" />
        </pattern>
        <pattern id="bf-stripes" width="4" height="4" patternUnits="userSpaceOnUse">
          <rect width="4" height="4" className="pat-crew-bg" />
          <rect width="4" height="1.9" className="pat-crew" />
        </pattern>
      </defs>

      <g className={`sys sys-${thermo}`}>
        <title>{sysTip("thermo")}</title>
        <ellipse className="glow" cx={W / 2} cy={112} rx={W / 2} ry={122} fill="url(#bf-glow)" />
        {MID.map((s) => plate({ id: `${s.region}:mid`, region: s.region, side: "mid" }, s.at, false, path(s.d)))}
        <g>
          {PAIRED.map((s) => plate({ id: `${s.region}:right`, region: s.region, side: "right" }, s.at, false, path(s.d)))}
        </g>
        <g transform={MIRROR}>
          {PAIRED.map((s) => plate({ id: `${s.region}:left`, region: s.region, side: "left" }, s.at, true, path(s.d)))}
        </g>
        {plate({ id: "back:mid", region: "back", side: "mid" }, SPINE_AT, false, spine)}
      </g>

      <g className={`sys sys-${cardio}`} {...watch("sys:cardio")}>
        <title>{sysTip("cardio")}</title>
        <circle className="halo" cx={71.5} cy={75.5} r={15.5} />
        <path className="organ heart" d={HEART} />
      </g>

      <g className="markers" aria-hidden="true">
        {markers.map((m) => (
          <g key={m.key} style={{ opacity: m.strength }}>
            <circle className="marker-ring" cx={m.x} cy={m.y} r={6.4} />
            <circle className="marker-dot" cx={m.x} cy={m.y} r={3.3} />
          </g>
        ))}
      </g>
    </svg>
  );
}
