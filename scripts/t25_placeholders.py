#!/usr/bin/env python3
"""A2/A4: resolve author placeholders. Internal interview count = 6 (authors,
6 Sep); branch named plainly as the Abu Dhabi estimation office (brackets
dropped; consistent with the vignette). Contractor bracket [4-6] stays by
author decision (A3: genuinely in progress)."""
import sys

from doc_editor import run

EDITS = [
    {"find": "Khoory\u2019s [Abu Dhabi] estimation office turned 640 pump RFQs",
     "replace": "Khoory\u2019s Abu Dhabi estimation office turned 640 pump RFQs",
     "unbold": True},
    {"find": "We measured a single branch, [the Abu Dhabi estimation office], whose 640 pump RFQs",
     "replace": "We measured a single branch, the Abu Dhabi estimation office, whose 640 pump RFQs",
     "unbold": True},
    {"row_anchor": "Internal interviews",
     "old_cell": "[n] structured interviews: estimators, sales, branch and line management",
     "new_cell": "6 structured interviews: estimators, sales, branch and line management"},
    # Table 3.1 caption: bracketed-counts caveat now only applies to contractors
    {"find": "The feasibility audit is a planned pilot instrument, not yet evidence. Bracketed counts to be finalized.",
     "replace": "The feasibility audit is a planned pilot instrument, not yet evidence. The contractor interview count is bracketed pending completion."},
]

# D20 (run separately): pilot budget in the executive summary
EDITS_A5 = [
    {"find": ("We recommend approving Phase 1 only: a three-month shadow-mode "
              "pilot on one inquiry tier, opening with the feasibility audit"),
     "replace": ("We recommend approving Phase 1 only: a three-month "
                 "shadow-mode pilot on one inquiry tier costing roughly "
                 "\u20ac30,000 (S), opening with the feasibility audit"),
     "unbold": True},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
