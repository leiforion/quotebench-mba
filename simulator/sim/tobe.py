"""To-be (QuoteBench) discrete-event model: system lane + confidence routing.

Flow per inquiry (working-hour clock, shared with sim/asis.py):
  arrival -> intake + extraction/validation (machine minutes, no queue) ->
  [consolidated clarification issued in minutes; contractor answers at the
  measured pace, BASE-24] -> route per 7.7 on min field confidence, tier,
  value gate V1 and discount band -> engineer lane:
    auto:     one-click release (minutes)
    assisted: pre-filled workspace review (minutes by tier)
    manual:   full workspace + senior review; as-is touch reduced by the
              assist credit scaled with extracted share (zero extraction =>
              zero credit => as-is touch: the continuity check)
Degraded mode (constraint four): the system is down, every inquiry drops into
the Section 4 manual process - noticing delay restored, no assist credit, full
as-is external waits, as-is defect model. This must reproduce the calibrated
as-is results; tests/test_tobe.py enforces it.
"""
from dataclasses import dataclass, field

import numpy as np
import simpy

from .asis import Estimator, lognormal, TIERS, TIER_PRIORITY
from .capability import (draw_docs, draw_value_eur, decide_route,
                         draw_asis_defects, draw_system_defects)


@dataclass
class ToBeRecord:
    tier: str
    t_arrival: float
    route: str = "manual"
    doc_class: str = ""
    min_conf: float = 0.0
    extracted_share: float = 0.0
    value_eur: float = 0.0
    clarified: bool = False
    reviewer: str = ""
    t_route_ready: float = None
    t_first_touch: float = None
    t_done: float = None
    touch_sys_min: float = 0.0
    touch_eng_wh: float = 0.0
    defects: list = field(default_factory=list)

    @property
    def cycle_wh(self):
        return self.t_done - self.t_arrival

    @property
    def review_queue_wh(self):
        return self.t_first_touch - self.t_route_ready


@dataclass
class ToBeResult:
    records: list = field(default_factory=list)
    horizon_wh: float = 0.0
    busy_wh: dict = field(default_factory=dict)

    def by_tier(self, attr):
        return {t: np.array([getattr(r, attr) for r in self.records if r.tier == t]
                            or [0.0]) for t in TIERS}

    def summary(self):
        cyc = self.by_tier("cycle_wh")
        eng = self.by_tier("touch_eng_wh")
        n = len(self.records)
        n_years = self.horizon_wh / (176 * 12)
        routes = {}
        for t in TIERS:
            recs = [r for r in self.records if r.tier == t]
            routes[t] = {rt: sum(r.route == rt for r in recs) / max(1, len(recs))
                         for rt in ("auto", "assisted", "manual")}
        defect_rate = {}
        for cls in ("extraction", "calculation", "selection", "pricing"):
            defect_rate[cls] = sum(cls in r.defects for r in self.records) / max(1, n)
        return {
            "cycle_median_wh": {t: float(np.median(cyc[t])) for t in TIERS},
            "cycle_p90_wh": {t: float(np.percentile(cyc[t], 90)) for t in TIERS},
            "eng_touch_median_wh": {t: float(np.median(eng[t])) for t in TIERS},
            "route_mix": routes,
            "defect_rate": defect_rate,
            "any_defect_rate": sum(bool(r.defects) for r in self.records) / max(1, n),
            "review_queue_median_wh": float(np.median(
                [r.review_queue_wh for r in self.records])),
            "annual_inquiries": n / n_years,
            "busy_wh_per_year": {k: v / n_years for k, v in self.busy_wh.items()},
        }


class ToBeModel:
    def __init__(self, params_tobe, params_asis, variant="central", seed=42,
                 extraction_override=None, degraded=False):
        self.pt = params_tobe
        self.pa = params_asis
        self.variant = variant
        self.extraction_override = extraction_override
        self.degraded = degraded
        self.rng = np.random.default_rng(seed)

    def run(self, years=8, warmup_months=2):
        pt, pa = self.pt, self.pa
        env = simpy.Environment()
        wh_month = pa["clock"]["working_hours_per_day"] * pa["clock"]["working_days_per_month"]
        horizon = years * 12 * wh_month
        warmup = warmup_months * wh_month
        result = ToBeResult()
        estimators = [Estimator(env, e["name"], e["speed"]) for e in pa["estimators"]]
        err_mult = {e["name"]: e.get("error_mult", 1.0) for e in pa["estimators"]}
        skill = {e["name"]: e.get("skill", e["name"]) for e in pa["estimators"]}
        result.busy_wh = {e["name"]: 0.0 for e in pa["estimators"]}

        # software error-reduction levers (disabled in the degraded as-is run).
        # Automated lanes: the deterministic calc engine / reference catalogue /
        # pricing rules cut those classes. Manual lane: validated AI prefill
        # cuts overall incidence in proportion to the share correctly prefilled.
        if self.degraded:
            class_mult, manual_credit = None, 0.0
        else:
            sdr = pt["software_defect_reduction"]
            class_mult = {c: 1.0 - sdr[c][self.variant]
                          for c in ("calculation", "selection", "pricing")}
            manual_credit = pt["manual_extraction_credit"][self.variant]

        def work(rec, est, duration, priority):
            remaining = duration
            while remaining > 1e-9:
                with est.res.request(priority=priority, preempt=(priority == 0)) as req:
                    yield req
                    if rec.t_first_touch is None:
                        rec.t_first_touch = env.now
                    start = env.now
                    try:
                        yield env.timeout(remaining)
                        worked = remaining
                        remaining = 0.0
                    except simpy.Interrupt:
                        worked = env.now - start
                        remaining -= worked
                    rec.touch_eng_wh += worked
                    if env.now > warmup:
                        result.busy_wh[est.name] += worked

        senior_names = {e["name"] for e in pa["estimators"]
                        if e.get("skill", e["name"]) == "senior"}

        def pick(prefer_senior=False):
            pool = estimators
            if prefer_senior:
                seniors = [e for e in estimators if e.name in senior_names]
                if seniors:
                    pool = seniors   # least-loaded senior; else fall through
            return min(pool, key=lambda e: e.load)

        def admin_external_median(tier):
            """As-is fitted external wait net of its embedded clarification
            content (drawn explicitly in the system lane; avoid double-count)."""
            f = pa["fitted"]
            embedded_clar = (pa["clarification"]["probability"][tier]
                             * pt["clarification"]["wait_median_wh"][tier])
            return max(0.3, f["residual_queue_median_wh"][tier] - embedded_clar)

        def manual_lane(rec, prio, credit):
            """Section 4 manual process, shared shape with sim/asis.py.
            credit=0 and degraded=True is exactly the as-is flow."""
            est = pick(prefer_senior=(not self.degraded and rec.tier == "tier3"))
            total = lognormal(self.rng, pa["touch_median_h"][rec.tier],
                              pa["touch_sigma"]) * est.speed * (1.0 - credit)
            split = pa["touch_split"]
            f = pa["fitted"]
            if self.degraded:
                # clarification cost lives inside the fitted external wait
                ext_median = f["residual_queue_median_wh"][rec.tier]
            else:
                ext_median = (pt["manual_external_factor"]
                              * admin_external_median(rec.tier))
            yield from work(rec, est, total * split["reading"], prio)
            yield from work(rec, est, total * split["calc_select"], prio)
            yield env.timeout(lognormal(self.rng, ext_median,
                                        f["residual_queue_sigma"][rec.tier]))
            yield from work(rec, est, total * split["assembly"], prio)
            rec.reviewer = est.name
            # validated prefill lowers manual-lane errors by credit x prefill
            # share (so it vanishes when extraction fails); as-is run keeps 1.0
            incidence_mult = 1.0 - manual_credit * rec.extracted_share
            rec.defects = draw_asis_defects(self.rng, rec.tier, pt,
                                            incidence_mult=incidence_mult)

        def inquiry(tier):
            rec = ToBeRecord(tier=tier, t_arrival=env.now)
            lo, hi = pa["pump_count_bounds"][tier]
            pumps = int(self.rng.integers(lo, hi + 1))
            prio = 0 if (tier == "tier3" and pumps >= pa["preemption_pump_threshold"]) \
                else TIER_PRIORITY[tier]

            if self.degraded:
                # constraint four: drop into the Section 4 process wholesale
                yield env.timeout(lognormal(self.rng, pa["notice_delay"]["median_wh"],
                                            pa["notice_delay"]["sigma"]))
                rec.clarified = self.rng.random() < pa["clarification"]["probability"][tier]
                rec.t_route_ready = env.now
                yield from manual_lane(rec, prio, credit=0.0)
            else:
                # system lane: machine minutes, no queue
                sysm = pt["system_lane_minutes"]
                rec.touch_sys_min = sysm["intake"] + sysm["extraction_validation"]
                yield env.timeout(rec.touch_sys_min / 60.0)

                docs = draw_docs(self.rng, tier, pt, self.variant,
                                 self.extraction_override)
                rec.doc_class = docs.doc_class
                rec.min_conf = docs.min_confidence
                rec.extracted_share = docs.extracted_share
                rec.value_eur = draw_value_eur(self.rng, tier, pt)

                # consolidated clarification issued in minutes (TOBE-03);
                # the contractor's answer keeps its measured pace (BASE-24)
                if self.rng.random() < pa["clarification"]["probability"][tier]:
                    rec.clarified = True
                    yield env.timeout(
                        (pt["system_lane_minutes"]["clarification_issue"]
                         - rec.touch_sys_min) / 60.0)
                    yield env.timeout(lognormal(
                        self.rng, pt["clarification"]["wait_median_wh"][tier],
                        pt["clarification"]["sigma"]))

                rec.route = decide_route(self.rng, tier, rec.value_eur, docs,
                                         pt, self.variant)
                rec.t_route_ready = env.now

                if rec.route == "auto":
                    est = pick()
                    yield from work(rec, est,
                                    pt["review_touch_minutes"]["auto_release"]
                                    / 60.0 * est.speed, prio)
                    rec.reviewer = est.name
                    rec.defects = draw_system_defects(
                        self.rng, docs, skill[est.name], "auto", pt,
                        err_mult[est.name], class_mult=class_mult)
                elif rec.route == "assisted":
                    est = pick()
                    yield from work(rec, est,
                                    pt["review_touch_minutes"]["assisted"][tier]
                                    / 60.0 * est.speed, prio)
                    rec.reviewer = est.name
                    rec.defects = draw_system_defects(
                        self.rng, docs, skill[est.name], "assisted", pt,
                        err_mult[est.name], class_mult=class_mult)
                else:
                    credit = (pt["manual_assist_credit"][self.variant]
                              * docs.extracted_share)
                    yield from manual_lane(rec, prio, credit)

            rec.t_done = env.now
            if rec.t_arrival > warmup:
                result.records.append(rec)

        def source(tier):
            rate = pa["arrivals_per_month"][tier] / wh_month
            while True:
                yield env.timeout(float(self.rng.exponential(1.0 / rate)))
                env.process(inquiry(tier))

        for t in TIERS:
            env.process(source(t))
        env.run(until=horizon + warmup)
        result.horizon_wh = horizon
        return result
