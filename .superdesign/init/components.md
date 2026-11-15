# Components

Framework: React 18 + Vite + TypeScript. No component library; hand-written SVG and plain CSS (`web/src/styles.css`). There are no shared UI primitives (buttons and the two-option vital control are plain elements styled in styles.css). The four feature components below make up the whole screen.

- `Figure` — the chart: Earth-normal limit, flat pre-flight range, moving Space-Normal range, hourly readings and daily means, crew journal row, monitor lanes, click-to-inspect cards.
- `CrewList` — crew column; the selected member opens into a card with `BodyFigure`.
- `BodyFigure` — segmented front-view body with heart, temperature outline and self-reported pain regions.
- `AlertPanel` — the astronaut card: OBSERVATION / CHECK NOW / ESCALATE IF / Not a diagnosis.

### `web/src/components/Figure.tsx`

```tsx
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { DETECTORS, type CrewMember, type Detector, type Mission, type Vital } from "../contract";
import { DETECTOR_LABEL, DIGITS, EVENT_LABEL, VITAL_LABEL, fixed, signed } from "../labels";

interface Props {
  mission: Mission;
  member: CrewMember;
  vital: Vital;
  day: number;
  dayIndex: number;
  detail: boolean;
  reserve: number; // vertical space taken by a banner above the chart
  onScrub: (day: number) => void;
}

// Every row shares one day axis, so a single playhead reads across all of them.
const GUTTER_L = 44;
const GUTTER_R = 172;
const CHART_TOP = 26;
const DECOMP_H = 64;
const LANE_H = 46;
const SIMPLE_LANES: Detector[] = ["fixed_thresholds", "frozen_baseline", "space_normal"];
// A Space-Normal red alert counts as active from its day until this many days after it,
// and for as long after that as the reading stays above the range without a break.
const ALERT_ACTIVE_DAYS = 3;

function useWidth(): [React.RefObject<HTMLDivElement>, number] {
  const ref = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(1000);
  useLayoutEffect(() => {
    if (!ref.current) return;
    setWidth(ref.current.getBoundingClientRect().width);
    const obs = new ResizeObserver(([entry]) => setWidth(entry.contentRect.width));
    obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);
  return [ref, width];
}

function niceTicks(lo: number, hi: number, target = 4): number[] {
  const raw = (hi - lo) / target;
  const pow = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1, 2, 5, 10].map((m) => m * pow).find((s) => s >= raw) ?? raw;
  const out: number[] = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(Number(v.toFixed(6)));
  return out;
}

/** Closed area between two series over runs of consecutive days where `keep` is true. */
function areaRuns(n: number, keep: (i: number) => boolean, upper: (i: number) => string, lower: (i: number) => string): string {
  const out: string[] = [];
  let run: number[] = [];
  const flush = () => {
    if (run.length) out.push(`M${run.map(upper).join("L")}L${run.map(lower).reverse().join("L")}Z`);
    run = [];
  };
  for (let i = 0; i < n; i++) { if (keep(i)) run.push(i); else flush(); }
  flush();
  return out.join("");
}

export function Figure({ mission, member, vital, day, dayIndex, detail, reserve, onScrub }: Props) {
  const [ref, width] = useWidth();
  const [picked, setPicked] = useState<number | null>(null); // index of the day whose point was clicked
  const press = useRef<{ x: number; dragged: boolean } | null>(null);
  const [note, setNote] = useState<number | null>(null); // index into the visible journal entries
  useEffect(() => { setPicked(null); setNote(null); }, [mission, member.id, vital]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") { setPicked(null); setNote(null); } };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
  const s = member.vitals[vital];
  const days = mission.days;
  const n = days.length;
  // The chart takes the height the window can spare; detail rows trade some of it away.
  const spare = Math.max(380, Math.min(640, window.innerHeight - 430 - reserve));
  const chartBottom = detail ? Math.max(260, spare - 190) : spare;
  const plotW = Math.max(240, width - GUTTER_L - GUTTER_R);
  const right = GUTTER_L + plotW;
  const x = (d: number) => GUTTER_L + ((d - days[0]) / (days[n - 1] - days[0])) * plotW;
  const playX = x(day);
  const barW = Math.max(2, (plotW / (n - 1)) * 0.66);

  const [yLo, yHi] = useMemo(() => {
    const values = [...s.band_low, ...s.band_high, ...s.earth_low, ...s.earth_high,
      ...(s.y.filter((v) => v !== null) as number[])];
    // Show the Earth-normal limit when it is close enough to matter for this vital.
    const span = Math.max(...values) - Math.min(...values);
    for (const limit of [s.fixed_low, s.fixed_high]) {
      if (limit !== null && limit > Math.min(...values) - span * 0.25 && limit < Math.max(...values) + span * 0.25) values.push(limit);
    }
    // Hourly readings scatter wider than daily means; let the extremes clip rather than flatten the chart.
    const hourly = (s.y_hourly.filter((v) => v !== null) as number[]).sort((a, b) => a - b);
    if (hourly.length) values.push(hourly[Math.floor(hourly.length * 0.01)], hourly[Math.floor(hourly.length * 0.99)]);
    const lo = Math.min(...values), hi = Math.max(...values);
    const pad = (hi - lo) * 0.07;
    return [lo - pad, hi + pad];
  }, [s]);
  const y = (v: number) => CHART_TOP + (1 - (v - yLo) / (yHi - yLo)) * (chartBottom - CHART_TOP);

  const paths = useMemo(() => {
    const pt = (i: number, v: number) => `${x(days[i]).toFixed(1)},${y(v).toFixed(1)}`;
    // The range is baseline + expected adaptation. Logged events sit on top of it as an allowance.
    const top = (i: number) => s.band_high[i] - s.events[i];
    const bottom = (i: number) => s.band_low[i] - s.events[i];
    const sigma = (i: number) => (s.band_high[i] - s.band_low[i]) / 4;
    let trace = "", pen = false;
    for (let i = 0; i < n; i++) {
      const v = s.y[i];
      if (v === null) { pen = false; continue; }
      trace += `${pen ? "L" : "M"}${pt(i, v)}`;
      pen = true;
    }
    // Hourly readings sit behind the daily means: day d's 24 readings span d-0.5 .. d+0.5.
    const spd = mission.samples_per_day;
    let hourly = "";
    if (spd > 1) {
      pen = false;
      s.y_hourly.forEach((v, i) => {
        if (v === null) { pen = false; return; }
        const tDay = days[0] + Math.floor(i / spd) - 0.5 + ((i % spd) + 0.5) / spd;
        hourly += `${pen ? "L" : "M"}${x(Math.max(days[0], tDay)).toFixed(1)},${y(v).toFixed(1)}`;
        pen = true;
      });
    }
    return {
      hourly,
      corridor: areaRuns(n, () => true, (i) => pt(i, top(i)), (i) => pt(i, bottom(i))),
      allowance: areaRuns(n, (i) => s.events[i] > 0.5 * sigma(i), (i) => pt(i, s.band_high[i]), (i) => pt(i, top(i))),
      excess: areaRuns(n, (i) => s.y[i] !== null && (s.y[i] as number) > s.band_high[i],
        (i) => pt(i, s.y[i] as number), (i) => pt(i, s.band_high[i])),
      trace,
    };
  }, [s, plotW, yLo, yHi, chartBottom, mission]);

  const earthTop = y(s.earth_high[0]), earthBottom = y(s.earth_low[0]);
  const { name } = VITAL_LABEL[vital];
  const dayNow = days[dayIndex];
  const episodes = mission.episodes.filter((e) => e.crew_id === member.id && e.onset_day <= dayNow);
  const snAlerts = mission.alerts.filter(
    (a) => a.detector === "space_normal" && a.level === "red" && a.crew_id === member.id && a.day <= dayNow);
  const rangeTopNow = y(s.band_high[dayIndex] - s.events[dayIndex]);
  const earthLabelY = (earthTop + earthBottom) / 2;
  const spaceLabelY = Math.min(rangeTopNow + 4, earthLabelY - 48); // keep the two labels apart early on

  const majors = mission.events.filter((e) => e.type !== "exercise" && e.day <= dayNow);
  const firstMajor = majors[0];

  // Optional detail rows.
  // Crew journal: free-text entries for this crew member (and whole-crew ones), revealed as days pass.
  const journalTitle = chartBottom + 40;
  const journalY = journalTitle + 17;
  const entries = mission.journal.filter((j) => j.crew_ids.includes(member.id) && j.day <= dayNow);
  const entryX = (j: { day: number; hour: number }) => x(Math.max(days[0], j.day - 0.5 + (j.hour + 0.5) / 24));

  const decompTitle = journalY + 38;
  const decompTop = decompTitle + 10;
  const dMax = useMemo(() => {
    let up = 1e-9, down = 1e-9;
    for (let i = 0; i < n; i++) {
      const parts = [s.adaptation[i], s.events[i], s.residual[i] ?? 0];
      up = Math.max(up, parts.filter((p) => p > 0).reduce((a, b) => a + b, 0));
      down = Math.max(down, -parts.filter((p) => p < 0).reduce((a, b) => a + b, 0));
    }
    return { up, down };
  }, [s]);
  const dScale = DECOMP_H / (dMax.up + dMax.down);
  const zeroY = decompTop + dMax.up * dScale;

  const lanes = detail ? [...DETECTORS] : SIMPLE_LANES;
  const lanesTop = detail ? decompTop + DECOMP_H + 14 : journalY + 18;
  const axisY = lanesTop + lanes.length * LANE_H + 4;
  const height = axisY + 26;
  const reds = mission.alerts.filter((a) => a.level === "red");
  // An illness is known once its symptoms have started. A monitor has missed it only when the
  // detection window (3 days past onset) has closed without a hit.
  const started = mission.episodes.filter((e) => e.onset_day <= dayNow).map((e) => e.crew_id);
  const closed = mission.episodes.filter((e) => e.onset_day + 3 < dayNow).map((e) => e.crew_id);

  const dayAt = (e: React.PointerEvent<SVGRectElement>) => {
    const box = e.currentTarget.getBoundingClientRect();
    return days[0] + ((e.clientX - box.left) / box.width) * (days[n - 1] - days[0]);
  };
  // A click picks the nearest revealed point; a drag scrubs the replay.
  const onDown = (e: React.PointerEvent<SVGRectElement>) => {
    e.currentTarget.setPointerCapture(e.pointerId);
    press.current = { x: e.clientX, dragged: false };
  };
  const onMove = (e: React.PointerEvent<SVGRectElement>) => {
    if (!press.current || !e.buttons) return;
    if (Math.abs(e.clientX - press.current.x) > 4) press.current.dragged = true;
    if (press.current.dragged) { setPicked(null); setNote(null); onScrub(dayAt(e)); }
  };
  const onUp = (e: React.PointerEvent<SVGRectElement>) => {
    const wasDrag = press.current?.dragged;
    press.current = null;
    if (wasDrag) return;
    const box = e.currentTarget.getBoundingClientRect();
    const localY = e.clientY - box.top + CHART_TOP;
    if (Math.abs(localY - journalY) <= 13) {
      // A click on the journal row opens the nearest entry.
      const px = e.clientX - box.left + GUTTER_L;
      let best = -1, dist = 14;
      entries.forEach((j, k) => { const d = Math.abs(entryX(j) - px); if (d < dist) { best = k; dist = d; } });
      setPicked(null);
      setNote(best >= 0 && best !== note ? best : null);
      return;
    }
    setNote(null);
    const i = Math.round(dayAt(e)) - days[0];
    setPicked(i >= 0 && i <= dayIndex && s.y[i] !== null && i !== picked ? i : null);
  };
  const tip = picked !== null && picked <= dayIndex && s.y[picked] !== null ? picked : null;
  const dg = DIGITS[vital];

  return (
    <div ref={ref} className="figure">
      <svg width={width} height={height} role="img"
        aria-label={`${name} for ${member.name} against the Earth-normal limit, the fixed pre-flight range and the moving Space-Normal range`}>
        <defs>
          <pattern id="earth-hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(40)">
            <rect width="7" height="7" fill="var(--earth-fill)" />
            <line x1="0" y1="0" x2="0" y2="7" stroke="var(--earth)" strokeWidth="1.3" opacity="0.42" />
          </pattern>
          <clipPath id="reveal"><rect x={0} y={0} width={playX} height={height} /></clipPath>
        </defs>

        {niceTicks(yLo, yHi).map((t) => (
          <g key={t}>
            <line x1={GUTTER_L} x2={right} y1={y(t)} y2={y(t)} className="grid" />
            <text x={GUTTER_L - 10} y={y(t) + 5} className="tick" textAnchor="end">{t}</text>
          </g>
        ))}

        {/* Earth normal: flat, fixed before launch */}
        <rect x={GUTTER_L} y={earthTop} width={plotW} height={earthBottom - earthTop} fill="url(#earth-hatch)" />
        <line x1={GUTTER_L} x2={right} y1={earthTop} y2={earthTop} className="earth-edge" />
        <line x1={GUTTER_L} x2={right} y1={earthBottom} y2={earthBottom} className="earth-edge" />
        <text x={right + 16} y={earthLabelY} className="band-label earth-text">Pre-flight range</text>
        <text x={right + 16} y={earthLabelY + 19} className="band-sub">personal, fixed at launch</text>
        {/* Earth normal: one limit for everyone */}
        {[s.fixed_high, s.fixed_low].map((limit, k) => limit !== null && limit > yLo && limit < yHi && (
          <g key={k}>
            <line x1={GUTTER_L} x2={right} y1={y(limit)} y2={y(limit)} className="fixed-limit" />
            <text x={GUTTER_L + 8} y={y(limit) + (k === 0 ? -7 : 17)} className="fixed-text">
              Earth normal {k === 0 ? "upper" : "lower"} limit, same for everyone
            </text>
          </g>
        ))}

        {/* Space-Normal: revealed as the mission runs */}
        <g clipPath="url(#reveal)">
          <path d={paths.corridor} className="corridor" />
          <path d={paths.allowance} className="allowance" />
          <path d={paths.hourly} className="hourly" />
          <path d={paths.excess} className="excess" />
          <path d={paths.trace} className="trace" />
          {days.map((d, i) => {
            const v = s.y[i];
            if (v === null) return null;
            // One noisy day is not a finding: mark a reading only if it stays high for two days, or is far out.
            const high = (j: number) => (s.z[j] ?? 0) > 2;
            const unexplained = d > 3 && high(i) && v > s.band_high[i] && (high(i - 1) || high(i + 1) || (s.z[i] ?? 0) > 3);
            // Above the range without meeting that rule: watched, not alarmed. A hollow ring, never red or amber.
            const watched = !unexplained && v > s.band_high[i];
            return <circle key={d} cx={x(d)} cy={y(v)} r={unexplained ? 5 : watched ? 4 : 2.6}
              className={unexplained ? "dot dot-red" : watched ? "dot dot-watch" : "dot"} />;
          })}
        </g>
        {dayIndex >= 5 && (
          <g>
            <line x1={playX} x2={right + 10} y1={rangeTopNow} y2={spaceLabelY - 5} className="leader" />
            <text x={right + 16} y={spaceLabelY} className="band-label space-text">Space-Normal</text>
            <text x={right + 16} y={spaceLabelY + 19} className="band-sub">moves with adaptation</text>
          </g>
        )}
        {firstMajor && (
          <text x={x(firstMajor.day) + barW} y={y(s.band_high[firstMajor.day - days[0]]) - 9}
            className="note-text event-text" textAnchor="middle">
            logged {(EVENT_LABEL[firstMajor.type] ?? firstMajor.type).toLowerCase()}
          </text>
        )}

        {episodes.map((e) => (
          <g key={`ep${e.onset_day}`}>
            <line x1={x(e.onset_day)} x2={x(e.onset_day)} y1={CHART_TOP} y2={chartBottom} className="onset" />
            <text x={x(e.onset_day)} y={chartBottom + 16} className="note-text" textAnchor="middle">symptoms start, day {e.onset_day}</text>
          </g>
        ))}
        {snAlerts.map((a) => (
          <g key={a.id} transform={`translate(${x(a.day)},${CHART_TOP - 14})`}>
            <path d="M0,16 L-8,0 L8,0 Z" className="alert-flag" />
            <text x={-14} y={12} className="alert-text" textAnchor="end">Space-Normal alert, day {a.day}</text>
          </g>
        ))}

        {/* crew journal */}
        <text x={GUTTER_L} y={journalTitle} className="row-title">
          Crew journal
          <tspan className="lane-how" dx="10">free text; the assistant reading is mocked in this demo</tspan>
        </text>
        <line x1={GUTTER_L} x2={right} y1={journalY} y2={journalY} className="lane-line" />
        {entries.map((j, k) => (
          <rect key={k} x={entryX(j) - 6} y={journalY - 6} width={12} height={12} rx={j.crew_ids.length > 1 ? 2.5 : 6}
            className={`entry ${j.accounted ? "entry-accounted" : ""} ${k === note ? "entry-open" : ""}`} />
        ))}
        <text x={right + 16} y={journalY + 5} className="lane-how">
          {entries.length} {entries.length === 1 ? "entry" : "entries"} so far
        </text>

        {detail && (
          <g>
            <text x={GUTTER_L} y={decompTitle} className="row-title">What moved each reading away from the pre-flight baseline</text>
            <line x1={GUTTER_L} x2={right} y1={zeroY} y2={zeroY} className="grid" />
            <g clipPath="url(#reveal)">
              {days.map((d, i) => {
                const parts: [number, string][] = [
                  [s.adaptation[i], "bar-adapt"], [s.events[i], "bar-event"],
                  [s.residual[i] ?? 0, (s.z[i] ?? 0) > 2 ? "bar-unexplained" : "bar-noise"],
                ];
                let up = zeroY, down = zeroY;
                return (
                  <g key={d}>
                    {parts.map(([value, cls], k) => {
                      const h = Math.abs(value) * dScale;
                      if (h < 0.4) return null;
                      const top = value >= 0 ? (up -= h) : down;
                      if (value < 0) down += h;
                      return <rect key={k} x={x(d) - barW / 2} y={top} width={barW} height={h} className={cls} />;
                    })}
                  </g>
                );
              })}
            </g>
            <g transform={`translate(${right + 16},${decompTop - 4})`} className="legend">
              <rect width="10" height="10" rx="2" className="bar-adapt" /><text x="17" y="10">expected adaptation</text>
              <rect y="19" width="10" height="10" rx="2" className="bar-event" /><text x="17" y="29">logged events</text>
              <rect y="38" width="10" height="10" rx="2" className="bar-unexplained" /><text x="17" y="48">unexplained</text>
              <rect y="57" width="10" height="10" rx="2" className="bar-noise" /><text x="17" y="67">day-to-day noise</text>
            </g>
          </g>
        )}

        {/* monitors */}
        {lanes.map((det, row) => {
          const top = lanesTop + row * LANE_H;
          const seen = reds.filter((a) => a.detector === det && a.day <= dayNow);
          const falseAlarms = seen.filter((a) => a.truth === "false_alarm").length;
          const caught = new Set(seen.filter((a) => a.truth === "hit").map((a) => a.crew_id));
          const hits = caught.size;
          const knownIllness = new Set([...started, ...caught]).size;
          const pending = started.some((c) => !caught.has(c) && !closed.includes(c));
          const isSN = det === "space_normal";
          const trackY = top + 33;
          return (
            <g key={det} className={isSN ? "lane lane-sn" : "lane"}>
              {isSN && <rect x={GUTTER_L - 12} y={top + 3} width={width - GUTTER_L + 10} height={LANE_H - 3} className="lane-highlight" rx={8} />}
              <text x={GUTTER_L} y={top + 21}>
                <tspan className="lane-name">{DETECTOR_LABEL[det].name}</tspan>
                <tspan className="lane-how" dx="10">{DETECTOR_LABEL[det].how}</tspan>
              </text>
              <line x1={GUTTER_L} x2={right} y1={trackY} y2={trackY} className="lane-line" />
              {seen.map((a) => a.truth === "hit"
                ? <circle key={a.id} cx={x(a.day)} cy={trackY} r={6} className="tick-hit" />
                : <rect key={a.id} x={x(a.day) - 2.5} y={trackY - 8} width={5} height={16} rx={2}
                    className={a.truth === "false_alarm" ? "tick-false" : "tick-near"} />)}
              <text x={right + 16} y={top + 21} className={falseAlarms ? "count count-bad" : "count count-good"}>
                {falseAlarms} false {falseAlarms === 1 ? "alarm" : "alarms"}
              </text>
              <text x={right + 16} y={top + 39} className="lane-how">
                {knownIllness === 0 ? "no illness so far"
                  : knownIllness === 1 ? (hits ? "illness caught" : pending ? "illness not flagged yet" : "illness missed")
                  : `${hits} of ${knownIllness} illnesses caught`}
              </text>
            </g>
          );
        })}

        {/* day axis and playhead */}
        {days.filter((d) => d === 1 || d % 7 === 0).map((d) => (
          <text key={d} x={x(d)} y={axisY + 18} className="tick" textAnchor="middle">{d}</text>
        ))}
        <text x={right + 16} y={axisY + 18} className="tick">mission day</text>
        <line x1={playX} x2={playX} y1={CHART_TOP - 4} y2={axisY} className="playhead" />
        {tip !== null && <circle cx={x(days[tip])} cy={y(s.y[tip] as number)} r={8.5} className="picked" />}
        <rect x={GUTTER_L} y={CHART_TOP} width={plotW} height={height - CHART_TOP} fill="transparent" style={{ cursor: "pointer" }}
          onPointerDown={onDown} onPointerMove={onMove} onPointerUp={onUp} />
      </svg>
      {note !== null && entries[note] && (() => {
        const j = entries[note];
        return (
          <div className="tip tip-journal" role="dialog" aria-label={`Journal entry, day ${j.day}`}
            style={{ left: Math.min(Math.max(entryX(j), 150), width - 150), top: journalY - 8 }}>
            <p className="tip-day">
              Day {j.day}, {String(j.hour).padStart(2, "0")}:00, {j.crew_ids.length > 1 ? "whole crew" : member.name}
            </p>
            <p className="tip-quote">“{j.text}”</p>
            <p className="tip-read">Assistant's reading (mock): {j.category}</p>
            <p className={j.accounted ? "tip-effect accounted" : "tip-effect"}>{j.effect}</p>
          </div>
        );
      })()}
      {tip !== null && (() => {
        const v = s.y[tip] as number;
        const z = s.z[tip] ?? 0;
        const verdict = v > s.band_high[tip] ? "Above the expected range" : v < s.band_low[tip] ? "Below the expected range" : "Inside the expected range";
        const outsideEarth = v > s.earth_high[tip] || v < s.earth_low[tip];
        const above = v > s.band_high[tip];
        // First day of the unbroken run of above-range days that ends at the picked day.
        let runStart = tip;
        while (above && runStart > 0 && s.y[runStart - 1] !== null && (s.y[runStart - 1] as number) > s.band_high[runStart - 1]) runStart--;
        const alertActive = mission.alerts.some((a) => a.detector === "space_normal" && a.level === "red"
          && a.crew_id === member.id && a.day <= days[tip] && a.day >= days[runStart] - ALERT_ACTIVE_DAYS);
        const px = x(days[tip]), py = y(v);
        return (
          <div className={`tip ${py < 190 ? "tip-below" : ""}`} role="dialog" aria-label={`Day ${days[tip]} reading`}
            style={{ left: Math.min(Math.max(px, 118), width - 118), top: py }}>
            <p className="tip-day">Day {days[tip]}</p>
            <p className="tip-value">{fixed(v, dg)} <small>{VITAL_LABEL[vital].unit}</small></p>
            <dl>
              <dt>Pre-flight baseline</dt><dd>{fixed(s.baseline[tip], dg)}</dd>
              <dt className="t-adapt">Expected adaptation</dt><dd>{signed(s.adaptation[tip], dg)}</dd>
              <dt className="t-event">Logged events</dt><dd>{signed(s.events[tip], dg)}</dd>
              <dt className={z > 2 ? "t-unexplained" : "t-noise"}>{z > 2 ? "Unexplained" : "Day-to-day variation"}</dt>
              <dd>{signed(s.residual[tip] ?? 0, dg)}</dd>
            </dl>
            <p className={`tip-verdict ${above ? "bad" : ""}`}>{verdict}</p>
            {above && !alertActive && (
              <p className="tip-watch">One day outside the range is watched, not alarmed. An alert needs a persistent shift.</p>
            )}
            {outsideEarth && <p className="tip-earth">Outside the pre-flight range</p>}
            {s.fixed_high !== null && v > s.fixed_high && <p className="tip-earth">Above the Earth-normal limit</p>}
          </div>
        );
      })()}
    </div>
  );
}

```

### `web/src/components/CrewList.tsx`

```tsx
import { useState } from "react";
import type { Mission, State, Vital } from "../contract";
import { BodyFigure, activeReports, describe, type PainReport, type System } from "./BodyFigure";

const ALERT_DAYS = 10; // how long a Space-Normal alert keeps a crew member marked
// Breathing rate is not shown in the UI, so it maps to no part of the figure.
const SYSTEM_OF: Partial<Record<Vital, System>> = { pulse: "cardio", sbp: "cardio", dbp: "cardio", temp_c: "thermo" };

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
        const parts = { cardio: systemState("cardio"), thermo: systemState("thermo") };
        const state: State = alerts.length ? flagged : parts.cardio === "event" || parts.thermo === "event" ? "event" : "expected";
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

```

### `web/src/components/BodyFigure.tsx`

```tsx
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

```

### `web/src/components/AlertPanel.tsx`

```tsx
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

```
### `web/src/labels.ts`

```ts
import type { Detector, Vital } from "./contract";

export const SCENARIO_LABEL: Record<string, string> = {
  single_illness: "One crew member falls ill",
};

/** Vitals offered in the demo UI. The contract and the detector still carry all five. */
export const DEMO_VITALS: Vital[] = ["temp_c", "pulse"];

export const VITAL_LABEL: Record<Vital, { name: string; unit: string }> = {
  pulse: { name: "Pulse", unit: "bpm" },
  temp_c: { name: "Core temperature", unit: "°C" },
  resp_rate: { name: "Breathing", unit: "/min" },
  sbp: { name: "Systolic BP", unit: "mmHg" },
  dbp: { name: "Diastolic BP", unit: "mmHg" },
};

export const DETECTOR_LABEL: Record<Detector, { name: string; how: string }> = {
  fixed_thresholds: { name: "Earth normal", how: "Same limits for everyone" },
  frozen_baseline: { name: "Pre-flight range", how: "Personal range fixed before launch (NASA CDSS concept)" },
  rolling_14: { name: "Rolling 14-day baseline", how: "Normal = the last 14 days" },
  space_normal: { name: "Space-Normal", how: "Normal moves with the expected adaptation" },
};

export const EVENT_LABEL: Record<string, string> = {
  schedule_shift: "Schedule shift",
  exercise: "Exercise session",
};

export const PROVENANCE_LABEL: Record<string, string> = {
  SYNTHETIC: "synthetic",
  REAL_BEDREST: "NASA bed rest",
  REAL_EARTH_ILLNESS: "real Earth illness",
  NONE: "none",
};

/** Rounds half up. With one decimal it mirrors _fmt in src/spacenormal/llm/note.py. */
export function fixed(x: number, digits = 1): string {
  const k = Math.pow(10, digits);
  const mag = Math.floor(Math.abs(x) * k + 0.5 + 1e-9) / k;
  return (x < 0 && mag > 0 ? "-" : "") + mag.toFixed(digits);
}

export function signed(x: number, digits = 1): string {
  const text = fixed(x, digits);
  return text.startsWith("-") ? text : "+" + text;
}

/** Temperature moves in tenths of a degree, so it needs a second decimal. */
export const DIGITS: Record<Vital, number> = { pulse: 1, temp_c: 2, resp_rate: 1, sbp: 1, dbp: 1 };

```
