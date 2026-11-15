import { useCallback, useEffect, useRef, useState } from "react";
import type { Alert, Mission, MissionIndex, Vital } from "./contract";

const FULL_REPLAY_SECONDS = 13; // one mission at 1x

export interface Replay {
  index: MissionIndex | null;
  mission: Mission | null;
  error: string | null;
  scenario: string;
  setScenario: (s: string) => void;
  day: number; // fractional mission day
  dayIndex: number; // index of the last fully revealed day
  setDay: (d: number) => void;
  playing: boolean;
  toggle: () => void;
  restart: () => void;
  speed: number;
  setSpeed: (s: number) => void;
  crewId: string;
  setCrewId: (id: string) => void;
  vital: Vital;
  setVital: (v: Vital) => void;
  activeAlert: Alert | null; // latest Space-Normal red alert at or before the playhead
}

export function useReplay(): Replay {
  const [index, setIndex] = useState<MissionIndex | null>(null);
  const [mission, setMission] = useState<Mission | null>(null);
  const [error, setError] = useState<string | null>(null);
  // ?scenario=outbreak&day=40 opens a specific moment (used for bookmarks and screenshots).
  const params = useRef(new URLSearchParams(window.location.search));
  const [scenario, setScenario] = useState(params.current.get("scenario") ?? "single_illness");
  const [day, setDayState] = useState(1);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [crewId, setCrewId] = useState("");
  const [vital, setVital] = useState<Vital>("temp_c");
  const dayRef = useRef(1);

  useEffect(() => {
    fetch("./cache/missions.json")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`missions.json: HTTP ${r.status}`))))
      .then(setIndex)
      .catch((e) => setError(`Could not load the mission cache. Run "make demo-synthetic" first. (${e.message})`));
  }, []);

  useEffect(() => {
    if (!index) return;
    const entry = index.missions.find((m) => m.scenario === scenario) ?? index.missions[0];
    if (!entry) return;
    setPlaying(false);
    fetch(`./cache/${entry.file}`)
      .then((r) => r.json())
      .then((m: Mission) => {
        const firstAlert = m.alerts.find((a) => a.detector === "space_normal" && a.level === "red");
        setMission(m);
        setCrewId(firstAlert?.crew_id ?? m.episodes[0]?.crew_id ?? m.crew[0].id);
        setVital("temp_c");
        const asked = Number(params.current.get("day"));
        params.current.delete("day"); // only for the first mission loaded
        const start = asked >= m.days[0] && asked <= m.days[m.days.length - 1] ? asked : m.days[0];
        dayRef.current = start;
        setDayState(start);
      })
      .catch((e) => setError(`Could not load ${entry.file}. (${e.message})`));
  }, [index, scenario]);

  const setDay = useCallback(
    (d: number) => {
      if (!mission) return;
      const clamped = Math.min(mission.days[mission.days.length - 1], Math.max(mission.days[0], d));
      dayRef.current = clamped;
      setDayState(clamped);
    },
    [mission],
  );

  useEffect(() => {
    if (!playing || !mission) return;
    const first = mission.days[0];
    const last = mission.days[mission.days.length - 1];
    const rate = ((last - first) / FULL_REPLAY_SECONDS) * speed; // days per second
    const reds = mission.alerts.filter((a) => a.detector === "space_normal" && a.level === "red");
    let frame = 0;
    let prev = performance.now();
    const tick = (now: number) => {
      // A frame's timestamp can precede the moment the loop started; never step backwards.
      const dt = Math.max(0, Math.min(0.1, (now - prev) / 1000));
      prev = now;
      {
        const before = dayRef.current;
        let next = Math.min(last, before + dt * rate);
        const crossed = reds.find((a) => a.day > before && a.day <= next);
        if (crossed) {
          // An alert stops the replay on that day; Play continues from there.
          next = crossed.day;
          setCrewId(crossed.crew_id);
          // Stay on the vital being watched if it is also clearly off; otherwise show the one that led the alert.
          const i = mission.days.indexOf(crossed.day);
          const member = mission.crew.find((c) => c.id === crossed.crew_id);
          setVital((v) => ((member?.vitals[v].z[i] ?? 0) > 2 ? v : crossed.vital));
        }
        dayRef.current = next;
        setDayState(next);
        if (crossed || next >= last) {
          setPlaying(false);
          return;
        }
      }
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing, mission, speed]);

  const toggle = useCallback(() => {
    if (!mission) return;
    if (dayRef.current >= mission.days[mission.days.length - 1]) setDay(mission.days[0]);
    setPlaying((p) => !p);
  }, [mission, setDay]);

  const restart = useCallback(() => {
    if (!mission) return;
    setDay(mission.days[0]);
    setPlaying(true);
  }, [mission, setDay]);

  const dayIndex = mission ? Math.max(0, Math.floor(day) - mission.days[0]) : 0;
  const activeAlert =
    mission?.alerts
      .filter((a) => a.detector === "space_normal" && a.level === "red" && a.day <= Math.floor(day))
      .sort((a, b) => b.day - a.day || (a.crew_id === crewId ? -1 : 1))[0] ?? null;

  return {
    index, mission, error, scenario, setScenario, day, dayIndex, setDay, playing, toggle, restart,
    speed, setSpeed, crewId, setCrewId, vital, setVital, activeAlert,
  };
}
