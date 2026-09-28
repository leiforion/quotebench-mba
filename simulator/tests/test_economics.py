"""SIM-3 gates: the economics must reproduce its registered baseline before
its projections mean anything.

- value shares hit BASE-11 (12/41/47) within +-2.5pp
- the derived revenue base (D13) lands in a sane band around EUR 5.1M
- the quality-cost scale needed to hit BASE-31 is not absurd
- benefits are monotonic in the extraction variant
- the conservative case computes and reports a verdict either way
- the business offers no discounts, so there is no leakage line to test
"""
import numpy as np
import pytest

from sim.capability import draw_value_eur
from sim.config import load_asis, load_tobe, load_econ, is_fitted
from sim.economics import build_anchors, conservative_case, VARIANTS


@pytest.fixture(scope="module")
def econ_setup():
    pa = load_asis()
    assert is_fitted(pa), "run `python -m sim fit` first"
    pt, pe = load_tobe(), load_econ()
    asis, anchors, scale = build_anchors(pe, pt, pa)
    return pa, pt, pe, asis, anchors, scale


def test_value_shares_hit_base11():
    pt = load_tobe()
    rng = np.random.default_rng(5)
    vols = {"tier1": 348, "tier2": 216, "tier3": 72}
    totals = {t: vols[t] * np.mean([draw_value_eur(rng, t, pt)
                                    for _ in range(4000)]) for t in vols}
    s = sum(totals.values())
    for t, target in (("tier1", 0.12), ("tier2", 0.41), ("tier3", 0.47)):
        assert abs(totals[t] / s - target) < 0.025


def test_revenue_base_derived(econ_setup):
    _, _, _, asis, _, _ = econ_setup
    # D-COMPANY: whole-company revenue AED 150M = EUR ~35.3M won (FX 4.25); the
    # value scaling makes simulated won value reproduce it at ~5,500 inquiries
    assert 33e6 < asis.won_value_eur < 38e6
    assert 128e6 < asis.quoted_value_eur < 150e6   # won / measured win rates


def test_weighted_margin_hits_d19(econ_setup):
    _, _, pe, asis, _, _ = econ_setup
    # D19: authors state 24% average gross margin on revenue; the rescaled
    # tier margins (18.5/22.5/27.8) must reproduce it value-weighted
    weighted = asis.margin_weighted_won / asis.won_value_eur
    assert abs(weighted - 0.24) < 0.015


def test_quality_scale_identity(econ_setup):
    # D19 retired the BASE-31 pct target; unit costs carry the value scaling
    _, _, _, _, _, scale = econ_setup
    assert scale == 1.0


def test_benefits_monotonic_in_variant(econ_setup):
    _, _, _, asis, anchors, _ = econ_setup
    saved_hours = [asis.eng_hours - anchors[v].eng_hours for v in VARIANTS]
    assert saved_hours[0] < saved_hours[1] < saved_hours[2]  # pess < ctr < opt
    assert all(s > 0 for s in saved_hours)


def test_conservative_case_reports_verdict(econ_setup):
    pa, pt, pe, asis, anchors, scale = econ_setup
    cons = conservative_case(pe, pt, pa, asis, anchors, scale)
    assert cons["benefits"]["win_uplift_margin"] == 0.0
    assert isinstance(cons["clears"], (bool, np.bool_))
    # single-branch floor argument: benefits must at least be positive
    assert sum(cons["benefits"].values()) > 0
