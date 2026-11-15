"""Loader for NASA Life Sciences Portal bed rest daily vitals (UTMB Campaigns 1, 3, CFT70).

The 29 per-subject files use 13 different header layouts, so columns are matched by
alias. Output follows spacenormal.data.schema (plus `block`, `date`, `comment`).

Split discipline: `load_daily("fit")` is always allowed. The two test splits raise
TestSetLocked until docs/claims.md carries a config hash (written by
scripts/hash_config.py just before the first test run). `inventory()` reads every file
but returns structure only: counts, day ranges, missingness. No test values leave it.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from spacenormal.config import REPO_ROOT, load_eval_config
from spacenormal.data.schema import DAILY_COLUMNS, PLAUSIBLE, VITALS, validate_daily

RAW = REPO_ROOT / "data" / "raw" / "nlsp"
CLAIMS = REPO_ROOT / "docs" / "claims.md"
SOURCE = "REAL_BEDREST"
VITALS_FOLDERS = {
    "C1": "CRF_Campaign_1_Daily_Vitals",
    "C3": "CRF_Campaign_3_Daily_Vitals",
    "CFT70": "CRF_CFT70_VITALS",
}
PHASE = {"PRE_TEST": "pre", "IN_TEST": "in", "POST_TEST": "post"}

# canonical name -> accepted raw headers (compared lower-cased, whitespace-collapsed)
ALIASES: dict[str, tuple[str, ...]] = {
    "subject": ("subject",),
    "date": ("date", "test_date"),
    "phase": ("test_phase",),
    "br_day": ("br_day",),
    "time": ("vitals time", "vitals collection time"),
    "pulse": ("pulse (bpm)", "pulse"),
    "sbp": ("sysbp (mmhg)", "sysbp", "blood pressure, systolic"),
    "dbp": ("diabp (mmhg)", "diabp", "blood pressure, diastolic"),
    "resp_rate": ("resp rate (rpm)", "resp rate", "respiration rate (rpm)", "respiration rate"),
    "temp_c": ("body temp (celsius)", "body temp", "temperature, body (celsius)"),
    "temp_f": ("temperature, body (fahrenheit)",),
    "weight_kg": ("weight (kg)", "weight"),
    "room_temp_f": ("ambient temperature (fahrenheit)", "temperature, ambient"),
    "room_rh": ("humidity (%)", "humidity, ambient %", "humidity, ambient (%)", "humidity, ambient"),
    "comment": ("comment", "nurse comments", "comments, vitals"),
}
NUMERIC = ("br_day", "pulse", "sbp", "dbp", "resp_rate", "temp_c", "temp_f", "weight_kg", "room_temp_f", "room_rh")


class TestSetLocked(RuntimeError):
    pass


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", str(name)).strip().lower()


def _f_to_c(f: pd.Series) -> pd.Series:
    return (f - 32.0) * 5.0 / 9.0


def subject_files() -> list[dict[str, Any]]:
    """Every per-subject vitals file with its campaign, block and canonical subject id."""
    out = []
    for campaign, folder in VITALS_FOLDERS.items():
        for path in sorted((RAW / folder).glob("*.csv")):
            stem = path.stem.replace(folder + "_", "")
            if campaign == "C1":
                if not stem.startswith("Subject_"):
                    continue  # "All" duplicates the three subject files
                block, sid = "C1", f"C1_{int(stem.split('_')[1]):04d}"
            elif campaign == "C3":
                block, num = stem.split("_")
                sid = f"{block}_{num}"
            else:
                block, sid = "CFT70", f"CFT70_{stem}"
            out.append({"campaign": campaign, "block": block, "subject_id": sid, "path": path})
    return out


def split_of(campaign: str, block: str) -> str:
    splits = load_eval_config()["splits"]
    if campaign == "CFT70":
        return "test_headline"
    if campaign == "C3" and block in splits["test_power"]["campaign_3_blocks"]:
        return "test_power"
    if campaign == "C1" or block in splits["fit"]["campaign_3_blocks"]:
        return "fit"
    raise ValueError(f"no split defined for campaign {campaign} block {block}")


def test_sets_unlocked() -> bool:
    return CLAIMS.exists() and "config_hash:" in CLAIMS.read_text(encoding="utf-8")


def read_subject(meta: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """One subject's file -> schema rows, plus a report of what was cleaned."""
    raw = pd.read_csv(meta["path"], encoding="utf-8-sig", na_values=["NA", "N/A", ""], dtype=str)
    by_norm = {_norm(c): c for c in raw.columns}
    cols: dict[str, pd.Series] = {}
    for canon, aliases in ALIASES.items():
        hit = next((by_norm[a] for a in aliases if a in by_norm), None)
        if hit is not None:
            cols[canon] = raw[hit]
    df = pd.DataFrame(cols)
    for name in NUMERIC:
        df[name] = pd.to_numeric(df[name], errors="coerce") if name in df else np.nan
    for name in ("time", "comment"):
        if name not in df:
            df[name] = pd.NA

    report: dict[str, Any] = {"rows_raw": len(df), "implausible": {}}
    df = df[df["phase"].isin(PHASE) & df["br_day"].notna()].copy()
    df["phase"] = df["phase"].map(PHASE)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Body temperature: Celsius column where present, else convert Fahrenheit. A value
    # above 60 in a Celsius-labelled or unlabelled column is Fahrenheit.
    temp = df["temp_c"].where(df["temp_c"].notna(), _f_to_c(df["temp_f"]))
    df["temp_c"] = temp.where(~(temp > 60), _f_to_c(temp)).round(2)
    # Ambient temperature is recorded in Fahrenheit; convert values that look like F.
    room = df["room_temp_f"]
    df["room_temp_c"] = room.where(~(room > 45), _f_to_c(room)).round(2)

    # Study day: pre counts down to the last day before tilt; post day 0 follows the last in-bed day.
    n_in = int(df.loc[df["phase"] == "in", "br_day"].max())
    day = df["br_day"].astype(int)
    df["study_day"] = np.select(
        [df["phase"] == "pre", df["phase"] == "in"], [-day, day], default=n_in + 1 + day)

    # More than one reading on a day: keep the earliest (the routine morning reading).
    df["_t"] = pd.to_datetime(df["time"], format="mixed", errors="coerce")
    df = df.sort_values(["study_day", "_t"], na_position="last")
    report["duplicate_day_rows"] = int(df.duplicated("study_day").sum())
    df = df.drop_duplicates("study_day", keep="first")

    for col, (lo, hi) in PLAUSIBLE.items():
        bad = df[col].notna() & ((df[col] < lo) | (df[col] > hi))
        if bad.any():
            report["implausible"][col] = int(bad.sum())
            df.loc[bad, col] = np.nan

    ordered = df.sort_values("study_day")
    dates = ordered["date"].dropna()
    report["dates_follow_study_day"] = bool(dates.is_monotonic_increasing)
    report["calendar_gaps"] = int((dates.diff().dt.days.dropna() != 1).sum())

    df["subject_id"], df["campaign"], df["block"] = meta["subject_id"], meta["campaign"], meta["block"]
    df["group"], df["source"] = meta["block"], SOURCE  # treatment arm is not in the vitals files
    keep = [*DAILY_COLUMNS, "block", "date", "comment"]
    return df.sort_values("study_day")[keep].reset_index(drop=True), report


def load_daily(split: str = "fit") -> pd.DataFrame:
    """Daily table for one split: 'fit', 'test_headline' or 'test_power'."""
    if split != "fit" and not test_sets_unlocked():
        raise TestSetLocked(
            f"split '{split}' is locked until scripts/hash_config.py writes the config hash to docs/claims.md")
    frames = [read_subject(m)[0] for m in subject_files() if split_of(m["campaign"], m["block"]) == split]
    if not frames:
        raise FileNotFoundError(f"no NLSP vitals files for split '{split}' under {RAW}; run scripts/fetch_nlsp.py")
    return validate_daily(pd.concat(frames, ignore_index=True))


def inventory() -> pd.DataFrame:
    """One row per subject: structure only (counts, day ranges, missingness, cleaning report)."""
    rows = []
    for meta in subject_files():
        df, report = read_subject(meta)
        inn = df[df["phase"] == "in"]
        row = {
            "subject_id": meta["subject_id"], "campaign": meta["campaign"], "block": meta["block"],
            "split": split_of(meta["campaign"], meta["block"]),
            "start": df["date"].min().date().isoformat() if df["date"].notna().any() else "",
            "pre_days": int((df["phase"] == "pre").sum()), "in_days": len(inn),
            "in_day_max": int(inn["study_day"].max()), "post_days": int((df["phase"] == "post").sum()),
            "has_room_climate": bool(df["room_temp_c"].notna().any()),
            "duplicate_day_rows": report["duplicate_day_rows"],
            "implausible_values": sum(report["implausible"].values()),
            "dates_follow_study_day": report["dates_follow_study_day"],
            "calendar_gaps": report["calendar_gaps"],
        }
        for v in (*VITALS, "weight_kg", "room_temp_c", "room_rh"):
            row[f"miss_in_{v}"] = round(float(inn[v].isna().mean()), 3)
        row["miss_pre_pulse"] = round(float(df.loc[df["phase"] == "pre", "pulse"].isna().mean()), 3)
        row["miss_pre_temp_c"] = round(float(df.loc[df["phase"] == "pre", "temp_c"].isna().mean()), 3)
        rows.append(row)
    return pd.DataFrame(rows)


# --- Symptom, medication and issue logs -------------------------------------------------

LOG_FOLDERS: dict[str, tuple[str, str]] = {
    "CRF_Campaign_1_Medical_Log": ("C1", "medication"),
    "CRF_Campaign_3_Symptom_Complaint": ("C3", "symptom"),
    "CRF_Campaign_3_Medication_Log": ("C3", "medication"),
    "CRF_Campaign_3_Protocol_Deviations": ("C3", "issue"),
    "CRF_CFT70_SYMPTOMS": ("CFT70", "symptom"),
    "CRF_CFT70_MEDLOG": ("CFT70", "medication"),
    "CRF_CFT70_ISSUES": ("CFT70", "issue"),
}
_LOG_META = {"id", "record", "subject", "campaign", "date", "time", "test_phase", "br_day", "crf status",
             "crf_status", "occur time", "time_administered", "time of med", "date of med", "signature",
             "signature_date", "reported_by", "reported_to", "reported by", "reported to"}

# Terms that suggest an infection-like or systemic illness rather than musculoskeletal pain.
ILLNESS_TERMS: dict[str, str] = {
    "fever": r"\bfever|febrile|\bchills\b",
    "upper_respiratory": r"sore throat|\bcough|congest|runny nose|rhinorrhea|sinus|\bcold\b|\buri\b|sneez",
    "gastrointestinal": r"nausea|vomit|emesis|diarrhea|loose stool",
    "infection": r"infect|antibiotic|amoxicillin|azithromycin|cephalexin|ciprofloxacin|\bflu\b|influenza|viral",
    "cold_medication": r"pseudoephedrine|sudafed|guaifenesin|robitussin|dextromethorphan|loratadine|claritin|nyquil|lozenge",
}


def load_logs() -> pd.DataFrame:
    """Long table of log entries: subject_id, split, log, phase, br_day, text (all free-text fields joined)."""
    ids = {(m["campaign"], m["subject_id"].split("_")[-1].lstrip("0") or "0"): m for m in subject_files()}
    rows = []
    for folder, (campaign, kind) in LOG_FOLDERS.items():
        for path in sorted((RAW / folder).glob("*.csv")):
            stem = path.stem.replace(folder + "_", "")
            if stem == "All":
                continue
            key = stem.split("_")[-1].lstrip("0") or "0"
            meta = ids.get((campaign, key))
            if meta is None:
                continue
            raw = pd.read_csv(path, encoding="utf-8-sig", dtype=str, na_values=["NA", "N/A", ""])
            norm = {_norm(c): c for c in raw.columns}
            text_cols = [c for n, c in norm.items() if n not in _LOG_META]
            text = raw[text_cols].fillna("").agg(" | ".join, axis=1)
            rows.append(pd.DataFrame({
                "subject_id": meta["subject_id"], "split": split_of(meta["campaign"], meta["block"]),
                "log": kind,
                "phase": raw[norm["test_phase"]].map(PHASE) if "test_phase" in norm else pd.NA,
                "br_day": pd.to_numeric(raw[norm["br_day"]], errors="coerce") if "br_day" in norm else np.nan,
                "text": text,
            }))
    return pd.concat(rows, ignore_index=True)


def illness_term_hits(logs: pd.DataFrame) -> pd.DataFrame:
    """Adds one boolean column per ILLNESS_TERMS key."""
    out = logs.copy()
    lower = out["text"].str.lower()
    for name, pattern in ILLNESS_TERMS.items():
        out[name] = lower.str.contains(pattern, regex=True)
    return out
