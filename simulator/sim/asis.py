"""As-is discrete-event model of the branch quoting process (Exhibit 4.1).

Clock unit: working hours (wh). Flow per inquiry:
  arrival -> noticing delay (mailbox/batching) -> estimator desk queue
  (emergent; small jobs triaged first, as observed) -> reading ->
  [clarification: recorded, wait calibrated in aggregate below] ->
  calculation & selection -> external + administrative wait (fitted per tier;
  covers contractor answers, pricing approval, dispatch batching) ->
  assembly & dispatch.

Modeling notes, stated for the paper:
- Desk discipline is small-job-first with one owner per inquiry: estimators
  knock out quick inquiries between large ones. This, not slow work, is what
  produces the measured Tier 3 delay pattern (88 wh median vs 11.4 h touch).
- Very large Tier 3 inquiries pre-empt in-progress work (the Innovo pattern).
- The measured 14 wh assignment median (BASE-23) is reproduced as an emergent
  diagnostic (noticing + desk queue), not imposed.
- Clarification incidence is drawn per tier (weighted to the measured 38%,
  BASE-26); its elapsed cost is calibrated inside the per-tier external wait,
  because only the aggregate is identified by the measured cycle distribution.
  To-be scenarios re-split that wait using BASE-23/24/25 at projection time.
"""
from dataclasses import dataclass, field

import numpy as np
import simpy

TIERS = ("tier1", "tier2", "tier3")
TIER_PRIORITY = {"tier1": 1, "tier2": 2, "tier3": 3}  # small jobs first


@dataclass
class InquiryRecord:
    tier: str
    t_arrival: float
    pumps: int = 0
    t_first_touch: float = None
    t_done: float = None
    touch_wh: float = 0.0
    preempted: int = 0
    clarified: bool = False

    @property
    def cycle_wh(self):
        return self.t_done - self.t_arrival

    @property
    def pickup_wh(self):
        return self.t_first_touch - self.t_arrival


@dataclass
class RunResult:
    records: list = field(default_factory=list)
    busy_wh: float = 0.0
    horizon_wh: float = 0.0
    n_estimators: int = 2

    def by_tier(self, attr):
        out = {}
        for t in TIERS:
            vals = [getattr(r, attr) for r in self.records if r.tier == t]
            out[t] = np.array(vals) if vals else np.array([0.0])
        return out

    def summary(self, rate_eur):
        cyc = self.by_tier("cycle_wh")
        tch = self.by_tier("touch_wh")
        n_years = self.horizon_wh / (176 * 12)
        s = {
            "cycle_median_wh": {t: float(np.median(cyc[t])) for t in TIERS},
            "cycle_p90_wh": {t: float(np.percentile(cyc[t], 90)) for t in TIERS},
            "touch_median_h": {t: float(np.median(tch[t])) for t in TIERS},
            "cost_per_quote_eur": {t: float(np.median(tch[t]) * rate_eur) for t in TIERS},
            "annual_inquiries": len(self.records) / n_years,
            "utilization": self.busy_wh / (self.horizon_wh * self.n_estimators),
            "pickup_median_wh": float(np.median([r.pickup_wh for r in self.records])),
            "clarified_share": float(np.mean([r.clarified for r in self.records])),
        }
        shares = {}
        for t in TIERS:
            med_c, med_t = np.median(cyc[t]), np.median(tch[t])
            shares[t] = 100.0 * (1 - med_t / med_c) if med_c else 0.0
        s["queue_share_pct"] = shares
        return s


class Estimator:
    def __init__(self, env, name, speed):
        self.res = simpy.PreemptiveResource(env, capacity=1)
        self.name = name
        self.speed = speed

    @property
    def load(self):
        return len(self.res.queue) + self.res.count


def lognormal(rng, median, sigma):
    return median * float(np.exp(sigma * rng.standard_normal()))


class AsIsModel:
    def __init__(self, params, seed=42):
        self.p = params
        self.rng = np.random.default_rng(seed)

    def run(self, years=12, warmup_months=2):
        p = self.p
        env = simpy.Environment()
        wh_month = p["clock"]["working_hours_per_day"] * p["clock"]["working_days_per_month"]
        horizon = years * 12 * wh_month
        warmup = warmup_months * wh_month
        result = RunResult()
        estimators = [Estimator(env, e["name"], e["speed"]) for e in p["estimators"]]
        result.n_estimators = len(estimators)

        def work(inq, est, duration, priority):
            remaining = duration
            while remaining > 1e-9:
                with est.res.request(priority=priority, preempt=(priority == 0)) as req:
                    yield req
                    if inq.t_first_touch is None:
                        inq.t_first_touch = env.now
                    start = env.now
                    try:
                        yield env.timeout(remaining)
                        worked = remaining
                        remaining = 0.0
                    except simpy.Interrupt:
                        worked = env.now - start
                        remaining -= worked
                        inq.preempted += 1
                    inq.touch_wh += worked
                    if env.now > warmup:
                        result.busy_wh += worked

        def inquiry(tier):
            lo, hi = p["pump_count_bounds"][tier]
            inq = InquiryRecord(tier=tier, t_arrival=env.now,
                                pumps=int(self.rng.integers(lo, hi + 1)))
            prio = 0 if (tier == "tier3" and inq.pumps >= p["preemption_pump_threshold"]) \
                else TIER_PRIORITY[tier]

            # 1. noticing delay (mailbox/batching before anyone engages)
            yield env.timeout(lognormal(self.rng, p["notice_delay"]["median_wh"],
                                        p["notice_delay"]["sigma"]))
            est = min(estimators, key=lambda e: e.load)

            total = lognormal(self.rng, p["touch_median_h"][tier], p["touch_sigma"]) * est.speed
            split = p["touch_split"]

            # 2. reading (desk queue in front of it is emergent)
            yield from work(inq, est, total * split["reading"], prio)

            # 3. clarification incidence (elapsed cost calibrated in step 5)
            if self.rng.random() < p["clarification"]["probability"][tier]:
                inq.clarified = True

            # 4. calculation & selection
            yield from work(inq, est, total * split["calc_select"], prio)

            # 5. external + administrative wait (fitted): contractor answers,
            #    pricing approval, dispatch batching
            f = p["fitted"]
            yield env.timeout(lognormal(self.rng, f["residual_queue_median_wh"][tier],
                                        f["residual_queue_sigma"][tier]))

            # 6. assembly & dispatch
            yield from work(inq, est, total * split["assembly"], prio)

            inq.t_done = env.now
            if inq.t_arrival > warmup:
                result.records.append(inq)

        def source(tier):
            rate = p["arrivals_per_month"][tier] / wh_month
            while True:
                yield env.timeout(float(self.rng.exponential(1.0 / rate)))
                env.process(inquiry(tier))

        for t in TIERS:
            env.process(source(t))
        env.run(until=horizon + warmup)
        result.horizon_wh = horizon
        return result
