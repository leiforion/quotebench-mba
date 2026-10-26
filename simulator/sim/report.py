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
    print(f"\n{'route mix':<12}{'auto':>8}{'assisted':>10}{'full-rev':>10}{'manual':>8}")
    for t in TIERS:
        m = s["route_mix"][t]
        print(f"{t:<12}{m['auto']:>8.0%}{m['assisted']:>10.0%}"
              f"{m['assisted_full']:>10.0%}{m['manual']:>8.0%}")

    import numpy as np
    t3 = res.by_tier("touch_eng_wh")["tier3"]
    print(f"\nTier 3 full-review engineer touch (h, 7.2): "
          f"median {np.median(t3):.1f}  P90 {np.percentile(t3, 90):.1f}  "
          f"P99 {np.percentile(t3, 99):.1f}  max {t3.max():.1f}")
    print(f"  7.2 Innovo walkthrough: ~28 h as-is -> ~13 h to-be; the Innovo-scale "
          f"job sits in the Tier-3 upper tail (P99 {np.percentile(t3, 99):.0f} h here).")
    print(f"\n{'residual defect rates':<26}{'as-is':>9}{'to-be':>9}")
    asis_rates = {"extraction": 0.09, "calculation": 0.035,
                  "selection": 0.05, "pricing": 0.04}   # BASE-29
    for cls, r in s["defect_rate"].items():
        print(f"{cls:<26}{asis_rates[cls]:>9.1%}{r:>9.2%}")
    asis_s = ToBeModel(pt, p, seed=seed, degraded=True).run(years=years).summary()
    print(f"{'any defect (incl. extraction)':<26}{asis_s['any_defect_rate']:>9.2%}"
          f"{s['any_defect_rate']:>9.2%}")
    print(f"{'material (model/price/spec) D24':<26}{asis_s['material_rate']:>9.2%}"
          f"{s['material_rate']:>9.2%}  <- the comparable definition")
    print(f"\nreview queue median: {s['review_queue_median_wh']:.2f} wh "
          f"(TOBE-05 assumes 2.5 h; emergent here, diagnostic)")
    print("engineer hours/year: "
          + ", ".join(f"{k} {v:.0f}" for k, v in s["busy_wh_per_year"].items())
          + f"  (as-is total ~{5500 * 4.34:.0f}, company-wide)")
    asis_hours = sum(asis_s["busy_wh_per_year"].values())
    tobe_hours = sum(s["busy_wh_per_year"].values())
    auto = 1 - tobe_hours / asis_hours if asis_hours else 0.0
    headroom = asis_hours / tobe_hours - 1 if tobe_hours else 0.0
    print(f"\nSection 8.2 capacity: automation of touch time {auto:.0%} "
          f"(to-be {tobe_hours:,.0f} h vs as-is {asis_hours:,.0f} h). At 16 "
          f"estimators this frees enough touch to absorb ~{headroom:.0%} more "
          f"inquiry volume before returning to today's workload.")
    path = write_manifest("tobe", seed, years,
                          {"variant": variant, "summary": s})
    print(f"manifest: {path}")
    return s


def pnl_report(seed=42, jobs=None):
    """SIM-3 output: company-level operating comparison, emergent automation,
    five-year Monte Carlo investment case, the floor case, and the AWS
    infrastructure cost broken down by service."""
    from .config import load_econ, load_tobe
    from .economics import (monte_carlo, conservative_case, run_cost_triangular,
                            company_revenue)
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
    rev = company_revenue(pe, asis)
    basis = comp.get("revenue_basis", "company")

    print(f"\nAnnual operating economics (as-is vs to-be central, EUR) "
          f"[company-wide]")
    rows = [
        ("quoted value", asis.quoted_value_eur, ctr.quoted_value_eur),
        ("won value (= company revenue)", asis.won_value_eur, ctr.won_value_eur),
        ("engineer hours", asis.eng_hours, ctr.eng_hours),
        ("quality cost", asis.quality_cost_eur, ctr.quality_cost_eur),
    ]
    print(f"{'':<32}{'as-is':>12}{'to-be':>12}")
    for name, a, b in rows:
        print(f"{name:<32}{a:>12,.0f}{b:>12,.0f}")
    if basis == "branch":
        br = comp["branch"]
        implied = rev * br["inquiries_per_year"] / comp["inquiries_per_year"]
        print(f"  company revenue DERIVED from as-is anchor (branch basis): "
              f"{rev:,.0f}")
        print(f"  cross-check: pro-rated to branch volume {implied:,.0f} vs "
              f"stated branch revenue {br['revenue_eur']:,.0f} "
              f"({implied / br['revenue_eur'] - 1:+.1%}, gate ±5%)")
    else:
        print(f"  won value vs revenue input: {asis.won_value_eur:,.0f} vs "
              f"{rev:,.0f} ({asis.won_value_eur / rev - 1:+.1%})")

    ab = getattr(asis, "breakdown", None)
    tbd = getattr(ctr, "breakdown", None)
    scale = mc["quality_scale"]
    arr = p["arrivals_per_month"]
    vshare = {t: arr[t] / sum(arr.values()) for t in TIERS}
    if ab:
        te = sum(ab[t]["error"] for t in TIERS)
        tw = sum(ab[t]["won"] for t in TIERS)
        print(f"\nAs-is quality (error) cost by tier (EUR/yr, value-proportional):")
        print(f"  {'tier':<8}{'error EUR':>13}{'err share':>11}{'won share':>11}")
        for t in TIERS:
            esh = ab[t]["error"] / te if te else 0.0
            wsh = ab[t]["won"] / tw if tw else 0.0
            print(f"  {t:<8}{ab[t]['error']:>13,.0f}{esh:>11.1%}{wsh:>11.1%}")
        print(f"  {'TOTAL':<8}{te:>13,.0f}")
        t3 = ab["tier3"]["error"] / te if te else 0.0
        w3 = ab["tier3"]["won"] / tw if tw else 0.0
        print(f"  -> Tier 3 carries {t3:.0%} of as-is error cost vs {w3:.0%} of won "
              f"value ({'the majority' if t3 > 0.5 else 'NOT the majority'}).")

    c_mat_a = c_mat_t = None
    if ab and tbd:
        # D24: report BOTH defect definitions once, then use MATERIAL everywhere.
        c_any_a = sum(vshare[t] * ab[t]["def_rate"] for t in TIERS)
        c_any_t = sum(vshare[t] * tbd[t]["def_rate"] for t in TIERS)
        c_mat_a = sum(vshare[t] * ab[t]["mat_rate"] for t in TIERS)
        c_mat_t = sum(vshare[t] * tbd[t]["mat_rate"] for t in TIERS)
        print(f"\nDefect definitions, company-wide (central), reported once:")
        print(f"  {'definition':<46}{'as-is':>8}{'to-be':>8}")
        print(f"  {'any-defect (incl. cosmetic extraction typos)':<46}"
              f"{c_any_a:>8.1%}{c_any_t:>8.1%}")
        print(f"  {'material (wrong model/price/missed spec) = GATE':<46}"
              f"{c_mat_a:>8.1%}{c_mat_t:>8.1%}")

        print(f"\nAs-is vs to-be by tier (MATERIAL defect rate + error cost, "
              f"central, scale {scale:.2f}):")
        print(f"  {'tier':<8}{'mat%a':>8}{'mat%t':>8}{'cut':>6}"
              f"{'cost a':>13}{'cost t':>13}{'cut':>6}{'flag':>6}")
        cut_by = {}
        for t in TIERS:
            ma, mt = ab[t]["mat_rate"], tbd[t]["mat_rate"]
            ca, ct = scale * ab[t]["error"], scale * tbd[t]["error"]
            cut_by[t] = (1 - ct / ca) if ca else 0.0
            flag = "EXCEED" if mt > ma + 1e-9 else ""
            print(f"  {t:<8}{ma:>8.1%}{mt:>8.1%}{(1 - mt / ma if ma else 0):>6.0%}"
                  f"{ca:>13,.0f}{ct:>13,.0f}{cut_by[t]:>6.0%}{flag:>6}")
        cma = scale * sum(ab[t]["error"] for t in TIERS)
        cmt = scale * sum(tbd[t]["error"] for t in TIERS)
        print(f"  {'COMPANY':<8}{c_mat_a:>8.1%}{c_mat_t:>8.1%}"
              f"{(1 - c_mat_t / c_mat_a if c_mat_a else 0):>6.0%}"
              f"{cma:>13,.0f}{cmt:>13,.0f}{(1 - cmt / cma if cma else 0):>6.0%}")

        exceed = [t for t in TIERS if tbd[t]["mat_rate"] > ab[t]["mat_rate"] + 1e-9]
        if exceed:
            print(f"  FLAG (rule D): to-be MATERIAL defects EXCEED as-is in "
                  f"{', '.join(exceed)} -> their win-uplift contribution is zeroed.")
        else:
            print(f"  OK: no tier's to-be material defect rate exceeds as-is "
                  f"(D24 dual gate holds).")
        # flag a tier whose % cost cut beats a simpler tier, with the driver
        order = list(TIERS)
        for i, t in enumerate(order):
            worse = [s for s in order[:i] if cut_by[t] > cut_by[s] + 1e-9]
            if worse:
                print(f"  FLAG: {t} error-cost cut {cut_by[t]:.0%} exceeds "
                      f"{'/'.join(f'{s} {cut_by[s]:.0%}' for s in worse)} - "
                      f"{t} as-is cost sat in the expensive selection/pricing/calc "
                      f"classes on high-value jobs ({scale*ab[t]['error']:,.0f} EUR), "
                      f"which source verification + engines remove wholesale.")

        print(f"\nRouting shares by tier at C1={pt['routing']['C1']:.2f} "
              f"C2={pt['routing']['C2']:.2f} "
              f"({'auto':>4} / {'light':>5} / {'full-review':>11} / {'manual':>6}):")
        for t in TIERS:
            r = tbd[t]["routes"]
            print(f"  {t:<8}{r['auto']:>7.0%}{r['assisted']:>9.0%}"
                  f"{r['assisted_full']:>14.0%}{r['manual']:>9.0%}")

    print(f"\nEmergent automation of touch time (DES output, NOT assumed):")
    ar = mc["automation_rate"]
    print(f"  pessimistic {ar['pessimistic']:.0%}   central {ar['central']:.0%}"
          f"   optimistic {ar['optimistic']:.0%}   "
          f"(author reference band 40 / 60 / 85%)")
    headroom = asis.eng_hours / ctr.eng_hours - 1 if ctr.eng_hours else 0.0
    print(f"  Section 8.2 demand headroom: the same 16 estimators spend "
          f"{ctr.eng_hours:,.0f} vs {asis.eng_hours:,.0f} as-is touch hours, so at "
          f"equal workload they can absorb ~{headroom:.0%} more inquiry volume "
          f"(~{(1+headroom)*comp['inquiries_per_year']:,.0f}/yr) before returning "
          f"to today's load.")

    # Headline annual benefit is the CENTRAL case (coherent all-central draws),
    # matching the stress base_central and floor exactly - the per-component MC
    # medians do not sum to any single scenario and differed by ~EUR 199k (the
    # right-skewed win-uplift median > its mode). The MC (below) carries the
    # spread into the NPV distribution; this line is the single reported benefit.
    from .economics import annual_benefits
    exclude = mc.get("uplift_exclude_tiers", ())
    central_uplift = pe["win_uplift_pp"]["triangular"][1]
    cb = annual_benefits(pe, asis, ctr, mc["quality_scale"],
                         win_uplift_frac=central_uplift, exclude_tiers=exclude)
    print(f"\nAnnual benefit (EUR/yr, full adoption, central case):")
    for k in ("labour_redeploy", "quality_savings", "win_uplift_margin",
              "error_lost_bid"):
        print(f"  {k:<22}{cb[k]:>10,.0f}")
    central_total = sum(cb.values())
    mc_median_total = mc["benefit_total_median"]
    print(f"  {'TOTAL (central/mode)':<22}{central_total:>10,.0f}  "
          f"<- the reported figure (win-uplift at its 2.0pp mode)")
    print(f"  {'TOTAL (MC median)':<22}{mc_median_total:>10,.0f}  "
          f"(win-uplift median ~{pe['win_uplift_pp']['triangular'][1]*1.118:.3f} "
          f"on the 0-5pp triangular; distribution carried into the NPV below)")
    print(f"  The paper reports the CENTRAL total (EUR {central_total:,.0f}); it "
          f"is coherent with the stress base and floor case. NPV uses the full "
          f"Monte Carlo, not this point estimate.")
    if exclude:
        cb_full = annual_benefits(pe, asis, ctr, mc["quality_scale"],
                                  win_uplift_frac=central_uplift)
        lost = cb_full["win_uplift_margin"] - cb["win_uplift_margin"]
        print(f"  rule D: win-uplift zeroed for {', '.join(exclude)} "
              f"(material defects above as-is there) -> win-uplift cut by "
              f"EUR {lost:,.0f}, total benefit {sum(cb_full.values()):,.0f} -> "
              f"{sum(cb.values()):,.0f}.")

    rc = run_cost_triangular(pe, infra_annual)
    print(f"\nCost structure (EUR):")
    print(f"  build (Y1 engineer):        {pe['financial']['build_cost_eur']:>10,.0f}")
    print(f"  run/yr = maint engineer + AWS infra: "
          f"{pe['financial']['maintenance_engineer_eur']:,.0f} + "
          f"{infra_annual:,.0f} = {rc[1]:,.0f}  (range {rc[0]:,.0f}-{rc[2]:,.0f})")
    print(f"  change (once):              "
          f"{pe['financial']['change_cost_triangular'][1]:>10,.0f}")
    print(f"  NOTE (D21): build EUR {pe['financial']['build_cost_eur']:,.0f}, change "
          f"{pe['financial']['change_cost_triangular'][1]:,.0f} and run {rc[1]:,.0f} "
          f"were sized against the OLD EUR ~35M branch base. They are effort/cost "
          f"inputs, not revenue-scaled; they await authors' sign-off for a company /\n"
          f"       multi-office rollout to 16 estimators (tested, unapproved, in the "
          f"'multi_office_rollout' stress scenario).")

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
    if cons["npv_at_12pct"] < 0:
        from .designs import floor_breakeven
        be = floor_breakeven(pe, pt, p, infra_annual_eur=infra_annual, jobs=jobs)
        print(f"  rule E: floor NPV@12% is NEGATIVE. Break-even "
              f"critical_field_share multiplier {be['crit_mult']:.2f} "
              f"(Tier-3 ~{be['crit_t3']:.0%}); break-even verification "
              f"{be['verify_min']:.1f} min/critical field.")
    else:
        print(f"  (rule E not triggered: floor NPV@12% is positive at "
              f"{cons['npv_at_12pct']:,.0f}.)")

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
        "benefit_central": cb,                  # D24: coherent central benefit
        "uplift_exclude_tiers": list(exclude),  # rule D (empty unless a tier > as-is)
        "material_rate_company": {"asis": c_mat_a, "tobe": c_mat_t},
        # extra context for the written narrative (sim all)
        "asis_eng_hours": asis.eng_hours,
        "tobe_eng_hours": ctr.eng_hours,
        "asis_won_value_eur": asis.won_value_eur,
        "revenue_basis": basis,
        "company_revenue_eur": rev,
        "asis_error_by_tier_eur": getattr(asis, "error_by_tier", None),
        "asis_won_by_tier_eur": getattr(asis, "won_by_tier", None),
        "asis_quality_cost_eur": asis.quality_cost_eur,
        "tobe_quality_cost_eur": ctr.quality_cost_eur,
        "run_cost_central_eur": rc[1],
        "build_cost_eur": pe["financial"]["build_cost_eur"],
        "benefit_total_eur": sum(cb.values()),   # D24: central, matches stress
    }
    path = write_manifest("pnl", seed, pe["monte_carlo"]["anchor_years"], summary)
    print(f"\nmanifest: {path}")
    return summary
