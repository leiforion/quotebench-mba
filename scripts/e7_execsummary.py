#!/usr/bin/env python3
"""Rewrite the executive summary to carry the simulation learnings the body
now states: the 990k central benefit and its proven/unproven split (8.2, 9.1),
the no-single-lever stress finding (9.3), the floor case at the hurdle (9.2),
evidential kill criteria (9.3, 11.1) and the reversion to hiring (11.1).
Paragraphs 1 (measured baseline) and 4 (data moat) are unchanged.
"""
import sys

from doc_editor import run

EDITS = [
    # P2: label the projection as simulated, matching Section 13's wording.
    {"find": ("In the central case, median cycle time falls to 2, 9 and 56 "
              "working hours by tier, and engineer touch time roughly "
              "halves."),
     "replace": ("In the simulated central case, median cycle time falls to "
                 "2, 9 and 56 working hours by tier, and engineer touch time "
                 "roughly halves.")},

    # P3 -> new P3 + P4: benefit decomposition, then robustness + evidential
    # kill criteria. All figures trace to 8.2, 9.1, 9.2 and 9.3.
    {"find": ("Across 20,000 Monte Carlo draws at a 12 percent discount "
              "rate, five-year NPV runs from \u20ac1.4 million (P10) through "
              "\u20ac2.7 million (P50) to \u20ac4.3 million (P90), clearing "
              "the 15 percent hurdle in every draw, with median payback of "
              "about four months. The floor case also clears. With the "
              "win-rate uplift at zero, extraction at its pessimistic bound "
              "and the build 30 percent over, NPV is still about \u20ac0.2 "
              "million on discount discipline and error reduction alone. The "
              "remaining risk sits in the evidence under the arithmetic: "
              "every capability input is simulated, and the pilot exists to "
              "test those inputs before the build is approved."),
     "replace": ("Simulated benefits reach about \u20ac990,000 a year at "
                 "full adoption. About \u20ac210,000 of that does not depend "
                 "on winning a single additional order. The rest is the "
                 "win-rate uplift from faster quoting, the model\u2019s "
                 "least proven input. Across 20,000 Monte Carlo draws at a "
                 "12 percent discount rate, five-year NPV runs from \u20ac1.4 "
                 "million (P10) through \u20ac2.7 million (P50) to \u20ac4.3 "
                 "million (P90), clearing the 15 percent hurdle in every "
                 "draw, with median payback of about four months.\n"
                 "Stress testing found no single lever that sinks the case "
                 "within its tested range. Even the floor case (win-rate "
                 "uplift at zero, extraction at its pessimistic bound, the "
                 "build 30 percent over) still returns about \u20ac0.2 "
                 "million of NPV at the hurdle, on labour, error cost and "
                 "discount discipline alone. Every capability figure is "
                 "simulated, so the pilot\u2019s kill criteria are set on "
                 "evidence: live extraction accuracy, engineer override "
                 "rates and escaped defects.")},

    # P6: name what happens when a gate is breached (11.1).
    {"find": ("inside a total build budget of \u20ac92,000 and with "
              "pre-committed kill criteria at every gate."),
     "replace": ("inside a total build budget of \u20ac92,000 and with "
                 "pre-committed kill criteria at every gate. Breach any gate "
                 "and the recommendation reverts to hiring.")},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
