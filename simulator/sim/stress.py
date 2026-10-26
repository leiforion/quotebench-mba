"""SIM-4: stress-test harness and kill-criteria finder.

Named adverse scenarios (scenarios/*.yaml) re-run the paired DES with
overridden parameters and price the central investment case under each.
The tornado ranks the financial parameters one-at-a-time, and the
kill-criteria finder bisects each stressor to the boundary where NPV at the
15% hurdle turns negative. Those boundaries feed Section 11 kill criteria
and 9.6 sensitivity: "the case fails if X falls below Y" stated as numbers.
"""
import copy
import glob
import os

import numpy as np
import yaml

from .config import BASE, load_asis, load_tobe, load_econ
from .economics import (LaneEconomics, automation_rate, build_anchors, cashflows,
                        company_revenue, compute_ref_value, lane_economics,
                        lost_bid_central, npv, run_cost_triangular,
                        scale_company_values)
from .tobe import ToBeModel

SCENARIO_DIR = os.path.join(BASE, "scenarios")
STRESS_SEEDS = [101, 102]   # lighter than the pnl anchors; stress is relative
STRESS_YEARS = 6


def load_scenarios():
    out = []
    for path in sorted(glob.glob(os.path.join(SCENARIO_DIR, "*.yaml"))):
        with open(path) as f:
            out.append(yaml.safe_load(f))
    return out


def central(tri):
    return tri[1]


def fin_centrals(pe, sc=None, infra_annual_eur=0.0):
    """Central financial draws, with scenario overrides applied."""
    fin = pe["financial"]
    sc = sc or {}
    return {
        "win_uplift_pp": sc.get("win_uplift_pp",
                                central(pe["win_uplift_pp"]["triangular"])),
        "build_overrun": sc.get("build_overrun",
                                central(fin["build_overrun_triangular"])),
        "run_cost": sc.get("run_cost",
                           central(run_cost_triangular(pe, infra_annual_eur))),
        "change_cost": sc.get("change_cost",
                              central(fin["change_cost_triangular"])),
        "p_loss": sc.get("p_loss", lost_bid_central(pe)),
    }


def apply_overrides(pa, pt, sc):
    pa, pt = copy.deepcopy(pa), copy.deepcopy(pt)
    if "arrivals_multiplier" in sc:
        for t in pa["arrivals_per_month"]:
            pa["arrivals_per_month"][t] *= sc["arrivals_multiplier"]
    if "estimators" in sc:
        pa["estimators"] = sc["estimators"]
    if sc.get("disable_auto"):
        pt["routing"]["C1"] = 2.0          # unreachable: no auto-drafts
    if "assist_credit_multiplier" in sc:
        for v in pt["manual_assist_credit"]:
            pt["manual_assist_credit"][v] *= sc["assist_credit_multiplier"]
    if "full_review_unflagged_miss" in sc:
        for v in pt["full_review_unflagged_miss"]:
            pt["full_review_unflagged_miss"][v] = sc["full_review_unflagged_miss"]
    if "tier3_design" in sc:
        pt["tier3_design"] = sc["tier3_design"]
    if "critical_field_share_variant" in sc:   # pin crit share to one variant's
        cv = sc["critical_field_share_variant"]  # values across all run variants
        for t in pt["critical_field_share"]:
            val = pt["critical_field_share"][t][cv]
            for v in pt["critical_field_share"][t]:
                pt["critical_field_share"][t][v] = val
    return pa, pt


def scenario_anchors(pa, pt, pe, variant="central",
                     seeds=STRESS_SEEDS, years=STRESS_YEARS, jobs=None):
    """As-is + one to-be variant, averaged over seeds. Company value scaling is
    applied so scenario anchors are at the same company scale as the base. The
    2 seeds x (as-is + to-be) replications run in parallel."""
    from .economics import _anchor_task, avg_lane_economics
    from .parallel import pmap
    pe, pt = scale_company_values(pe, pt)
    ref_value = compute_ref_value(pe, pt, pa, seeds[0], years)

    tasks = [(pe, pt, pa, "asis", None, s, years, ref_value) for s in seeds]
    tasks += [(pe, pt, pa, "tobe", variant, s, years, ref_value) for s in seeds]
    results = pmap(_anchor_task, tasks, jobs=jobs, desc="scenario DES")
    asis = avg_lane_economics([r[2] for r in results if r[0] == "asis"])
    tobe = avg_lane_economics([r[2] for r in results if r[0] == "tobe"])
    return asis, tobe


def case_npvs(asis, tobe, scale, pe, fin_vals):
    fin = pe["financial"]
    comp = pe["company"]
    p_loss = fin_vals.get("p_loss", 0.0)
    benefits = (automation_rate(asis, tobe) * comp["n_estimators"]
                * comp["loaded_cost_eur"]
                + scale * (asis.quality_cost_eur - tobe.quality_cost_eur)
                + fin_vals["win_uplift_pp"] * company_revenue(pe, asis)
                * comp["blended_margin"]
                + p_loss * (asis.lost_bid_base_eur - tobe.lost_bid_base_eur))
    flows = cashflows(benefits, fin, fin_vals["build_overrun"],
                      fin_vals["run_cost"], fin_vals["change_cost"])
    return {
        "benefits_yr": benefits,
        "npv12": npv(fin["discount_rate"], flows),
        "npv_hurdle": npv(fin["hurdle_rate"], flows),
    }


def run_scenarios(pa, pt, pe, base_asis, base_tobe, scale, verbose=True,
                  infra_annual_eur=0.0, jobs=None):
    from .runlog import log
    rows = []
    base = case_npvs(base_asis, base_tobe, scale, pe,
                     fin_centrals(pe, infra_annual_eur=infra_annual_eur))
    rows.append({"name": "base_central", "desc": "no stress", **base})
    scenarios = load_scenarios()
    for i, sc in enumerate(scenarios, 1):
        log(f"scenario {i}/{len(scenarios)}: {sc['name']}")
        if sc.get("reuse_base_anchors"):
            asis, tobe = base_asis, base_tobe
        else:
            sa, st = apply_overrides(pa, pt, sc)
            asis, tobe = scenario_anchors(sa, st, pe,
                                          variant=sc.get("variant", "central"),
                                          jobs=jobs)
        r = case_npvs(asis, tobe, scale, pe,
                      fin_centrals(pe, sc, infra_annual_eur=infra_annual_eur))
        rows.append({"name": sc["name"], "desc": sc["description"], **r})
        if verbose:
            print(f"  {sc['name']:<24} benefits {r['benefits_yr']:>9,.0f}  "
                  f"NPV@12% {r['npv12']:>9,.0f}  @hurdle {r['npv_hurdle']:>9,.0f}  "
                  f"{'CLEARS' if r['npv_hurdle'] > 0 else 'FAILS'}")
    return rows


def tornado(pe, base_asis, anchors3, scale, infra_annual_eur=0.0):
    """One-at-a-time low/high NPV@12% ranges over the financial levers.
    anchors3: {variant: LaneEconomics} from economics.build_anchors. The
    DES-level Tier-3 full-review miss lever is added by stress_all (it needs a
    DES re-run, so it is not computable from cached anchors alone)."""
    fin = pe["financial"]
    run_tri = run_cost_triangular(pe, infra_annual_eur)

    def npv_at(**over):
        w = over.pop("extraction", None)
        tobe = anchors3["central"] if w is None else \
            anchors3["pessimistic"] if w == 0 else anchors3["optimistic"]
        vals = fin_centrals(pe, infra_annual_eur=infra_annual_eur)
        vals.update(over)
        return case_npvs(base_asis, tobe, scale, pe, vals)["npv12"]

    # Plain-label levers for Exhibit 9.3. The inert defect-killed-bid sweep is
    # dropped (central p_loss = 0 -> zero width). The two DES-level bars ("wrong
    # values slipping past review", "share of critical fields") are appended by
    # the figure/stress drivers, which can re-run the anchors.
    levers = {
        "document readability (5.2)": [npv_at(extraction=0), npv_at(extraction=1)],
        "extra tenders won (0-5% of revenue)": [
            npv_at(win_uplift_pp=pe["win_uplift_pp"]["triangular"][0]),
            npv_at(win_uplift_pp=pe["win_uplift_pp"]["triangular"][2])],
        "build overrun": [
            npv_at(build_overrun=fin["build_overrun_triangular"][2]),
            npv_at(build_overrun=fin["build_overrun_triangular"][0])],
        "running cost": [npv_at(run_cost=run_tri[2]),
                         npv_at(run_cost=run_tri[0])],
        "change cost": [npv_at(change_cost=fin["change_cost_triangular"][2]),
                        npv_at(change_cost=fin["change_cost_triangular"][0])],
    }
    return {k: sorted(v) for k, v in levers.items()}


def fr_miss_tornado_bar(pe, pa, pt, base_asis, scale, infra_annual_eur=0.0,
                        jobs=None):
    """DES-level tornado bar for the Tier-3 full-review automation-bias miss
    rate: re-run the central to-be anchor at the parameter's [opt, pess] bounds
    (extraction held central) and price at central financials."""
    fr_tri = pt["full_review_unflagged_miss"]

    def npv(val):
        _, st = apply_overrides(pa, pt, {"full_review_unflagged_miss": val})
        _, tobe = scenario_anchors(pa, st, pe, variant="central", jobs=jobs)
        vals = fin_centrals(pe, infra_annual_eur=infra_annual_eur)
        return case_npvs(base_asis, tobe, scale, pe, vals)["npv12"]

    return sorted([npv(fr_tri["optimistic"]), npv(fr_tri["pessimistic"])])


def crit_share_tornado_bar(pe, pa, pt, base_asis, scale, infra_annual_eur=0.0,
                           jobs=None):
    """DES-level tornado bar for the D24 critical-field share: re-run the central
    to-be anchor with the critical share pinned to its optimistic vs pessimistic
    values (extraction held central) and price at central financials."""
    def npv(variant_label):
        _, st = apply_overrides(pa, pt,
                                {"critical_field_share_variant": variant_label})
        _, tobe = scenario_anchors(pa, st, pe, variant="central", jobs=jobs)
        vals = fin_centrals(pe, infra_annual_eur=infra_annual_eur)
        return case_npvs(base_asis, tobe, scale, pe, vals)["npv12"]

    return sorted([npv("optimistic"), npv("pessimistic")])


def bisect_boundary(f, lo, hi, iters=24):
    """Find x where f crosses zero, assuming f(lo) and f(hi) differ in sign.
    Returns None if no sign change (the case never fails on this axis)."""
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0:
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if f_mid * f_lo <= 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def kill_criteria(pa, pt, pe, base_asis, anchors3, scale, verbose=True,
                  infra_annual_eur=0.0, jobs=None):
    """Bisection per stressor to the NPV@hurdle = 0 boundary."""
    fin = pe["financial"]
    results = {}

    def hurdle_npv(tobe=None, **over):
        vals = fin_centrals(pe, infra_annual_eur=infra_annual_eur)
        vals.update(over)
        return case_npvs(base_asis, tobe or anchors3["central"],
                         scale, pe, vals)["npv_hurdle"]

    def interp(w):
        lo, mid, hi = (anchors3["pessimistic"], anchors3["central"],
                       anchors3["optimistic"])
        a, b, t = (lo, mid, w * 2) if w < 0.5 else (mid, hi, (w - 0.5) * 2)
        out = LaneEconomics()
        for fld in vars(out):
            setattr(out, fld, getattr(a, fld) + t * (getattr(b, fld) - getattr(a, fld)))
        return out

    # arithmetic stressors (cheap bisection)
    results["win_uplift_pp (below)"] = bisect_boundary(
        lambda x: hurdle_npv(win_uplift_pp=x), 0.0, 0.05)
    results["extraction weight (below)"] = bisect_boundary(
        lambda w: hurdle_npv(tobe=interp(w)), 0.0, 1.0)
    results["build multiplier (above)"] = bisect_boundary(
        lambda x: hurdle_npv(build_overrun=x), 1.0, 6.0)
    results["run cost EUR/yr (above)"] = bisect_boundary(
        lambda x: hurdle_npv(run_cost=x), 15000, 200000)

    # demand multiplier: DES-level bisection (coarser: 7 iterations, 1 seed)
    cache = {}

    def demand_hurdle(m):
        m = round(m, 3)
        if m not in cache:
            sa, st = apply_overrides(pa, pt, {"arrivals_multiplier": m})
            asis, tobe = scenario_anchors(sa, st, pe, seeds=[101], years=5,
                                          jobs=jobs)
            cache[m] = case_npvs(asis, tobe, scale, pe,
                                 fin_centrals(pe, infra_annual_eur=infra_annual_eur)
                                 )["npv_hurdle"]
        return cache[m]

    results["demand multiplier (below)"] = bisect_boundary(
        demand_hurdle, 0.2, 1.0, iters=7)

    if verbose:
        for k, v in results.items():
            if v is None:
                print(f"  {k:<28} no failure boundary in tested range")
            else:
                print(f"  {k:<28} {v:,.3f}")
    return results


def stress_all(seed=42, verbose=True, jobs=None):
    from .manifest import write_manifest
    from .infra import cost_model
    from .runlog import log
    pa, pt, pe = load_asis(), load_tobe(), load_econ()
    infra_annual = cost_model()["annual_full_eur"]

    log("building base anchors (3 variants + as-is)...")
    base_asis, anchors3, scale = build_anchors(pe, pt, pa, jobs=jobs)
    base_tobe = anchors3["central"]

    print("\nScenario table (central financial draws):")
    rows = run_scenarios(pa, pt, pe, base_asis, base_tobe, scale,
                         verbose=verbose, infra_annual_eur=infra_annual,
                         jobs=jobs)

    log("computing tornado ranges")
    print("\nTornado (NPV@12% one-at-a-time ranges, EUR):")
    tor = tornado(pe, base_asis, anchors3, scale, infra_annual_eur=infra_annual)
    tor["wrong values slipping past review"] = fr_miss_tornado_bar(
        pe, pa, pt, base_asis, scale, infra_annual_eur=infra_annual, jobs=jobs)
    tor["share of critical fields"] = crit_share_tornado_bar(
        pe, pa, pt, base_asis, scale, infra_annual_eur=infra_annual, jobs=jobs)
    for k, (lo, hi) in sorted(tor.items(), key=lambda kv: -(kv[1][1] - kv[1][0])):
        print(f"  {k:<24} {lo:>10,.0f} .. {hi:>10,.0f}   width {hi - lo:>9,.0f}")

    log("finding kill-criteria boundaries (bisection)")
    print("\nKill criteria (NPV at the 15% hurdle turns negative when):")
    kills = kill_criteria(pa, pt, pe, base_asis, anchors3, scale,
                          verbose=verbose, infra_annual_eur=infra_annual,
                          jobs=jobs)

    path = write_manifest("stress", seed, STRESS_YEARS, {
        "scenarios": [{k: r[k] for k in ("name", "benefits_yr", "npv12",
                                         "npv_hurdle")} for r in rows],
        "tornado": tor,
        "kill_criteria": kills,
        "quality_scale": scale,
    })
    print(f"\nmanifest: {path}")
    return rows, tor, kills
