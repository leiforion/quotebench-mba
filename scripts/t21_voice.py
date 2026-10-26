#!/usr/bin/env python3
"""T15 voice pass: remove announced-rigor phrases (honest/exactly/plainly used
as emphasis), thin the stacked "X, not Y" pattern in Sections 8-9, and drop
one "deliberately". No number, tag or claim changes. Sections 1 and 10-13 are
still outline bullets (T17/T12) and are out of scope.
"""
import sys

from doc_editor import run

EDITS = [
    # announced rigor / emphasis tics
    {"find": "The honest baseline competitor is not technology at all",
     "replace": "The baseline competitor is not technology at all"},
    {"find": "it is the cheapest and the least likely to fail, and an honest matrix says so",
     "replace": "it is the cheapest and the least likely to fail, and the matrix says so"},
    {"find": "The current state, measured honestly, is the design brief.",
     "replace": "The measured current state is the design brief."},
    {"find": "because what we honestly have are ranges, not points",
     "replace": "because what we have are ranges, not points"},
    {"find": "Stated plainly, this investment is a bet that faster, cleaner quotes",
     "replace": "This investment is a bet that faster, cleaner quotes"},
    {"find": "The evidence that de-risks the bet is exactly what Phase 1 of the pilot measures first",
     "replace": "The evidence that de-risks the bet is what Phase 1 of the pilot measures first"},
    {"find": "Section 9 weakens, and the pilot's first gate exists to catch exactly that.",
     "replace": "Section 9 weakens, and the pilot's first gate is built to catch it."},
    # pattern stack thinning ("X, not Y" x3 within Section 9)
    {"find": "The revenue base behind those percentages is derived, not read from accounts (D13)",
     "replace": "The revenue base behind those percentages is derived rather than read from accounts (D13)"},
    {"find": "The assumption is redeployment, not redundancy;",
     "replace": "The assumption is redeployment rather than redundancy;"},
    # adverb tic
    {"find": "Routing stays deliberately cautious: 15 percent",
     "replace": "Routing stays cautious: 15 percent"},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
