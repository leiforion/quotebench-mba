"""Calibration report: measured register values vs simulated, with gate verdict.

This table is the 8.2 calibration exhibit: the model earns the right to project
a future only by reproducing the measured past.
"""
from .asis import AsIsModel, TIERS
from .config import load_asis, is_fitted, params_checksum
from .manifest import write_manifest

TOL = 0.10


def gate_rows(seed=42, years=12):
    """The calibration table as data (for the SIM-6 figure export)."""
    p = load_asis()
    s = AsIsModel(p, seed=seed).run(years=years)
    summ = s.summary(p["hourly_rate_eur"])
    tgt = p["calibration_targets"]
    rows = []
    for t in TIERS:
        for metric, tkey, skey in (
                ("cycle median (wh)", "cycle_median_wh", "cycle_median_wh"),
                ("cycle P90 (wh)", "cycle_p90_wh", "cycle_p90_wh"),
                ("touch median (h)", "touch_median_h", "touch_median_h"),
                ("cost/quote (EUR)", "cost_per_quote_eur", "cost_per_quote_eur")):
            target, actual = tgt[tkey][t], summ[skey][t]
            verdict = "PASS" if abs(actual - target) <= TOL * target else "FAIL"
            rows.append((metric, t, f"{target:.1f}", f"{actual:.1f}", verdict))
    target, actual = tgt["annual_inquiries"], summ["annual_inquiries"]
    rows.append(("annual inquiries", "all", f"{target:.0f}", f"{actual:.0f}",
                 "PASS" if abs(actual - target) <= 0.08 * target else "FAIL"))
    qs = summ["queue_share_pct"]
    qlo, qhi = tgt["queue_share_pct"]["low"], tgt["queue_share_pct"]["high"]
    rows.append(("queue share (%)", "all", f"{qlo}-{qhi}",
                 "/".join(f"{qs[t]:.0f}" for t in TIERS),
                 "PASS" if all(qlo <= qs[t] <= qhi for t in TIERS) else "FAIL"))
    rows.append(("utilization", "all", "<100%", f"{summ['utilization']:.0%}",
                 "PASS" if summ["utilization"] < 1 else "FAIL"))
    rows.append(("pickup median (wh)", "all", f"{tgt['pickup_median_wh']:.1f}",
                 f"{summ['pickup_median_wh']:.1f}", "info"))
    rows.append(("clarified share", "all", f"{tgt['clarified_share']:.2f}",
                 f"{summ['clarified_share']:.2f}", "info"))
    return rows


def calibration_report(seed=42, years=12, return_summary=False):
    p = load_asis()
    if not is_fitted(p):
        print("Not fitted yet. Run: python -m sim fit")
        return (False, None) if return_summary else False
    s = AsIsModel(p, seed=seed).run(years=years)
    summ = s.summary(p["hourly_rate_eur"])
    tgt = p["calibration_targets"]

    rows, ok = [], True

    def row(metric, t, target, actual, tol=TOL):
        nonlocal ok
        good = abs(actual - target) <= tol * target
        ok &= good
        rows.append((metric, t, target, actual, "PASS" if good else "FAIL"))

    for t in TIERS:
        row("cycle median (wh)", t, tgt["cycle_median_wh"][t], summ["cycle_median_wh"][t])
        row("cycle P90 (wh)", t, tgt["cycle_p90_wh"][t], summ["cycle_p90_wh"][t])
        row("touch median (h)", t, tgt["touch_median_h"][t], summ["touch_median_h"][t])
        row("cost/quote (EUR)", t, tgt["cost_per_quote_eur"][t], summ["cost_per_quote_eur"][t])
    row("annual inquiries", "all", tgt["annual_inquiries"], summ["annual_inquiries"], 0.08)

    print(f"Calibration report  (seed {seed}, {years} simulated years, "
          f"params {params_checksum()})")
    print(f"{'metric':<22}{'tier':<7}{'measured':>10}{'simulated':>11}{'gate':>7}")
    for m, t, target, actual, verdict in rows:
        print(f"{m:<22}{t:<7}{target:>10.1f}{actual:>11.1f}{verdict:>7}")
    qs = summ["queue_share_pct"]
    qlo, qhi = tgt["queue_share_pct"]["low"], tgt["queue_share_pct"]["high"]
    q_ok = all(qlo <= qs[t] <= qhi for t in TIERS)
    ok &= q_ok
    print(f"{'queue share (%)':<22}{'all':<7}{f'{qlo}-{qhi}':>10}"
          f"{'/'.join(f'{qs[t]:.0f}' for t in TIERS):>11}{'PASS' if q_ok else 'FAIL':>7}")
    print(f"{'utilization':<22}{'all':<7}{'<100%':>10}{summ['utilization']:>10.0%}"
          f"{'PASS' if summ['utilization'] < 1 else 'FAIL':>7}")
    # emergent diagnostics (not imposed, not gated)
    print(f"{'pickup median (wh)':<22}{'all':<7}{tgt['pickup_median_wh']:>10.1f}"
          f"{summ['pickup_median_wh']:>11.1f}{'info':>7}")
    print(f"{'clarified share':<22}{'all':<7}{tgt['clarified_share']:>10.2f}"
          f"{summ['clarified_share']:>11.2f}{'info':>7}")
    print(f"\nGATE: {'PASSED — to-be scenarios may run' if ok else 'FAILED — to-be scenarios locked'}")
    path = write_manifest("calibration", seed, years,
                          {"gate": "PASS" if ok else "FAIL", "summary": summ})
    print(f"manifest: {path}")
    summ["_worst_rel_err"] = max(
        abs(a - t) / t for t, a in (
            (tgt["cycle_median_wh"][x], summ["cycle_median_wh"][x]) for x in TIERS))
    return (ok, summ) if return_summary else ok


def tobe_report(variant="central", seed=42, years=8):
    """To-be run summary: cycle vs the as-is baseline, route mix, engineer
    touch, residual defects. All to-be numbers are projections from S-tagged
    design assumptions; the as-is column is the calibrated baseline."""
    from .config import load_tobe
    from .tobe import ToBeModel

    p = load_asis()
    if not is_fitted(p):
        print("As-is not fitted. Run: python -m sim fit")
        return False
    pt = load_tobe()
    res = ToBeModel(pt, p, variant=variant, seed=seed).run(years=years)
    s = res.summary()
    tgt = p["calibration_targets"]

    print(f"To-be projection  (variant {variant}, seed {seed}, {years} simulated "
          f"years, params {params_checksum()})")
    print(f"\n{'metric':<26}{'tier':<7}{'as-is':>9}{'to-be':>9}")
    for t in TIERS:
        print(f"{'cycle median (wh)':<26}{t:<7}{tgt['cycle_median_wh'][t]:>9.1f}"
              f"{s['cycle_median_wh'][t]:>9.1f}")
    for t in TIERS:
        print(f"{'cycle P90 (wh)':<26}{t:<7}{tgt['cycle_p90_wh'][t]:>9.1f}"
              f"{s['cycle_p90_wh'][t]:>9.1f}")
    for t in TIERS:
        print(f"{'engineer touch median (h)':<26}{t:<7}{tgt['touch_median_h'][t]:>9.1f}"
              f"{s['eng_touch_median_wh'][t]:>9.2f}")
    print(f"\n{'route mix':<12}{'auto':>8}{'assisted':>10}{'manual':>8}")
    for t in TIERS:
        m = s["route_mix"][t]
        print(f"{t:<12}{m['auto']:>8.0%}{m['assisted']:>10.0%}{m['manual']:>8.0%}")
    print(f"\n{'residual defect rates':<26}{'as-is':>9}{'to-be':>9}")
    asis_rates = {"extraction": 0.09, "calculation": 0.035,
                  "selection": 0.05, "pricing": 0.04}   # BASE-29
    for cls, r in s["defect_rate"].items():
        print(f"{cls:<26}{asis_rates[cls]:>9.1%}{r:>9.2%}")
    print(f"{'any defect':<26}{'9.2%':>9}{s['any_defect_rate']:>9.2%}")
    print(f"\nreview queue median: {s['review_queue_median_wh']:.2f} wh "
          f"(TOBE-05 assumes 2.5 h; emergent here, diagnostic)")
    print("engineer hours/year: "
          + ", ".join(f"{k} {v:.0f}" for k, v in s["busy_wh_per_year"].items())
          + f"  (as-is total ~{5500 * 4.34:.0f}, company-wide)")
    path = write_manifest("tobe", seed, years,
                          {"variant": variant, "summary": s})
    print(f"manifest: {path}")
    return s


def pnl_report(seed=42, jobs=None):
    """SIM-3 output: company-level operating comparison, emergent automation,
    five-year Monte Carlo investment case, the floor case, and the AWS
    infrastructure cost broken down by service."""
    from .config import load_econ, load_tobe
    from .economics import monte_carlo, conservative_case, run_cost_triangular
    from .infra import cost_model, format_breakdown, write_cost_csv
    from .runlog import log

    p = load_asis()
    if not is_fitted(p):
        print("As-is not fitted. Run: python -m sim fit")
        return False
    pt, pe = load_tobe(), load_econ()
    comp = pe["company"]

    cm = cost_model(ramp=pe["financial"]["adoption_ramp"])
    infra_annual = cm["annual_full_eur"]

    print(f"P&L and investment case  (seed {seed}, params {params_checksum()})")
    log("building DES anchors (3 variants x 3 seeds + as-is baseline)...")
    mc = monte_carlo(pe, pt, p, seed=seed, verbose=True,
                     infra_annual_eur=infra_annual, jobs=jobs)
    log("anchors built; running 20k-draw financial Monte Carlo")
    asis, ctr = mc["asis"], mc["anchors"]["central"]

    print(f"\nAnnual operating economics (as-is vs to-be central, EUR) "
          f"[company-wide]")
    rows = [
        ("quoted value", asis.quoted_value_eur, ctr.quoted_value_eur),
        ("won value (vs revenue input)", asis.won_value_eur, ctr.won_value_eur),
        ("engineer hours", asis.eng_hours, ctr.eng_hours),
        ("quality cost", asis.quality_cost_eur, ctr.quality_cost_eur),
    ]
    print(f"{'':<32}{'as-is':>12}{'to-be':>12}")
    for name, a, b in rows:
        print(f"{name:<32}{a:>12,.0f}{b:>12,.0f}")
    print(f"  won value vs revenue input: {asis.won_value_eur:,.0f} vs "
          f"{comp['revenue_eur']:,.0f} "
          f"({asis.won_value_eur / comp['revenue_eur'] - 1:+.1%})")

    print(f"\nEmergent automation of touch time (DES output, NOT assumed):")
    ar = mc["automation_rate"]
    print(f"  pessimistic {ar['pessimistic']:.0%}   central {ar['central']:.0%}"
          f"   optimistic {ar['optimistic']:.0%}   "
          f"(author reference band 40 / 60 / 85%)")

    print(f"\nAnnual benefit medians (EUR/yr, full adoption):")
    for k, val in mc["benefit_medians"].items():
        print(f"  {k:<22}{val:>10,.0f}")
    print(f"  {'TOTAL':<22}{sum(mc['benefit_medians'].values()):>10,.0f}")

    rc = run_cost_triangular(pe, infra_annual)
    print(f"\nCost structure (EUR):")
    print(f"  build (Y1 engineer):        {pe['financial']['build_cost_eur']:>10,.0f}")
    print(f"  run/yr = maint engineer + AWS infra: "
          f"{pe['financial']['maintenance_engineer_eur']:,.0f} + "
          f"{infra_annual:,.0f} = {rc[1]:,.0f}  (range {rc[0]:,.0f}-{rc[2]:,.0f})")
    print(f"  change (once):              "
          f"{pe['financial']['change_cost_triangular'][1]:>10,.0f}")

    print(f"\nFive-year investment case ({pe['monte_carlo']['iterations']:,} draws):")
    p10, p50, p90 = mc["npv12_p10_p50_p90"]
    print(f"  NPV @12%:  P10 {p10:>10,.0f}   P50 {p50:>10,.0f}   P90 {p90:>10,.0f}")
    print(f"  P(clears 15% hurdle): {mc['p_clears_hurdle']:.1%}")
    print(f"  IRR median: {mc['irr_median']:.1%}   "
          f"payback median: {mc['payback_median_years']:.1f} yrs")

    cons = conservative_case(pe, pt, p, asis, mc["anchors"], mc["quality_scale"],
                             infra_annual_eur=infra_annual)
    print(f"\nFloor case (pessimistic extraction, zero win-uplift, +30% build):")
    for k, val in cons["benefits"].items():
        print(f"  {k:<22}{val:>10,.0f}")
    verdict = "CLEARS" if cons["clears"] else "DOES NOT CLEAR"
    print(f"  NPV @12%: {cons['npv_at_12pct']:,.0f}   "
          f"NPV @15% hurdle: {cons['npv_at_hurdle']:,.0f}")
    print(f"  -> {verdict} the hurdle on cost + error savings alone")

    print()
    print(format_breakdown(cm))
    import os
    from .config import BASE
    csv_path = os.path.join(BASE, "results", "aws_costs_by_service.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    write_cost_csv(cm, csv_path)
    print(f"\nAWS cost table (CSV for the report): {os.path.relpath(csv_path, BASE)}")

    summary = {
        "npv12_p10_p50_p90": mc["npv12_p10_p50_p90"],
        "p_clears_hurdle": mc["p_clears_hurdle"],
        "irr_median": mc["irr_median"],
        "payback_median_years": mc["payback_median_years"],
        "automation_rate": mc["automation_rate"],
        "benefit_medians": mc["benefit_medians"],
        "infra_annual_eur": infra_annual,
        "infra_by_service_eur": cm["by_service_eur"],
        "conservative_case": {k: v for k, v in cons.items() if k != "benefits"},
        "conservative_benefits": cons["benefits"],
        # extra context for the written narrative (sim all)
        "asis_eng_hours": asis.eng_hours,
        "tobe_eng_hours": ctr.eng_hours,
        "asis_won_value_eur": asis.won_value_eur,
        "revenue_input_eur": comp["revenue_eur"],
        "run_cost_central_eur": rc[1],
        "build_cost_eur": pe["financial"]["build_cost_eur"],
        "benefit_total_eur": sum(mc["benefit_medians"].values()),
    }
    path = write_manifest("pnl", seed, pe["monte_carlo"]["anchor_years"], summary)
    print(f"\nmanifest: {path}")
    return summary
