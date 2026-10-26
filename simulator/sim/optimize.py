"""SIM-5: self-improvement loop over the design's decision variables.

Decision variables: routing thresholds C1 and C2 (7.7) and the value gate V1.
Grid search maximizing P50 NPV@12% subject to two constraints:
  1. error-escape rate <= the as-is baseline (the design must not ship more
     defects than the process it replaces), and
  2. P10 of NPV at the 15% hurdle >= 0 (the downside tail must clear the
     approval rate, not just the median).

Each (C1, C2) routing combo requires its own DES run; the business offers no
discounts, so there is no pricing decision variable to sweep.
The chosen operating point is written back to model/assumptions.csv as
S-tagged rows sourced to this run's manifest: these are the design parameters
the paper recommends for the pilot (7.7, 11.1). The managerial finding is
which constraints bind, not just the optimum.
"""
import copy
import csv
import os

import numpy as np

from .asis import TIERS
from .config import BASE, load_asis, load_econ, load_tobe
from .economics import (LaneEconomics, lane_economics, mc_from_anchors,
                        ref_value_from_records, scale_company_values)
from .tobe import ToBeModel

C1_GRID = [0.85, 0.90, 0.95]
C2_GRID = [0.65, 0.70, 0.75, 0.80]
OPT_SEEDS = [101, 102]
OPT_YEARS = 6
VARIANTS = ("pessimistic", "central", "optimistic")

REGISTER = os.path.normpath(os.path.join(BASE, "..", "model", "assumptions.csv"))


def avg_lanes(lanes):
    out = LaneEconomics()
    for f in vars(out):
        setattr(out, f, float(np.mean([getattr(x, f) for x in lanes])))
    return out


def asis_baseline(pa, pt, pe):
    reslist = [(s, ToBeModel(pt, pa, seed=s, degraded=True).run(years=OPT_YEARS))
               for s in OPT_SEEDS]
    summ = [res.summary() for _, res in reslist]
    rates = [x["any_defect_rate"] for x in summ]
    mats = [x["material_rate_by_tier"] for x in summ]
    asis_mat = {t: float(np.mean([m[t] for m in mats])) for t in TIERS}
    ref_value = (ref_value_from_records(reslist[0][1])
                 if pe.get("error_cost_value_proportional") else None)
    runs = [lane_economics(res, "asis", pe, pt, seed=s, ref_value=ref_value)
            for s, res in reslist]
    asis = avg_lanes(runs)
    if "quality_cost_target_pct" in pe:   # pre-D19 pct calibration
        scale = (pe["quality_cost_target_pct"] * asis.won_value_eur
                 / max(1.0, asis.quality_cost_eur))
    else:                                 # D19: value-scaled unit costs
        scale = 1.0
    return asis, scale, float(np.mean(rates)), ref_value, asis_mat


def run_routing_combo(pa, pt, c1, c2):
    """DES runs for one (C1, C2); returns raw results per variant + central
    defect rate."""
    pt2 = copy.deepcopy(pt)
    pt2["routing"]["C1"], pt2["routing"]["C2"] = c1, c2
    results = {}
    central_summ = []
    for v in VARIANTS:
        results[v] = []
        for s in OPT_SEEDS:
            res = ToBeModel(pt2, pa, variant=v, seed=s).run(years=OPT_YEARS)
            res.variant = v
            results[v].append(res)
            if v == "central":
                central_summ.append(res.summary())
    defect_rate = float(np.mean([x["any_defect_rate"] for x in central_summ]))
    mat_by_tier = {t: float(np.mean([x["material_rate_by_tier"][t]
                                     for x in central_summ])) for t in TIERS}
    return pt2, results, defect_rate, mat_by_tier


def price_combo(pe, pt2, results, asis, scale, seed=42, infra_annual_eur=0.0,
                ref_value=None):
    """Re-price cached DES runs for one routing combo; full MC."""
    anchors = {v: avg_lanes([lane_economics(r, "tobe", pe, pt2, seed=s,
                                            ref_value=ref_value)
                             for s, r in zip(OPT_SEEDS, results[v])])
               for v in VARIANTS}
    mc = mc_from_anchors(pe, asis, anchors, scale, seed=seed,
                         infra_annual_eur=infra_annual_eur)
    return mc, anchors["central"].quality_cost_eur


def _combo_task(args):
    """Picklable worker: all DES runs for one (C1, C2) routing combo, priced.
    DES results stay in the child; only the small summary row is returned."""
    pe, pt, pa, c1, c2, asis, scale, infra_annual_eur, seed, ref_value = args
    pt2, results, defect_rate, mat_by_tier = run_routing_combo(pa, pt, c1, c2)
    mc, error_cost = price_combo(pe, pt2, results, asis, scale, seed=seed,
                                 infra_annual_eur=infra_annual_eur,
                                 ref_value=ref_value)
    return {
        "c1": c1, "c2": c2,
        "p50": mc["npv12_p10_p50_p90"][1],
        "p10": mc["npv12_p10_p50_p90"][0],
        "p10_hurdle": mc["npv_hurdle_p10"],
        "p_clears": mc["p_clears_hurdle"],
        "defect_rate": defect_rate,
        "mat_by_tier": mat_by_tier,
        "error_cost": error_cost,
    }


def select_optimum(rows):
    """Pure selection + constraint-binding report. D24 DUAL gate, feasible iff:
    (1) to-be value-proportional error COST <= as-is (D23); (2) no tier's
    MATERIAL defect rate exceeds its as-is rate; and (3) the P10 of NPV@hurdle is
    non-negative."""
    for r in rows:
        r["ok_cost"] = r["error_cost"] <= r["error_cap"]
        r["ok_material"] = all(r["mat_by_tier"][t] <= r["asis_mat"][t] + 1e-9
                               for t in r["asis_mat"])
        r["ok_tail"] = r["p10_hurdle"] >= 0
        r["feasible"] = r["ok_cost"] and r["ok_material"] and r["ok_tail"]
    feasible = [r for r in rows if r["feasible"]]
    best = max(feasible, key=lambda r: r["p50"]) if feasible else None
    binding = {
        "cost_rejected": sum(not r["ok_cost"] for r in rows),
        "material_rejected": sum(not r["ok_material"] for r in rows),
        "tail_rejected": sum(not r["ok_tail"] for r in rows),
        "n_feasible": len(feasible),
    }
    if best is not None and feasible:
        # does any infeasible point beat the optimum? then a constraint binds
        better_infeasible = [r for r in rows
                             if not r["feasible"] and r["p50"] > best["p50"]]
        binding["constraint_binds_at_optimum"] = bool(better_infeasible)
        binding["foregone_p50_eur"] = (max(r["p50"] for r in better_infeasible)
                                       - best["p50"]) if better_infeasible else 0.0
    return best, binding


def write_register_rows(best, manifest_path, pt):
    """Write the chosen operating point to the assumptions register (S-tagged)."""
    manifest = os.path.basename(manifest_path)
    rows = [
        ["SIM5-01", "Routing threshold C1 (auto-draft)", f"{best['c1']:.2f}",
         "min field confidence", "S", f"sim/optimize.py ({manifest})",
         "7.7;11.1", "proposed",
         "SIM-5 optimum (D24 dual gate: cost + per-tier material defect); adopted in parameters_tobe.yaml; pilot validates"],
        ["SIM5-02", "Routing threshold C2 (assisted)", f"{best['c2']:.2f}",
         "min field confidence", "S", f"sim/optimize.py ({manifest})",
         "7.7;11.1", "proposed",
         "SIM-5 optimum (D24 dual gate: cost + per-tier material defect); adopted in parameters_tobe.yaml; pilot validates"],
        ["SIM5-03", "Value gate V1",
         str(int(pt["routing"]["V1_eur"])), "EUR", "S",
         f"sim/optimize.py ({manifest})", "7.7;11.1", "proposed",
         "Kept at tier-1 band edge (D19-scaled); only gates tier-1 auto-drafts"],
    ]
    with open(REGISTER) as f:
        existing = list(csv.reader(f))
    existing = [r for r in existing if not (r and r[0].startswith("SIM5-"))]
    with open(REGISTER, "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(existing)
        w.writerows(rows)
    return [r[0] for r in rows]


def optimize(seed=42, verbose=True, write_register=True, jobs=None):
    from .manifest import write_manifest
    from .infra import cost_model
    from .parallel import pmap
    from .runlog import log
    pa, pt, pe = load_asis(), load_tobe(), load_econ()
    pe, pt = scale_company_values(pe, pt)
    infra_annual = cost_model()["annual_full_eur"]

    log("as-is baseline (error-cost + material-defect caps + quality scale)...")
    asis, scale, defect_cap, ref_value, asis_mat = asis_baseline(pa, pt, pe)
    error_cap = asis.quality_cost_eur
    print(f"  as-is error-cost cap EUR {error_cap:,.0f} (D23 cost gate); "
          f"as-is material-defect cap by tier "
          f"{'/'.join(f'{asis_mat[t]:.1%}' for t in TIERS)} (D24 dual gate); "
          f"as-is any-defect rate {defect_cap:.1%} (info); scale {scale:.2f}")

    combos = [(c1, c2) for c1 in C1_GRID for c2 in C2_GRID if c2 < c1]
    tasks = [(pe, pt, pa, c1, c2, asis, scale, infra_annual, seed, ref_value)
             for c1, c2 in combos]
    log(f"routing grid: {len(combos)} (C1,C2) combos")
    rows = pmap(_combo_task, tasks, jobs=jobs, desc="routing combo")
    for r in rows:
        r["defect_cap"] = defect_cap
        r["error_cap"] = error_cap
        r["asis_mat"] = asis_mat

    best, binding = select_optimum(rows)

    print("\nOperating-point grid (top 8 by P50 NPV@12%):")
    print(f"{'C1':>5}{'C2':>6}{'P50':>11}{'P10@hurdle':>12}"
          f"{'err cost':>11}{'vs cap':>8}{'T3 mat%':>8}{'okMat':>6}{'feas':>6}")
    for r in sorted(rows, key=lambda r: -r["p50"])[:8]:
        print(f"{r['c1']:>5.2f}{r['c2']:>6.2f}"
              f"{r['p50']:>11,.0f}{r['p10_hurdle']:>12,.0f}"
              f"{r['error_cost']:>11,.0f}{r['error_cost'] / r['error_cap']:>8.0%}"
              f"{r['mat_by_tier']['tier3']:>8.1%}{str(r['ok_material']):>6}"
              f"{str(r['feasible']):>6}")

    if best is None:
        print("\nNO FEASIBLE OPERATING POINT — constraints cannot be met.")
    else:
        matstr = "/".join(f"{best['mat_by_tier'][t]:.1%}" for t in TIERS)
        capstr = "/".join(f"{asis_mat[t]:.1%}" for t in TIERS)
        print(f"\nChosen operating point: C1={best['c1']:.2f} C2={best['c2']:.2f}")
        print(f"  P50 NPV@12% {best['p50']:,.0f}; P10@hurdle "
              f"{best['p10_hurdle']:,.0f}; error cost {best['error_cost']:,.0f} "
              f"vs cap {best['error_cap']:,.0f} "
              f"({best['error_cost'] / best['error_cap']:.0%}); material by tier "
              f"{matstr} vs cap {capstr}")
    print(f"Constraint report: {binding['cost_rejected']} rejected on error cost, "
          f"{binding['material_rejected']} on the material-defect dual gate, "
          f"{binding['tail_rejected']} on the P10 tail; "
          f"{binding['n_feasible']} feasible (D24 dual gate).")
    if binding.get("constraint_binds_at_optimum"):
        print(f"  A constraint BINDS at the optimum: an infeasible point offers "
              f"+{binding['foregone_p50_eur']:,.0f} EUR P50. That gap is the "
              f"price of the error-escape guarantee.")
    else:
        print("  No constraint binds at the optimum: the NPV-best point is "
              "also the defect-safe point.")

    path = write_manifest("optimize", seed, OPT_YEARS, {
        "grid": [{k: r[k] for k in ("c1", "c2", "p50", "p10_hurdle",
                                    "defect_rate", "error_cost", "feasible")}
                 for r in rows],
        "best": {k: best[k] for k in ("c1", "c2", "p50",
                                      "p10_hurdle", "defect_rate")} if best else None,
        "binding": binding,
    })
    print(f"manifest: {path}")

    if best is not None and write_register:
        ids = write_register_rows(best, path, pt)
        print(f"register rows written: {', '.join(ids)} -> model/assumptions.csv")
    return rows, best, binding
