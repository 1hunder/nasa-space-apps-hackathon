import numpy as np
import pandas as pd
import pytest

from spacenormal.data.schema import SchemaError, validate_daily
from spacenormal.data.synthetic import illness_shape


def test_seeded_runs_are_identical(make):
    a, b = make("outbreak", 7), make("outbreak", 7)
    pd.testing.assert_frame_equal(a.daily, b.daily)
    pd.testing.assert_frame_equal(a.events, b.events)


def test_everything_is_labelled_synthetic(make):
    m = make("single_illness")
    assert set(m.daily["source"]) == {"SYNTHETIC"}
    assert set(m.provenance.values()) == {"SYNTHETIC"}


def test_null_has_no_episodes_and_no_illness(make):
    m = make("healthy_crew")
    assert m.episodes.empty
    assert m.provenance["illness"] == "NONE"
    assert (m.truth["illness"] == 0).all()


def test_outbreak_onsets_are_staggered(make):
    onsets = make("outbreak").episodes["onset_day"]
    assert 2 <= len(onsets) <= 3
    assert onsets.nunique() > 1
    assert onsets.max() - onsets.min() <= 4


def test_shared_event_is_logged_for_all_crew(make):
    m = make("shared_event")
    shift = m.events[m.events["event_type"] == "schedule_shift"]
    assert shift.groupby("study_day")["subject_id"].nunique().eq(4).all()
    assert m.episodes.empty


def test_truth_components_add_up_to_the_signal(make):
    m = make("single_illness")
    total = m.truth.assign(v=lambda t: t.baseline + t.adaptation + t.events + t.illness + t.noise)
    wide = total.pivot(index=["subject_id", "study_day"], columns="vital", values="v")
    obs = m.daily.set_index(["subject_id", "study_day"])
    for vital, tol in [("pulse", 0.5), ("temp_c", 0.05)]:
        diff = (obs[vital] - wide[vital]).dropna()
        assert diff.abs().max() <= tol + 1e-9


def test_illness_shape_peaks_after_onset_and_ends():
    d = np.arange(-10, 30)
    shape = illness_shape(d)
    assert shape.max() == pytest.approx(1.0) and d[shape.argmax()] == 1
    assert (shape[d < -3] == 0).all() and (shape[d > 12] == 0).all()


def test_schema_rejects_duplicates_and_bad_values(make):
    daily = make("healthy_crew").daily
    with pytest.raises(SchemaError):
        validate_daily(pd.concat([daily, daily.head(1)]))
    with pytest.raises(SchemaError):
        validate_daily(daily.assign(pulse=500.0))
    with pytest.raises(SchemaError):
        validate_daily(daily.drop(columns=["room_rh"]))
