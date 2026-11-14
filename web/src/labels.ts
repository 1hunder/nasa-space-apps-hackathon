import type { Detector, Vital } from "./contract";

export const SCENARIO_LABEL: Record<string, string> = {
  real_null: "Healthy crew",
  transplant_single: "One crew member falls ill",
  transplant_outbreak: "Illness spreads",
  shared_event: "Schedule change",
};

export const VITAL_LABEL: Record<Vital, { name: string; unit: string }> = {
  pulse: { name: "Pulse", unit: "bpm" },
  temp_c: { name: "Core temperature", unit: "°C" },
  resp_rate: { name: "Breathing", unit: "/min" },
  sbp: { name: "Systolic BP", unit: "mmHg" },
  dbp: { name: "Diastolic BP", unit: "mmHg" },
};

export const DETECTOR_LABEL: Record<Detector, { name: string; how: string }> = {
  fixed_thresholds: { name: "Fixed clinical limits", how: "Same limits for everyone" },
  frozen_baseline: { name: "Earth-normal monitor", how: "Personal baseline, fixed before launch" },
  rolling_14: { name: "Rolling recalibration", how: "Normal = the last 14 days" },
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
