import numpy as np
from hypothesis import given, settings, strategies as st
from hypothesis.extra.numpy import arrays

from spacenormal.detect.crew import outbreak_alerts
from spacenormal.detect.cusum import RED, YELLOW, combine_z, cusum, levels, upcrossings
from spacenormal.llm.note import build_note, template_note, verify_numbers
from spacenormal.model.simple import decompose_subject

finite_z = arrays(float, st.integers(5, 80), elements=st.floats(-6, 6))


def _decompose(mission, cfg, cid="C1"):
    sub = mission.daily[mission.daily["subject_id"] == cid]
    ev = mission.events[mission.events["subject_id"] == cid]
    return sub, ev, decompose_subject(sub, ev, cfg["synthetic"]["priors"], cfg)


def test_decomposition_adds_up(make, cfg):
    _, _, dec = _decompose(make("single_illness"), cfg)
    for d in dec.values():
        ok = np.isfinite(d.y)
        np.testing.assert_allclose((d.baseline + d.adaptation + d.events + d.residual)[ok], d.y[ok])
        assert (d.band_low < d.band_high).all()


def test_scale_is_bounded_and_frozen_after_day_21(make, cfg):
    _, _, dec = _decompose(make("healthy_crew", 3), cfg)
    lo, hi = cfg["model"]["scale_bounds"]
    for d in dec.values():
        assert ((d.scale >= lo) & (d.scale <= hi)).all()
        assert np.ptp(d.scale[d.days >= 22]) == 0


def test_scoring_is_causal(make, cfg):
    """Changing later days must not change earlier z-scores."""
    sub, ev, dec = _decompose(make("healthy_crew", 5), cfg)
    tampered = sub.copy()
    tampered.loc[tampered["study_day"] > 15, "pulse"] += 25
    dec2 = decompose_subject(tampered, ev, cfg["synthetic"]["priors"], cfg)
    early = dec["pulse"].days <= 15
    np.testing.assert_array_equal(dec["pulse"].z[early], dec2["pulse"].z[early])


def test_scale_recovers_a_strong_adaptation(make, cfg):
    """Averaged over people, the fitted scale tracks the true one."""
    errs = []
    for seed in range(12):
        m = make("healthy_crew", seed)
        for cid in m.crew:
            _, _, dec = _decompose(m, cfg, cid)
            t = m.truth[(m.truth.subject_id == cid) & (m.truth.vital == "pulse") & (m.truth.study_day == 70)]
            true_final = float(t["adaptation"].iloc[0])
            errs.append(dec["pulse"].adaptation[-1] - true_final)
    assert abs(np.mean(errs)) < 1.0 and np.std(errs) < 2.5


@given(finite_z)
def test_cusum_is_nonnegative_and_ignores_gaps(z):
    s = cusum(z, 0.5)
    assert (s >= 0).all()
    with_gap = np.insert(z, len(z) // 2, np.nan)
    assert cusum(with_gap, 0.5)[-1] == s[-1]


@given(finite_z)
@settings(max_examples=60)
def test_no_red_in_burn_in_and_one_red_per_excursion(z):
    days = np.arange(1, len(z) + 1)
    lv = levels(cusum(z, 0.5), days, 3.0, 5.0, burn_in=3)
    assert (lv[days <= 3] != RED).all()
    crossings = upcrossings(lv)
    reds = [i for i, level in crossings if level == RED]
    for a, b in zip(reds, reds[1:]):
        assert (lv[a:b] == 0).any()
    assert all(level in (YELLOW, RED) for _, level in crossings)


def test_combine_z_keeps_unit_scale_and_handles_missing():
    w = {"pulse": 0.6, "temp_c": 0.25, "resp_rate": 0.15}
    rng = np.random.default_rng(0)
    zs = {v: rng.normal(size=20000) for v in w}
    assert abs(np.std(combine_z(zs, w)) - 1) < 0.03
    zs["temp_c"][:10] = np.nan
    assert np.isfinite(combine_z(zs, w)[:10]).all()
    assert np.isnan(combine_z({v: np.full(3, np.nan) for v in w}, w)).all()


def _crew_z(onsets: dict[str, int], n=40):
    out = {}
    for cid in ["C1", "C2", "C3", "C4"]:
        z = np.zeros(n)
        if cid in onsets:
            z[onsets[cid] - 1: onsets[cid] + 5] = 3.0
        out[cid] = z
    return out, np.arange(1, n + 1)


def test_outbreak_needs_staggered_unexplained_onsets(cfg):
    z, days = _crew_z({"C1": 20, "C3": 22})
    alerts = outbreak_alerts(z, days, set(), cfg)
    assert len(alerts) == 1 and alerts[0]["crew_ids"] == ["C1", "C3"] and alerts[0]["onsets"] == [20, 22]

    same_day, _ = _crew_z({"C1": 20, "C2": 20, "C3": 20, "C4": 20})
    assert outbreak_alerts(same_day, days, set(), cfg) == []

    far_apart, _ = _crew_z({"C1": 10, "C3": 30})
    assert outbreak_alerts(far_apart, days, set(), cfg) == []

    assert outbreak_alerts(z, days, {20, 22}, cfg) == []
    assert outbreak_alerts(_crew_z({"C2": 20})[0], days, set(), cfg) == []


def test_note_numbers_are_verified_and_tampering_is_caught():
    d = {"y": 81.0, "baseline": 64.2, "adaptation": 5.8, "events": 0.4, "residual": 10.6, "z": 3.1}
    note = build_note("C3", 41, "pulse", d, [])
    assert note["numbers_verified"] is True
    assert note["text"].startswith("Unexplained residual +3.1σ on pulse, C3, day 41. Non-diagnostic.")
    assert note["bytes"] > 0 and len(note["questions"]) == 3

    text, allowed = template_note("C3", 41, "pulse", d)
    assert verify_numbers(text, allowed)
    assert not verify_numbers(text.replace("+3.1", "+1.3"), allowed)
    assert not verify_numbers(text + " Roughly 12 bpm above normal.", allowed)
