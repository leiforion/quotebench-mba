# Financial Model Simulator — Approach Analysis & Development Plan

> **D19 rebase (6 Sep, post-SIM-6).** The authors supplied the actual 2025
> branch revenue: ~AED 150M won pump-only (EUR ~34.5M), average margin 24% on
> revenue, ~6.1x the SIM-3 derived base. All value parameters scaled x6.125
> (bands, mega range, V1 gate), margins rescaled 14/17/21 → 18.5/22.5/27.8
> (weighted 24.1%), BASE-30 defect unit costs value-scaled, BASE-31 pct target
> retired (quality scale = 1.0). All 37 tests pass; the calibration gate is
> unaffected (the process model is value-independent). New headline: NPV
> P10/P50/P90 = 1.49/2.82/4.40M EUR, hurdle cleared in every draw, floor case
> +342k @12%, no kill boundary in any tested stress range. Operating point
> unchanged (C1 0.85 / C2 0.70 / band ±1%). Paper Sections 1, 4.4, 6.3, 8.4
> and 9 restated; Exhibits 9.1–9.3 replaced (t24_rebase.py, t24b_images.py).

Authors' direction (6 Sep 2026): no audited source information will be available.
The simulator's inputs must be **generated** from the evidence already in the paper,
with variance for engineer skill and inquiry complexity, and the as-is model must
reproduce the measured current state (RFQ response times) before any projection is
trusted. The simulator runs in a terminal (Python), will be published to GitHub for
readers to reproduce, and doubles as the operating model for the product itself:
its outputs feed back into the design (routing thresholds, staffing, pricing bands).

---

## 1. Approaches considered

### Option A — single-layer financial Monte Carlo (what `monte_carlo.py` does today)
Annual benefit formulas sampled over parameter distributions; no queues, no
inquiries, no engineers.
- **Pros:** exists; fast; easy to explain.
- **Cons:** cannot calibrate to cycle times (it has no notion of elapsed time);
  cannot express skill or complexity variance except as hand-set multipliers;
  cannot answer capacity or utilization questions; weak as a self-improvement
  vehicle because the design parameters (confidence thresholds, value gates,
  staffing) do not appear in it.

### Option B — two separate models chained (the paper's original 3.3 wording)
A discrete-event process simulation for cycle time and capacity, whose summary
outputs feed a separate financial Monte Carlo.
- **Pros:** matches the current Section 3.3/8.2/9.5 text; clean division of labour.
- **Cons:** two parameter sets to keep consistent; the financial layer only sees
  aggregates, so inquiry-level effects (a specific Tier 3 quote won because it went
  out three days earlier) are lost; stress tests must be wired twice.

### Option C — unified inquiry-level simulation with embedded economics (recommended)
One discrete-event simulation of the branch, one inquiry at a time, where every
inquiry carries its own economics; the financial statements are aggregations of
simulated inquiries, and Monte Carlo is the outer loop (many simulated years over
sampled parameters).
- Arrivals by tier at measured 2025 rates; each inquiry gets complexity attributes
  (pump count, document-quality class, CAD flag, clarification need) and a quoted
  value drawn from tier-calibrated distributions.
- Estimators are resources with **skill profiles** (speed multiplier, error
  propensity, review throughput); queue discipline as observed, including
  pre-emption by large inquiries.
- **As-is mode is the calibration gate:** simulated median and P90 cycle time by
  tier, touch hours, queue share and cost per quote must match the measured
  register values within tolerance before to-be mode unlocks (enforced in code).
- **To-be mode** replaces the automated steps with system-lane times and routes
  each inquiry through the 7.7 confidence logic. The automation capability is
  **generated, not audited**: per-field extraction success by document-quality
  class, seeded from the published ranges already cited in 5.3, with the mix of
  document classes inferred from tier definitions; skill and complexity variances
  spread the outcomes.
- **Economics per inquiry:** labour at the loaded rate, error-cost events by class,
  discount variance against a reference price, win probability by tier adjusted by
  a response-time elasticity floored at zero. Aggregate a simulated year, subtract
  build/run/change costs, discount at 12% against the 15% hurdle, repeat across
  seeds and parameter draws for distributions.
- **Pros:** one code path and one input registry; the calibration story ("it
  reproduces 2025 before it projects 2030") is airtight and demonstrable in a
  terminal; skill and complexity are first-class; stress tests and the
  self-improvement loop act on the same decision variables the product would use.
- **Cons:** the most build effort of the three; needs discipline to keep runtimes
  reasonable (mitigated: a simulated year is ~640 inquiries, so 10k years is cheap).

### Option D — agent-based market simulation (contractors, competitors as agents)
Rejected: the paper has no behavioural data to parameterize competitor or
contractor agents; it would manufacture precision the evidence cannot support.

**Recommendation: Option C.** It is the only approach that satisfies all four
stated goals at once: calibrates to the current state, generates its own capability
assumptions with skill/complexity variance, stress-tests the finances, and exposes
the exact levers (thresholds, staffing, pricing bands) the product would ship with.
The existing `monte_carlo.py` is absorbed as the outer financial loop and its
`--validate` checks become part of the calibration gate.

## 2. Evidence the generator draws on (all already registered)

| Register rows | Feeds |
|---|---|
| BASE-10/11/12/13/14 (tier mix, value shares/bands, arrivals) | arrival and value generators |
| BASE-15/16/17 (cycle medians/P90, touch by tier) | calibration targets + step distributions |
| BASE-22/23/24/25/26 (queue share, assignment, clarification) | queue model |
| BASE-05/06 (loaded cost/rate) | labour economics |
| BASE-19/28/29/30/31 (defect rates, classes, unit costs) | error events |
| BASE-32/33 (discount spread, leakage) | pricing variance model |
| BASE-20/21 (win rates, margins) | win/margin model |
| BASE-09 + 9.3 triangulation (speed-loss bound) | elasticity ceiling |
| FIN-08, D11 (build cost, discount/hurdle rates) | investment case |
| 5.3 published extraction ranges | capability priors (replaces audit) |

## 3. Development phases

**SIM-0 — Repo and environment scaffolding.**
Separate `simulator/` tree (GitHub-ready): `python3 -m venv .venv`,
`requirements.txt` (numpy, simpy, matplotlib, pytest, pyyaml), `data/` seeded from
`model/assumptions.csv` (values only, no client-identifying text), `scenarios/`
YAML, `results/` gitignored, README with one-command reproduction
(`make reproduce` or `./run.sh`), fixed-seed protocol, MIT or no licence per
authors.

**SIM-1 — As-is engine + calibration gate.**
Discrete-event model of Exhibit 4.1 (arrivals, assignment queue, reading,
clarification loop at p=0.38 and 41 wh median, calculation, selection, pricing
approval, dispatch), estimators as resources with skill profiles, pre-emption for
large Tier 3. Fit step distributions (lognormal) so that simulated tier medians
18/39/88 wh, P90 34/71/162 wh, touch 2.1/5.5/11.4 h, queue share 86–88% and cost
per quote 25/66/137 EUR all land within ±10%. Calibration is a pytest suite; the
CLI refuses to run to-be scenarios if it fails. This phase is the credibility of
everything downstream.

**SIM-2 — Capability and variance layer (to-be mode).**
Document-quality classes per inquiry (clean digital / scanned / fragmented /
CAD-dependent) with a tier-conditioned mix; per-field extraction success by class
seeded from the 5.3 published ranges; 7.7 routing (auto-draft / assisted / manual
by confidence and value gate); engineer review times by skill; residual error
model (what review fails to catch). Skill profiles: named levels with speed and
error multipliers. Every parameter in one YAML with source notes.

**SIM-3 — Economics layer and P&L assembly.**
Per-inquiry: labour, error events and costs, discount vs reference price, win
draw with response-time elasticity (floored at zero), margin. Annual aggregation
to a projected P&L (labour, quality cost, discount recovery, incremental gross
margin, run costs), five-year cash flows with build/change costs, NPV at 12%,
hurdle at 15%, IRR, payback. Absorbs `model/monte_carlo.py`; its validation
checks migrate into the SIM-1 gate.

**SIM-4 — Stress-test harness.**
Scenario grid runner with named scenarios (demand surge/collapse, senior-estimator
attrition, extraction degradation to the pessimistic end of published ranges,
elasticity = 0, build overrun +30/+60%, adoption failure at Phase 2 gate);
tornado and P10/P50/P90 outputs; a kill-criteria finder that searches for the
parameter values at which NPV at the hurdle turns negative and reports them as
explicit boundaries (these become Section 11 kill criteria and 9.6 sensitivity).

**SIM-5 — Self-improvement loop.**
Expose the design's decision variables (confidence thresholds C1/C2, value gate
V1, tier routing defaults, discount-band width, staffing plan) as an optimization
surface; grid or evolutionary search maximizing risk-adjusted NPV subject to an
error-escape constraint; the chosen operating point is written back to the
assumptions register as S-tagged rows and becomes the parameter set the paper
recommends for the pilot. This is the "the model we test is the model we ship"
requirement made concrete.

**SIM-6 — Reader package and paper integration.**
Reproduce-everything entry point, seeds and data in the repo, figures/tables
exported for Sections 8–9 (calibration table, cycle-time distributions, NPV fan,
tornado), README quality pass, and the paper edits that re-source the simulation's
inputs (per the audit-framing decision) with a one-line pointer to the public repo.

## 4. Decisions (resolved 6 Sep 2026, D12-D16 in model/decisions.md)

1. **Audit**: 8.1 stays as a recommended pilot activity; simulation inputs come from
   published 5.3 ranges + variance + calibration (D12).
2. **Revenue base**: derived from registered tier volumes, value bands and win
   rates; S-tagged (D13).
3. **Skill mix**: branch 1 senior + 1 mid; company ~25/50/25 (D14, YAML-editable).
4. **Packaging**: `simulator/` in this workspace, GitHub later (D15).
5. **Stack**: numpy + simpy + matplotlib + pytest + pyyaml in .venv (D16).

Final task prompts: SIM-0..6 in `backlog.md`. SIM-0 and SIM-1 are unblocked.

## 5. SIM-1 build notes (6 Sep 2026) — structural deviations from the prompt

Both deviations were forced by the measured register values, not chosen for
convenience; both make the model more honest about how the branch works.

1. **Desk discipline is small-job-first, not FIFO.** The prompt specified FIFO
   within a desk. Under FIFO, emergent queueing at ~68% utilization pushes the
   Tier 1 cycle median to 25+ wh against the measured 18, and no non-negative
   fitted wait can pull it back. The measured pattern (Tier 1 barely delayed
   beyond pickup; Tier 3 at 88 wh median on 11.4 h of touch) is the signature
   of estimators knocking out quick inquiries between large ones. The engine
   uses tier priority in the desk queue, with very large Tier 3 arrivals
   pre-empting in-progress work as specified.
2. **The 41 wh clarification wait is calibrated in aggregate, not additive.**
   Treating BASE-24 as a separate additive delay is arithmetically
   incompatible with BASE-15/16: with 45% of Tier 2 clarified at a 41 wh
   median wait, the Tier 2 mixture median lands near 60 wh (measured: 39) and
   its P90 above 85 (measured: 71). The measured values only reconcile if the
   contractor's answer overlaps other waiting, i.e. the inquiry parks in
   the desk and approval queues while the answer comes. Clarification
   incidence is still drawn per tier (weighted to the measured 38%); its
   elapsed cost lives inside the fitted per-tier external wait. To-be
   scenarios re-split that wait using BASE-23/24/25 at projection time, where
   the split is identified because the to-be design changes the components
   separately.

Calibration outcome (seed 42, 12 simulated years): 15/15 gate assertions pass
within ±10%; pickup median 13.5 wh (measured 14, emergent, not imposed) and
clarification share 37% (measured 38%) reproduced as diagnostics. Fitted
external waits: `simulator/data/fitted_asis.yaml`; exhibit table via
`python -m sim report calibration`.

## 6. SIM-2 build notes (6 Sep 2026)

Delivered: `sim/capability.py` + `sim/tobe.py` + `data/parameters_tobe.yaml`
(every value S-tagged with a rationale note; extraction seeded from the 5.3
published ranges per D12, three variants). 21/21 tests pass, including the two
degradation gates: with the system down every inquiry drops into the calibrated
Section 4 process and reproduces the as-is baseline; with the system up but
extraction forced to zero, 100% of inquiries route manual at full as-is touch
(Tier 3 lands on the senior per 7.7, so his speed multiplier applies) and
as-is defect rates.

Central-variant projection (seed 42, 8 years), the numbers 8.x will draw on:
cycle medians 18/39/88 -> 1.9/8.3/54.7 wh; P90s 34/71/162 -> 7.0/35.2/105.1;
engineer touch medians 2.1/5.5/11.4 -> 0.8/2.7/6.0 h; engineer hours ~2,778 ->
~1,339 per year (~0.78 FTE freed); any-defect rate 9.2% -> 8.6%.

Findings that matter for the paper:

1. **Routing is far more manual than the walk-through suggests.** Central
   variant: Tier 1 = 22% auto / 16% assisted / 62% manual; Tier 2 = 22%
   assisted; Tier 3 = 100% manual (by design in Phase 1 routing). The cause is
   the paper's own honesty device (TOBE-08): routing on *minimum* field
   confidence over 12-24 fields compounds per-field uncertainty brutally, so
   one mediocre field sinks an otherwise clean inquiry. The benefits case
   survives because manual work is still assisted (pre-fill, calc engine,
   pricing rules). This is the strongest argument yet for SIM-5's threshold
   optimization and for the flywheel narrative: C1/C2 as stated are
   conservative, and 8.x should say so.
2. **Defect improvement in Phase 1 is modest (9.2% -> 8.6%), and honestly so:**
   the manual lane conservatively keeps full as-is defect rates, and most
   volume routes manual. The defect case improves with the route mix, i.e.
   with the flywheel, not before it.
3. **BASE-24 required tier-conditioning (4/20/41 wh for tiers 1/2/3).** The
   global 41 wh median is additive-incompatible with BASE-15/16 for tiers 1-2
   (same arithmetic as SIM-1 build note 2); Tier 3 keeps the full measured
   41 wh, matching the flagship case's multi-day replies. The as-is fitted
   external waits are charged to the manual lane net of their embedded
   clarification content to avoid double-counting.
4. **The walk-through (7.9) is a best case, and the simulation shows it:**
   simulated Tier 3 median lands at ~55 wh, not the ~20 wh the Innovo
   walk-through implies, because Phase 1 routes all Tier 3 through senior
   manual review. Worth a sentence in 7.9 or 8.x.

## 7. SIM-3 build notes (6 Sep 2026)

Delivered: `sim/economics.py` + `data/parameters_econ.yaml`; the old
`model/monte_carlo.py` harness is absorbed and retired. Design change worth
stating in 9.5: operational benefits now emerge from paired discrete-event
runs (as-is = the degraded to-be model, which reproduces the calibrated
baseline) instead of an assumed automation rate; the Monte Carlo draws
financial uncertainty (build overrun, run/change costs, pricing adoption,
win elasticity, and where on the published 5.3 spectrum the documents fall)
over those anchors, 20,000 iterations.

Baseline economics reproduced before projecting: value-band medians
calibrated so simulated tier value shares hit BASE-11 (12/41/47) within 1pp,
implying EUR ~19.9M quoted and ~5.1M won per year - the D13 derived revenue
base, landing where the old harness's placeholder guessed. Simulated
discount leakage reproduces BASE-33's 1.9% of revenue with the measured
4-18% spread anchored at a 9% like-for-like median.

Headline results (seed 42): NPV@12% P10/P50/P90 = EUR 82k/232k/408k;
P(clears 15% hurdle) = 98%; IRR median 64%; payback median 1.7 years.
Benefit medians per year at full adoption: labour redeployment 17.7k,
quality savings 16.5k, discount recovery 24.0k, win-uplift margin 85.7k.

Findings that matter for the paper:

1. **The 9.5 conservative case DOES NOT CLEAR the hurdle** (NPV@15% =
   EUR -121k; @12% = -119k). On cost + error + discounting alone, one branch
   at 640 RFQs/yr cannot pay for a EUR 92k build plus run costs. This is the
   same arithmetic as SEC6-01's 1,000-1,300 crossover, now confirmed by
   simulation. Section 9.5 must say so plainly and pivot the floor argument
   to what it actually is: the case rests on the win-rate elasticity
   (~37% of central-case benefits) and/or multi-branch deployment (9.1).
2. **The win-rate elasticity is the single largest benefit component**
   (median EUR 86k/yr of a ~144k total), which the paper itself calls its
   most attackable assumption (9.3). The P(hurdle)=98% headline leans on it;
   9.6's tornado will show it on top. Honest framing: without elasticity and
   without scale, this is a capability investment, not a cash machine.
3. **Quality savings can go NEGATIVE under pessimistic extraction**
   (unscaled to-be quality cost 30.8k vs as-is 30.0k): bad extraction plus
   automation-bias miss rates in the assisted lane produce slightly more
   escaped defects than all-manual work. This is 5.4's warning appearing
   unprompted in the numbers, and it strengthens the case for the
   conservative reviewer-miss parameters and the shadow-mode Phase 1.
4. **A quality-cost scale of ~2.3 was needed** to reconcile BASE-29/30
   (per-class frequencies and unit costs, both E) with BASE-31's 1.2%-of-
   revenue total (also E): the register's parts undershoot its whole by half.
   Flag for the authors; one of the two estimates should be revisited, or the
   1.2% treated as the anchor (as the simulator does).

### SIM-3 amendment (6 Sep, D17): pump costs researched, mega stream added

Authors confirmed quotes are pump-only and directed that the model carry at
least two flagship-museum-scale quotes per year. Researched trade prices
(Grundfos NB/NBS end-suction EUR 3.5-8.5k, CR multistage 1.2-7k, Hydro MPC
booster sets 11-60k, NFPA-20 fire skids 45-70k) support a pump-only package
of EUR 0.8-1.5M for a Guggenheim-class museum (~60-120 pumps on district
cooling: ETS/secondary CHW, zone circulators, boosters, two-zone fire,
drainage, TSE). Implemented as an explicit mega stream (2 of 72 Tier 3
inquiries/yr, uniform EUR 0.8-1.5M, ~22% of Tier 3 quoted value); value-band
medians recalibrated so BASE-11 shares still hold (8.3k/37.9k/84.5k).

Result: derived base EUR ~22.2M quoted / ~5.6M won (AED ~97M / ~25M). Revised
headlines: NPV@12% P10/P50/P90 = 94k/260k/457k; P(hurdle) 98.5%; IRR median
69%; payback 1.6 yrs; conservative case still DOES NOT CLEAR (-88k @15%,
improved from -121k). Win-gating in the economics is now expectation-weighted
(win probability multiplies value/leakage/quality contributions instead of a
Bernoulli draw): rare heavy-tailed quality events made lane deltas noisy at 3
seeds; means are unchanged.

**Structural note for the authors:** with BASE-11 value shares (12/41/47, M)
and the Tier 1 band cap (EUR 9.2k, M) both locked, total quoted value is
mathematically capped near EUR 22-27M regardless of how fat the Tier 3 tail
is made - Tier 1 must carry 12% of value at <=9.2k per quote. If the branch's
actual pump revenue is materially above ~EUR 5.6M won (~AED 25M), then
BASE-11 or the 640-log values are wrong and must be re-measured; that is
author data, not a simulator knob.

*(Logged as O9 in decisions.md; a bold AUTHORS-TO-CONFIRM note now sits in
the Doc at 9.1 so it cannot be missed at submission.)*

## SIM-4 build notes (6 Sep)

Built as specified: `sim/stress.py`, eight named scenarios in
`scenarios/*.yaml`, tornado, kill-criteria bisection, `sim stress` CLI behind
the calibration gate. Manifest: `results/stress_20260906_152724.json`.

Scenario table (central financial draws, NPV at the 15% hurdle):
only **elasticity_zero fails** (-28k). Everything else clears with room:
adoption failure +188k, build +60% +161k, demand collapse (-40% arrivals)
+59k, extraction pessimistic +158k, senior attrition +222k, demand surge
+357k. Senior attrition slightly *raises* the delta because losing the senior
hurts the as-is world more than the to-be world (the system lane does not
resign).

Tornado (NPV@12% one-at-a-time widths): win uplift 650k >> extraction 101k >
pricing adoption 65k > run cost 43k > build overrun 28k > change cost 20k.

Kill criteria (case fails at the 15% hurdle if):
- speed-win uplift falls below **~0.2pp** (all else central);
- build cost exceeds **~3.3x** plan (~EUR 308k);
- run costs exceed **~EUR 83k/yr** (~4x plan);
- demand falls below **~50%** of current volume;
- no failure boundary exists on extraction quality or pricing adoption alone.

Managerial reading for 9.6/11: the case is one-legged. Every operational
stressor has multiples of headroom; the single kill risk is the speed-win
elasticity, and even it only needs to be a tenth of the literature's low end.
That is what the pilot must measure first (11.1) and what the kill criterion
in Section 11 should be written around.

Engine fix en route: estimators now carry an explicit `skill` field
(reviewer-miss tables are keyed senior/mid) so attrition scenarios can staff
two mids without breaking defect draws.

## SIM-5 build notes (6 Sep)

Built `sim/optimize.py` + `sim optimize` CLI. Grid: C1 x C2 (12 valid DES
combos, C2 < C1) x discount-band halfwidth (re-priced from cached runs; the
Monte Carlo was refactored into `mc_from_anchors` so pricing knobs do not
re-simulate). Objective: P50 NPV@12%. Constraints: (1) to-be defect escape
rate <= as-is baseline (9.0% at the optimizer's seeds), (2) P10 of NPV at the
15% hurdle >= 0. Manifest: `results/optimize_20260906_153149.json`.

Chosen operating point (written to the register as SIM5-01..04, proposed):
**C1 = 0.85, C2 = 0.70, V1 = 9000, band halfwidth = +/-1%.** P50 NPV@12%
EUR 304k (vs 260k at design defaults), P10@hurdle +119k, defects 8.8% vs the
9.0% cap.

Findings that matter more than the optimum:
1. **The discount band dominates the search.** Halfwidth +/-1% beats +/-3% by
   EUR 70-90k of P50 NPV at *every* routing combination; C1/C2 tuning moves
   at most ~15k and part of that is seed noise (2 seeds). The real design
   lever is pricing discipline, not routing thresholds - feed to 7.6/9.2.
2. **The defect constraint binds, but costs almost nothing.** 21 of 36 grid
   points shipped more defects than as-is and were rejected; the best of them
   offered only EUR 515 more P50. The error-escape guarantee is nearly free -
   a strong line for 11.2 change-management.
3. **The P10 tail constraint never binds** (0 rejections): any operating
   point that respects defects also clears the hurdle at P10.
4. Caveat for the paper: the optimizer rewards ever-narrower discount bands
   because pricer-adoption risk is not modeled as a function of band width;
   +/-1% should be presented as "narrowest band governance will accept," not
   as a free lunch.

## SIM-6 build notes (6 Sep) — repo side complete

`sim figures` exports the four Doc exhibits at 6.5in/150dpi
(fig_calibration, fig_cycletimes, fig_npv_fan, fig_tornado, committed under
figures/). README rewritten with the claims framing, full command list and
headline outputs; run.sh now reproduces everything (fit, tests, calibration,
tobe, pnl, stress, optimize, figures) in one command; register snapshot
refreshed with the SIM5 rows. Remaining half of SIM-6 is Doc prose
(re-sourcing 3.3/8.1-8.2/9.5 per D12 + the repo pointer sentence): deferred
to T14, which writes Section 9 from the same manifests and should land the
language once.
