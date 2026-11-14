import { useLayoutEffect, useMemo, useRef, useState } from "react";
import { DETECTORS, type CrewMember, type Detector, type Mission, type Vital } from "../contract";
import { DETECTOR_LABEL, EVENT_LABEL, VITAL_LABEL } from "../labels";

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
const SIMPLE_LANES: Detector[] = ["frozen_baseline", "space_normal"];

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
  const s = member.vitals[vital];
  const days = mission.days;
  const n = days.length;
  // The chart takes the height the window can spare; detail rows trade some of it away.
  const spare = Math.max(380, Math.min(640, window.innerHeight - 340 - reserve));
  const chartBottom = detail ? Math.max(260, spare - 190) : spare;
  const plotW = Math.max(240, width - GUTTER_L - GUTTER_R);
  const right = GUTTER_L + plotW;
  const x = (d: number) => GUTTER_L + ((d - days[0]) / (days[n - 1] - days[0])) * plotW;
  const playX = x(day);
  const barW = Math.max(2, (plotW / (n - 1)) * 0.66);

  const [yLo, yHi] = useMemo(() => {
    const values = [...s.band_low, ...s.band_high, ...s.earth_low, ...s.earth_high,
      ...(s.y.filter((v) => v !== null) as number[])];
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
  const decompTitle = chartBottom + 40;
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
  const lanesTop = detail ? decompTop + DECOMP_H + 14 : chartBottom + 30;
  const axisY = lanesTop + lanes.length * LANE_H + 4;
  const height = axisY + 26;
  const reds = mission.alerts.filter((a) => a.level === "red");
  const knownIllness = mission.episodes.filter((e) => e.onset_day <= dayNow + 3).length;

  const scrub = (e: React.PointerEvent<SVGRectElement>) => {
    const box = e.currentTarget.getBoundingClientRect();
    onScrub(days[0] + ((e.clientX - box.left) / box.width) * (days[n - 1] - days[0]));
  };

  return (
    <div ref={ref} className="figure">
      <svg width={width} height={height} role="img"
        aria-label={`${name} for ${member.name} against the fixed Earth range and the moving Space-Normal range`}>
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
        <text x={right + 16} y={earthLabelY} className="band-label earth-text">Earth normal</text>
        <text x={right + 16} y={earthLabelY + 19} className="band-sub">fixed before launch</text>

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
            const unexplained = (s.z[i] ?? 0) > 2 && v > s.band_high[i] && d > 3;
            return <circle key={d} cx={x(d)} cy={y(v)} r={unexplained ? 5 : 2.6} className={unexplained ? "dot dot-red" : "dot"} />;
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

        {detail && (
          <g>
            <text x={GUTTER_L} y={decompTitle} className="row-title">What moved each reading away from the Earth baseline</text>
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
          const hits = new Set(seen.filter((a) => a.truth === "hit").map((a) => a.crew_id)).size;
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
                  : knownIllness === 1 ? (hits ? "illness caught" : "illness missed")
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
        <rect x={GUTTER_L} y={CHART_TOP} width={plotW} height={height - CHART_TOP} fill="transparent" style={{ cursor: "ew-resize" }}
          onPointerDown={(e) => { e.currentTarget.setPointerCapture(e.pointerId); scrub(e); }}
          onPointerMove={(e) => { if (e.buttons) scrub(e); }} />
      </svg>
    </div>
  );
}
