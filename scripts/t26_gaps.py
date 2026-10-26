#!/usr/bin/env python3
"""G6 re-run numbers + remaining mechanical gap fixes.

G6: run cost restated (authors: maintenance ~EUR 40k/yr, build EUR 92k is
build-only) -> run 45-65k/yr; NPV P10/P50/P90 now 1.37/2.70/4.28M, floor
+226k @12% / +197k @hurdle, elasticity-zero +326k @hurdle. Also: G3 (cut
submittal from 2.4), G4 (manufacturer special-quote sentence in 8.2), G5
(surge result added to 9.6), G7 (640 vs 636 reconciled), G9 (defect-parity
phrasing), G10 (direct cost wording), G12 (renumber Exhibit 8.2 -> 8.1),
G14 (declined-volume claim softened).
"""
import sys

from doc_editor import run

EDITS = [
    # ---- G6: exec summary numbers
    {"find": ("five-year NPV runs from \u20ac1.5 million (P10) through "
              "\u20ac2.8 million (P50) to \u20ac4.4 million (P90), clearing "
              "the 15 percent hurdle in every draw, with median payback of "
              "about four months. The floor case also clears: with the "
              "win-rate uplift at zero, extraction at its pessimistic bound "
              "and the build 30 percent over, NPV is still about \u20ac0.3 "
              "million on discount discipline and error reduction alone."),
     "replace": ("five-year NPV runs from \u20ac1.4 million (P10) through "
                 "\u20ac2.7 million (P50) to \u20ac4.3 million (P90), "
                 "clearing the 15 percent hurdle in every draw, with median "
                 "payback of about four months. The floor case also clears: "
                 "with the win-rate uplift at zero, extraction at its "
                 "pessimistic bound and the build 30 percent over, NPV is "
                 "still about \u20ac0.2 million on discount discipline and "
                 "error reduction alone."),
     "unbold": True},
    # ---- G3: cut submittal from scope
    {"find": ("The technical workflow from RFQ receipt through quote "
              "generation, plus the submittal stage once a project is won. "
              "The commercial negotiation"),
     "replace": ("The technical workflow from RFQ receipt through quote "
                 "generation. The commercial negotiation"),
     "unbold": True},
    # ---- G10: 4.1 direct cost wording
    {"find": ("the median inquiry carries about \u20ac66 of direct labour, "
              "developed by tier in 4.3."),
     "replace": ("the median inquiry carries about \u20ac66 of direct cost "
                 "(labour plus a licence allocation), developed by tier in "
                 "4.3."),
     "unbold": True},
    # ---- G4: manufacturer special-quote round trip carried unchanged
    {"find": ("median engineer touch drops from 2.1 to 0.8 hours, 5.5 to 2.7 "
              "and 11.4 to 6.2 by tier (S)."),
     "replace": ("median engineer touch drops from 2.1 to 0.8 hours, 5.5 to "
                 "2.7 and 11.4 to 6.2 by tier (S). As with the contractor "
                 "reply, the manufacturer special-quote round trip on "
                 "complex work is outside the design's control and is "
                 "carried at its measured pace inside the fitted external "
                 "waits."),
     "unbold": True},
    # ---- G9: defect-parity phrasing (reads as section numbers)
    {"find": ("Escaped defects hold at parity with the baseline (9.1 versus "
              "9.2 percent of inquiries), which is a design constraint"),
     "replace": ("Escaped defects hold at parity with the baseline (a "
                 "simulated 9.2 percent of inquiries against the measured "
                 "9.1 percent), which is a design constraint"),
     "unbold": True},
    # ---- G12: renumber the cycle-time exhibit 8.2 -> 8.1
    {"find": "with P90s falling in step (Exhibit 8.2); median engineer touch",
     "replace": "with P90s falling in step (Exhibit 8.1); median engineer touch",
     "unbold": True},
    {"find": ("Exhibit 8.2. Simulated cycle-time distributions by tier, as-is "
              "versus to-be central case; dashed lines mark medians (S)."),
     "replace": ("Exhibit 8.1. Simulated cycle-time distributions by tier, "
                 "as-is versus to-be central case; dashed lines mark medians "
                 "(S).")},
    # ---- G7: 640 vs 636 reconciled
    {"find": ("Direct quoting cost is about \u20ac33,000 a year: 636 "
              "inquiries at \u20ac25, \u20ac66 and \u20ac137 per quote by "
              "tier (E),"),
     "replace": ("Direct quoting cost is about \u20ac33,000 a year: 636 "
                 "inquiries a year (the Table 4.2 monthly volumes "
                 "annualized; the log holds 640) at \u20ac25, \u20ac66 and "
                 "\u20ac137 per quote by tier (E),"),
     "unbold": True},
    # ---- G14: soften the declined-volume claim
    {"find": ("A fifth benefit, volume the branch currently declines or "
              "ignores, is real but unmodelled; it is left out of every "
              "number in this paper, which is the conservative direction."),
     "replace": ("A fifth benefit is possible but unevidenced: if capacity "
                 "constraints suppress intake today, the recovered volume is "
                 "upside the pilot can log; it is left out of every number "
                 "in this paper, which is the conservative direction."),
     "unbold": True},
    # ---- G6: 9.4 run-cost sentence
    {"find": ("Run: \u20ac15,000\u201327,000 a year for inference and API "
              "usage at projected volume, licences, and 0.2\u20130.5 FTE of "
              "maintenance; this range is provisional, and vendor quotations "
              "replace it before any build decision."),
     "replace": ("Run: \u20ac45,000\u201365,000 a year: platform maintenance "
                 "and upkeep at about \u20ac40,000 (E, management estimate; "
                 "the \u20ac92,000 engineer-year is the build alone), plus "
                 "inference and API usage at projected volume and licences; "
                 "the usage component is provisional, and vendor quotations "
                 "replace it before any build decision."),
     "unbold": True},
    # ---- G6: 9.5 appraisal numbers
    {"find": ("Five-year NPV comes out at \u20ac1.5 million at P10, \u20ac2.8 "
              "million at P50 and \u20ac4.4 million at P90; every one of the "
              "20,000 draws clears the hurdle,"),
     "replace": ("Five-year NPV comes out at \u20ac1.4 million at P10, "
                 "\u20ac2.7 million at P50 and \u20ac4.3 million at P90; "
                 "every one of the 20,000 draws clears the hurdle,"),
     "unbold": True},
    {"find": ("and benefits still run about \u20ac180,000 a year: NPV is "
              "\u20ac342,000 at 12 percent and \u20ac304,000 at the hurdle."),
     "replace": ("and benefits still run about \u20ac180,000 a year: NPV is "
                 "\u20ac226,000 at 12 percent and \u20ac197,000 at the "
                 "hurdle."),
     "unbold": True},
    # ---- G6 + G5: 9.6 boundaries updated, surge result reported
    {"find": ("The uplift at zero still clears (\u20ac0.43 million at the "
              "hurdle), the build at six times plan still clears, run costs "
              "at \u20ac200,000 a year still clear, and demand at one-fifth "
              "of the 2025 rate still clears (S)."),
     "replace": ("The uplift at zero still clears (\u20ac0.33 million at the "
                 "hurdle), the build at six times plan still clears, run "
                 "costs at \u20ac200,000 a year still clear, and demand at "
                 "one-fifth of the 2025 rate still clears; in the other "
                 "direction, the 40 percent demand surge that breaks the "
                 "as-is desk raises annual benefits to about \u20ac1.2 "
                 "million (S)."),
     "unbold": True},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
