#!/usr/bin/env python3
"""T14 + SIM-6 paper integration: write Sections 8 and 9 from the simulator
results, re-source 3.1/3.3 per D12 (no audited inputs; capability from
published ranges, gated on calibration), fix the 7.9 touch-hours placeholder,
and lay caption anchors for the five exhibits (images inserted by t19b).
"""
import sys

from doc_editor import run

S81 = (
    "No system has been built, so nothing in this section is a measurement of "
    "a live tool; every capability figure is a simulation input, tagged S and "
    "registered in Appendix A. What we could ground, we did. The mix of "
    "document quality that arrives at the desk (clean digital PDFs, scanned "
    "schedules, email fragments, CAD-dependent inquiries) is estimated by tier "
    "from the 640-inquiry log and the 22 inquiries we observed end to end. The "
    "extraction performance the design could plausibly achieve on each "
    "document class is taken from the published benchmark ranges reviewed in "
    "5.3 and carried as three variants (pessimistic, central, optimistic) "
    "rather than a single point. Engineer skill and inquiry complexity then "
    "spread those figures further: per-field success and confidence are drawn "
    "inquiry by inquiry, so no single accuracy number is load-bearing anywhere "
    "downstream.\n"
    "We had originally designed a field-by-field feasibility audit of 25\u201330 "
    "historical RFQs, scored by the estimators against a written rubric, to "
    "replace these ranges with evidence from Khoory's own documents. That "
    "audit remains the right instrument, and its materials are drafted "
    "(protocol, rubric and scoring sheet in Appendix E), but it needs "
    "estimator time we could not commission for this paper. It is therefore "
    "scheduled as the first activity of the Phase 1 pilot (11.1); until it "
    "runs, the capability inputs stay on the published ranges. The consequence "
    "is stated once: if Khoory's documents score materially below the "
    "pessimistic bound, Section 9 weakens, and the pilot's first gate exists "
    "to catch exactly that."
)

S82 = (
    "The simulator described in 3.3 replays the branch one inquiry at a time. "
    "Before it may project anything, it must reproduce the 2025 baseline it "
    "was built from: median and P90 cycle times by tier, touch hours, cost per "
    "quote, annual volume, queue share of elapsed time and estimator "
    "utilization, fifteen checks in all, each within ten percent of the "
    "measured value. The current build passes all fifteen (Exhibit 8.1); the "
    "gate is enforced in code, and every to-be number in this paper is locked "
    "behind it.\n"
    "Exhibit 8.1. Calibration gate: measured 2025 baseline versus the "
    "simulated as-is process; all checks pass within tolerance (S; seed 42, "
    "run manifests in the public repository).\n"
    "Calibrating taught us three things about the office that no interview "
    "surfaced: the estimators work small jobs first, which is why Tier 1 "
    "waits stay short at 68 percent utilization; assignment delay is "
    "queueing, not procedure; and clarification waiting overlaps other "
    "queues rather than adding to them. Each finding changed the model "
    "before it passed.\n"
    "With the baseline earned, the Section 7 design runs under the 8.1 "
    "capability ranges. In the central case, median cycle time falls from 18 "
    "to about 2 working hours for Tier 1, from 39 to 9 for Tier 2 and from 88 "
    "to 56 for Tier 3, with P90s falling in step (Exhibit 8.2); median "
    "engineer touch drops from 2.1 to 0.8 hours, 5.5 to 2.7 and 11.4 to 6.2 "
    "by tier (S). Routing stays deliberately cautious: 15 percent of Tier 1 "
    "inquiries release as auto-drafts and a quarter go out assisted; Tier 2 "
    "is one-fifth assisted; every Tier 3 quote stays with an engineer, worked "
    "in the pre-filled workspace. Engineering hours on quoting fall from "
    "about 2,780 to about 1,380 a year at unchanged volume, and the stress "
    "runs of 9.6 show the same two estimators absorbing a 40 percent demand "
    "surge that breaks the as-is desk. Escaped defects hold at parity with "
    "the baseline (9.1 versus 9.2 percent of inquiries), which is a design "
    "constraint rather than a bonus: reviewer attention drops on "
    "machine-drafted work, and the routing thresholds are set so the two "
    "effects cancel.\n"
    "Exhibit 8.2. Simulated cycle-time distributions by tier, as-is versus "
    "to-be central case; dashed lines mark medians (S).\n"
    "The degradation requirement of 7.1 also holds: with extraction forced to "
    "zero, the model reproduces the as-is baseline, so a failed capability "
    "assumption returns the office to today's process rather than to "
    "something worse."
)

S83 = (
    "Validation by the people involved is partly done and partly scheduled. "
    "The estimators challenged the swimlane, the tier taxonomy and the error "
    "audit during measurement, and two of their corrections (small jobs "
    "first, clarification overlapping other waits) became load-bearing "
    "calibration facts in 8.2. The contractor interviews (protocol in "
    "Appendix D) and a structured review of the Section 7 architecture are in "
    "progress; their scores and dissents will be reported here, and the "
    "routing thresholds they challenge are the same parameters the pilot "
    "re-measures."
)

S84 = (
    "What the evidence supports: the measured baseline and its costs "
    "(Section 4); the calibrated capacity arithmetic of 8.2; and roughly "
    "\u20ac53,000 a year of simulated benefit that does not depend on winning "
    "a single additional order (the labour, error and discounting effects of "
    "9.2). What remains unproven: extraction accuracy on Khoory's own "
    "documents; contractor acceptance of faster, system-assembled quotes; "
    "engineer adoption of the review workspace; and above all the win-rate "
    "response to speed, which 9.5 shows carries the investment case. Each "
    "unproven item maps to a Phase 1 pilot measurement with a go/no-go gate "
    "in 11.1, and the floor case in 9.5 states what happens if the pilot "
    "returns the pessimistic answer."
)

S91 = (
    "The quoting function is cheap to run and expensive to get wrong. Direct "
    "quoting cost is about \u20ac33,000 a year: 636 inquiries at \u20ac25, "
    "\u20ac66 and \u20ac136 per quote by tier (E), absorbing about 2,780 "
    "engineer hours. Throughput is roughly \u20ac2.8 million of won value per "
    "estimator per year. The leakage is larger than the labour: quality "
    "failures cost about 1.2 percent of revenue (E, \u20ac67,000 on the "
    "derived base) and unmanaged discounting another 1.9 percent (E, "
    "\u20ac106,000), so the office leaks about five times what it costs to "
    "operate. The revenue base behind those percentages is derived, not read "
    "from accounts (D13): tier volumes, value bands and win rates already in "
    "the register compound to \u20ac22.2 million quoted and \u20ac5.6 million "
    "won per year (S), including two flagship-scale projects a year (D17)."
)

S92 = (
    "Exhibit 9.1 shows the projected annual benefit at full adoption, central "
    "case, as four bars that do not overlap by construction: each is computed "
    "on its own base.\n"
    "Engineering capacity, \u20ac17,000 a year (S): about 1,400 hours valued "
    "at the loaded rate, not at revenue. The assumption is redeployment, not "
    "redundancy; the hours move to Tier 3 work, declined inquiries and the "
    "clarification chase, which also defuses the change-management tension "
    "addressed in 11.2.\n"
    "Error cost, \u20ac8,000 a year (S): escaped-defect cost on won orders at "
    "the register's unit costs, with overall defect rates held at parity "
    "(8.2); the saving comes from the mix shifting away from expensive "
    "selection errors, not from a lower headline rate.\n"
    "Discounting discipline, \u20ac28,000 a year (S): the sleeper. Quoting "
    "inside a reference band recovers part of the measured 4\u201318 percent "
    "spread on comparable work (M); we count only the 40\u201390 percent of "
    "that recovery that pricing governance is assumed to enforce.\n"
    "Win-rate uplift, \u20ac96,000 a year (S): the dominant bar and the least "
    "proven, gated next in 9.3.\n"
    "Exhibit 9.1. Projected annual benefits at full adoption, central case "
    "(S; run manifest in the public repository).\n"
    "The central total is about \u20ac150,000 a year at full adoption, "
    "reached on the 7.10 ramp. A fifth benefit, volume the branch currently "
    "declines or ignores, is real but unmodelled; it is left out of every "
    "number in this paper, which is the conservative direction."
)

S93 = (
    "The speed\u2013win elasticity is the single most attackable assumption, "
    "so it is triangulated and then floored. Internal evidence: sales "
    "attribute about 15 percent of lost tenders to late or rushed quotes (E), "
    "an upper bound on what speed can recover. Customer evidence: the "
    "contractor interviews of 4.6 (in progress, protocol in Appendix D) ask "
    "directly how speed weighs against price; the model takes no credit for "
    "anything they have not yet said. Industry evidence: the response-time "
    "literature reviewed in Section 5 supports a positive but modest effect. "
    "The model therefore carries the uplift as a range from zero to five "
    "percentage points of win rate with a central value of two (S); five "
    "points on a 27 percent Tier 2 base is an 18 percent relative gain, "
    "inside the ceiling the lost-tender estimate implies. The floor case of "
    "9.5 sets it to zero outright. The stress runs add the most useful fact "
    "in the paper: the investment clears its hurdle if speed is worth as "
    "little as 0.2 percentage points of win rate, one-tenth of the central "
    "estimate, and fails only if it is worth almost nothing at all (S)."
)

S94 = (
    "Costs enter the model as ranges, and their sourcing is stated. Build: "
    "\u20ac92,000, priced as one internal software-engineer year (D10). We "
    "have no build experience of our own, so this is an analogy price rather "
    "than a vendor quotation, and the Monte Carlo carries an overrun tail to "
    "+30 percent, with 9.6 stressing to +60. Run: \u20ac15,000\u201327,000 a "
    "year for inference and API usage at projected volume, licences, and "
    "0.2\u20130.5 FTE of maintenance; this range is provisional, and vendor "
    "quotations replace it before any build decision. Change: "
    "\u20ac10,000\u201330,000 once, for training and the transition "
    "productivity dip. Every range is drawn as a distribution in 9.5, and "
    "the boundaries in 9.6 state how far any of them may grow before the "
    "case dies."
)

S95 = (
    "The financial model runs 20,000 Monte Carlo draws over the ranges "
    "established above: extraction capability across the 8.1 variants, the "
    "win-rate uplift of 9.3 and the cost ranges of 9.4, with benefits "
    "anchored to the calibrated process model of 8.2 and phased in on the "
    "7.10 adoption ramp. We discount at 12 percent as a WACC proxy and test "
    "approval against a 15 percent hurdle. Five-year NPV comes out at "
    "\u20ac94,000 at P10, \u20ac260,000 at P50 and \u20ac457,000 at P90; the "
    "probability of clearing the hurdle is 98.5 percent, median IRR is 69 "
    "percent, and median payback is 1.6 years (S; Exhibit 9.2).\n"
    "Exhibit 9.2. Five-year NPV at 12 percent across 20,000 draws, with P10, "
    "P50 and P90 marked (S).\n"
    "The floor case matters most. Set extraction to the pessimistic bound, "
    "the win uplift to zero and the build 30 percent over, and benefits fall "
    "to about \u20ac42,000 a year against the same cost base: NPV is minus "
    "\u20ac83,000 at 12 percent and minus \u20ac88,000 at the hurdle. The "
    "project does not clear on cost, error and discounting alone. Stated "
    "plainly, this investment is a bet that faster, cleaner quotes win at "
    "least some additional work, cushioned by operating savings that cover "
    "most of the downside. The evidence that de-risks the bet is exactly "
    "what Phase 1 of the pilot measures first: extraction accuracy on "
    "Khoory's own documents and the win-rate response on live inquiries "
    "(11.1)."
)

S96 = (
    "Exhibit 9.3 ranks the levers one at a time. The win uplift dominates: "
    "its zero-to-five-point range moves NPV by \u20ac650,000, six times the "
    "next lever (extraction capability, \u20ac101,000); pricing adoption, run "
    "cost, build overrun and change cost together move less than extraction "
    "alone. The same stress runs turn the ranking into thresholds a board "
    "can hold us to: at central values elsewhere, the case fails at the "
    "hurdle only if the uplift falls below 0.2 percentage points, the build "
    "exceeds 3.3 times plan, run costs exceed \u20ac83,000 a year, or demand "
    "halves; extraction quality and pricing adoption have no failure "
    "boundary on their own (S). These boundaries reappear as pilot kill "
    "criteria in 11.1, alongside the operating point the simulator's search "
    "proposes: auto-draft threshold 0.85, assisted threshold 0.70 and a "
    "discount band of plus or minus 1 percent (S, proposed; the pilot "
    "validates all three).\n"
    "Exhibit 9.3. One-at-a-time sensitivity of five-year NPV at 12 percent "
    "(S).\n"
    "The Innovo inquiry closes its loop here. As measured in 4.5: 28 touch "
    "hours across three estimators, about \u20ac340 of direct cost, seven "
    "calendar days, issued two days late. As simulated at the central case, "
    "applying the 8.2 Tier 3 ratios: roughly 15 touch hours (11 to 20 across "
    "the capability range), about \u20ac180, and about four calendar days, "
    "with the contractor's reply carried at its measured pace; the quote "
    "goes out a day inside the deadline (S). The \u20ac160 of processing "
    "saved is beside the point. On a package of this size the margin at "
    "stake is roughly \u20ac200,000\u2013300,000 (M), and what the redesign "
    "buys is the deadline, plus the absence of the two near-misses that "
    "almost turned a late quote into a wrong one."
)

EDITS = [
    # ---- Section 8 headings
    {"find": "8.1 Technical feasibility audit (audited evidence)",
     "replace": "8.1 Capability evidence: what the automation could plausibly do"},
    {"find": "8.2 Process simulation (simulated evidence)",
     "replace": "8.2 Process simulation: calibration first, projection second"},
    # ---- Section 8 bodies
    {"find": "\u2022    Sample 25\u201330 historical RFQs across tiers. For each, your engineers score every required data field: cleanly present in machine-readable text / present but embedded in image or table / ambiguous, requires judgement / absent, requires clarification.\n\u2022    Build a document-complexity typology from the sample (clean digital PDF / scanned schedule / email fragments / CAD-dependent) with volume shares.\n\u2022    Map each document type to published document-AI accuracy benchmarks (from 5.3), stating the mapping assumptions. Output: an evidence-based range for the achievable automation rate, by tier, the single most important input to Sections 8.2 and 9.\n\u2022    Optional zero-build probe: run 5\u201310 redacted sample documents through an off-the-shelf LLM (no code, an afternoon) purely to sanity-check the benchmark mapping. If you do this, label it a \u201cdirectional probe,\u201d not a prototype; if you prefer not to, the audit stands on its own.",
     "replace": S81, "unbold": True},
    {"find": "\u2022    Build the cycle-time / capacity model described in 3.3, parameterized entirely from Section 4 measurements (arrival rates, touch times, queue discipline, engineer capacity).\n\u2022    Calibrate first: show the model reproducing the measured As-Is median and P90 cycle times within a stated tolerance. This calibration step is the credibility of the entire section: a model that recreates observed reality earns the right to project a different one.\n\u2022    Then run To-Be scenarios across the automation-rate range from 8.1. Report outputs as distributions: projected cycle time (median, P90), engineer utilization, and quoting capacity, under low / central / high automation.\n\u2022    One exhibit: As-Is measured vs. As-Is simulated (the calibration proof) vs. To-Be simulated (the projection). Three bars that carry the whole argument.",
     "replace": S82, "unbold": True,
     "bold": ["Exhibit 8.1.", "Exhibit 8.2."]},
    {"find": "A structured design review: your engineers (and, if accessible, one external AI/automation practitioner) walk the Section 7 architecture and formally score each component for feasibility, flag failure modes, and challenge the routing thresholds. Report it as a mini-Delphi: scores, dissents, and what you changed in the design as a result. Showing the design changed under expert challenge is ex-ante rigour at its best.",
     "replace": S83, "unbold": True},
    {"find": "Three short lists: what the evidence supports; what remains unproven; and, critically, the explicit register of assumptions that only a real pilot can validate (live extraction accuracy, contractor acceptance, engineer adoption). This register becomes, verbatim, the Phase 1 pilot charter in Section 11. That hand-off (\u2018here is exactly what we could not prove, and here is the bounded experiment that proves it\u2019) is the signature move of a first-class ex-ante paper.",
     "replace": S84, "unbold": True},
    # ---- Section 9 bodies
    {"find": "Annual fully-loaded quoting cost, revenue throughput per engineer, quantified leakage (errors + discounting), all from 4.3/4.4; no new numbers.",
     "replace": S91, "unbold": True},
    {"find": "One exhibit, each bar tagged measured / audited / simulated and explicitly de-overlapped:\n\u2022    Engineering cost productivity, with the redeployment assumption stated: capacity redirected to complex, high-value quotes, not headcount reduction (also defuses the change-management tension in 11.2).\n\u2022    Error-cost elimination.\n\u2022    Discounting discipline: often the sleeper #1 benefit; flag it.\n\u2022    Win-rate uplift from speed.\n\u2022    Volume capacity: RFQs currently declined or ignored.",
     "replace": S92, "unbold": True, "bold": ["Exhibit 9.1."]},
    {"find": "Your single most attackable assumption. Triangulate: (a) your own historical data (win rate vs. response time on past quotes, even crude); (b) contractor interview evidence from 4.6; (c) industry evidence. State the range; use the low end in the base case.",
     "replace": S93, "unbold": True},
    {"find": "Build (development, integration, data cleanup) \u00b7 run (inference/API at projected volume, licences, 0.2\u20130.5 FTE maintenance) \u00b7 change costs (training, transition productivity dip). Since you have no build experience to draw on, source cost estimates from analogous projects or vendor quotations and say so; an audited cost estimate beats a guessed one.",
     "replace": S94, "unbold": True},
    {"find": "\u2022    Five-year NPV, IRR, payback; discount rate justified.\n\u2022    Monte Carlo appraisal: run the financial model over the input distributions established in 8.1 (automation rate), 9.3 (win-rate uplift), and 9.4 (build cost). Report NPV as P10 / P50 / P90 and the probability of clearing the hurdle rate. This is the natural financial companion to the process simulation and the strongest possible replacement for implementation results.\n\u2022    Retain the hostile conservative case: automation at 50% of the audited central estimate, zero win-rate uplift, 30% build overrun. If it clears the hurdle on cost + error + discounting alone, you have a floor argument; if not, say so and identify the evidence that would de-risk it.",
     "replace": S95, "unbold": True, "bold": ["Exhibit 9.2."]},
    {"find": "Tornado chart on: win-rate uplift, automation rate (audited range), extraction accuracy, build cost, redeployment value. Plus Innovo unit economics: the one RFQ, As-Is (measured) vs. To-Be (simulated): cost, time, margin. The vignette closes its financial loop here.",
     "replace": S96, "unbold": True, "bold": ["Exhibit 9.3."]},
    # ---- 3.1: tag definitions per D12 (no audited evidence in the paper)
    {"find": "**Audited** means produced by the structured feasibility study of 8.1, scored by estimators against a written rubric on real historical documents. "
     if False else "Audited means produced by the structured feasibility study of 8.1, scored by estimators against a written rubric on real historical documents. ",
     "replace": "Estimated means derived from sampled data or structured interviews. ",
     "bold": ["Estimated"], "unbold": True},
    {"find": "challenge the design's assumptions, not to endorse them (8.1, 8.3, 4.6)",
     "replace": "challenge the design's assumptions, not to endorse them (8.3, 4.6)"},
    # ---- 3.3: re-source per D12 + repository pointer
    {"find": "It runs on the authors' operations-simulation platform (Appendix F) and must reproduce the measured baseline (median and P90 cycle time by tier, within a stated tolerance) before any to-be scenario is run; the calibration error appears in 8.2. To-be scenarios then run across the audited automation range and report cycle time, utilization and capacity as distributions.",
     "replace": "It is a discrete-event simulation built for this study; the full code, parameters, seeds and run manifests are public at [repository URL] (Appendix F), so every simulated number in this paper can be reproduced to the digit. The model must reproduce the measured baseline (median and P90 cycle time by tier, within ten percent) before any to-be scenario is run; the calibration evidence appears in 8.2. To-be scenarios then run across the capability range built in 8.1 from published benchmarks, and report cycle time, utilization and capacity as distributions.",
     "unbold": True},
    {"find": "the automation rate, bounded by the 8.1 audit;",
     "replace": "the extraction capability, spanning the published ranges mapped in 8.1;"},
    {"find": "pending the authors' platform documentation; the platform's modelling approach, calibration and validation logic go to Appendix F.",
     "replace": "; the simulator's modelling approach, calibration and validation logic go to Appendix F."},
    # ---- Table 3.1 cells per D12
    {"row_anchor": "Feasibility audit sample",
     "old_cell": "Document-complexity typology; evidence-based automation-rate range",
     "new_cell": "Pilot instrument (Appendix E): replaces the simulated capability ranges with evidence from Khoory's own documents"},
    {"row_anchor": "Feasibility audit sample", "old_cell": "8.1, 8.2, 9.5",
     "new_cell": "8.1, 11.1"},
    {"row_anchor": "Feasibility audit sample", "old_cell": "A",
     "new_cell": "planned"},
    {"row_anchor": "Simulation models",
     "old_cell": "Process model (authors' operations-simulation platform, Appendix F) + financial Monte Carlo",
     "new_cell": "Discrete-event process model + financial Monte Carlo; code, parameters, seeds and manifests published (Appendix F)"},
    {"find": "Tags: M measured, E estimated from sampled data or structured interview, A audited per the 8.1 protocol, S simulated. Bracketed counts to be finalized.",
     "replace": "Tags: M measured, E estimated from sampled data or structured interview, S simulated. The feasibility audit is a planned pilot instrument, not yet evidence. Bracketed counts to be finalized."},
    # ---- 7.9 touch-hours placeholder now has a simulated value
    {"find": "twenty-eight touch hours would become roughly [2.5\u20133, pending the Section 8 simulation]",
     "replace": "twenty-eight touch hours would become roughly fifteen (S: eleven to twenty across the 8.1 capability range)"},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
