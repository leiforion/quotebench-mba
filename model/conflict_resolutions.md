# Conflict Resolutions (T04) — canonical values and propagation worksheet

All monetary conversions at AED 1 = €0.23 (D1). Status key: **LOCKED** (resolve and
propagate), **PROPOSED** (needs one-line author confirmation before propagation),
**OPEN** (needs author input to resolve at all).

---

## C1 — Currency · LOCKED
Canonical: EUR everywhere. Add one sentence at the end of 3.2:
> "All monetary figures are stated in euros, converted from UAE dirhams at
> AED 1 = €0.23; the underlying records are dirham-denominated."
Key conversions used throughout: €22,000/yr estimator cost · €12/h loaded rate ·
cost per quote €25 / €66 / €137 · tier thresholds <€9k / €9k–80k / >€80k ·
error unit costs ≈ €140 / €440 / €1,840 / €740 (site-failure tail > €5,750).

## C2 + C3 — Tier 2 definition and effort in 2.2 · LOCKED
Canonical: Table 4.1 taxonomy (3–12 pumps, ≤2 applications) and Table 4.2 touch
(5.5 h). Replace the 2.2 "Speed" opening:
> "A standard inquiry — three to twelve pumps across one or two applications —
> takes an estimator around five and a half hours of concentrated work: reading
> the specification and CAD files, running head loss calculations, selecting the
> model, and pricing it."

## C4 + C5 — Large-inquiry size and effort in 2.2 · LOCKED
Canonical: Tier 3 = >12 pumps; archetype = Innovo at 75 pumps / 28 h. Replace:
> "The largest inquiries — several dozen pumps across multiple applications, the
> Innovo package ran to seventy-five — demand twenty-five to thirty hours of
> estimating effort against deadlines that can be as tight as two or three days.
> They arrive roughly once a month but cannot be staffed as if routine."

## C6 — Error-rate phrasing in 2.2 · LOCKED
Canonical: inquiry-level defect rates 6/11/19% (Table 4.2). Replace:
> "Errors are not rare. Across the 2025 quotation audit, roughly one standard
> inquiry in nine went out containing at least one defect — a wrong model, a
> wrong price, or a missed specification requirement — rising to one in five on
> the largest, most valuable work. The full taxonomy and its costs are developed
> in Section 4.4."

## C7 — Loaded-rate bridge · LOCKED
The two figures reconcile at ~1,840 productive hours/yr (52 weeks − ~6 weeks
leave and public holidays = 46 weeks × 40 h): €22,080 ÷ 1,840 = €12.00/h exactly
(AED check: 96,000 ÷ 1,846 ≈ 52). Propagate:
- 2.2: "A fully loaded estimator costs the business approximately €22,000 a year."
- 4.1: "At a fully loaded rate of €12 per hour — €22,000 a year over roughly
  1,840 productive hours — the median inquiry carries about €66 of direct labour
  before overhead."
- Table 4.2 row: €25 / €66 / €137.

## C8 — 12 inquiries/estimator-week vs. 640/yr branch · PROPOSED
The clean reconciliation: **640 counts pump RFQs only** (the paper's product
scope), while estimators quote all product lines (pumps, valves, HVAC) at ~12
inquiries/estimator-week. Proposed 3.1 sentence:
> "Khoory's 16 estimators each handle on the order of twelve inquiries a week
> across all product lines; the 640 inquiries studied here are the pump RFQs of
> a single branch, the slice of that workload this paper's scope covers."
**Authors must confirm this is factually how the 640 was counted.** If not, one
of the two figures is wrong — say which.

## C9 — Queue-share range · LOCKED
Recomputed from Table 4.2: Tier 1 (18−2.1)/18 = 88.3%, Tier 2 85.9%, Tier 3
87.0%. Exhibit 4.2 caption becomes "between 86% and 88%".

## C10 — Table 4.4 chronology · LOCKED (rebuild)
Constraints preserved: touch = 28.0 h; receipt Thu 16:30; deadline Tue; issue
the following Thu (7 calendar days, 2 past deadline). Rebuilt rows:

| When | What happened | Touch | Waiting |
|---|---|---|---|
| Thu 16:30 | Inquiry received; sits unread overnight | — | — |
| Fri 10:15 | Triaged and assigned | 0.3 h | 17.5 h |
| Fri–Sat | Specs, schedules, drawings read across five applications; schedules transcribed; gaps found on two systems | 6.0 h | 0.5 h |
| Sat 14:00 | Consolidated clarification sent | 0.7 h | 0.3 h |
| Tue 11:20 | Contractor replies (weekend + Monday in between) | — | ~2.5 working days |
| Tue–Wed | Head-loss calculations, all five systems | 7.0 h | 1.5 h |
| Wed–Thu | Model selection across 75 pumps; curve-edge duty points | 8.0 h | 3.0 h |
| Thu | Senior estimator confirms curve-edge calls; booster re-check | 3.0 h | 2.0 h |
| Thu | Pricing and discount debated between sales and estimation | 2.0 h | 1.0 h |
| Thu evening | Quotation assembled and issued — two days past the deadline | 1.0 h | — |

Note: the old "~41 h" on the contractor row was the process-wide median from 4.1
echoed into a specific case; state Innovo's actual interval and keep the median
where it belongs.

## C11 — Innovo to-be touch figure in 7.9 · PROPOSED (value pending 8.2)
Replace "5.5 touch hours would become roughly 25 minutes" (a Tier 2 median inside
a Tier 3 case) with the Innovo-specific projection, bracketed until the
simulation runs:
> "Twenty-eight touch hours would become roughly [2.5–3]: the review of a
> 75-pump draft, the senior's confirmation of the flagged curve-edge selections,
> and a pricing check against the band."
The 5.5 h → 25 min contrast stays in 7.2 only, where it correctly describes the
Tier 2 median.

## C12 — Contractor reply time in the to-be walk-through · LOCKED (authors, 6 Sep)
7.2's own rule says the contractor's reply is "carried over unchanged from
measurement," but 7.9 has the reply arriving ~18 h after a Thursday-evening
request. Proposed: apply Innovo's own measured latency (request seen next
working day, reply the following morning). New 7.9 timeline: clarification out
Thu 16:53 → contractor sees it Friday → reply Monday morning → draft quote held
minutes later → reviewed at the estimator's 14:00 slot → **quote out Monday
afternoon: seven calendar days become four, a day ahead of the deadline instead
of two days late.** Slightly less dramatic than "one day," and much more
defensible — the only assumption it adds is that the request goes out five
calendar days sooner, which is the design's actual claim. Alternative (keep
Friday reply) requires a named assumption that consolidated same-evening
requests get faster answers — weaker ground.

## C13 — "22 hours" pre-clarification claim · LOCKED
Derivation: assignment queue median 14 wh (4.1) + reading/gap-finding ~6 h +
drafting ≈ 21–22 wh; Innovo's actual was ~21.5 wh (Thu 16:30 → Sat 14:00 in
worked hours). Keep "22 working hours" in 7.3/7.9 with a cross-reference to
Exhibit 4.1 ("median 14 hours to assignment plus a day of reading").

## C14 — Untagged percentages in 6.1 · LOCKED
Option B: "removes around 20 to 30 percent of the manual effort (E, estimator
interviews) — the curve reading and model matching." Option C: "addresses
roughly 10 to 15 percent of the touch time measured in Section 4 — pricing and
quote assembly (E)." Both get tags or get cut in the 6.x rewrite (T09).

## C15 — "15% of tenders lost" · LOCKED
Tag as (E, sales and management interviews) at first mention in 2.2, with a
forward reference: "an estimate the financial model treats as an upper bound
and triangulates in 9.3."

## C16 — Table/exhibit numbering · deferred to T07 (mechanical).

## C17 — Business-model frame · RESOLVED by D7
Internal case carries Section 9; workbook becomes the 10.3 licensing exhibit.

## C18 — Workbook currency · LOCKED
Convert the 10.3 exhibit to EUR at 0.23 when built (Phase 4).

## C19 — Build cost sourcing · OPEN (context clarified 6 Sep)
Yes, technology-focused: "vendor quotes" means priced estimates for building the
QuoteBench MVP — the intake/extraction pipeline, product database, hydraulic
engine, review workspace, and ERP integration. Section 9.4's own standard says
the build cost must be *sourced*, not guessed, via any of:
(a) indicative quotes from 1–2 software development firms / system integrators
    for the Phase 1 scope (strongest evidence; authors would request these);
(b) a bottom-up engineer-month estimate at market rates (buildable now from the
    7.8 component table — agent task);
(c) analogous-project benchmarks.
Run costs (LLM API inference at projected inquiry volume, hosting, manufacturer
API access) are separately priceable from public price lists — agent task.
The €92k MVP figure currently has no basis of any kind; route (b) + run-cost
pricing gives it one until real quotes arrive, and the MC's build-cost
distribution gets centred on it with the +30% overrun tail.

## C20 — Product name · RESOLVED by D7
"Khoory's QuoteBench." Introduce once at the top of Section 7 ("the proposed
system, referred to here as QuoteBench"), use sparingly after.

## C21 — Monte Carlo drivers · RESOLVED by D7
Internal driver model to be built in Phase 4 (T13 prompt updated).

## C22 — Discount / hurdle rate · PROPOSED (recommendation given 6 Sep)
Benchmark context: listed industrial distributors (Grainger, Fastenal, Ferguson,
Rexel, Applied Industrial) carry WACCs of ~8–11% — stable demand, modest betas.
A private, family-owned UAE trading group adds size and illiquidity premia,
putting a defensible cost of capital at ~10–13%; GCC family groups commonly
apply 12–15% hurdle rates to internal projects.
**Recommendation: discount at 12% (WACC proxy), approve against a 15% hurdle,
and let the Monte Carlo carry the project-specific risk in the cash flows.**
The finance-methods point for 9.5: risk must not be double-counted — the MC
already models automation-rate, win-rate and build-cost uncertainty in the cash
flows, so the discount rate should NOT also carry an ad-hoc technology premium
(that is what the workbook's 20% implicitly did). Sensitivity tests the rate
from 10% to 20%. The 20% stays only in the 10.3 venture exhibit, where
early-stage venture risk genuinely lives in the rate.

## C23 — Margin conflation guard · LOCKED (style rule)
Distributor product margins (14–21%) and any software-business margin (~82%)
never appear in the same paragraph without entity labels.

## C24 — "??" unit costs in workbook · OPEN
€7.4k/customer/yr cost-of-revenue and €4.1k onboarding equivalents need sourcing
before the 10.3 exhibit is credible. (Owner: authors.)
