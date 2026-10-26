"""SIM-3 gates: the economics must reproduce its registered baseline before
its projections mean anything.

- value shares hit BASE-11 (12/41/47) within +-2.5pp
- company revenue is DERIVED from the as-is anchor (branch basis, D21) and,
  pro-rated to branch volume, reproduces the stated AED 150M within 5%
- the defect-killed-bid line (D21) is inert at central p_loss = 0
- benefits are monotonic in the extraction variant
- the conservative case computes and reports a verdict either way
- the business offers no discounts, so there is no leakage line to test
"""
import copy

import numpy as np
import pytest

from sim.capability import draw_value_eur
from sim.config import load_asis, load_tobe, load_econ, is_fitted
from sim.economics import (build_anchors, company_revenue, conservative_case,
                           mc_from_anchors, VARIANTS)


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


def test_revenue_matches_branch_within_5pct(econ_setup):
    _, _, pe, asis, _, _ = econ_setup
    # D21: the AED 150M (~EUR 35.3M) is the BRANCH, so company revenue is DERIVED
    # from the as-is anchor at company volume (~EUR 300M). The gate: pro-rated
    # back to branch volume it must reproduce the stated branch revenue within 5%.
    comp = pe["company"]
    assert comp["revenue_basis"] == "branch"
    rev = company_revenue(pe, asis)
    assert rev == asis.won_value_eur            # derived, not hard-coded
    assert 250e6 < rev < 350e6                  # company scale, not branch scale
    implied_branch = (rev * comp["branch"]["inquiries_per_year"]
                      / comp["inquiries_per_year"])
    assert abs(implied_branch - comp["branch"]["revenue_eur"]) \
        <= 0.05 * comp["branch"]["revenue_eur"]
    assert asis.quoted_value_eur > asis.won_value_eur   # won / measured win rates


def test_value_proportional_concentrates_in_tier3(econ_setup):
    # D21 fix: per-defect cost scales with the INDIVIDUAL quote value, normalised
    # by ONE company-wide ref_value, so high-value Tier 3 carries more of the as-is
    # error cost than its share of won value. Flat costs (the earlier silent bug)
    # roughly track volume x win and put Tier 3 BELOW its won share.
    _, _, pe, asis, _, _ = econ_setup
    assert pe["error_cost_value_proportional"] is True
    assert asis.ref_value and asis.ref_value > 0        # normaliser is real, not 0
    err, won = asis.error_by_tier, asis.won_by_tier
    assert err and won
    err_share3 = err["tier3"] / sum(err.values())
    won_share3 = won["tier3"] / sum(won.values())
    assert err_share3 > won_share3


def test_lost_bid_zero_is_inert(econ_setup):
    # D21 change 3: central p_loss = 0, so the defect-killed-bid line is wired
    # but contributes nothing; headline results equal change 1 + 2 alone.
    _, _, pe, asis, anchors, scale = econ_setup
    assert pe["error_lost_bid"]["p_loss_triangular"][1] == 0.0
    mc = mc_from_anchors(pe, asis, anchors, scale, seed=42, infra_annual_eur=5000.0)
    assert mc["benefit_medians"]["error_lost_bid"] == 0.0
    pe_off = copy.deepcopy(pe)
    pe_off.pop("error_lost_bid", None)
    mc_off = mc_from_anchors(pe_off, asis, anchors, scale, seed=42,
                             infra_annual_eur=5000.0)
    assert mc["npv12_p10_p50_p90"] == mc_off["npv12_p10_p50_p90"]
    assert mc["p_clears_hurdle"] == mc_off["p_clears_hurdle"]


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


def test_rule_d_zeroes_uplift_for_tier_above_asis():
    """D24 rule D: a tier whose to-be MATERIAL defect rate exceeds as-is has its
    win-uplift contribution zeroed (faster-but-worse quotes can't be assumed to
    win more)."""
    from sim.economics import (LaneEconomics, material_exceed_tiers,
                               uplift_revenue_base, annual_benefits)
    pe = load_econ()
    asis = LaneEconomics()
    asis.won_value_eur, asis.eng_hours, asis.quality_cost_eur = 300e6, 25000, 1.4e6
    asis.won_by_tier = {"tier1": 60e6, "tier2": 120e6, "tier3": 120e6}
    asis.breakdown = {"tier1": {"mat_rate": 0.05}, "tier2": {"mat_rate": 0.095},
                      "tier3": {"mat_rate": 0.159}}
    tobe = LaneEconomics()
    tobe.eng_hours, tobe.quality_cost_eur = 11000, 0.6e6
    tobe.breakdown = {"tier1": {"mat_rate": 0.03}, "tier2": {"mat_rate": 0.06},
                      "tier3": {"mat_rate": 0.20}}        # tier3 above as-is
    exclude = material_exceed_tiers(asis, tobe)
    assert exclude == ("tier3",)
    assert uplift_revenue_base(pe, asis, exclude) == 300e6 - 120e6
    full = annual_benefits(pe, asis, tobe, 1.0, win_uplift_frac=0.02)
    excl = annual_benefits(pe, asis, tobe, 1.0, win_uplift_frac=0.02,
                           exclude_tiers=exclude)
    assert excl["win_uplift_margin"] < full["win_uplift_margin"]
    # no exclusion when every tier is at or below as-is
    tobe.breakdown["tier3"]["mat_rate"] = 0.03
    assert material_exceed_tiers(asis, tobe) == ()


def test_conservative_case_reports_verdict(econ_setup):
    pa, pt, pe, asis, anchors, scale = econ_setup
    cons = conservative_case(pe, pt, pa, asis, anchors, scale)
    assert cons["benefits"]["win_uplift_margin"] == 0.0
    assert isinstance(cons["clears"], (bool, np.bool_))
    # single-branch floor argument: benefits must at least be positive
    assert sum(cons["benefits"].values()) > 0
