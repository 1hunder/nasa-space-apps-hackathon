"""Loader tests on small hand-written files in the real layouts, plus checks on the
real NASA files when they have been fetched (skipped otherwise, e.g. in CI)."""

import numpy as np
import pandas as pd
import pytest

from spacenormal.data import nlsp, stanford

LAYOUT_NEW = (
    "﻿Record,Subject,Date,Test_Phase,BR_Day,Vitals Time,Pulse (bpm),SysBP (mmHg),DiaBP (mmHg),"
    "Resp Rate (rpm),Tilt Verified,Weight (Kg),Body Temp (Celsius),Height (cm),Humidity (%),"
    "Ambient Temperature (Fahrenheit),Comment,Issues Reported,Issue Reported Number\n"
    "1,9999,1/1/2013,PRE_TEST,2,8:00,70,120,80,16,,80.0,36.6,180,45,72.5,,No,\n"
    "2,9999,1/2/2013,PRE_TEST,1,6:00,68,118,78,16,,80.1,36.5,,46,72.0,,No,\n"
    "3,9999,1/3/2013,IN_TEST,1,6:00,72,115,75,18,Yes,79.9,36.7,,47,73.0,,No,\n"
    "4,9999,1/3/2013,IN_TEST,1,14:00,90,130,85,20,Yes,,36.9,,47,73.0,recheck,No,\n"
    "5,9999,1/4/2013,IN_TEST,2,6:00,400,116,76,NA,Yes,79.5,NA,,48,73.4,,No,\n"
    "6,9999,1/5/2013,POST_TEST,0,6:00,75,119,79,16,,79.0,36.6,,44,71.0,,No,\n"
)
LAYOUT_OLD = (
    "ID,Subject,Date,Test_Phase,BR_Day,Pulse (bpm),\"Blood Pressure, systolic\",\"Blood Pressure, diastolic\","
    "Respiration rate (rpm),Vitals collection time,\"Temperature, body (Celsius)\","
    "\"Temperature, body (Fahrenheit)\",Weight (kg),Height (cm),\"Temperature, ambient\","
    "\"Humidity, ambient %\",Nurse Comments,6-degree Tilt Verified\n"
    "1,C1G0001,8/30/2004,PRE_TEST,1,62,108,68,18,6:10:00,NA,98.6,81,180,70,50,NA,NA\n"
    "2,C1G0001,8/31/2004,IN_TEST,1,59,105,62,12,6:08:00,NA,NA,81,NA,NA,NA,NA,NA\n"
)


def _meta(tmp_path, text, name="f.csv"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return {"campaign": "CFT70", "block": "CFT70", "subject_id": "CFT70_9999", "path": path}


def test_new_layout_is_normalised(tmp_path):
    df, report = nlsp.read_subject(_meta(tmp_path, LAYOUT_NEW))
    assert list(df["study_day"]) == [-2, -1, 1, 2, 3]            # pre counts down; post follows last in-bed day
    assert list(df["phase"]) == ["pre", "pre", "in", "in", "post"]
    assert df.loc[df.study_day == 1, "pulse"].item() == 72        # earliest reading of the day is kept
    assert report["duplicate_day_rows"] == 1
    assert np.isnan(df.loc[df.study_day == 2, "pulse"].item())    # 400 bpm is a data error, not a finding
    assert report["implausible"] == {"pulse": 1}
    assert df["room_temp_c"].iloc[0] == pytest.approx(22.5)       # 72.5 F
    assert set(df["source"]) == {"REAL_BEDREST"}
    assert report["dates_follow_study_day"] is True


def test_old_layout_falls_back_to_fahrenheit(tmp_path):
    df, _ = nlsp.read_subject(_meta(tmp_path, LAYOUT_OLD))
    assert df["temp_c"].iloc[0] == pytest.approx(37.0)            # 98.6 F
    assert df["room_temp_c"].iloc[0] == pytest.approx(21.11, abs=0.01)
    assert np.isnan(df["temp_c"].iloc[1]) and np.isnan(df["room_temp_c"].iloc[1])
    assert df["sbp"].tolist() == [108, 105]


def test_splits_follow_eval_config():
    assert nlsp.split_of("CFT70", "CFT70") == "test_headline"
    assert nlsp.split_of("C3", "C3G") == nlsp.split_of("C3", "C3H") == "test_power"
    assert {nlsp.split_of("C3", b) for b in ("C3A", "C3C", "C3D", "C3E")} == {"fit"}
    assert nlsp.split_of("C1", "C1") == "fit"


def test_test_sets_are_locked_without_a_config_hash(tmp_path, monkeypatch):
    monkeypatch.setattr(nlsp, "CLAIMS", tmp_path / "claims.md")
    for split in ("test_headline", "test_power"):
        with pytest.raises(nlsp.TestSetLocked):
            nlsp.load_daily(split)
    (tmp_path / "claims.md").write_text("config_hash: abc123\n")
    assert nlsp.test_sets_unlocked()


def test_illness_terms_separate_congestion_from_muscle_pain():
    logs = pd.DataFrame({"text": [
        "Subject reports muscle soreness after supine cycle", "Nasal congestion and scratchy throat",
        "Temp 38.2, febrile, chills", "Nausea after tilt", "It is cold in the room", "Sudafed 60 mg given",
    ]})
    hits = nlsp.illness_term_hits(logs)
    assert not hits.iloc[0, 1:].any()
    assert hits.loc[1, "upper_respiratory"] and hits.loc[2, "fever"] and hits.loc[3, "gastrointestinal"]
    assert hits.loc[5, "cold_medication"]


@pytest.mark.skipif(not (nlsp.RAW / "CRF_CFT70_VITALS").exists(), reason="NLSP data not fetched")
def test_real_inventory_matches_the_approved_splits():
    inv = nlsp.inventory()
    assert inv.groupby("split")["subject_id"].count().to_dict() == {"fit": 18, "test_headline": 3, "test_power": 8}
    fit = nlsp.load_daily("fit")
    assert fit["subject_id"].nunique() == 18 and set(fit["source"]) == {"REAL_BEDREST"}
    assert not ({"CFT70", "C3G", "C3H"} & set(fit["block"]))


def _write_p1(tmp_path, pid="AAAAAAA"):
    base = tmp_path / "COVID-19-Wearables"
    base.mkdir()
    ts = pd.date_range("2024-01-01 00:00", "2024-01-03 23:59", freq="min")
    hr = np.where(ts.hour < 6, 55, 80)
    steps = np.where((ts.hour >= 6) | ((ts.hour == 2) & (ts.minute < 30)), 12, 0)
    hr = np.where((ts.hour == 2) & (ts.minute < 30), 110, hr)           # a night walk must not count as rest
    pd.DataFrame({"user": pid, "datetime": ts.astype(str), "heartrate": hr}).to_csv(base / f"{pid}_hr.csv", index=False)
    pd.DataFrame({"user": pid, "datetime": ts.astype(str), "steps": steps}).to_csv(base / f"{pid}_steps.csv", index=False)
    return base


def test_stanford_night_resting_hr_uses_only_zero_step_night_minutes(tmp_path):
    _write_p1(tmp_path)
    files = stanford.participant_files(1, tmp_path)
    assert list(files) == ["AAAAAAA"]
    daily = stanford.night_resting_hr(**{"hr_path": files["AAAAAAA"]["hr"], "steps_path": files["AAAAAAA"]["steps"]})
    assert len(daily) == 3 and (daily["night_rhr"] == 55).all() and (daily["night_minutes"] == 330).all()


def test_stanford_phase2_layout_and_labels(tmp_path):
    folder = tmp_path / "COVID-19-Phase2-Wearables" / "P000001"
    folder.mkdir(parents=True)
    ts = pd.date_range("2028-03-26 00:00:06", periods=6 * 60 * 6, freq="10s")
    (folder / "Orig_Fitbit_HR.csv").write_text("\n" + pd.DataFrame({"datetime": ts.astype(str), "heartrate": 60}).to_csv(index=False))
    (folder / "Orig_Fitbit_ST.csv").write_text("\ndatetime,steps\n2028-03-26 01:22:00,31\n")
    files = stanford.participant_files(2, tmp_path)
    daily = stanford.night_resting_hr(files["P000001"]["hr"], files["P000001"]["steps"])
    assert len(daily) == 1 and daily["night_rhr"].item() == 60 and daily["night_minutes"].item() == 359

    with pytest.raises(FileNotFoundError):
        stanford.load_labels(2, tmp_path)
    (tmp_path / "labels.csv").write_text("participant_id,symptom_onset_date\nP000001,2028-04-02\nP000002,\n")
    assert len(stanford.load_labels(2, tmp_path)) == 1

    split = stanford.split_participants([f"P{i}" for i in range(20)], seed=1)
    assert sorted(sum(split.values(), [])) == sorted(f"P{i}" for i in range(20))
    assert split == stanford.split_participants([f"P{i}" for i in range(20)], seed=1)
