// Data contract between the Python pipeline and the dashboard.
// Mirrored by src/spacenormal/contract.py; scripts/validate_contract.py checks every cache file.
// Rule: the UI shows no number that is not in this JSON.

export type Provenance = "REAL_BEDREST" | "REAL_EARTH_ILLNESS" | "SYNTHETIC";
export type State = "expected" | "event" | "unexplained" | "crew" | "not_monitored";
export type Vital = "pulse" | "temp_c" | "resp_rate" | "sbp" | "dbp";
export type Level = "yellow" | "red";

export const VITALS: Vital[] = ["pulse", "temp_c", "resp_rate", "sbp", "dbp"];
export const DETECTORS = ["fixed_thresholds", "frozen_baseline", "rolling_14", "space_normal"] as const;
export type Detector = (typeof DETECTORS)[number];

/** One entry per mission day. `null` in y / residual / z means no measurement that day. */
export interface VitalSeries {
  y: (number | null)[];
  baseline: number[];
  adaptation: number[];
  events: number[];
  residual: (number | null)[];
  z: (number | null)[];
  band_low: number[];
  band_high: number[];
}

export interface SystemsDay {
  day: number;
  cardio: State;
  resp: State;
  thermo: State;
  fluids: State;
}

export interface CrewMember {
  id: string;
  group: string;
  vitals: Record<Vital, VitalSeries>;
  systems: SystemsDay[];
}

export interface Alert {
  id: string;
  detector: Detector;
  crew_id: string;
  day: number;
  level: Level;
  vital: Vital;
  z: number;
}

export interface MissionEvent {
  day: number;
  type: string;
  crew_ids: string[];
}

export interface CrewAlert {
  day: number;
  crew_ids: string[];
  onsets: number[];
}

export interface Note {
  text: string;
  numbers_verified: boolean;
  bytes: number;
  context_items: { text: string; source_ref: string }[];
  questions: string[];
}

export interface MissionProvenance {
  adaptation: Provenance;
  illness: Provenance | "NONE";
  events: Provenance;
}

export interface Mission {
  mission_id: string;
  scenario: string;
  days: number[];
  provenance: MissionProvenance;
  crew: CrewMember[];
  events: MissionEvent[];
  alerts: Alert[];
  crew_alerts: CrewAlert[];
  /** Keyed by Alert.id. Present for Space-Normal red alerts. */
  notes: Record<string, Note>;
}

/** public/cache/missions.json */
export interface MissionIndex {
  missions: { file: string; mission_id: string; scenario: string; provenance: MissionProvenance }[];
}
