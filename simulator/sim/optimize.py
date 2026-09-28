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

from .config import BASE, load_asis, load_econ, load_tobe
from .economics import (LaneEconomics, lane_economics, mc_from_anchors,
                        scale_company_values)
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
    runs, rates = [], []
    for s in OPT_SEEDS:
        res = ToBeModel(pt, pa, seed=s, degraded=True).run(years=OPT_YEARS)
        runs.append(lane_economics(res, "asis", pe, pt, seed=s))
        rates.append(res.summary()["any_defect_rate"])
    asis = avg_lanes(runs)
    if "quality_cost_target_pct" in pe:   # pre-D19 pct calibration
        scale = (pe["quality_cost_target_pct"] * asis.won_value_eur
                 / max(1.0, asis.quality_cost_eur))
    else:                                 # D19: value-scaled unit costs
        scale = 1.0
    return asis, scale, float(np.mean(rates))


def run_routing_combo(pa, pt, c1, c2):
    """DES runs for one (C1, C2); returns raw results per variant + central
    defect rate."""
    pt2 = copy.deepcopy(pt)
    pt2["routing"]["C1"], pt2["routing"]["C2"] = c1, c2
    results = {}
    for v in VARIANTS:
        results[v] = []
        for s in OPT_SEEDS:
            res = ToBeModel(pt2, pa, variant=v, seed=s).run(years=OPT_YEARS)
            res.variant = v
            results[v].append(res)
    defect_rate = float(np.mean([r.summary()["any_defect_rate"]
                                 for r in results["central"]]))
    return pt2, results, defect_rate


def price_combo(pe, pt2, results, asis, scale, seed=42, infra_annual_eur=0.0):
    """Re-price cached DES runs for one routing combo; full MC."""
    anchors = {v: avg_lanes([lane_economics(r, "tobe", pe, pt2, seed=s)
                             for s, r in zip(OPT_SEEDS, results[v])])
               for v in VARIANTS}
    return mc_from_anchors(pe, asis, anchors, scale, seed=seed,
                           infra_annual_eur=infra_annual_eur)


def _combo_task(args):
    """Picklable worker: all DES runs for one (C1, C2) routing combo, priced.
    DES results stay in the child; only the small summary row is returned."""
    pe, pt, pa, c1, c2, asis, scale, infra_annual_eur, seed = args
    pt2, results, defect_rate = run_routing_combo(pa, pt, c1, c2)
    mc = price_combo(pe, pt2, results, asis, scale, seed=seed,
                     infra_annual_eur=infra_annual_eur)
    return {
        "c1": c1, "c2": c2,
        "p50": mc["npv12_p10_p50_p90"][1],
        "p10": mc["npv12_p10_p50_p90"][0],
        "p10_hurdle": mc["npv_hurdle_p10"],
        "p_clears": mc["p_clears_hurdle"],
        "defect_rate": defect_rate,
    }


def select_optimum(rows):
    """Pure selection + constraint-binding report. Each row needs:
    p50, p10_hurdle, defect_rate, defect_cap, feasible flags are derived."""
    for r in rows:
        r["ok_defects"] = r["defect_rate"] <= r["defect_cap"]
        r["ok_tail"] = r["p10_hurdle"] >= 0
        r["feasible"] = r["ok_defects"] and r["ok_tail"]
    feasible = [r for r in rows if r["feasible"]]
    best = max(feasible, key=lambda r: r["p50"]) if feasible else None
    binding = {
        "defects_rejected": sum(not r["ok_defects"] for r in rows),
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
         "7.7;11.1", "proposed", "SIM-5 optimum; pilot validates"],
        ["SIM5-02", "Routing threshold C2 (assisted)", f"{best['c2']:.2f}",
         "min field confidence", "S", f"sim/optimize.py ({manifest})",
         "7.7;11.1", "proposed", "SIM-5 optimum; pilot validates"],
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

    log("as-is baseline (defect cap + quality scale)...")
    asis, scale, defect_cap = asis_baseline(pa, pt, pe)
    print(f"  as-is any-defect rate {defect_cap:.1%} (constraint cap), "
          f"quality scale {scale:.2f}")

    combos = [(c1, c2) for c1 in C1_GRID for c2 in C2_GRID if c2 < c1]
    tasks = [(pe, pt, pa, c1, c2, asis, scale, infra_annual, seed)
             for c1, c2 in combos]
    log(f"routing grid: {len(combos)} (C1,C2) combos")
    rows = pmap(_combo_task, tasks, jobs=jobs, desc="routing combo")
    for r in rows:
        r["defect_cap"] = defect_cap

    best, binding = select_optimum(rows)

    print("\nOperating-point grid (top 8 by P50 NPV@12%):")
    print(f"{'C1':>5}{'C2':>6}{'P50':>11}{'P10@hurdle':>12}"
          f"{'defects':>9}{'feasible':>10}")
    for r in sorted(rows, key=lambda r: -r["p50"])[:8]:
        print(f"{r['c1']:>5.2f}{r['c2']:>6.2f}"
              f"{r['p50']:>11,.0f}{r['p10_hurdle']:>12,.0f}"
              f"{r['defect_rate']:>9.1%}{str(r['feasible']):>10}")

    if best is None:
        print("\nNO FEASIBLE OPERATING POINT — constraints cannot be met.")
    else:
        print(f"\nChosen operating point: C1={best['c1']:.2f} C2={best['c2']:.2f}")
        print(f"  P50 NPV@12% {best['p50']:,.0f}; P10@hurdle "
              f"{best['p10_hurdle']:,.0f}; defects {best['defect_rate']:.1%} "
              f"vs cap {best['defect_cap']:.1%}")
    print(f"Constraint report: {binding['defects_rejected']} points rejected on "
          f"defects, {binding['tail_rejected']} on the P10 tail; "
          f"{binding['n_feasible']} feasible.")
    if binding.get("constraint_binds_at_optimum"):
        print(f"  A constraint BINDS at the optimum: an infeasible point offers "
              f"+{binding['foregone_p50_eur']:,.0f} EUR P50. That gap is the "
              f"price of the error-escape guarantee.")
    else:
        print("  No constraint binds at the optimum: the NPV-best point is "
              "also the defect-safe point.")

    path = write_manifest("optimize", seed, OPT_YEARS, {
        "grid": [{k: r[k] for k in ("c1", "c2", "p50",
                                    "p10_hurdle", "defect_rate", "feasible")}
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
