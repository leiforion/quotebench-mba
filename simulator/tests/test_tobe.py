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
    """System up, extraction success forced to zero. Tiers 1-2: no route clears
    C2, the assist credit vanishes, touch collapses to as-is. Tier 3 (7.2):
    always runs the engines + full review, so it does NOT fall back to manual -
    its touch stays at the full-review level (engines draft regardless of
    extraction) while its defects spike (every field wrong, only flagged-rate
    review). This is the design's intended asymmetry: robust capacity gain,
    extraction-dependent quality gain."""
    import copy
    pt, pa = params
    # touch-continuity is cleanest on design (b) (engines + full review, no
    # verification add-on); design (c) adds verification touch, checked below.
    ptb = copy.deepcopy(pt)
    ptb["tier3_design"] = "b"
    res = ToBeModel(ptb, pa, seed=11, extraction_override=0.0).run(years=8)
    s = res.summary()
    senior_speed = next(e["speed"] for e in pa["estimators"]
                        if e.get("skill", e["name"]) == "senior")
    for t in ("tier1", "tier2"):
        assert s["route_mix"][t]["manual"] > 0.999
        tgt = pa["calibration_targets"]["touch_median_h"][t]
        assert abs(s["eng_touch_median_wh"][t] - tgt) <= TOL * tgt
    # Tier 3 stays in the full-review lane (never manual) even at zero extraction
    assert s["route_mix"]["tier3"]["assisted_full"] > 0.999
    assert s["route_mix"]["tier3"]["manual"] < 0.001
    # touch is cut by the full-review credit off the as-is Tier-3 touch (senior)
    credit = pt["full_review_touch_credit"]["central"]
    tgt3 = pa["calibration_targets"]["touch_median_h"]["tier3"] * senior_speed \
        * (1.0 - credit)
    assert abs(s["eng_touch_median_wh"]["tier3"] - tgt3) <= TOL * tgt3
    # zero extraction => Tier 3 full review cannot save bad fields: D24 means
    # most survivors now PROPAGATE (critical misreads -> calc/selection), so the
    # material classes spike while cheap extraction survivors persist too.
    assert s["defect_rate"]["extraction"] > 0.0
    assert s["material_rate_by_tier"]["tier3"] > 0.0
    # design (c) source verification adds engineer touch on top of (b)
    sc = ToBeModel(pt, pa, seed=11, extraction_override=0.0).run(years=8).summary()
    assert sc["eng_touch_median_wh"]["tier3"] > s["eng_touch_median_wh"]["tier3"]


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


def test_asis_material_reproduces_audit(params):
    """D24 fix: the as-is MATERIAL rate must reproduce the paper's audit (BASE-19
    6/11/19%, 9.2% company). Every hand-built audited defect is material (wrong
    model / price / missed spec), so as-is material == p_defective by tier."""
    pt, pa = params
    s = ToBeModel(pt, pa, seed=5, degraded=True).run(years=12).summary()
    m = s["material_rate_by_tier"]
    for t, target in (("tier1", 0.06), ("tier2", 0.11), ("tier3", 0.19)):
        assert abs(m[t] - target) <= 0.10 * target + 0.01
    assert abs(s["material_rate"] - 0.092) <= 0.015


def test_critical_misread_propagates_to_calc_or_selection(params):
    """D24: a misread that survives review on a CRITICAL field is priced as a
    calculation or selection defect, not a cheap extraction typo. Non-critical
    survivors stay in the (immaterial) extraction class. class_mult=0 zeroes the
    deterministic system rates so only propagation shows; error_mult forces the
    wrong field to survive review."""
    from sim.capability import DocsDraw, draw_system_defects
    pt, _ = params
    docs = DocsDraw("clean_digital", 1, 1, np.array([False]),
                    np.array([0.95]), np.array([False]))   # 1 wrong, unflagged
    rng = np.random.default_rng(0)
    off = {"calculation": 0.0, "selection": 0.0, "pricing": 0.0}

    sel = draw_system_defects(rng, docs, "senior", "assisted", pt, 100.0,
                              class_mult=off, crit_share=1.0, p_select_change=1.0)
    assert "selection" in sel and "extraction" not in sel
    calc = draw_system_defects(rng, docs, "senior", "assisted", pt, 100.0,
                               class_mult=off, crit_share=1.0, p_select_change=0.0)
    assert "calculation" in calc and "extraction" not in calc
    extr = draw_system_defects(rng, docs, "senior", "assisted", pt, 100.0,
                               class_mult=off, crit_share=0.0, p_select_change=1.0)
    assert extr == ["extraction"]                      # non-critical: immaterial
    # design (c) source verification catches the critical misread outright
    caught = draw_system_defects(rng, docs, "senior", "assisted_full", pt, 100.0,
                                 class_mult=off, crit_share=1.0, p_select_change=1.0,
                                 fr_unflagged_miss={"senior": 1.0, "mid": 1.0},
                                 verify_critical=True, verify_miss=0.0)
    assert caught == []


def test_central_beats_asis_on_error_cost(params):
    """D23: the escape gate is value-proportional error COST, not raw count. The
    design must beat the baseline on error cost - the engines kill the expensive
    calc/selection/pricing classes - even though it may ship MORE cheap
    extraction defects by count on the high-field Tier-3 full-review jobs."""
    pt, pa = params
    from sim.config import load_econ
    from sim.economics import lane_economics, ref_value_from_records
    pe = load_econ()
    asis_res = ToBeModel(pt, pa, seed=19, degraded=True).run(years=6)
    rv = (ref_value_from_records(asis_res)
          if pe.get("error_cost_value_proportional") else None)
    asis = lane_economics(asis_res, "asis", pe, pt, seed=19, ref_value=rv)
    tobe_res = ToBeModel(pt, pa, variant="central", seed=19).run(years=6)
    tobe = lane_economics(tobe_res, "tobe", pe, pt, seed=19, ref_value=rv)
    assert tobe.quality_cost_eur < asis.quality_cost_eur          # cost escape gate
    # the engines must cut the expensive non-extraction classes below as-is
    s = tobe_res.summary()
    assert s["defect_rate"]["calculation"] < 0.035
    assert s["defect_rate"]["selection"] < 0.05
    assert s["defect_rate"]["pricing"] < 0.04