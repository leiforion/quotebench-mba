"""SIM-4 gates: harness logic tested on synthetic anchors (fast, no DES);
one integration check that scenario overrides actually reach the parameters.
"""
import numpy as np

from sim.config import load_asis, load_econ, load_tobe
from sim.economics import LaneEconomics
from sim.stress import (apply_overrides, bisect_boundary, case_npvs,
                        fin_centrals, load_scenarios, tornado)


def lane(labour, quality, mwq):
    e = LaneEconomics()
    e.labour_eur, e.quality_cost_eur = labour, quality
    e.margin_weighted_quoted = mwq
    return e


ASIS = lane(34000, 25000, 0)
TOBE = lane(17000, 22000, 4.3e6)


def test_scenarios_load_and_are_named():
    scs = load_scenarios()
    names = {s["name"] for s in scs}
    assert {"demand_surge", "demand_collapse", "senior_attrition",
            "extraction_pessimistic", "elasticity_zero", "build_overrun_30",
            "build_overrun_60", "adoption_failure"} <= names
    assert all(s.get("description") for s in scs)


def test_overrides_reach_parameters():
    pa, pt = load_asis(), load_tobe()
    sa, st = apply_overrides(pa, pt, {"arrivals_multiplier": 1.4,
                                      "disable_auto": True,
                                      "assist_credit_multiplier": 0.5})
    assert sa["arrivals_per_month"]["tier1"] == pa["arrivals_per_month"]["tier1"] * 1.4
    assert st["routing"]["C1"] == 2.0
    assert st["manual_assist_credit"]["central"] == \
        pt["manual_assist_credit"]["central"] * 0.5
    # originals untouched
    assert pt["routing"]["C1"] == 0.90


def test_elasticity_zero_hurts_npv():
    pe = load_econ()
    scale = 2.3
    base = case_npvs(ASIS, TOBE, scale, pe, fin_centrals(pe))
    zero = case_npvs(ASIS, TOBE, scale, pe,
                     fin_centrals(pe, {"win_uplift_pp": 0.0}))
    assert zero["npv12"] < base["npv12"]


def test_bisection_finds_known_root():
    root = bisect_boundary(lambda x: x - 1.7, 0.0, 5.0)
    assert abs(root - 1.7) < 1e-4
    assert bisect_boundary(lambda x: x + 1.0, 0.0, 5.0) is None


def test_tornado_widths_positive_and_uplift_dominates():
    pe = load_econ()
    anchors3 = {"pessimistic": lane(17000, 30000, 4.0e6),
                "central": TOBE,
                "optimistic": lane(17000, 18000, 4.5e6)}
    tor = tornado(pe, ASIS, anchors3, scale=2.3)
    widths = {k: hi - lo for k, (lo, hi) in tor.items()}
    assert all(w >= 0 for w in widths.values())
    assert max(widths, key=widths.get) == "win uplift (0-5pp)"


def test_build_multiplier_boundary_above_one():
    pe = load_econ()
    from sim.stress import case_npvs as cn

    def f(mult):
        vals = fin_centrals(pe)
        vals["build_overrun"] = mult
        return cn(ASIS, TOBE, 2.3, pe, vals)["npv_hurdle"]

    b = bisect_boundary(f, 1.0, 10.0)
    assert b is not None and b > 1.0