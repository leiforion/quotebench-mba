#!/usr/bin/env python3
"""Phase 2, pass 1: edit Sections 1-2 per the confirmed audit.

Section 1 (362 -> ~350): style pass only. Semicolon out, contrast
constructions thinned to one, appositive fixed.

Section 2 (1,046 -> ~770, 5 subs -> 2):
  - 2.0 heading deleted; vignette becomes the section opener, trimmed.
  - 2.1+2.2 merged under "2.1 The technical-expertise function: slow,
    capacity-bound, error-prone".
  - 2.3+2.4 merged under "2.2 Research questions and scope"; section
    pointers move into the RQ bullets; bridging paragraph deleted.
"""
import sys

from doc_editor import run

EDITS = [
    # ---------------- Section 1 ----------------
    {"find": ("by complexity tier, of which only 2.1 to 11.4 hours is "
              "engineering work; the rest is queueing."),
     "replace": ("by complexity tier. Only 2.1 to 11.4 of those hours are "
                 "engineering work. The rest is queueing.")},
    {"find": "No prototype exists: capability inputs are taken",
     "replace": "No prototype exists. Capability inputs are taken"},
    {"find": ("The floor case also clears: with the win-rate uplift at zero, "
              "extraction at its pessimistic bound and the build 30 percent "
              "over, NPV is still"),
     "replace": ("The floor case also clears. With the win-rate uplift at "
                 "zero, extraction at its pessimistic bound and the build 30 "
                 "percent over, NPV is still")},
    {"find": ("The remaining risk is not the arithmetic but the evidence "
              "under it: every capability input is simulated"),
     "replace": ("The remaining risk sits in the evidence under the "
                 "arithmetic: every capability input is simulated")},
    {"find": ("Strategically, automated quoting converts the branch\u2019s "
              "inquiry flow into structured transaction data that neither "
              "manufacturers nor marketplaces hold, the distributor\u2019s "
              "defensible position as the channel digitizes."),
     "replace": ("Automated quoting also converts the branch\u2019s inquiry "
                 "flow into structured transaction data that neither "
                 "manufacturers nor marketplaces hold. That data is the "
                 "distributor\u2019s defensible position as the channel "
                 "digitizes.")},

    # ---------------- Section 2: vignette ----------------
    {"find": "2.0 Opening vignette\n", "replace": ""},
    {"find": ("lands at M.A.H.Y. Khoory's Abu Dhabi branch on a Thursday "
              "evening around 16:30: roughly 75 pumps"),
     "replace": ("lands at M.A.H.Y. Khoory's Abu Dhabi branch on a Thursday "
                 "evening: roughly 75 pumps")},
    {"find": ("the same Grundfos range it carries, so the job will be won or "
              "lost on price and speed of response as much as on brand."),
     "replace": ("the same Grundfos range it carries. The job will be won or "
                 "lost on price and speed of response as much as on brand.")},
    {"find": ("Worked properly, with every schedule and specification read, "
              "head losses calculated for each application, and every "
              "selection run through the manufacturer software, an inquiry "
              "this size is close to twenty-eight hours"),
     "replace": ("Worked properly, an inquiry this size is close to "
                 "twenty-eight hours")},
    {"find": ("It is not enough. Tuesday comes and the quotation is not "
              "ready.\nThe quote goes out"),
     "replace": "It is not enough. The quote goes out"},
    {"find": "Khoory ultimately wins the project",
     "replace": "Khoory still wins the project"},

    # ---------------- Section 2: merged 2.1 ----------------
    {"find": "2.1 Industry context",
     "replace": ("2.1 The technical-expertise function: slow, capacity-bound, "
                 "error-prone")},
    {"find": ("A distributor exists in this chain because the manufacturer "
              "cannot do what the distributor does, whether economically or "
              "at all. The first and costliest of the distributor's functions "
              "is technical expertise. Every RFQ means reading consultant "
              "specifications, CAD files and drawings, extracting flow, head "
              "and efficiency requirements, running head-loss calculations, "
              "and working out which model across a manufacturer's full range "
              "actually fits the site; for unusual applications it means "
              "going back to the manufacturer for a special quote before "
              "pricing the contractor. A multinational manufacturer selling "
              "into dozens of regions cannot build that regional depth "
              "itself. It is exactly this function that nearly failed under "
              "pressure in the Innovo inquiry.\n"
              "The second function is credit: rather than extend "
              "project-linked payment terms, bank guarantees and retentions "
              "to dozens of individual contractors, the manufacturer works "
              "through one distributor and lets it carry the market and the "
              "credit risk.\n"
              "The third is local presence: testing, commissioning and "
              "warranty support from a party the contractor can actually "
              "reach when something goes wrong.\n"
              "Each of these functions is under pressure from digitization, "
              "and this paper examines what happens when the most defensible "
              "of them becomes automatable. Credit and local presence are "
              "largely fixed costs of being in the market; technical "
              "expertise is not: it needs trained estimators and hours of "
              "manual work per inquiry, and it scales directly with volume "
              "and complexity. The question the paper pursues is whether the "
              "reading, the calculations and the model selection can be "
              "digitized without losing the judgment that makes them "
              "valuable. "),
     "replace": ("A distributor exists in this chain because the manufacturer "
                 "cannot do what the distributor does. Three functions "
                 "justify the position: technical expertise, credit, and "
                 "local presence for testing, commissioning and warranty "
                 "support. Credit and presence are largely fixed costs of "
                 "being in the market. Technical expertise is the costliest "
                 "and the one under examination here. Every RFQ means reading "
                 "consultant specifications, CAD files and drawings, "
                 "extracting flow, head and efficiency requirements, running "
                 "head-loss calculations, and working out which model across "
                 "a manufacturer's full range fits the site. It needs trained "
                 "estimators, it scales with volume and complexity, and it is "
                 "what nearly failed under pressure in the Innovo inquiry. "
                 "The paper asks whether the reading, the calculations and "
                 "the model selection can be digitized without losing the "
                 "judgment that makes them valuable.\n"
                 "At Khoory the function shows three symptoms."),
     "unbold": True},
    {"find": "2.2 Problem decomposition\n", "replace": ""},
    {"find": ("Speed. A standard inquiry of three to twelve pumps across one "
              "or two applications takes an estimator around five and a half "
              "hours of concentrated work: reading the specification and CAD "
              "files, running head loss calculations, selecting the model, "
              "and pricing it. The largest inquiries, several dozen pumps "
              "across multiple applications (the Innovo package ran to "
              "seventy-five), demand twenty-five to thirty hours of "
              "estimating effort and require pulling multiple estimators "
              "simultaneously, against deadlines sometimes as tight as two to "
              "three days. These large inquiries arrive roughly once a month "
              "but cannot be staffed as if routine. Timing costs real "
              "business: an estimated 15% of tenders are lost specifically to "
              "late or rushed quotes (E, sales and management interviews; "
              "treated as an upper bound and triangulated in 9.3), "
              "concentrated among first-time customers with no relationship "
              "to buy patience, and fast-track projects landing while the "
              "team is already stretched."),
     "replace": ("Speed. A standard inquiry of three to twelve pumps takes an "
                 "estimator around five and a half hours of concentrated "
                 "work. The largest inquiries (the Innovo package ran to "
                 "seventy-five pumps) demand twenty-five to thirty hours and "
                 "several estimators at once, against deadlines sometimes as "
                 "tight as two to three days. They arrive roughly once a "
                 "month but cannot be staffed as if routine. An estimated 15% "
                 "of tenders are lost specifically to late or rushed quotes "
                 "(E, sales and management interviews, treated as an upper "
                 "bound and triangulated in 9.3), concentrated among "
                 "first-time customers with no relationship to buy "
                 "patience."),
     "bold": ["Speed."], "unbold": True},
    {"find": ("Cost. Khoory carries 16 estimators across all branches, each "
              "handling roughly 12 RFQs a week across the company's full "
              "product range. A fully loaded estimator costs the business "
              "approximately \u20ac22,000 a year. Hiring a qualified "
              "replacement takes two to three months, and a further three to "
              "four months before they are fully productive. Estimator "
              "capacity is therefore a hard constraint rather than a soft "
              "one: it directly determines how fast the business can take on "
              "new sales and new customers, independent of demand."),
     "replace": ("Cost. Khoory carries 16 estimators across all branches, "
                 "each handling roughly 12 RFQs a week. A fully loaded "
                 "estimator costs the business approximately \u20ac22,000 a "
                 "year, and a qualified replacement takes two to three months "
                 "to hire and a further three to four to become productive. "
                 "Estimator capacity is a hard constraint: it directly "
                 "determines how fast the business can take on new sales and "
                 "new customers, independent of demand."),
     "bold": ["Cost."], "unbold": True},
    {"find": ("Quality. Errors are not rare. Across the 2025 quotation "
              "audit, roughly one standard inquiry in nine went out "
              "containing at least one defect (a wrong model, a wrong price, "
              "or a missed specification requirement), rising to one in five "
              "on the largest, most valuable work. The full error taxonomy "
              "and its cost consequences are developed in Section 4.4."),
     "replace": ("Quality. Across the 2025 quotation audit, roughly one "
                 "standard inquiry in nine went out containing at least one "
                 "defect (a wrong model, a wrong price, or a missed "
                 "specification requirement), rising to one in five on the "
                 "largest, most valuable work. Section 4.4 develops the error "
                 "taxonomy and its cost."),
     "bold": ["Quality."], "unbold": True},

    # ---------------- Section 2: merged RQ + scope ----------------
    {"find": "2.3 Research questions",
     "replace": "2.2 Research questions and scope"},
    {"find": ("and what evidence supports its technical feasibility?"),
     "replace": ("and what evidence supports its technical feasibility? "
                 "(Sections 6 to 8)")},
    {"find": "and how robust is that projection under uncertainty?",
     "replace": ("and how robust is that projection under uncertainty? "
                 "(Section 9)")},
    {"find": "and what implementation path best manages the risks?",
     "replace": ("and what implementation path best manages the risks? "
                 "(Sections 10 and 11)")},
    {"find": ("Slow turnaround, hard capacity constraints and error rates "
              "that erode margin and trust are all downstream of one "
              "question: whether the distributor's technical-expertise "
              "function can be automated without losing the judgment that "
              "makes it valuable. Three research questions address it: RQ1 in "
              "Sections 6 through 8, RQ2 in Section 9, and RQ3 in Sections "
              "10 and 11.\n"),
     "replace": ""},
    {"find": "2.4 Scope\n", "replace": ""},
    {"find": ("Product. The scope is limited to pumps, where the technical "
              "selection burden is heaviest and the case for automation "
              "strongest; valves, HVAC and Khoory's other product lines are "
              "excluded, though they are the natural extension once the "
              "pump-focused system is proven."),
     "replace": ("Product. Pumps only, where the technical selection burden "
                 "is heaviest. Valves, HVAC and Khoory's other product lines "
                 "are the natural extension once the system is proven."),
     "bold": ["Product."], "unbold": True},
    {"find": ("Geography. The UAE only, where the volume and the pain are "
              "concentrated today; GCC expansion is a near-term next step, "
              "since specifications and practices across the region closely "
              "mirror the UAE market."),
     "replace": ("Geography. The UAE only, where the volume and the pain "
                 "concentrate today. GCC specifications closely mirror the "
                 "UAE market, so regional expansion is a near-term step."),
     "bold": ["Geography."], "unbold": True},
    {"find": ("The commercial negotiation between quote and LOI is excluded "
              "deliberately: the paper"),
     "replace": ("The commercial negotiation between quote and LOI is "
                 "excluded: the paper")},
    {"find": ("Depth of evaluation. No software has been built and no pilot "
              "run; the paper evaluates the investment before it is made. "
              "The analysis rests on a calibrated simulation of the current "
              "process, an audited feasibility assessment, and a financial "
              "projection under uncertainty (Sections 6\u20139); a live pilot "
              "is recommended, not conducted (Section 11)."),
     "replace": ("Depth. No software has been built and no pilot run. The "
                 "paper evaluates the investment before it is made, on a "
                 "calibrated simulation of the current process, an audited "
                 "feasibility assessment and a financial projection under "
                 "uncertainty (Sections 6\u20139). A live pilot is "
                 "recommended in Section 11 and has not been conducted."),
     "bold": ["Depth."], "unbold": True},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
