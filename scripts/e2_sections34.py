#!/usr/bin/env python3
"""Phase 2, pass 2: Sections 3-4 per the confirmed audit.

Section 3 (758 -> ~560, 4 subs -> 2): 3.2 folds into 3.1 ("Research design
and evidence base"); 3.4 folds into 3.3 ("Simulation method and its limits").
Section 4 (1,866 -> ~1,470, 7 subs -> opener + 4): 4.1 becomes section-opening
prose; 4.2+4.3 -> "4.1 Segmentation and baseline performance"; 4.4 -> 4.2;
4.5 -> 4.3 (kept per authors); 4.6 folds into 4.7 -> "4.4 Root causes and the
customer's view". Cross-references renumbered across the paper.
Exhibits 4.2/4.3 image moves are handled by e2b_images.py.
"""
import sys

from doc_editor import run

EDITS = [
    # ---------------- Section 3 ----------------
    {"find": "3.1 Research design",
     "replace": "3.1 Research design and evidence base"},
    {"find": ("Nothing in this paper has been built yet; the study is what "
              "investment appraisal calls an ex-ante evaluation. We evaluate "
              "the proposed transformation the way a board evaluates any "
              "capital request: measure"),
     "replace": ("Nothing in this paper has been built yet. The study is an "
                 "ex-ante evaluation: we assess the proposed transformation "
                 "the way a board assesses any capital request. Measure")},
    {"find": ("Four components carry the evaluation: a measured baseline of "
              "the current quoting process (Section 4); a design assembled "
              "from components whose behaviour is already documented, so the "
              "novelty lies in the assembly and not in any unproven part "
              "(Section 7); a simulation of the future state, a process model "
              "for cycle time and capacity plus a financial model that turns "
              "its outputs into an investment case stated as ranges (Sections "
              "8 and 9); and validation by the people involved: we use the "
              "estimators and the contractors to challenge the design's "
              "assumptions, not to endorse them (8.3, 4.6)."),
     "replace": ("Four components carry the evaluation: a measured baseline "
                 "of the current quoting process (Section 4); a design "
                 "assembled from components whose behaviour is already "
                 "documented (Section 7); a simulation of the future state, "
                 "covering cycle time, capacity and the investment case as "
                 "ranges (Sections 8 and 9); and validation by the estimators "
                 "and contractors, who challenge the design's assumptions "
                 "(8.3, 4.4)."),
     "bold": ["measured baseline", "design", "simulation of the future state",
              "validation"],
     "unbold": True},
    {"find": ("One scoping point matters for every number downstream. Khoory "
              "operates 16 estimators across its UAE branches, each handling "
              "around twelve inquiries a week across all product lines. We "
              "measured a single branch, the Abu Dhabi estimation office, "
              "whose 640 pump RFQs in 2025 are the study population; every "
              "figure in the paper, including the Section 9 investment case, "
              "is single-branch, and no company-wide scaling is used. We "
              "chose to measure one branch deeply rather than all branches "
              "thinly, because the Section 8 simulation needs step-level "
              "timings that only direct observation can supply."),
     "replace": ("One scoping point matters for every number downstream. We "
                 "measured a single branch, the Abu Dhabi estimation office, "
                 "whose 640 pump RFQs in 2025 are the study population. Every "
                 "figure in the paper, including the Section 9 investment "
                 "case, is single-branch, and no company-wide scaling is "
                 "used. We measured one branch deeply because the Section 8 "
                 "simulation needs step-level timings that only direct "
                 "observation can supply."),
     "unbold": True},
    {"find": "3.2 Data sources\n", "replace": ""},
    {"find": "3.3 Simulation methodology",
     "replace": "3.2 Simulation method and its limits"},
    {"find": ("The process model replays the branch operation of Exhibit "
              "4.1: arrivals by tier at 2025 rates, touch times from the "
              "observed step distributions, estimator capacity as the "
              "constraint, and queue discipline as observed, with large "
              "inquiries modelled as pre-emption because the Innovo case "
              "shows that is what happens. It is a discrete-event simulation "
              "built for this study; the full code, parameters, seeds and "
              "run manifests are public at [repository URL] (Appendix F), so "
              "every simulated number in this paper can be reproduced to the "
              "digit. The model must reproduce the measured baseline (median "
              "and P90 cycle time by tier, within ten percent) before any "
              "to-be scenario is run; the calibration evidence appears in "
              "8.2. To-be scenarios then run across the capability range "
              "built in 8.1 from published benchmarks, and report cycle "
              "time, utilization and capacity as distributions."),
     "replace": ("The process model replays the branch operation of Exhibit "
                 "4.1: arrivals by tier at 2025 rates, touch times from the "
                 "observed step distributions, estimator capacity as the "
                 "constraint, and large inquiries as pre-emption, which is "
                 "what the Innovo case shows happens. It is a discrete-event "
                 "simulation built for this study. The full code, "
                 "parameters, seeds and run manifests are public at "
                 "[repository URL] (Appendix F), so every simulated number "
                 "in this paper can be reproduced to the digit. The model "
                 "must reproduce the measured baseline before any to-be "
                 "scenario is run (8.2). To-be scenarios then run across the "
                 "capability ranges of 8.1 and report cycle time, "
                 "utilization and capacity as distributions."),
     "bold": ["The process model"], "unbold": True},
    {"find": ("The financial model converts those projections into five-year "
              "NPV by Monte Carlo, because what we have are ranges, not "
              "points. Three inputs dominate and are drawn as distributions:"),
     "replace": ("The financial model converts those projections into "
                 "five-year NPV by Monte Carlo, because the inputs arrive as "
                 "ranges. Three dominate and are drawn as distributions:"),
     "bold": ["The financial model"], "unbold": True},
    {"find": ("with the probability of clearing the hurdle rate; every input "
              "distribution is documented in Appendix C"),
     "replace": ("with the probability of clearing the hurdle rate. Every "
                 "input distribution is documented in Appendix C")},
    {"find": (" The simulator's modelling approach, calibration and "
              "validation logic go to Appendix F."),
     "replace": ""},
    {"find": "3.4 Limitations of method\n", "replace": ""},

    # ---------------- Section 4: opener (old 4.1) ----------------
    {"find": ("tagged (E). Everything the later sections project is anchored "
              "to what this section can demonstrate."),
     "replace": "tagged (E)."},
    {"find": "4.1 The as-is process: a swimlane view\n", "replace": ""},
    {"find": "The work is not slow; the waiting is.",
     "replace": "The work is not slow. The waiting is."},
    {"find": "developed by tier in 4.3.",
     "replace": "developed by tier in Table 4.2."},

    # ---------------- 4.2+4.3 -> 4.1 ----------------
    {"find": "4.2 RFQ segmentation",
     "replace": "4.1 Segmentation and baseline performance"},
    {"find": ("The tiers are defined by pump count, data completeness at "
              "receipt and value band; the full criteria and 2025 mix are "
              "Table 4.1 (Appendix K)."),
     "replace": "The full criteria and 2025 mix are Table 4.1 (Appendix K)."},
    {"find": ("the documents messiest, and the expertise thinnest: two "
              "estimators can handle a chilled-water package unassisted, and "
              "one of them handles most. A redesign"),
     "replace": "the documents messiest, and the expertise thinnest. A redesign"},
    {"find": "4.3 Baseline metrics\n", "replace": ""},
    {"find": ("contains only 11.4 hours of work), so the delay problem is "
              "structural, not a matter of effort."),
     "replace": ("contains only 11.4 hours of work), so the delay problem is "
                 "structural.")},
    {"find": ("Third, and read together with the value shares of 4.2: the "
              "business earns its margin where its process performs worst. "
              "That tension is what the Innovo inquiry in 4.5 makes "
              "concrete."),
     "replace": ("Third, read together with the value shares above: the "
                 "business earns its margin where its process performs "
                 "worst. The Innovo inquiry in 4.3 makes that concrete.")},

    # ---------------- 4.4 -> 4.2 ----------------
    {"find": "4.4 Error taxonomy and the cost of poor quality",
     "replace": "4.2 Error taxonomy and the cost of poor quality"},
    {"find": ("surfaced four distinct classes of error; the full taxonomy "
              "with frequencies and unit costs is Table 4.3 (Appendix K)."),
     "replace": ("surfaced four distinct classes of error. The full taxonomy "
                 "with frequencies and unit costs is Table 4.3 (Appendix "
                 "K).")},
    {"find": ("The classes differ not only in frequency but in when they are "
              "discovered, and discovery timing drives cost far more than "
              "the mistake itself:"),
     "replace": ("Discovery timing drives cost far more than the mistake "
                 "itself:")},

    # ---------------- 4.5 -> 4.3 ----------------
    {"find": "4.5 The Innovo inquiry: Guggenheim Abu Dhabi, as-is",
     "replace": "4.3 The Innovo inquiry: Guggenheim Abu Dhabi, as-is"},
    {"find": ("The numbers above describe the process in aggregate; the "
              "Innovo inquiry that opened this paper shows"),
     "replace": ("The numbers above describe the process in aggregate. The "
                 "Innovo inquiry that opened this paper shows")},
    {"find": ("Seven calendar days from receipt to quotation; twenty-eight "
              "hours of work across three estimators and a weekend of "
              "overtime, well above the Tier 3 median of Table 4.2. What "
              "made it memorable was not that it was unusual, but that the "
              "process could not absorb a job this size inside the deadline, "
              "however many people were thrown at it."),
     "replace": ("Seven calendar days from receipt to quotation, and "
                 "twenty-eight hours of work across three estimators and a "
                 "weekend of overtime, well above the Tier 3 median of Table "
                 "4.2. The process could not absorb a job this size inside "
                 "the deadline, however many people were thrown at it.")},
    {"find": ("would have undersized the booster set for the taller "
              "building; it was caught only because"),
     "replace": ("would have undersized the booster set for the taller "
                 "building. It was caught only because")},

    # ---------------- 4.6 body deleted (folded into 4.4) ----------------
    {"find": "4.6 Voice of the customer\n", "replace": ""},
    {"find": ("Contractor interviews are in progress at the time of writing "
              "(protocol in Appendix D): four to six structured "
              "conversations covering what drives supplier choice, how speed "
              "weighs against price, and, because no live system exists to "
              "observe, each contractor's stated reaction to the "
              "hypothetical of an automated quote. Preliminary conversations "
              "consistently point to response speed and error-free technical "
              "submittals as decisive selection factors, which supports the "
              "direction of this design; verbatim quotations, including any "
              "dissenting views, will be incorporated once transcripts are "
              "complete (E, provisional). Stated preferences are the paper's "
              "only demand-side evidence, and Section 9.3 treats them "
              "accordingly: as an upper bound to be triangulated, not a "
              "measurement.\n"),
     "replace": ""},

    # ---------------- 4.7 -> 4.4 ----------------
    {"find": "4.7 Root causes",
     "replace": "4.4 Root causes and the customer's view"},
    {"find": ("Compressing the evidence of this section (the swimlane "
              "timings, the tier metrics, the error audit, and the Innovo "
              "inquiry) yields four root causes, shown as a driver tree in "
              "Exhibit 4.3. They are worth stating separately because each "
              "demands a different remedy,"),
     "replace": ("Compressing the evidence of this section yields four root "
                 "causes, shown as a driver tree in Exhibit 4.3 (Appendix "
                 "B). Each demands a different remedy,")},
    {"find": ("The 86\u201388% queue share in Exhibit 4.2 is the signature "
              "of serial ownership, not of slow work."),
     "replace": ("The 86\u201388% queue share in Exhibit 4.2 (Appendix B) is "
                 "the signature of serial ownership.")},
    {"find": ("each triggering a round trip to the contractor at a median "
              "cost of 41 working hours; nothing alerts anyone when the "
              "answer lands."),
     "replace": ("each triggering a round trip to the contractor at a median "
                 "cost of 41 working hours. Nothing alerts anyone when the "
                 "answer lands.")},
    {"find": ("and the rules-based pricing engine because of the fourth. The "
              "measured current state is the design brief."),
     "replace": ("and the rules-based pricing engine because of the fourth. "
                 "The measured current state is the design brief.\n"
                 "The customer's view supports the diagnosis. Contractor "
                 "interviews are in progress (protocol in Appendix D): four "
                 "to six structured conversations covering what drives "
                 "supplier choice, how speed weighs against price, and each "
                 "contractor's stated reaction to an automated quote. "
                 "Preliminary conversations point to response speed and "
                 "error-free technical submittals as decisive selection "
                 "factors (E, provisional). Verbatim quotations will be "
                 "incorporated once transcripts are complete. Stated "
                 "preferences are the paper's only demand-side evidence, and "
                 "9.3 treats them as an upper bound to be triangulated.")},

    # ---------------- cross-reference renumbering elsewhere ----------------
    {"find": "Section 4.4 develops the error taxonomy and its cost.",
     "replace": "Section 4.2 develops the error taxonomy and its cost."},
    {"find": "Its limits are the arithmetic of 2.2:",
     "replace": "Its limits are the arithmetic of 2.1:"},
    {"find": "it walks out the door with every resignation (2.2)",
     "replace": "it walks out the door with every resignation (2.1)"},
    {"find": "The simulator described in 3.3 replays",
     "replace": "The simulator described in 3.2 replays"},
    {"find": "classifies the inquiry into the 4.2 taxonomy [A1]",
     "replace": "classifies the inquiry into the 4.1 taxonomy [A1]"},
    {"find": "the inquiry of Section 4.5 processed under the proposed design",
     "replace": "the inquiry of Section 4.3 processed under the proposed design"},
    {"find": "As measured in 4.5: 28 touch hours",
     "replace": "As measured in 4.3: 28 touch hours"},
    {"find": "attacks all four root causes of 4.7 at once",
     "replace": "attacks all four root causes of 4.4 at once"},
    {"find": "the roughly \u20ac850,000 of 4.4 is shared",
     "replace": "the roughly \u20ac850,000 of 4.2 is shared"},

    # scope lead-in (Section 2, follows the RQ bullets)
    {"insert_before": "Product. Pumps only, where the technical selection",
     "text": "The scope is deliberately narrow.\n"},

    # Appendix B now hosts the Section 4 exhibits too
    {"find": "Appendix B (extract): Section 7 Exhibits",
     "replace": "Appendix B (extract): Section 4 and Section 7 Exhibits"},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
