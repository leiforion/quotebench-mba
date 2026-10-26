#!/usr/bin/env python3
"""Phase 2, pass 5: Sections 10-13 per the confirmed audit.

Section 10 (653 -> ~620, 3 subs -> 2): 10.3 folds into 10.2.
Section 11 (905 -> ~840, 5 subs -> 3): 11.5 dashboard folds into 11.1;
11.3 liability folds into 11.2; 11.4 -> 11.3.
Section 12 (263 -> ~250, 2 subs -> 0): headings removed.
Section 13 (425 -> ~405): style pass only.
"""
import sys

from doc_editor import run

DASHBOARD = (
    "The pilot and any rollout run on seven indicators, each mapped to the "
    "simulation output it validates or refutes: automation rate (share of "
    "fields drafted without intervention, against the 8.2 variants); "
    "override rate (engineer corrections per quote, the flywheel\u2019s "
    "input and the adoption signal); extraction accuracy (field level, "
    "against the 5.2 range the case is priced on); cycle time median and "
    "P90 by tier (against Exhibit 8.1); win rate by tier (against the "
    "measured 2025 rates and, from Phase 2, the 9.1 uplift); margin per "
    "quote (against the measured discount spread and the plus or minus 1 "
    "percent band); and error escapes (against the parity constraint of "
    "8.2). Targets tighten by phase, and every number the dashboard "
    "produces replaces a simulated input with a measured one.")

EDITS = [
    # ================= SECTION 10 =================
    {"find": "10.1 Dual Business Model Canvas",
     "replace": "10.1 The business-model shift: from expertise to data"},
    {"find": ("Competitors can hire estimators; they cannot buy the "
              "branch\u2019s inquiry history."),
     "replace": ("Competitors can hire estimators. They cannot buy the "
                 "branch\u2019s inquiry history.")},
    {"find": "10.2 Resolving the disintermediation question",
     "replace": ("10.2 Resolving the disintermediation question and the "
                 "options beyond it")},
    {"find": ("the distributor\u2019s technical function is not captured by "
              "anyone; it simply stops being paid for."),
     "replace": ("the distributor\u2019s technical function is not captured "
                 "by anyone. It simply stops being paid for.")},
    {"find": "10.3 New strategic options unlocked\n", "replace": ""},
    {"find": ("sold as a service level rather than granted as a favour; the "
              "simulated Tier 1 cycle time of 2 working hours (8.2) is what "
              "would make the promise printable, and 9.1\u2019s evidence "
              "says the speed is worth paying for."),
     "replace": ("sold as a service level rather than granted as a favour. "
                 "The simulated Tier 1 cycle time of 2 working hours (8.2) "
                 "would make the promise printable, and 9.1\u2019s evidence "
                 "says the speed is worth paying for.")},
    {"find": "product-agnostic by construction (7.2, 12.2)",
     "replace": "product-agnostic by construction (7.2, 12)"},
    {"find": ("Each option would monetize the platform beyond one "
              "branch\u2019s P&L; none is needed for the investment to "
              "clear, which is what makes them options rather than "
              "promises."),
     "replace": ("Each option would monetize the platform beyond one "
                 "branch\u2019s P&L. None is needed for the investment to "
                 "clear.")},

    # ================= SECTION 11 =================
    {"find": "11.1 Stage-gated roadmap",
     "replace": "11.1 Stage gates, kill criteria and the dashboard"},
    {"find": ("The gates are evidential rather than financial, because 9.3 "
              "found no single lever"),
     "replace": "The gates are evidential because 9.3 found no single lever"},
    {"find": ("Phase 3 makes assisted routing the Tier 2 default and "
              "revisits the deferred items (pricing optimization, CAD) on "
              "the strength of accumulated data (7.1)."),
     "replace": ("Phase 3 makes assisted routing the Tier 2 default and "
                 "revisits the deferred items (pricing optimization, CAD) on "
                 "the strength of accumulated data (7.1).\n" + DASHBOARD)},
    {"find": "11.2 Change management, applied",
     "replace": "11.2 Adoption, liability and trust"},
    {"find": "to win rate and margin per quote (11.5), which rewards",
     "replace": "to win rate and margin per quote (11.1), which rewards"},
    {"find": ("The known failure mode is automation bias (5.2); the design "
              "counters it by"),
     "replace": ("The known failure mode is automation bias (5.2). The "
                 "design counters it by")},
    {"find": "11.3 Liability & trust\n", "replace": ""},
    {"find": ("an engineer releases every quotation whatever lane drafted it "
              "(7.7):"),
     "replace": ("an engineer releases every quotation whatever lane drafted "
                 "it (7.2):")},
    {"find": ("is a fact question we could not close; it is a named Phase 1 "
              "legal check."),
     "replace": ("is a fact question we could not close. It is a named Phase "
                 "1 legal check.")},
    {"find": "Contractor-facing trust is designed rather than assumed:",
     "replace": "Contractor-facing trust is designed in:"},
    {"find": "11.4 Risk register", "replace": "11.3 Risk register"},
    {"find": "the engineer-release rule and the 11.3 legal check",
     "replace": "the engineer-release rule and the 11.2 legal check"},
    {"find": "11.5 Governance dashboard\n" + DASHBOARD + "\n",
     "replace": ""},

    # ================= SECTION 12 =================
    {"find": "12.1 Limitations\n", "replace": ""},
    {"find": "12.2 Generalizability\n", "replace": ""},
    {"find": "Two things generalize; the numbers do not.",
     "replace": "Two things generalize. The numbers do not."},

    # ================= SECTION 13 =================
    {"find": ("before projecting anything (8.2); in the simulated central "
              "case, median cycle time falls"),
     "replace": ("before projecting anything (8.2). In the simulated central "
                 "case, median cycle time falls")},
    {"find": ("led by discounting discipline and the win-rate uplift; "
              "simulated five-year NPV spans"),
     "replace": ("led by discounting discipline and the win-rate uplift. "
                 "Simulated five-year NPV spans")},
    {"find": ("Robustness was tested rather than asserted: across eight "
              "stress scenarios and six boundary searches, no single lever "
              "within its tested range sinks the case (9.3)."),
     "replace": ("Across eight stress scenarios and six boundary searches, "
                 "no single lever within its tested range sinks the case "
                 "(9.3).")},
    {"find": ("What remains uncertain is not the arithmetic but the inputs "
              "beneath it, which no simulation can settle."),
     "replace": ("What remains uncertain is the inputs beneath the "
                 "arithmetic, which no simulation can settle.")},
    {"find": ("Every number above the measured baseline is simulated; the "
              "pilot is priced at what it costs"),
     "replace": ("Every number above the measured baseline is simulated. The "
                 "pilot is priced at what it costs")},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
