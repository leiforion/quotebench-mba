"""SIM-2 gates.

The load-bearing one is graceful degradation (constraint four, mirrored):
with the system down, the to-be model must reproduce the calibrated as-is
baseline; with the system up but extraction forced to zero, everything must
route manual at full as-is touch and as-is defect rates. The rest are routing
and monotonicity sanity checks.
"""
import numpy as np
import pytest

from sim.capability import draw_docs
from sim.config import load_asis, load_tobe, is_fitted
from sim.tobe import ToBeModel

TOL = 0.10


@pytest.fixture(scope="module")
def params():
    p = load_asis()
    assert is_fitted(p), "run `python -m sim fit` first"
    return load_tobe(), p


def test_degraded_reproduces_asis(params):
    """System down: every inquiry drops into the Section 4 process; the model
    must land on the calibrated baseline."""
    pt, pa = params
    res = ToBeModel(pt, pa, seed=7, degraded=True).run(years=12)
    s = res.summary()
    tgt = pa["calibration_targets"]
    for t in ("tier1", "tier2", "tier3"):
        assert abs(s["cycle_median_wh"][t] - tgt["cycle_median_wh"][t]) \
            <= TOL * tgt["cycle_median_wh"][t]
        assert abs(s["eng_touch_median_wh"][t] - tgt["touch_median_h"][t]) \
            <= TOL * tgt["touch_median_h"][t]


def test_zero_extraction_routes_manual_at_asis_touch(params):
    """System up, extraction success forced to zero: no route can clear C2,
    the assist credit vanishes, and touch collapses to as-is."""
    pt, pa = params
    res = ToBeModel(pt, pa, seed=11, extraction_override=0.0).run(years=8)
    s = res.summary()
    senior_speed = next(e["speed"] for e in pa["estimators"]
                        if e.get("skill", e["name"]) == "senior")
    for t in ("tier1", "tier2", "tier3"):
        assert s["route_mix"][t]["manual"] > 0.999
        tgt = pa["calibration_targets"]["touch_median_h"][t]
        # Tier 3 manual work routes to the senior (7.7 ELSE branch), whose
        # speed multiplier applies; tiers 1-2 spread across both estimators.
        if t == "tier3":
            tgt = tgt * senior_speed
        assert abs(s["eng_touch_median_wh"][t] - tgt) <= TOL * tgt
    # manual lane keeps the as-is defect model: BASE-19 weighted ~9.2%
    assert abs(s["any_defect_rate"] - 0.092) <= 0.02


def test_routing_constraints(params):
    """No Tier 3 auto-draft; every auto-draft cleared C1 and the value gate."""
    pt, pa = params
    res = ToBeModel(pt, pa, variant="central", seed=13).run(years=8)
    autos = [r for r in res.records if r.route == "auto"]
    assert autos, "central variant should produce some auto-drafts"
    for r in autos:
        assert r.tier == "tier1"
        assert r.min_conf >= pt["routing"]["C1"]
        assert r.value_eur < pt["routing"]["V1_eur"]
    assert all(r.route != "assisted" for r in res.records if r.tier == "tier3")


def test_variants_monotonic(params):
    """Better extraction must never mean less automation or worse defects."""
    pt, pa = params
    shares, defects = {}, {}
    for v in ("optimistic", "central", "pessimistic"):
        s = ToBeModel(pt, pa, variant=v, seed=17).run(years=6).summary()
        auto_assisted = [s["route_mix"][t]["auto"] + s["route_mix"][t]["assisted"]
                         for t in ("tier1", "tier2")]
        shares[v] = np.mean(auto_assisted)
        defects[v] = s["any_defect_rate"]
    assert shares["optimistic"] > shares["central"] > shares["pessimistic"]
    assert defects["optimistic"] <= defects["central"] <= defects["pessimistic"]


def test_confidence_correlates_with_correctness(params):
    pt, _ = params
    rng = np.random.default_rng(3)
    conf_c, conf_w = [], []
    for _ in range(400):
        d = draw_docs(rng, "tier2", pt, "central")
        conf_c.extend(d.confidence[d.correct])
        conf_w.extend(d.confidence[~d.correct])
    assert np.mean(conf_c) > 0.9
    assert np.mean(conf_w) < 0.6


def test_central_defects_below_asis(params):
    """The design must beat the baseline on residual defects, or Section 7
    has no case."""
    pt, pa = params
    s = ToBeModel(pt, pa, variant="central", seed=19).run(years=8).summary()
    assert s["any_defect_rate"] < 0.092
    assert s["defect_rate"]["extraction"] < 0.09