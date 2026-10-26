#!/usr/bin/env python3
"""T17: replace the Section 1 outline bullets with the executive summary.

Half-page limit: ~290 words, five paragraphs (problem / solution+feasibility /
financials / strategic claim / recommendation). Every number is lifted from
Sections 4, 8, 9 and 11; no new figures. Style contract applies (no em dashes,
no announced rigor).
"""
import sys

from doc_editor import run

OLD = (
    "\u2022    1.1 Problem in one sentence, with the three measured baseline "
    "numbers (time, cost, error rate).\n"
    "\u2022    1.2 The proposed solution in one sentence, plus the headline "
    "feasibility finding (\u201ca structured audit of 30 historical RFQs found "
    "X% of extraction fields technically automatable with current document-AI "
    "capability; a calibrated process simulation projects median cycle time "
    "falling from X days to Y hours\u201d), evidence-led but honestly ex-ante.\n"
    "\u2022    1.3 Financial headline as a range, not a point: projected NPV "
    "(P10 / P50 / P90 from the Monte Carlo in 9.5), payback, and the floor "
    "case (\u201cclears the hurdle rate on cost savings alone under "
    "conservative assumptions\u201d).\n"
    "\u2022    1.4 The strategic claim: transaction data as the distributor\u2019s "
    "future moat.\n"
    "\u2022    1.5 The actual recommendation, where the framing is critical: "
    "not \u201cbuild the system\u201d but \u201capprove a stage-gated pilot "
    "investment of \u20ac X, with explicit go/no-go criteria at each gate.\u201d "
    "An ex-ante paper that recommends a bounded, testable next step is far "
    "more credible than one that recommends a rollout.\n"
)

NEW = (
    "Khoory\u2019s [Abu Dhabi] estimation office turned 640 pump RFQs into "
    "quotations in 2025 at measured median cycle times of 18, 39 and 88 "
    "working hours by complexity tier, of which only 2.1 to 11.4 hours is "
    "engineering work; the rest is queueing. Between 6 and 19 percent of "
    "quotations carry at least one defect, and the function leaks about five "
    "times its \u20ac33,000 running cost: roughly \u20ac67,000 a year to "
    "quality failures and \u20ac106,000 to unmanaged discounting.\n"
    "We propose QuoteBench, a document-extraction and pricing layer that "
    "drafts every quote and routes each by confidence, so engineers review "
    "rather than retype and judgement concentrates on the inquiries that need "
    "it. No prototype exists: capability inputs are taken from published "
    "document-AI benchmarks as ranges and fed to a process simulation that "
    "had to reproduce the 2025 baseline on fifteen checks before projecting "
    "anything. In the central case, median cycle time falls to 2, 9 and 56 "
    "working hours by tier, and engineer touch time roughly halves.\n"
    "Across 20,000 Monte Carlo draws at a 12 percent discount rate, five-year "
    "NPV runs from \u20ac94,000 (P10) through \u20ac260,000 (P50) to "
    "\u20ac457,000 (P90), with median payback of 1.6 years and a 98.5 percent "
    "probability of clearing the 15 percent hurdle. The floor case is "
    "negative: with the win-rate uplift at zero and extraction at its "
    "pessimistic bound, NPV is minus \u20ac83,000. The investment is a bet "
    "that faster, cleaner quotes win work, and the pilot tests that bet "
    "first.\n"
    "Strategically, automated quoting converts the branch\u2019s inquiry flow "
    "into structured transaction data that neither manufacturers nor "
    "marketplaces hold, the distributor\u2019s defensible position as the "
    "channel digitizes.\n"
    "We do not recommend building the system. We recommend approving Phase 1 "
    "only: a three-month shadow-mode pilot on one inquiry tier, opening with "
    "the feasibility audit of 25\u201330 historical RFQs on Khoory\u2019s own "
    "documents, inside a total build budget of \u20ac92,000 and with "
    "pre-committed kill criteria at every gate.\n"
)

EDITS = [{
    "find": OLD,
    "replace": NEW,
    "unbold": True,
    "bold": ["We do not recommend building the system."],
}]

if __name__ == "__main__":
    words = len(NEW.split())
    print(f"executive summary: {words} words")
    run(EDITS, apply="--apply" in sys.argv)
