"""Build data/raw/stanford_p1/labels.csv from Mishra et al. 2020, Supplementary Table 3.

    python scripts/build_stanford_labels.py

Input: data/raw/stanford_p1/mishra2020_MOESM3.xlsx (the paper's supplementary tables,
https://doi.org/10.1038/s41551-020-00640-6). Dates are shifted per participant.

One row per illness episode. For COVID-19 participants who report several symptom
dates, the episode is the symptom date closest to the diagnosis date; the other dates
are dropped. Other-illness rows keep every reported symptom date.
"""

from __future__ import annotations

import re
import warnings

import pandas as pd

from spacenormal.data.stanford import RAW_P1

SHEET = "SuppTable3_Fig2a_COVID-19"
_DATE = re.compile(r"Timestamp\('(\d{4}-\d{2}-\d{2})")


def _dates(cell: object) -> list[pd.Timestamp]:
    return [pd.Timestamp(d) for d in _DATE.findall(str(cell))]


def build() -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw = pd.read_excel(RAW_P1 / "mishra2020_MOESM3.xlsx", sheet_name=SHEET, header=3)
    rows = []
    for r in raw.itertuples(index=False):
        # "AA0HAI1_Illness_2" is stored in the archive as AA0HAI1_2_hr.csv
        pid = re.sub(r"_Illness_(\d+)$", r"_\1", str(r.ParticipantID))
        category = "covid" if str(r.Category).startswith("COVID") else "other_illness"
        symptoms, diagnosis = _dates(r.Symptom_dates), _dates(r.covid_diagnosis_dates)
        dx = diagnosis[0] if diagnosis else pd.NaT
        if category == "covid" and symptoms and diagnosis:
            symptoms = [min(symptoms, key=lambda d: abs((d - dx).days))]
        for onset in symptoms:
            rows.append({"participant_id": pid, "symptom_onset_date": onset.date().isoformat(),
                         "category": category, "detail": str(r.Category),
                         "diagnosis_date": dx.date().isoformat() if pd.notna(dx) else ""})
    return pd.DataFrame(rows).drop_duplicates().sort_values(["category", "participant_id", "symptom_onset_date"])


if __name__ == "__main__":
    labels = build()
    out = RAW_P1 / "labels.csv"
    labels.to_csv(out, index=False)
    print(labels.groupby("category").agg(episodes=("participant_id", "size"), participants=("participant_id", "nunique")))
    print(f"wrote {len(labels)} episodes to {out}")
