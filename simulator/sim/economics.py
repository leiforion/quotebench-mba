"""Economics layer and P&L assembly (SIM-3). Absorbs model/monte_carlo.py.

Design: operational quantities EMERGE from the discrete-event runs instead of
being assumed. Labour savings = simulated as-is engineer hours minus to-be
hours (the old harness assumed an automation rate; here the rate is an output).
The as-is economic anchor is the degraded to-be model, which reproduces the
calibrated baseline and carries defect draws.

Structure:
  lane_economics()  - price one simulation run: labour, quoted/won value,
                      discount leakage pool, quality cost (unscaled)
  build_anchors()   - DES runs per extraction variant + as-is; quality-cost
                      scale calibrated so the as-is lane reproduces BASE-31
  monte_carlo()     - 20k arithmetic draws over the anchors + financial
                      distributions; NPV/IRR/payback/P(hurdle)
  conservative_case() - 9.5 hostile case: pessimistic extraction, zero
                      elasticity, +30% build, on cost+error+discount alone
"""
import copy
from dataclasses import dataclass

import numpy as np

from .asis import TIERS
from .capability import draw_value_eur
from .tobe import ToBeModel

VARIANTS = ("pessimistic", "central", "optimistic")


def scale_company_values(pe, pt):
    """Rescale the branch-calibrated value bands (and the value-linked unit
    costs and routing gate) by company.value_scale so simulated won value
    reproduces company revenue at ~5,500 inquiries. Share-invariant, so routing
    mix and tier value shares are preserved. Returns fresh (pe, pt) copies."""
    s = pe.get("company", {}).get("value_scale", 1.0)
    if s == 1.0:
        return pe, pt
    pe, pt = copy.deepcopy(pe), copy.deepcopy(pt)
    vb = pt["value_bands_eur"]
    for t in TIERS:
        for k in ("median", "min", "max"):
            vb[t][k] *= s
    vb["mega"]["value_range"] = [x * s for x in vb["mega"]["value_range"]]
    pt["routing"]["V1_eur"] *= s
    for k in pe["error_unit_cost_eur"]:
        pe["error_unit_cost_eur"][k] *= s
    pe["calc_site_failure"]["cost_eur"] *= s
    return pe, pt


def run_cost_triangular(pe, infra_annual_eur):
    """Run cost = maintenance engineer + AWS infra x uncertainty (author, 13
    Sep). Returns a (lo, mode, hi) triangular in EUR/yr."""
    fin = pe["financial"]
    maint = fin["maintenance_engineer_eur"]
    lo, mode, hi = fin["infra_mult_triangular"]
    return (maint + infra_annual_eur * lo,
            maint + infra_annual_eur * mode,
            maint + infra_annual_eur * hi)


@dataclass
class LaneEconomics:
    """Annualized economics of one simulated lane."""
    labour_eur: float = 0.0
    quoted_value_eur: float = 0.0
    won_value_eur: float = 0.0          # the derived revenue base (D13)
    quality_cost_eur: float = 0.0       # unscaled defect cost
    margin_weighted_quoted: float = 0.0 # sum(quoted_t * margin_t), for uplift
    margin_weighted_won: float = 0.0    # sum(won_t * margin_t); /won = avg
                                        # realized margin (D19 gate: 24%)
    eng_hours: float = 0.0


def lane_economics(result, lane, pe, pt, seed):
    """Price one run's records. lane: 'asis' (degraded) or 'tobe'.

    The business does not offer discounts (author, 13 Sep), so there is no
    discount-leakage pool and no pricing-recovery benefit; pricing is at the
    like-for-like reference for every quote."""
    rng = np.random.default_rng(seed)
    e = LaneEconomics()
    years = result.horizon_wh / (176 * 12)

    for rec in result.records:
        value = rec.value_eur if rec.value_eur > 0 else \
            draw_value_eur(rng, rec.tier, pt)
        e.labour_eur += rec.touch_eng_wh * pe["hourly_rate_eur"]
        e.eng_hours += rec.touch_eng_wh
        e.quoted_value_eur += value
        e.margin_weighted_quoted += value * pe["margin"][rec.tier]

        # win probability is expectation-weighted rather than drawn: quality is
        # a rare heavy-tailed event and Bernoulli win gates add sampling noise
        # that would swamp the small lane deltas the case is built on.
        p_win = pe["win_rate"][rec.tier]
        e.won_value_eur += value * p_win
        e.margin_weighted_won += value * p_win * pe["margin"][rec.tier]

        # quality cost (credit notes exist only on orders)
        w = p_win if pe["error_cost_on_won_only"] else 1.0
        sf = pe["calc_site_failure"]
        for cls in rec.defects:
            if cls == "calculation":
                unit = (1 - sf["probability"]) * pe["error_unit_cost_eur"][cls] \
                    + sf["probability"] * sf["cost_eur"]
            else:
                unit = pe["error_unit_cost_eur"][cls]
            e.quality_cost_eur += w * unit

    for f in ("labour_eur", "quoted_value_eur", "won_value_eur",
              "quality_cost_eur", "margin_weighted_quoted", "margin_weighted_won",
              "eng_hours"):
        setattr(e, f, getattr(e, f) / years)
    return e


def avg_lane_economics(lanes):
    out = LaneEconomics()
    for f in vars(out):
        setattr(out, f, float(np.mean([getattr(x, f) for x in lanes])))
    return out


def _anchor_task(args):
    """Picklable worker: one DES replication -> its LaneEconomics. Runs in a
    child process. Returns (lane, variant, LaneEconomics)."""
    pe, pt, pa, lane, variant, seed, years = args
    if lane == "asis":
        res = ToBeModel(pt, pa, seed=seed, degraded=True).run(years=years)
    else:
        res = ToBeModel(pt, pa, variant=variant, seed=seed).run(years=years)
        res.variant = variant
    return lane, variant, lane_economics(res, lane, pe, pt, seed=seed)


def build_anchors(pe, pt, pa, verbose=False, jobs=None):
    """Run the DES per variant and for the as-is baseline; average over seeds.
    Returns (asis: LaneEconomics, anchors: {variant: LaneEconomics}, scale).
    Company value scaling is applied first so all EUR figures are company-scale.
    The 3 seeds x (as-is + 3 variants) = 12 replications run in parallel; the
    average over seeds is order-independent so results match the serial path."""
    from .parallel import pmap
    pe, pt = scale_company_values(pe, pt)
    seeds = pe["monte_carlo"]["anchor_seeds"]
    years = pe["monte_carlo"]["anchor_years"]

    tasks = [(pe, pt, pa, "asis", None, s, years) for s in seeds]
    for v in VARIANTS:
        tasks += [(pe, pt, pa, "tobe", v, s, years) for s in seeds]

    results = pmap(_anchor_task, tasks, jobs=jobs, desc="DES anchor")

    asis = avg_lane_economics([le for lane, _, le in results if lane == "asis"])
    anchors = {}
    for v in VARIANTS:
        anchors[v] = avg_lane_economics(
            [le for lane, vv, le in results if lane == "tobe" and vv == v])
        if verbose:
            print(f"  anchor {v:<12} eng hours {anchors[v].eng_hours:7.0f}  "
                  f"quality {anchors[v].quality_cost_eur:8.0f}")

    # Quality-cost scale. Pre-D19 this was calibrated so the as-is lane
    # reproduced BASE-31 (1.2% of the then-derived revenue). D19 retired that
    # target: unit costs are now value-scaled absolutes (BASE-30 x6.125), so
    # the scale is identity unless a target pct is explicitly configured.
    if "quality_cost_target_pct" in pe:
        scale = (pe["quality_cost_target_pct"] * asis.won_value_eur
                 / max(1.0, asis.quality_cost_eur))
    else:
        scale = 1.0
    return asis, anchors, scale


def interpolate(anchors, w):
    """w in [0,1]: 0 = pessimistic, 0.5 = central, 1 = optimistic."""
    lo, mid, hi = (anchors["pessimistic"], anchors["central"],
                   anchors["optimistic"])
    a, b, t = (lo, mid, w * 2) if w < 0.5 else (mid, hi, (w - 0.5) * 2)
    out = LaneEconomics()
    for f in vars(out):
        setattr(out, f, getattr(a, f) + t * (getattr(b, f) - getattr(a, f)))
    return out


def automation_rate(asis, tobe):
    """Emergent automation of touch time: the fraction of as-is engineer hours
    the to-be process removes. An OUTPUT of the DES, not the assumed 60%."""
    return max(0.0, 1.0 - tobe.eng_hours / asis.eng_hours) \
        if asis.eng_hours else 0.0


def annual_benefits(pe, asis, tobe, scale, win_uplift_frac):
    """Two company-level benefits (the business offers no discounts, so there
    is no pricing-recovery line). Redeployment is valued on the headcount basis
    (author choice): emergent automation rate x 16 estimators x loaded cost.
    Win uplift is a fraction of company revenue at gross margin. The quality
    (error) reduction emerges from the DES defect model."""
    comp = pe["company"]
    auto = automation_rate(asis, tobe)
    return {
        "labour_redeploy": auto * comp["n_estimators"] * comp["loaded_cost_eur"],
        "quality_savings": scale * (asis.quality_cost_eur - tobe.quality_cost_eur),
        "win_uplift_margin": win_uplift_frac * comp["revenue_eur"]
                             * comp["blended_margin"],
    }


def npv(rate, flows):
    return float(sum(cf / (1 + rate) ** t for t, cf in enumerate(flows)))


def cashflows(benefits_total, fin, build_overrun, run_cost, change_cost):
    y0 = -(fin["build_cost_eur"] * build_overrun + change_cost)
    return [y0] + [benefits_total * ramp - run_cost
                   for ramp in fin["adoption_ramp"]]


def irr_vec(flows_matrix, lo=-0.9, hi=5.0, iters=80):
    """Vectorized bisection IRR over an (n, T) cash-flow matrix."""
    t = np.arange(flows_matrix.shape[1])

    def f(rate):
        return (flows_matrix / (1 + rate[:, None]) ** t).sum(axis=1)

    lo_v = np.full(len(flows_matrix), lo)
    hi_v = np.full(len(flows_matrix), hi)
    bad = f(lo_v) * f(hi_v) > 0        # no sign change: IRR undefined
    for _ in range(iters):
        mid = (lo_v + hi_v) / 2
        pos = f(mid) > 0
        lo_v = np.where(pos, mid, lo_v)
        hi_v = np.where(pos, hi_v, mid)
    out = (lo_v + hi_v) / 2
    out[bad] = np.nan
    return out


def payback_vec(flows_matrix):
    cum = np.cumsum(flows_matrix, axis=1)
    pb = np.full(len(flows_matrix), np.nan)
    for t in range(1, flows_matrix.shape[1]):
        newly = np.isnan(pb) & (cum[:, t] >= 0)
        frac = np.where(flows_matrix[newly, t] != 0,
                        -cum[newly, t - 1] / flows_matrix[newly, t], 0.0)
        pb[newly] = t - 1 + frac
    return pb


def monte_carlo(pe, pt, pa, seed=42, verbose=False, infra_annual_eur=None,
                jobs=None):
    if infra_annual_eur is None:
        from .infra import cost_model
        infra_annual_eur = cost_model()["annual_full_eur"]
    asis, anchors, scale = build_anchors(pe, pt, pa, verbose=verbose, jobs=jobs)
    out = mc_from_anchors(pe, asis, anchors, scale, seed=seed,
                          infra_annual_eur=infra_annual_eur)
    out.update({"asis": asis, "anchors": anchors, "quality_scale": scale,
                "infra_annual_eur": infra_annual_eur,
                "automation_rate": {
                    v: automation_rate(asis, anchors[v]) for v in VARIANTS}})
    return out


def mc_from_anchors(pe, asis, anchors, scale, seed=42, return_draws=False,
                    infra_annual_eur=0.0):
    """The 20k-draw financial Monte Carlo over given DES anchors. Split out so
    the SIM-5 optimizer can re-price cached runs without re-simulating."""
    fin = pe["financial"]
    comp = pe["company"]
    mc = pe["monte_carlo"]
    n = mc["iterations"]
    rng = np.random.default_rng(seed)

    w = rng.triangular(*mc["extraction_weight_triangular"], n)
    uplift = rng.triangular(*pe["win_uplift_pp"]["triangular"], n)
    overrun = rng.triangular(*fin["build_overrun_triangular"], n)
    run_cost = rng.triangular(*run_cost_triangular(pe, infra_annual_eur), n)
    change = rng.triangular(*fin["change_cost_triangular"], n)

    # vectorize the anchor interpolation per benefit component
    def anchor_vec(field):
        lo, mid, hi = (getattr(anchors[v], field) for v in VARIANTS)
        return np.where(w < 0.5, lo + w * 2 * (mid - lo),
                        mid + (w - 0.5) * 2 * (hi - mid))

    # redeployment on the headcount basis: emergent automation x pool cost.
    # No discount benefit (the business does not discount).
    auto = np.clip(1.0 - anchor_vec("eng_hours") / asis.eng_hours, 0.0, 1.0)
    labour = auto * comp["n_estimators"] * comp["loaded_cost_eur"]
    quality = scale * (asis.quality_cost_eur - anchor_vec("quality_cost_eur"))
    uplift_margin = uplift * comp["revenue_eur"] * comp["blended_margin"]
    benefits = labour + quality + uplift_margin

    ramp = np.array(fin["adoption_ramp"])
    flows = np.empty((n, 1 + len(ramp)))
    flows[:, 0] = -(fin["build_cost_eur"] * overrun + change)
    flows[:, 1:] = benefits[:, None] * ramp[None, :] - run_cost[:, None]

    t = np.arange(flows.shape[1])
    npv12 = (flows / (1 + fin["discount_rate"]) ** t).sum(axis=1)
    npv_hurdle = (flows / (1 + fin["hurdle_rate"]) ** t).sum(axis=1)
    irrs = irr_vec(flows)
    pbs = payback_vec(flows)

    out = {
        "npv12_p10_p50_p90": [float(np.percentile(npv12, p)) for p in (10, 50, 90)],
        "npv_hurdle_p10": float(np.percentile(npv_hurdle, 10)),
        "p_clears_hurdle": float((npv_hurdle > 0).mean()),
        "irr_median": float(np.nanmedian(irrs)),
        "payback_median_years": float(np.nanmedian(pbs)),
        "automation_rate_median": float(np.median(auto)),
        "benefit_medians": {
            "labour_redeploy": float(np.median(labour)),
            "quality_savings": float(np.median(quality)),
            "win_uplift_margin": float(np.median(uplift_margin)),
        },
    }
    if return_draws:
        out["npv12_draws"] = npv12
    return out


def conservative_case(pe, pt, pa, asis, anchors, scale, infra_annual_eur=0.0):
    """9.5 hostile case: extraction at the pessimistic bound, elasticity zero,
    +30% build, central run/change costs. Must clear or fail the 15% hurdle on
    cost + error alone (no discount benefit exists), and say which."""
    fin = pe["financial"]
    b = annual_benefits(pe, asis, anchors["pessimistic"], scale,
                        win_uplift_frac=0.0)
    total = sum(b.values())            # win_uplift_margin is zero by design
    flows = cashflows(total, fin, build_overrun=1.30,
                      run_cost=run_cost_triangular(pe, infra_annual_eur)[1],
                      change_cost=fin["change_cost_triangular"][1])
    return {
        "benefits": b,
        "npv_at_12pct": npv(fin["discount_rate"], flows),
        "npv_at_hurdle": npv(fin["hurdle_rate"], flows),
        "clears": npv(fin["hurdle_rate"], flows) > 0,
    }
