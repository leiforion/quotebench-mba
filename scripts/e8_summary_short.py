#!/usr/bin/env python3
"""Shorten the executive summary to three paragraphs per author direction:
QuoteBench named as the proposed automated system, and the recommendation
restated as building the system in strategic phases to prevent
over-committing. Section 13's closing recommendation is aligned so the paper
does not contradict itself.
"""
import sys

from doc_editor import run

EDITS = [
    # P1: compress the leakage line and fold the proposal sentence in.
    {"find": ("Between 6 and 19 percent of quotations carry at least one "
              "defect, and against the branch\u2019s \u20ac34.5 million of "
              "won pump orders the function leaks about twenty-five times "
              "its \u20ac33,000 running cost: roughly \u20ac177,000 a year "
              "to quality failures and \u20ac673,000 to unmanaged "
              "discounting."),
     "replace": ("Between 6 and 19 percent of quotations carry at least one "
                 "defect, and the function leaks about twenty-five times its "
                 "\u20ac33,000 running cost, mostly to unmanaged "
                 "discounting. We propose QuoteBench, an automated quoting "
                 "system: a document-extraction and pricing layer that "
                 "drafts every quote and routes each by confidence, so "
                 "engineers review rather than retype and judgement "
                 "concentrates on the inquiries that need it.")},

    # Old P2 becomes the single evidence-and-numbers paragraph.
    {"find": ("We propose QuoteBench, a document-extraction and pricing "
              "layer that drafts every quote and routes each by confidence, "
              "so engineers review rather than retype and judgement "
              "concentrates on the inquiries that need it. No prototype "
              "exists. Capability inputs are taken from published "
              "document-AI benchmarks as ranges and fed to a process "
              "simulation that had to reproduce the 2025 baseline on "
              "fifteen checks before projecting anything. In the simulated "
              "central case, median cycle time falls to 2, 9 and 56 working "
              "hours by tier, and engineer touch time roughly halves."),
     "replace": ("No prototype exists. Capability inputs come from published "
                 "document-AI benchmarks, fed through a process simulation "
                 "that reproduced the 2025 baseline on fifteen checks before "
                 "projecting anything. In the simulated central case, median "
                 "cycle time falls to 2, 9 and 56 working hours by tier and "
                 "engineer touch time roughly halves. Benefits reach about "
                 "\u20ac990,000 a year at full adoption, of which about "
                 "\u20ac210,000 does not depend on winning a single "
                 "additional order. Five-year NPV runs from \u20ac1.4 "
                 "million (P10) to \u20ac4.3 million (P90) across 20,000 "
                 "Monte Carlo draws, and every draw clears the 15 percent "
                 "hurdle. No single lever within its tested range sinks the "
                 "case, even with the win-rate uplift set to zero. "
                 "QuoteBench also converts the branch\u2019s inquiry flow "
                 "into structured transaction data that neither "
                 "manufacturers nor marketplaces hold, the distributor\u2019s "
                 "defensible position as the channel digitizes.")},

    # Delete the three paragraphs now folded in above.
    {"find": ("Simulated benefits reach about \u20ac990,000 a year at full "
              "adoption. About \u20ac210,000 of that does not depend on "
              "winning a single additional order. The rest is the win-rate "
              "uplift from faster quoting, the model\u2019s least proven "
              "input. Across 20,000 Monte Carlo draws at a 12 percent "
              "discount rate, five-year NPV runs from \u20ac1.4 million "
              "(P10) through \u20ac2.7 million (P50) to \u20ac4.3 million "
              "(P90), clearing the 15 percent hurdle in every draw, with "
              "median payback of about four months.\n"),
     "replace": ""},
    {"find": ("Stress testing found no single lever that sinks the case "
              "within its tested range. Even the floor case (win-rate "
              "uplift at zero, extraction at its pessimistic bound, the "
              "build 30 percent over) still returns about \u20ac0.2 million "
              "of NPV at the hurdle, on labour, error cost and discount "
              "discipline alone. Every capability figure is simulated, so "
              "the pilot\u2019s kill criteria are set on evidence: live "
              "extraction accuracy, engineer override rates and escaped "
              "defects.\n"),
     "replace": ""},
    {"find": ("Automated quoting also converts the branch\u2019s inquiry "
              "flow into structured transaction data that neither "
              "manufacturers nor marketplaces hold. That data is the "
              "distributor\u2019s defensible position as the channel "
              "digitizes.\n"),
     "replace": ""},

    # Recommendation paragraph: build, in phases, with the gates.
    {"find": ("We do not recommend building the system. We recommend "
              "approving Phase 1 only: a three-month shadow-mode pilot on "
              "one inquiry tier costing roughly \u20ac30,000 (S), opening "
              "with the feasibility audit of 25\u201330 historical RFQs on "
              "Khoory\u2019s own documents, inside a total build budget of "
              "\u20ac92,000 and with pre-committed kill criteria at every "
              "gate. Breach any gate and the recommendation reverts to "
              "hiring."),
     "replace": ("We recommend building QuoteBench in strategic phases "
                 "designed to prevent over-committing. Spend is released "
                 "gate by gate as evidence replaces simulation. Phase 1 is a "
                 "three-month shadow-mode pilot on one inquiry tier costing "
                 "roughly \u20ac30,000 (S), opening with the feasibility "
                 "audit of 25\u201330 historical RFQs on Khoory\u2019s own "
                 "documents, inside a total build budget of \u20ac92,000. "
                 "Every gate carries pre-committed kill criteria set on "
                 "evidence (live extraction accuracy, engineer override "
                 "rates, escaped defects), and a breached gate reverts the "
                 "recommendation to hiring."),
     "unbold": True,
     "bold": ["We recommend building QuoteBench in strategic phases "
              "designed to prevent over-committing."]},

    # Section 13: align the closing recommendation with the new framing.
    {"find": ("We therefore recommend what Section 1 promised: not the "
              "system, the experiment. Approve Phase 1 only, a three-month "
              "\u20ac30,000 shadow-mode pilot with pre-committed kill "
              "criteria,"),
     "replace": ("We therefore recommend what Section 1 promised: building "
                 "QuoteBench in stage-gated phases that commit spend only as "
                 "evidence accumulates. Phase 1 comes first, a three-month "
                 "\u20ac30,000 shadow-mode pilot with pre-committed kill "
                 "criteria,")},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
