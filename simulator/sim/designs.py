"""D24 step 4: compare the three Tier-3 designs under the corrected (propagated)
pricing, apply the decision rules, and recommend one.

  a) manual lane with AI prefill (D21)
  b) engines + full engineer review (D22)
  c) engines + full review + mandatory source verification of critical fields

Each design is priced with critical-field propagation on, so a surviving
hydraulic misread is costed as a calculation/selection defect, not a cheap
extraction typo. The gates are (D23) company error cost <= as-is and (D24) no
tier's MATERIAL defect rate above as-is. "Lowest total cost" among gate-passers
is read as the highest P50 NPV (least net cost of ownership).

This module only REPORTS and recommends; parameters_tobe.yaml is hand-written,
so the adopted tier3_design and the SIM-5 C1/C2 are set there by hand.
"""
import copy

import numpy as np

from .asis import TIERS
from .economics import (build_anchors, mc_from_anchors, material_exceed_tiers,
                        scale_company_values)
from .tobe import ToBeModel

DESIGNS = ("a", "b", "c")
LABEL = {"a": "manual + AI prefill",
         "b": "engines + full review",
         "c": "engines + full review + critical verification"}


def _run_design(pe, pt, pa, design, infra_annual_eur, jobs=None, seed=101):
    ptd = copy.deepcopy(pt)
    ptd["tier3_design"] = design
    asis, anchors, scale = build_anchors(pe, ptd, pa, jobs=jobs)
    exclude = material_exceed_tiers(asis, anchors["central"])
    mc = mc_from_anchors(pe, asis, anchors, scale, infra_annual_eur=infra_annual_eur,
                         exclude_tiers=exclude)
    ctr = anchors["central"]
    # one central run for Tier-3 touch-hour distribution (engineer + Innovo tail)
    pes, pts = scale_company_values(pe, ptd)
    res = ToBeModel(pts, pa, variant="central", seed=seed).run(years=6)
    t3 = res.by_tier("touch_eng_wh")["tier3"]

    mat = {t: ctr.breakdown[t]["mat_rate"] for t in TIERS}
    asis_mat = {t: asis.breakdown[t]["mat_rate"] for t in TIERS}
    ok_cost = ctr.quality_cost_eur <= asis.quality_cost_eur
    ok_material = all(mat[t] <= asis_mat[t] + 1e-9 for t in TIERS)
    return {
        "design": design,
        "asis": asis, "anchors": anchors, "scale": scale, "exclude": exclude,
        "t3_mat": mat["tier3"], "asis_t3_mat": asis_mat["tier3"],
        "mat_by_tier": mat, "asis_mat_by_tier": asis_mat,
        "t3_err": scale * ctr.breakdown["tier3"]["error"],
        "asis_t3_err": scale * asis.breakdown["tier3"]["error"],
        "company_err": scale * ctr.quality_cost_eur,
        "asis_company_err": scale * asis.quality_cost_eur,
        "t3_touch_median": float(np.median(t3)),
        "innovo_touch": float(np.percentile(t3, 99)),
        "p50": mc["npv12_p10_p50_p90"][1],
        "ok_cost": ok_cost, "ok_material": ok_material,
        "both_gates": ok_cost and ok_material,
    }


def _apply_rules(r):
    """Decision rules A-C over the design results dict -> (design, rule, note)."""
    c = r["c"]
    if c["both_gates"]:
        return "c", "A", "design (c) meets both gates"
    # Rule B: (c) fails ONLY because Tier-3 material still exceeds as-is
    t12_ok = all(c["mat_by_tier"][t] <= c["asis_mat_by_tier"][t] + 1e-9
                 for t in ("tier1", "tier2"))
    if c["ok_cost"] and not c["ok_material"] and t12_ok \
            and c["t3_mat"] > c["asis_t3_mat"] + 1e-9:
        return "c_widened", "B", ("design (c) fails only on Tier-3 material; "
                                  "widen verification and retest once")
    passing = [d for d in DESIGNS if r[d]["both_gates"]]
    if passing:   # some design passes, but not (c): lowest total cost = max P50
        best = max(passing, key=lambda d: r[d]["p50"])
        return best, "step4", f"gate-passing design with highest P50 NPV ({best})"
    # Rule C: no design meets both gates
    best = min(DESIGNS, key=lambda d: r[d]["t3_mat"])
    return best, "C", ("no design meets both gates; adopt lowest Tier-3 material "
                       "and keep Tier 3 out of the error-reduction benefit")


def _widen_verification(pe, pt, pa, infra_annual_eur, jobs=None):
    """Rule B: widen source verification (deeper check -> lower verify miss, and a
    wider critical set) and re-test design (c) once."""
    ptw = copy.deepcopy(pt)
    ptw["tier3_design"] = "c"
    for v in ptw["critical_verification_miss"]:            # deeper verification
        ptw["critical_verification_miss"][v] *= 0.5
    for v in ptw["verification_minutes_per_critical_field"]:
        ptw["verification_minutes_per_critical_field"][v] *= 1.5
    res = _run_design(pe, ptw, pa, "c", infra_annual_eur, jobs=jobs)
    res["design"] = "c_widened"
    return res


def floor_breakeven(pe, pt, pa, infra_annual_eur, jobs=None):
    """Rule E: only called when the floor NPV@12% is negative. Coarse bisection
    for the critical_field_share multiplier and the verification minutes at which
    the floor (pessimistic) case breaks even."""
    from .economics import build_anchors, conservative_case

    def floor_npv(crit_mult=1.0, verify_min=None):
        ptd = copy.deepcopy(pt)
        ptd["tier3_design"] = "c"
        for t in ptd["critical_field_share"]:
            for v in ptd["critical_field_share"][t]:
                ptd["critical_field_share"][t][v] = min(
                    1.0, ptd["critical_field_share"][t][v] * crit_mult)
        if verify_min is not None:
            for v in ptd["verification_minutes_per_critical_field"]:
                ptd["verification_minutes_per_critical_field"][v] = verify_min
        asis, anchors, scale = build_anchors(pe, ptd, pa, jobs=jobs)
        return conservative_case(pe, ptd, pa, asis, anchors, scale,
                                 infra_annual_eur=infra_annual_eur)["npv_at_12pct"]

    def bisect(f, lo, hi, iters=6):
        if f(lo) * f(hi) > 0:
            return None
        for _ in range(iters):
            mid = (lo + hi) / 2
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2

    crit_mult = bisect(lambda m: floor_npv(crit_mult=m), 2.0, 0.2)
    verify_min = bisect(lambda vm: floor_npv(verify_min=vm), 0.5, 20.0)
    crit_t3 = (pt["critical_field_share"]["tier3"]["central"]
               * (crit_mult or float("nan")))
    return {"crit_mult": crit_mult or float("nan"), "crit_t3": crit_t3,
            "verify_min": verify_min or float("nan")}


def compare_designs(seed=42, jobs=None, verbose=True):
    from .config import load_asis, load_econ, load_tobe
    from .infra import cost_model
    from .runlog import log
    pa, pt, pe = load_asis(), load_tobe(), load_econ()
    infra = cost_model()["annual_full_eur"]

    r = {}
    for d in DESIGNS:
        log(f"design ({d}) {LABEL[d]} ...")
        r[d] = _run_design(pe, pt, pa, d, infra, jobs=jobs)

    design, rule, note = _apply_rules(r)
    if rule == "B":
        log("rule B: widening verification and re-testing design (c) ...")
        r["c_widened"] = _widen_verification(pe, pt, pa, infra, jobs=jobs)
        design = "c_widened" if r["c_widened"]["both_gates"] else \
            min(DESIGNS, key=lambda d: r[d]["t3_mat"])
        rule = "B->adopt" if r["c_widened"]["both_gates"] else "B->C"

    if verbose:
        print("\nThree Tier-3 designs under corrected (propagated) pricing "
              "(central; gates vs as-is):")
        print(f"  as-is Tier-3: material {r['a']['asis_t3_mat']:.1%}, "
              f"error EUR {r['a']['asis_t3_err']:,.0f}; company error cap "
              f"EUR {r['a']['asis_company_err']:,.0f}")
        print(f"  {'design':<40}{'T3 mat%':>8}{'T3 err':>11}{'% cut':>7}"
              f"{'touch h':>9}{'Innovo h':>9}{'gates':>7}{'P50 NPV':>12}")
        for d in [x for x in ("a", "b", "c", "c_widened") if x in r]:
            x = r[d]
            cut = 1 - x["t3_err"] / x["asis_t3_err"] if x["asis_t3_err"] else 0
            gates = ("cost " if x["ok_cost"] else "COST ") + \
                    ("mat" if x["ok_material"] else "MAT")
            print(f"  {d + ') ' + LABEL[d]:<40}{x['t3_mat']:>8.1%}"
                  f"{x['t3_err']:>11,.0f}{cut:>7.0%}{x['t3_touch_median']:>9.1f}"
                  f"{x['innovo_touch']:>9.1f}{gates:>7}{x['p50']:>12,.0f}")
        print(f"\n  ADOPTED: design ({design}) via rule {rule} - {note}")
    return r, design, rule, note
