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

/** One entry per mission day (daily means). `null` in y / residual / z means no measurement that day. */
export interface VitalSeries {
  y: (number | null)[];
  /** Mission.samples_per_day readings per day, with the person's time-of-day pattern removed. */
  y_hourly: (number | null)[];
  baseline: number[];
  adaptation: number[];
  events: number[];
  residual: (number | null)[];
  z: (number | null)[];
  band_low: number[];
  band_high: number[];
  /** Fixed band around the pre-mission baseline: what an Earth-calibrated monitor calls normal. */
  earth_low: number[];
  earth_high: number[];
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
  /** Display name; equals id when none is given. */
  name: string;
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
  /** Scored against known episodes: hit = within 7 days before to 3 days after onset. */
  truth: "hit" | "false_alarm" | "near_episode";
}

export interface MissionEvent {
  day: number;
  type: string;
  crew_ids: string[];
}

export interface Episode {
  crew_id: string;
  onset_day: number;
  provenance: Provenance;
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
  /** Readings per day in y_hourly (24 = hourly; 1 = daily data only). */
  samples_per_day: number;
  provenance: MissionProvenance;
  crew: CrewMember[];
  events: MissionEvent[];
  alerts: Alert[];
  crew_alerts: CrewAlert[];
  /** Known illness onsets (planted in synthetic and transplant scenarios). */
  episodes: Episode[];
  /** Keyed by Alert.id. Present for Space-Normal red alerts. */
  notes: Record<string, Note>;
}

/** public/cache/missions.json */
export interface MissionIndex {
  missions: { file: string; mission_id: string; scenario: string; provenance: MissionProvenance }[];
}
