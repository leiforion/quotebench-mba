#!/usr/bin/env python3
"""T13 harness — Khoory internal investment case, Monte Carlo (decision D7).

Two modes:
  python3 model/monte_carlo.py --validate
      Reproduce the measured as-is baseline from locked register values.
      A model earns the right to project a future only by reproducing a
      measured past (Section 3.3). Must pass before any run is trusted.

  python3 model/monte_carlo.py --run --provisional
      Full Monte Carlo. The --provisional flag is mandatory until the 8.1
      audit (automation rate), 9.3 triangulation (win uplift) and 9.4 cost
      model (run costs) replace the PROVISIONAL inputs below. Outputs from
      provisional runs MUST NOT enter the paper.

All monetary values EUR (D1: AED 1 = 0.23). Seed fixed. Stdlib only.
"""
import argparse
import json
import os
import random
import statistics
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# INPUTS. status: LOCKED = traceable to model/assumptions.csv / decisions.md.
#         PROVISIONAL = placeholder awaiting T10 audit / 9.3 / 9.4 / authors.
# ----------------------------------------------------------------------------
INPUTS = {
    # --- locked register values ---
    "hourly_rate_eur":        {"v": 12.0,   "status": "LOCKED", "src": "BASE-05/06: EUR 22k / 1,840 productive h"},
    "estimators_branch":      {"v": 2,      "status": "LOCKED", "src": "BASE-01"},
    "productive_hours_yr":    {"v": 1840,   "status": "LOCKED", "src": "BASE-05 note"},
    "inquiries_per_month":    {"v": (29, 18, 6),          "status": "LOCKED", "src": "BASE-14"},
    "touch_hours_tier":       {"v": (2.1, 5.5, 11.4),     "status": "LOCKED", "src": "BASE-17"},
    "cost_per_quote_tier":    {"v": (25, 66, 137),        "status": "LOCKED", "src": "BASE-18 (EUR)"},
    "tier_volume_shares":     {"v": (0.55, 0.33, 0.12),   "status": "LOCKED", "src": "BASE-10"},
    "tier_value_shares":      {"v": (0.12, 0.41, 0.47),   "status": "LOCKED", "src": "BASE-11"},
    "win_rate_tier":          {"v": (0.34, 0.27, 0.22),   "status": "LOCKED", "src": "BASE-20"},
    "margin_tier":            {"v": (0.14, 0.17, 0.21),   "status": "LOCKED", "src": "BASE-21"},
    "quality_cost_pct":       {"v": 0.012,  "status": "LOCKED", "src": "BASE-31"},
    "discount_leakage_pct":   {"v": 0.019,  "status": "LOCKED", "src": "BASE-33"},
    "build_cost_eur":         {"v": 92000,  "status": "LOCKED", "src": "FIN-08/D10: AED 400k x 0.23, one engineer-year"},
    "discount_rate":          {"v": 0.12,   "status": "LOCKED", "src": "D11: WACC proxy"},
    "hurdle_rate":            {"v": 0.15,   "status": "LOCKED", "src": "D11: approval hurdle"},
    "horizon_years":          {"v": 5,      "status": "LOCKED", "src": "paper convention (9.5)"},

    # --- provisional distributions (triangular low/mode/high) ---
    "automation_rate":        {"v": (0.35, 0.55, 0.75),   "status": "PROVISIONAL", "src": "REPLACE with 8.1 audit range (T10)"},
    "win_uplift_pp":          {"v": (0.00, 0.02, 0.05),   "status": "PROVISIONAL", "src": "REPLACE with 9.3 triangulation; floored at 0 by design"},
    "build_overrun":          {"v": (1.00, 1.05, 1.30),   "status": "PROVISIONAL", "src": "multiplier on FIN-08; +30% tail per 9.5 hostile case"},
    "run_cost_yr_eur":        {"v": (15000, 20000, 27000),"status": "PROVISIONAL", "src": "REPLACE with 9.4: inference/API, licences, 0.2-0.5 FTE maintenance"},
    "change_cost_eur":        {"v": (10000, 18000, 30000),"status": "PROVISIONAL", "src": "REPLACE with 9.4: training + transition productivity dip"},
    "pricing_adoption":       {"v": (0.40, 0.70, 0.90),   "status": "PROVISIONAL", "src": "share of 1.9% leakage actually recovered; author judgement pending pilot"},
    "error_reduction_factor": {"v": None,  "status": "PROVISIONAL", "src": "simplification: = automation_rate (41% of defects are extraction-born, BASE-28; chain argument 4.4)"},

    # --- required from authors ---
    "revenue_branch_eur":     {"v": 5_000_000, "status": "PROVISIONAL", "src": "AUTHORS TO SUPPLY: branch pump revenue; % -of-revenue benefits scale on it"},
    "scale_factor":           {"v": 1.0,    "status": "PROVISIONAL", "src": "1.0 = single branch; multi-branch rollout per 9.1 scaling (see 6.3)"},
    "adoption_ramp":          {"v": (0.5, 0.85, 1.0, 1.0, 1.0), "status": "PROVISIONAL", "src": "benefit ramp Y1-Y5 through 7.10 phases"},
}

N_ITER = 20_000
SEED = 42


def v(name):
    return INPUTS[name]["v"]


def blended(weights, values):
    return sum(w * x for w, x in zip(weights, values))


# ----------------------------------------------------------------------------
# Validation: reproduce the measured baseline
# ----------------------------------------------------------------------------
def validate():
    ok = True

    def check(label, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {label}: model {got:.2f} vs register {want} (tol {tol})")

    print("Baseline validation (locked register values only):")
    ipm = v("inquiries_per_month")
    touch = v("touch_hours_tier")
    rate = v("hourly_rate_eur")

    # 1. direct cost per quote by tier = touch x rate (BASE-18)
    for i, want in enumerate(v("cost_per_quote_tier")):
        check(f"cost/quote tier {i+1}", touch[i] * rate, want, 1.0)

    # 2. annual volume vs log
    annual = sum(ipm) * 12
    check("annual inquiries (tier sum x12 vs 640 log)", annual, 640, 8)

    # 3. weighted average touch hours (quoted in 6.3 as ~4.3)
    shares = v("tier_volume_shares")
    avg_touch = blended(shares, touch)
    check("avg touch hours per inquiry", avg_touch, 4.3, 0.1)

    # 4. estimator utilization on estimation work < 100%
    util = annual * avg_touch / (v("estimators_branch") * v("productive_hours_yr"))
    print(f"  {'PASS' if util < 1 else 'FAIL'}  estimation utilization {util:.0%} of 2 estimators' productive hours")
    ok &= util < 1

    # 5. annual direct quoting labour (baseline economics, 9.1)
    labour = annual * avg_touch * rate
    print(f"  INFO  annual branch quoting labour: EUR {labour:,.0f}")

    # 6. 6.3 crossover volume, labour-only arithmetic (provisional inputs flagged)
    a_lo, a_c, a_hi = v("automation_rate")
    r_lo, r_c, r_hi = v("run_cost_yr_eur")
    annualized = v("build_cost_eur") / v("horizon_years")
    for a, r, label in [(a_c, r_c, "central"), (a_hi, r_lo, "favourable")]:
        cross = (annualized + r) / (avg_touch * rate * a)
        print(f"  INFO  6.3 crossover volume ({label}, PROVISIONAL): {cross:,.0f} RFQs/yr")

    print("VALIDATION", "PASSED" if ok else "FAILED")
    return ok


# ----------------------------------------------------------------------------
# Cash-flow model
# ----------------------------------------------------------------------------
def cashflows(sample):
    """Return list of net cash flows [Y0, Y1..Y5] for one parameter sample."""
    annual_inq = sum(v("inquiries_per_month")) * 12 * v("scale_factor")
    avg_touch = blended(v("tier_volume_shares"), v("touch_hours_tier"))
    revenue = v("revenue_branch_eur") * v("scale_factor")
    win_blend = blended(v("tier_value_shares"), v("win_rate_tier"))
    margin_blend = blended(v("tier_value_shares"), v("margin_tier"))
    quoted_value = revenue / win_blend

    a = sample["automation_rate"]
    benefits_full = {
        "labour_redeploy": annual_inq * avg_touch * a * v("hourly_rate_eur"),
        "error_savings": v("quality_cost_pct") * revenue * a,  # error_reduction_factor = a
        "discount_recovery": v("discount_leakage_pct") * revenue * sample["pricing_adoption"],
        "win_uplift": quoted_value * sample["win_uplift_pp"] * margin_blend,
    }
    total_full = sum(benefits_full.values())

    y0 = -(v("build_cost_eur") * sample["build_overrun"] + sample["change_cost"])
    flows = [y0]
    for ramp in v("adoption_ramp"):
        flows.append(total_full * ramp - sample["run_cost"])
    return flows, benefits_full


def npv(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows, lo=-0.9, hi=5.0):
    f_lo, f_hi = npv(lo, flows), npv(hi, flows)
    if f_lo * f_hi > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        if npv(mid, flows) * f_lo <= 0:
            hi = mid
        else:
            lo, f_lo = mid, npv(mid, flows)
    return (lo + hi) / 2


def payback(flows):
    cum = 0.0
    for t, cf in enumerate(flows):
        cum += cf
        if cum >= 0 and t > 0:
            prev = cum - cf
            return t - 1 + (-prev / cf) if cf else t
    return None


def draw(rng):
    return {
        "automation_rate": rng.triangular(*v("automation_rate")),
        "win_uplift_pp": rng.triangular(*v("win_uplift_pp")),
        "build_overrun": rng.triangular(*v("build_overrun")),
        "run_cost": rng.triangular(*v("run_cost_yr_eur")),
        "change_cost": rng.triangular(*v("change_cost_eur")),
        "pricing_adoption": rng.triangular(*v("pricing_adoption")),
    }


def central_sample():
    return {
        "automation_rate": v("automation_rate")[1],
        "win_uplift_pp": v("win_uplift_pp")[1],
        "build_overrun": v("build_overrun")[1],
        "run_cost": v("run_cost_yr_eur")[1],
        "change_cost": v("change_cost_eur")[1],
        "pricing_adoption": v("pricing_adoption")[1],
    }


def pct(sorted_xs, p):
    i = max(0, min(len(sorted_xs) - 1, int(p / 100 * len(sorted_xs))))
    return sorted_xs[i]


def run():
    rng = random.Random(SEED)
    d_rate, h_rate = v("discount_rate"), v("hurdle_rate")

    npvs, irrs, paybacks, clears = [], [], [], 0
    for _ in range(N_ITER):
        flows, _ = cashflows(draw(rng))
        npvs.append(npv(d_rate, flows))
        r = irr(flows)
        if r is not None:
            irrs.append(r)
        pb = payback(flows)
        if pb is not None:
            paybacks.append(pb)
        if npv(h_rate, flows) > 0:
            clears += 1
    npvs.sort()

    # tornado: one-at-a-time low/high on each distribution, others central
    tornado = {}
    base_flows, _ = cashflows(central_sample())
    base_npv = npv(d_rate, base_flows)
    for key, iname in [("automation_rate", "automation_rate"), ("win_uplift_pp", "win_uplift_pp"),
                       ("build_overrun", "build_overrun"), ("run_cost", "run_cost_yr_eur"),
                       ("change_cost", "change_cost_eur"), ("pricing_adoption", "pricing_adoption")]:
        lo_s, hi_s = central_sample(), central_sample()
        lo_s[key] = v(iname)[0]
        hi_s[key] = v(iname)[2]
        tornado[key] = sorted([npv(d_rate, cashflows(lo_s)[0]), npv(d_rate, cashflows(hi_s)[0])])

    # hostile conservative case: automation 50% of central, zero uplift, +30% build
    cons = central_sample()
    cons["automation_rate"] = 0.5 * v("automation_rate")[1]
    cons["win_uplift_pp"] = 0.0
    cons["build_overrun"] = 1.30
    cons_flows, cons_benefits = cashflows(cons)

    results = {
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "seed": SEED, "iterations": N_ITER,
        "input_status": {k: d["status"] for k, d in INPUTS.items()},
        "provisional_inputs": [k for k, d in INPUTS.items() if d["status"] == "PROVISIONAL"],
        "npv_at_12pct": {"P10": pct(npvs, 10), "P50": pct(npvs, 50), "P90": pct(npvs, 90)},
        "prob_clearing_15pct_hurdle": clears / N_ITER,
        "irr_median": statistics.median(irrs) if irrs else None,
        "payback_median_years": statistics.median(paybacks) if paybacks else None,
        "tornado_npv_ranges": tornado,
        "conservative_case": {
            "npv_at_12pct": npv(d_rate, cons_flows),
            "npv_at_15pct_hurdle": npv(h_rate, cons_flows),
            "clears_hurdle_on_cost_error_discount_alone": npv(h_rate, cons_flows) > 0,
            "benefits_full_year": cons_benefits,
        },
    }

    print(f"PROVISIONAL RUN — {len(results['provisional_inputs'])} inputs are placeholders; not for the paper.\n")
    print(f"NPV @12%: P10 {results['npv_at_12pct']['P10']:>10,.0f}  P50 {results['npv_at_12pct']['P50']:>10,.0f}  P90 {results['npv_at_12pct']['P90']:>10,.0f} EUR")
    print(f"P(clears 15% hurdle): {results['prob_clearing_15pct_hurdle']:.1%}")
    print(f"IRR median: {results['irr_median']:.1%}   Payback median: {results['payback_median_years']:.1f} yrs")
    print("Tornado (NPV range, EUR):")
    for k, (lo, hi) in sorted(tornado.items(), key=lambda kv: -(kv[1][1] - kv[1][0])):
        print(f"  {k:<18} {lo:>10,.0f} .. {hi:>10,.0f}   (width {hi-lo:,.0f})")
    cc = results["conservative_case"]
    print(f"Conservative case: NPV@12% {cc['npv_at_12pct']:,.0f}; @15% hurdle {cc['npv_at_15pct_hurdle']:,.0f} -> "
          f"{'CLEARS' if cc['clears_hurdle_on_cost_error_discount_alone'] else 'DOES NOT CLEAR'} on cost+error+discount alone")

    outdir = os.path.join(BASE, "results")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"mc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_PROVISIONAL.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=1)
    print(f"\nmanifest: {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--provisional", action="store_true",
                    help="acknowledge that PROVISIONAL inputs are placeholders")
    args = ap.parse_args()
    if args.validate:
        raise SystemExit(0 if validate() else 1)
    if args.run:
        if not args.provisional:
            raise SystemExit("Refusing to run: pass --provisional to acknowledge placeholder "
                             "inputs (8.1 audit / 9.3 / 9.4 not yet available). "
                             "Outputs must not enter the paper.")
        if not validate():
            raise SystemExit("Baseline validation failed; fix before running.")
        print()
        run()
    if not (args.validate or args.run):
        ap.print_help()
