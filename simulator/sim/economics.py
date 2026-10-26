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
from .capability import draw_value_eur, is_material
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


def company_revenue(pe, asis):
    """Company revenue used for the win-uplift (and, when priced, lost-bid)
    benefits. Under the branch basis (D21) it is DERIVED from the as-is anchor
    (simulated as-is won value at company volume), not read from YAML; under the
    company basis it is the supplied company.revenue_eur."""
    comp = pe["company"]
    if comp.get("revenue_basis", "company") == "branch":
        return asis.won_value_eur
    return comp["revenue_eur"]


def material_exceed_tiers(asis, tobe):
    """D24 rule D: tiers whose to-be MATERIAL defect rate exceeds the as-is rate.
    Faster-but-less-accurate quotes on those tiers cannot be assumed to win more,
    so their win-uplift contribution is zeroed (see uplift_revenue_base)."""
    ab = getattr(asis, "breakdown", None)
    tb = getattr(tobe, "breakdown", None)
    if not ab or not tb:
        return ()
    return tuple(t for t in TIERS if tb[t]["mat_rate"] > ab[t]["mat_rate"] + 1e-9)


def uplift_revenue_base(pe, asis, exclude_tiers=()):
    """Company revenue carried into the win-uplift benefit, net of any tier whose
    material defects rose above as-is (rule D)."""
    rev = company_revenue(pe, asis)
    if not exclude_tiers:
        return rev
    wbt = getattr(asis, "won_by_tier", None) or {}
    return max(0.0, rev - sum(wbt.get(t, 0.0) for t in exclude_tiers))


@dataclass
class LaneEconomics:
    """Annualized economics of one simulated lane."""
    labour_eur: float = 0.0
    quoted_value_eur: float = 0.0
    won_value_eur: float = 0.0          # the derived revenue base (D13)
    quality_cost_eur: float = 0.0       # defect cost (value-proportional, D21)
    margin_weighted_quoted: float = 0.0 # sum(quoted_t * margin_t), for uplift
    margin_weighted_won: float = 0.0    # sum(won_t * margin_t); /won = avg
                                        # realized margin (D19 gate: 24%)
    eng_hours: float = 0.0
    lost_bid_base_eur: float = 0.0      # D21: sum over defective quotes of
                                        # value * p_win * margin; x p_loss gives
                                        # the margin lost to defect-killed bids


def _defect_unit_cost(cls, pe):
    """Expected ledger cost of one defect of class `cls` (BASE-30), before any
    value scaling. The calculation class carries the site-failure tail."""
    if cls == "calculation":
        sf = pe["calc_site_failure"]
        return ((1 - sf["probability"]) * pe["error_unit_cost_eur"][cls]
                + sf["probability"] * sf["cost_eur"])
    return pe["error_unit_cost_eur"][cls]


def lane_economics(result, lane, pe, pt, seed, ref_value=None):
    """Price one run's records. lane: 'asis' (degraded) or 'tobe'.

    The business does not offer discounts (author, 13 Sep), so there is no
    discount-leakage pool and no pricing-recovery benefit; pricing is at the
    like-for-like reference for every quote.

    Defect cost is value-proportional (D21) when error_cost_value_proportional is
    on and a ref_value is given: each defect costs unit x (value / ref_value).
    ref_value (the as-is defect-weighted mean value) normalises the AVERAGE
    as-is cost per defect back to the ledger units, and is shared by both lanes.
    """
    rng = np.random.default_rng(seed)
    e = LaneEconomics()
    years = result.horizon_wh / (176 * 12)
    vprop = bool(pe.get("error_cost_value_proportional")) and ref_value

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

        # quality cost (credit notes exist only on orders), value-proportional
        w = p_win if pe["error_cost_on_won_only"] else 1.0
        vmult = (value / ref_value) if vprop else 1.0
        for cls in rec.defects:
            e.quality_cost_eur += w * _defect_unit_cost(cls, pe) * vmult

        # D21: margin at risk on a defective quote that would otherwise have won
        # (x p_loss, applied in the MC / case pricing, gives bids lost to defects)
        if rec.defects:
            e.lost_bid_base_eur += value * p_win * pe["margin"][rec.tier]

    for f in ("labour_eur", "quoted_value_eur", "won_value_eur",
              "quality_cost_eur", "margin_weighted_quoted", "margin_weighted_won",
              "eng_hours", "lost_bid_base_eur"):
        setattr(e, f, getattr(e, f) / years)
    return e


def ref_value_from_records(result):
    """Defect-weighted mean quote value over a lane's records: the mean of the
    quote value across every defect instance. Used to normalise the
    value-proportional defect cost so the average as-is cost per defect equals
    the ledger units (D21)."""
    vals = [rec.value_eur for rec in result.records for _ in rec.defects]
    return float(np.mean(vals)) if vals else 1.0


ROUTES = ("auto", "assisted", "assisted_full", "manual")


def tier_breakdown(result, pe, ref_value):
    """Per-tier breakdown of one run: error cost (EUR/yr, same value-proportional
    rule as lane_economics.quality_cost_eur), won value (EUR/yr), any-defect rate
    (by count) and route-mix shares. Feeds the D21/D22 by-tier reporting and the
    Tier-3 error-vs-won-share test."""
    vprop = bool(pe.get("error_cost_value_proportional")) and ref_value
    years = result.horizon_wh / (176 * 12)
    err = {t: 0.0 for t in TIERS}
    won = {t: 0.0 for t in TIERS}
    ndef = {t: 0 for t in TIERS}
    nmat = {t: 0 for t in TIERS}
    ntot = {t: 0 for t in TIERS}
    routes = {t: {r: 0 for r in ROUTES} for t in TIERS}
    for rec in result.records:
        t = rec.tier
        ntot[t] += 1
        if rec.defects:
            ndef[t] += 1
        if is_material(rec.defects, rec.route):        # D24 material defect
            nmat[t] += 1
        routes[t][rec.route] = routes[t].get(rec.route, 0) + 1
        value = rec.value_eur
        p_win = pe["win_rate"][t]
        won[t] += value * p_win
        w = p_win if pe["error_cost_on_won_only"] else 1.0
        vmult = (value / ref_value) if vprop else 1.0
        for cls in rec.defects:
            err[t] += w * _defect_unit_cost(cls, pe) * vmult
    out = {}
    for t in TIERS:
        n = max(1, ntot[t])
        out[t] = {"error": err[t] / years, "won": won[t] / years,
                  "def_rate": ndef[t] / n, "mat_rate": nmat[t] / n,
                  "routes": {r: routes[t][r] / n for r in ROUTES}}
    return out


def avg_breakdowns(items):
    """Average a list of per-tier breakdowns across seeds."""
    out = {}
    for t in TIERS:
        out[t] = {
            "error": float(np.mean([b[t]["error"] for b in items])),
            "won": float(np.mean([b[t]["won"] for b in items])),
            "def_rate": float(np.mean([b[t]["def_rate"] for b in items])),
            "mat_rate": float(np.mean([b[t]["mat_rate"] for b in items])),
            "routes": {r: float(np.mean([b[t]["routes"][r] for b in items]))
                       for r in ROUTES},
        }
    return out


def avg_lane_economics(lanes):
    out = LaneEconomics()
    for f in vars(out):
        setattr(out, f, float(np.mean([getattr(x, f) for x in lanes])))
    return out


def _anchor_task(args):
    """Picklable worker: one DES replication -> its LaneEconomics. Runs in a
    child process. Returns (lane, variant, LaneEconomics)."""
    pe, pt, pa, lane, variant, seed, years, ref_value = args
    if lane == "asis":
        res = ToBeModel(pt, pa, seed=seed, degraded=True).run(years=years)
    else:
        res = ToBeModel(pt, pa, variant=variant, seed=seed).run(years=years)
        res.variant = variant
    le = lane_economics(res, lane, pe, pt, seed=seed, ref_value=ref_value)
    return lane, variant, le, tier_breakdown(res, pe, ref_value)


def compute_ref_value(pe, pt, pa, seed, years):
    """Reference as-is run -> ref_value, ONE company-wide normaliser over all
    defective as-is quotes (not per tier, which would cancel the value-
    proportional effect). None when value-proportional costing is off."""
    if not pe.get("error_cost_value_proportional"):
        return None
    res = ToBeModel(pt, pa, seed=seed, degraded=True).run(years=years)
    return ref_value_from_records(res)


def build_anchors(pe, pt, pa, verbose=False, jobs=None):
    """Run the DES per variant and for the as-is baseline; average over seeds.
    Returns (asis: LaneEconomics, anchors: {variant: LaneEconomics}, scale).
    Company value scaling is applied first so all EUR figures are company-scale.
    The 3 seeds x (as-is + 3 variants) = 12 replications run in parallel; the
    average over seeds is order-independent so results match the serial path.

    When error_cost_value_proportional is on, a reference as-is run first fixes
    ref_value (the defect-cost normaliser) and the as-is error-by-tier split;
    both are shared across every lane and attached to the returned as-is anchor."""
    from .parallel import pmap
    pe, pt = scale_company_values(pe, pt)
    seeds = pe["monte_carlo"]["anchor_seeds"]
    years = pe["monte_carlo"]["anchor_years"]

    ref_value = compute_ref_value(pe, pt, pa, seeds[0], years)

    tasks = [(pe, pt, pa, "asis", None, s, years, ref_value) for s in seeds]
    for v in VARIANTS:
        tasks += [(pe, pt, pa, "tobe", v, s, years, ref_value) for s in seeds]

    results = pmap(_anchor_task, tasks, jobs=jobs, desc="DES anchor")

    def attach_breakdown(obj, items):
        obj.breakdown = avg_breakdowns(items)
        obj.error_by_tier = {t: obj.breakdown[t]["error"] for t in TIERS}
        obj.won_by_tier = {t: obj.breakdown[t]["won"] for t in TIERS}

    asis = avg_lane_economics([r[2] for r in results if r[0] == "asis"])
    asis.ref_value = ref_value
    attach_breakdown(asis, [r[3] for r in results if r[0] == "asis"])
    anchors = {}
    for v in VARIANTS:
        sub = [r for r in results if r[0] == "tobe" and r[1] == v]
        anchors[v] = avg_lane_economics([r[2] for r in sub])
        attach_breakdown(anchors[v], [r[3] for r in sub])
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


def lost_bid_central(pe):
    """Central p_loss for the defect-killed-bid benefit (D21); 0.0 if unset."""
    return pe.get("error_lost_bid", {}).get("p_loss_triangular", [0.0, 0.0, 0.0])[1]


def annual_benefits(pe, asis, tobe, scale, win_uplift_frac, p_loss=None,
                    exclude_tiers=()):
    """Company-level benefits (the business offers no discounts, so there is no
    pricing-recovery line). Redeployment is valued on the headcount basis
    (author choice): emergent automation rate x 16 estimators x loaded cost. Win
    uplift is a fraction of company revenue at gross margin; company revenue is
    DERIVED from the as-is anchor under the branch basis (D21). The quality
    (error) reduction emerges from the DES defect model, and error_lost_bid
    values the defect-killed bids the to-be process recovers."""
    comp = pe["company"]
    auto = automation_rate(asis, tobe)
    if p_loss is None:
        p_loss = lost_bid_central(pe)
    return {
        "labour_redeploy": auto * comp["n_estimators"] * comp["loaded_cost_eur"],
        "quality_savings": scale * (asis.quality_cost_eur - tobe.quality_cost_eur),
        "win_uplift_margin": win_uplift_frac
                             * uplift_revenue_base(pe, asis, exclude_tiers)
                             * comp["blended_margin"],
        "error_lost_bid": p_loss * (asis.lost_bid_base_eur - tobe.lost_bid_base_eur),
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
    exclude = material_exceed_tiers(asis, anchors["central"])   # rule D
    out = mc_from_anchors(pe, asis, anchors, scale, seed=seed,
                          infra_annual_eur=infra_annual_eur, exclude_tiers=exclude)
    out.update({"asis": asis, "anchors": anchors, "quality_scale": scale,
                "infra_annual_eur": infra_annual_eur,
                "uplift_exclude_tiers": exclude,
                "automation_rate": {
                    v: automation_rate(asis, anchors[v]) for v in VARIANTS}})
    return out


def mc_from_anchors(pe, asis, anchors, scale, seed=42, return_draws=False,
                    infra_annual_eur=0.0, exclude_tiers=()):
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
    lb_tri = pe.get("error_lost_bid", {}).get("p_loss_triangular", [0.0, 0.0, 0.0])
    # guard the degenerate [0,0,0] (np.triangular rejects left == right): when
    # there is no lost-bid estimate the benefit is identically zero.
    p_loss = rng.triangular(*lb_tri, n) if lb_tri[2] > lb_tri[0] else np.zeros(n)

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
    uplift_margin = (uplift * uplift_revenue_base(pe, asis, exclude_tiers)
                     * comp["blended_margin"])
    lost_bid = p_loss * (asis.lost_bid_base_eur - anchor_vec("lost_bid_base_eur"))
    benefits = labour + quality + uplift_margin + lost_bid

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
        "benefit_total_median": float(np.median(benefits)),   # D24: median of sum
        "benefit_medians": {
            "labour_redeploy": float(np.median(labour)),
            "quality_savings": float(np.median(quality)),
            "win_uplift_margin": float(np.median(uplift_margin)),
            "error_lost_bid": float(np.median(lost_bid)),
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
