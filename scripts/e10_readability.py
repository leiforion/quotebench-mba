#!/usr/bin/env python3
"""Readability pass per author answers (6 Sep): strip internal register and
decision IDs from prose (keep M/E/S), fix three stale 11.3 liability refs
(now 11.2), add the three approved glosses (BMC, ADKAR, percentiles), rewrite
the flagged hard-parse passages for interpretability (clarity over brevity),
introduce Khoory plainly in the vignette (F11, minimal), and take the two
approved page-recovery cuts. Body refs to Table 6.1 and Exhibit 9.2 are
repointed to their appendix destinations (moved by e11_moves.py).
"""
import sys

from doc_editor import run

C1 = ("QuoteBench is governed by five constraints. "
      "Automate the mechanical, augment the judgement: ")
C2 = "Nothing ships unreviewed below confidence: "
C3 = "Every automated decision is auditable: "
C4 = "Fail back to the manual process: "
C5 = "Every correction is training data: "

EDITS = [
    # ---- F11: introduce Khoory plainly in the vignette ----
    {"find": ("lands at M.A.H.Y. Khoory's Abu Dhabi branch on a "
              "Thursday evening: roughly 75 pumps"),
     "replace": ("lands on a Thursday evening at the Abu Dhabi branch of "
                 "M.A.H.Y. Khoory, a UAE pump distributor: roughly 75 "
                 "pumps")},

    # ---- F5: percentile gloss at first use (3.2) ----
    {"find": ("Results are reported at P10, P50 and P90. Input "
              "distributions are documented"),
     "replace": ("Results are reported at P10, P50 and P90: one outcome in "
                 "ten falls below the P10 value, half below the P50, and "
                 "nine in ten below the P90. Input distributions are "
                 "documented")},

    # ---- Cut: the "three readings" paragraph under Table 4.2 ----
    {"find": ("Three readings follow. First, cycle time grows faster than "
              "touch time as complexity rises (an 88-hour Tier 3 median "
              "contains only 11.4 hours of work), so the delay problem is "
              "structural. Second, the defect rate triples between Tier 1 "
              "and Tier 3, tracking the volume of manual transcription each "
              "tier demands. Third, read together with the value shares "
              "above: the business earns its margin where its process "
              "performs worst. The Innovo inquiry in 4.3 makes that "
              "concrete.\n"),
     "replace": ""},

    # ---- ID strips, Section 4 ----
    {"find": ("Gross margins restate the measured tier pattern to the "
              "branch\u2019s stated 24 percent average on revenue (D19)."),
     "replace": ("Gross margins restate the measured tier pattern to the "
                 "branch\u2019s stated 24 percent average on revenue.")},
    {"find": ("since a defect on a larger order costs proportionally more "
              "(D19)."),
     "replace": "since a defect on a larger order costs proportionally more."},

    # ---- 6.2: bridge to the moved matrix, drop "ordinally" (F8) ----
    {"find": ("Table 6.1 scores the five options against the six criteria "
              "the investment decision turns on, ordinally, from 1 (worst) "
              "to 5 (best)."),
     "replace": ("Table 6.1 (Appendix K) scores the five options against "
                 "the six criteria the investment decision turns on, from 1 "
                 "(worst) to 5 (best).")},
    {"find": "6.2 The decision matrix and the concession",
     "replace": "6.2 The decision matrix and where hiring wins"},
    {"find": "the concession below states the conditions under which A wins it.",
     "replace": ("the closing paragraph states the conditions under which A "
                 "wins it.")},

    # ---- 7.0 intro: tags promise without per-claim IDs ----
    {"find": ("Everything in this section is a proposal: to-be times and "
              "behaviours are projections, each tagged with the Appendix A "
              "assumption that supplies its value, while figures carried "
              "over from Section 4 remain measured."),
     "replace": ("Everything in this section is a proposal: to-be times and "
                 "behaviours are projections, each traceable to a named "
                 "assumption in the Appendix A register, while figures "
                 "carried over from Section 4 remain measured.")},

    # ---- F6: the five constraints as bold-led lines ----
    {"find": ("QuoteBench is governed by five constraints, written as "
              "obligations. First, automate extraction and calculation, and "
              "augment judgement: the system takes over the reading, "
              "transcription and arithmetic where Section 4.2 located 41% "
              "of defects, and presents judgement calls to a person. "
              "Second, no quote leaves below defined confidence without "
              "human review. In Phase 1 the gate is absolute. Third, every "
              "automated decision is auditable: each extracted field, "
              "calculation input, ranked option and price logged with "
              "source, confidence and timestamp, feeding the liability "
              "analysis of 11.3. Fourth, graceful degradation: on any "
              "failure, the inquiry drops into the Section 4 manual process "
              "with partial work attached. Fifth, every human correction is "
              "captured as labelled training data, the constraint that "
              "turns review burden into the flywheel of 7.2."),
     "replace": (C1 + "the system takes over the reading, transcription and "
                 "arithmetic where Section 4.2 located 41% of defects, and "
                 "presents the judgement calls to a person.\n"
                 + C2 + "no quote leaves below defined confidence without "
                 "human review, and in Phase 1 the gate is absolute.\n"
                 + C3 + "each extracted field, calculation input, ranked "
                 "option and price is logged with source, confidence and "
                 "timestamp, feeding the liability analysis of 11.2.\n"
                 + C4 + "on any failure, the inquiry drops into the Section "
                 "4 manual process with partial work attached.\n"
                 + C5 + "every human correction is captured as labelled "
                 "data, the constraint that turns review burden into the "
                 "flywheel of 7.2."),
     "unbold": True,
     "bold": ["Automate the mechanical, augment the judgement:",
              "Nothing ships unreviewed below confidence:",
              "Every automated decision is auditable:",
              "Fail back to the manual process:",
              "Every correction is training data:"]},

    # ---- 7.1/7.2/7.3: [A*] strips and clarity ----
    {"find": "a projected 2.5-hour median [A6])",
     "replace": "a projected 2.5-hour median)"},
    {"find": ("Within minutes of arrival the intake layer classifies the "
              "inquiry into the 4.1 taxonomy [A1] and validates "
              "completeness against the extraction schema, producing a "
              "definitive list of gaps while the inquiry is minutes old."),
     "replace": ("Within minutes of arrival the intake layer classifies the "
                 "inquiry into the 4.1 taxonomy and validates completeness "
                 "against the extraction schema, so every gap is known "
                 "while the inquiry is minutes old.")},
    {"find": "one consolidated clarification covering every gap at once [A3], where",
     "replace": "one consolidated clarification covering every gap at once, where"},
    {"find": "flagging duty points near a curve edge [A5].",
     "replace": "flagging duty points near a curve edge."},
    {"find": "classified, valued, in band [A1].",
     "replace": "classified, valued, in band."},
    {"find": "with the riser ambiguity flagged as an explicit conflict [A2].",
     "replace": "with the riser ambiguity flagged as an explicit conflict."},
    {"find": "thirteen minutes after receipt instead of 22 working hours [A3].",
     "replace": "thirteen minutes after receipt instead of 22 working hours."},
    {"find": ("The senior's confirmation is two lines, one alternate is "
              "added, the discount stays in band [A6, A7]."),
     "replace": ("The senior's confirmation is two lines, one alternate is "
                 "added, the discount stays in band.")},
    {"find": "the quote would go out with the estimator's name on it per 11.3,",
     "replace": "the quote would go out with the estimator's name on it (11.2),"},
    {"find": "Whose signature a quote carries is taken up in 11.3.",
     "replace": "Whose signature a quote carries is taken up in 11.2."},

    # ---- F7 split + page-recovery cut in 7.3 (numbers stay in 9.3) ----
    {"find": ("Within minutes of the reply the system has merged the "
              "thread, re-validated, run the head-loss calculations, "
              "filtered the product store, queried the selection API, and "
              "holds a draft quote: models ranked, the booster duty point "
              "flagged near its curve edge, prices in band."),
     "replace": ("Within minutes of the reply the system has merged the "
                 "thread, re-validated, and run the calculations and "
                 "selection queries. It now holds a draft quote: models "
                 "ranked, the booster duty point flagged near its curve "
                 "edge, prices in band.")},
    {"find": (" Seven calendar days would become four, and twenty-eight "
              "touch hours roughly fifteen (S: eleven to twenty across the "
              "8.1 capability range): the review of a 75-pump draft rather "
              "than its manual construction."),
     "replace": (" Twenty-eight hours of manual construction would become "
                 "the review of a 75-pump draft (S), and Section 9.3 prices "
                 "the difference.")},

    # ---- 9.1: hard-parse revenue sentence (F13) + ID strips ----
    {"find": ("The revenue those hours carry is a stated management figure: "
              "the branch's 2025 pump-only revenue was approximately AED "
              "150 million, \u20ac34.5 million at the paper's conversion "
              "(M, D19), and the simulator's value model reproduces it with "
              "about \u20ac136 million quoted implied by the measured win "
              "rates (S), including two flagship-scale projects a year "
              "(D17)."),
     "replace": ("The revenue those hours carry is a stated management "
                 "figure: the branch's 2025 pump-only revenue was "
                 "approximately AED 150 million, \u20ac34.5 million at the "
                 "paper's conversion (M). Working backwards through the "
                 "measured win rates, winning that much implies roughly "
                 "\u20ac136 million of value quoted each year (S), "
                 "including two flagship-scale projects.")},
    {"find": ("full adoption, central case (S, run manifest in the public "
              "repository)."),
     "replace": "full adoption, central case (S)."},
    {"find": "Build: \u20ac92,000, priced as one internal software-engineer year (D10).",
     "replace": "Build: \u20ac92,000, priced as one internal software-engineer year."},
    {"find": ("median payback is about four months (S, Exhibit 9.2). At "
              "this scale"),
     "replace": ("median payback is about four months (S; Exhibit 9.2, "
                 "Appendix F). At this scale")},

    # ---- F3: BMC gloss (10.1) ----
    {"find": ("Set side by side, the as-is and to-be business model "
              "canvases differ in only three blocks, and they are the ones "
              "that matter."),
     "replace": ("Set side by side, the as-is and to-be business model "
                 "canvases (the one-page map of how the branch creates, "
                 "delivers and captures value) differ in only three of "
                 "their nine blocks, and they are the ones that matter.")},

    # ---- F4: ADKAR gloss; F9: modal (11.x) ----
    {"find": "we apply ADKAR at the level it operates: the individual estimator.",
     "replace": ("we apply ADKAR, the change model that moves one person "
                 "through awareness, desire, knowledge, ability and "
                 "reinforcement, at the level it operates: the individual "
                 "estimator.")},
    {"find": "on Tier 2, the modal inquiry and the richest document mix:",
     "replace": "on Tier 2, the most common inquiry and the richest document mix:"},

    # ---- F10, F14: Section 12 ----
    {"find": ("This is an ex-ante study: no part of QuoteBench exists and "
              "no implementation evidence is offered."),
     "replace": ("The study evaluates the investment before anything is "
                 "built: no part of QuoteBench exists and no implementation "
                 "evidence is offered.")},
    {"find": ("stated preferences may differ from revealed behaviour when a "
              "system-assembled quote actually arrives."),
     "replace": ("what contractors say they value may differ from what they "
                 "do when a system-assembled quote actually arrives.")},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
