#!/usr/bin/env python3
"""Phase 2, pass 6: sentence-level tightening (cut order levels 5-7),
after the structural passes. Fixes the last stale cross-references
((8.3, 4.4) and two (9.4)s), removes non-list semicolons, thins contrast
constructions, varies repeated paragraph openers, and takes ~500 words
out of the longest sections.
"""
import sys

from doc_editor import run

EDITS = [
    # ---- stale refs ----
    {"find": "who challenge the design's assumptions (8.3, 4.4).",
     "replace": "who challenge the design's assumptions (8.2, 4.4)."},
    {"find": ("triangulated in 9.3 and floored at zero in the conservative "
              "case; and the build cost (9.4)."),
     "replace": ("triangulated in 9.1 and floored at zero in the "
                 "conservative case; and the build cost (9.2).")},
    # ---- Section 3 ----
    {"find": ("The approach follows established practice: discrete-event "
              "models of service operations"),
     "replace": ("Both models follow established practice: discrete-event "
                 "models of service operations")},
    {"find": ("Results are reported at P10, P50 and P90 with the probability "
              "of clearing the hurdle rate. Every input distribution is "
              "documented in Appendix C and named in the Appendix A "
              "register."),
     "replace": ("Results are reported at P10, P50 and P90. Input "
                 "distributions are documented in Appendix C and named in "
                 "the Appendix A register.")},
    {"find": ("All monetary figures in this paper are stated in euros, "
              "converted from UAE dirhams at AED 1 = \u20ac0.23; the "
              "underlying records are dirham-denominated."),
     "replace": ("All monetary figures are stated in euros, converted from "
                 "the dirham-denominated records at AED 1 = \u20ac0.23.")},

    # ---- Section 4 ----
    {"find": ("Exhibit 4.1 maps the path, annotating each step with touch "
              "time (someone actively working on the inquiry) and queue time "
              "(the inquiry waiting its turn)."),
     "replace": ("Exhibit 4.1 maps the path, annotating each step with touch "
                 "time and queue time.")},
    {"find": ("The exhibit carries the central finding of the current-state "
              "study: the median case consumed 5.5 hours of actual work "
              "spread over roughly 39 working hours of elapsed time (M)."),
     "replace": ("The exhibit carries the section's central finding: the "
                 "median case consumed 5.5 hours of work spread over 39 "
                 "working hours of elapsed time (M).")},
    {"find": ("The cost side is simpler: at a fully loaded \u20ac12 per hour "
              "(\u20ac22,000 a year over roughly 1,840 productive hours; E, "
              "payroll records), the median inquiry carries about \u20ac66 "
              "of direct cost (labour plus a licence allocation), developed "
              "by tier in Table 4.2."),
     "replace": ("The cost side is simpler: at a fully loaded \u20ac12 per "
                 "hour (E, payroll records), the median inquiry carries "
                 "about \u20ac66 of direct cost, developed by tier in Table "
                 "4.2.")},
    {"find": ("Exhibit 4.1. Median values across the 22 observed inquiries "
              "(M). The clarification loop and the management approval loop "
              "occur on a subset of inquiries; their queue times are medians "
              "within that subset."),
     "replace": ("Exhibit 4.1. Median values across the 22 observed "
                 "inquiries (M). The clarification and management approval "
                 "loops occur on a subset of inquiries. Their queue times "
                 "are medians within that subset.")},
    {"find": ("Cost per quote combines touch hours at loaded rates with a "
              "per-inquiry allocation of estimation software licences; "
              "defect rates were estimated by auditing a stratified sample "
              "of 120 quotations against source documents."),
     "replace": ("Cost per quote combines touch hours at loaded rates with a "
                 "per-inquiry licence allocation. Defect rates were "
                 "estimated by auditing a stratified sample of 120 "
                 "quotations against source documents.")},
    {"find": ("Unit costs are stated at the branch\u2019s actual 2025 order "
              "values: the audit\u2019s original estimates were made against "
              "order sizes about six times smaller than the revenue "
              "reconciliation later established, and a defect on a larger "
              "order costs proportionally more (D19)."),
     "replace": ("Unit costs are restated at the branch's actual 2025 order "
                 "values, since a defect on a larger order costs "
                 "proportionally more (D19).")},
    {"find": ("Table 4.4 (Appendix K) reconstructs its path step by step, "
              "timestamped from the mailbox records and the estimators' "
              "logs: received Thursday evening and unread overnight, first "
              "touched late Friday morning, the consolidated clarification "
              "not sent until Saturday afternoon, and the contractor's "
              "Tuesday reply then sitting unread in the same shared mailbox "
              "that delayed the start."),
     "replace": ("Table 4.4 (Appendix K) reconstructs its path from the "
                 "mailbox records and the estimators' logs: unread "
                 "overnight, first touched late Friday, the consolidated "
                 "clarification not sent until Saturday afternoon, the "
                 "contractor's reply then sitting unread in the same shared "
                 "mailbox.")},
    {"find": ("Thirty-eight percent of inquiries need at least one loop "
              "(M); complex inquiries often need two."),
     "replace": ("Thirty-eight percent of inquiries need at least one loop "
                 "(M), and complex inquiries often need two.")},

    # ---- Section 6 ----
    {"find": ("What it cannot do is move the operational needles of cycle "
              "time, error rate and discount spread, because it adds hands "
              "to an unchanged process."),
     "replace": ("What it cannot do is move cycle time, error rate or the "
                 "discount spread.")},
    {"find": ("Option A is faster to first value than anything proposed here "
              "(an estimator hired in March is quoting by summer, while "
              "Phase 1 of Section 11 is still running in shadow), and hiring "
              "is reversible in a way build spend is not."),
     "replace": ("Option A is faster to first value than anything proposed "
                 "here (an estimator hired in March is quoting by summer), "
                 "and hiring is reversible in a way build spend is not.")},
    {"find": ("On touch time alone, hiring even wins the arithmetic: at the "
              "measured tier mix the average inquiry carries about 4.3 touch "
              "hours (M, Table 4.2), roughly \u20ac52 of labour at the "
              "loaded rate, so at 640 RFQs a year the labour the automation "
              "could redeploy (about \u20ac17,000 a year) does not cover the "
              "system's amortized build cost (\u20ac92,000, one internal "
              "engineer-year) and its running costs (developed in 9.4)."),
     "replace": ("On touch time alone, hiring even wins the arithmetic: the "
                 "average inquiry carries about 4.3 touch hours (M, Table "
                 "4.2), roughly \u20ac52 of labour, so the labour the "
                 "automation could redeploy (about \u20ac17,000 a year) does "
                 "not cover the amortized build (\u20ac92,000) and running "
                 "costs (9.2).")},
    {"find": ("Table 6.1. Option scoring, 1 (worst) to 5 (best); criteria "
              "are not equally weighted. Cost and implementation risk score "
              "five-year exposure; strategic optionality scores the "
              "transaction-data asset of Section 10."),
     "replace": ("Table 6.1. Option scoring, 1 (worst) to 5 (best). Cost "
                 "and implementation risk score five-year exposure, and "
                 "strategic optionality scores the transaction-data asset of "
                 "Section 10.")},

    # ---- Section 7 ----
    {"find": ("A projected Tier 2 inquiry would need roughly 25 minutes of "
              "human attention against the measured 5.5 hours, the "
              "difference redeployed rather than removed (9.1, 11.2)."),
     "replace": ("A projected Tier 2 inquiry would need roughly 25 minutes "
                 "of human attention against the measured 5.5 hours, the "
                 "difference redeployed (9.1, 11.2).")},
    {"find": ("owning the flagged uncertainties, the curve-edge calls and "
              "the Tier 3 work that genuinely needs judgement (11.2)."),
     "replace": ("owning the flagged uncertainties and the Tier 3 work that "
                 "needs judgement (11.2).")},
    {"find": ("The contractor's reply is the one interval no redesign "
              "controls, so it is carried over at its measured pace: the "
              "request is seen on Friday and answered Monday morning."),
     "replace": ("The contractor's reply, the one interval no redesign "
                 "controls, is carried at its measured pace: seen Friday, "
                 "answered Monday morning.")},
    {"find": (" It is waiting on someone, rather than someone waiting on "
              "it."),
     "replace": ""},

    # ---- Section 8 ----
    {"find": ("Engineer skill and inquiry complexity then spread those "
              "figures further: per-field success and confidence are drawn "
              "inquiry by inquiry, so no single accuracy number is "
              "load-bearing anywhere downstream."),
     "replace": ("Engineer skill and inquiry complexity spread those figures "
                 "further, drawn inquiry by inquiry, so no single accuracy "
                 "number is load-bearing.")},
    {"find": ("carried as three variants (pessimistic, central, optimistic) "
              "rather than a single point."),
     "replace": ("carried as three variants: pessimistic, central, "
                 "optimistic.")},
    {"find": ("We had originally designed a field-by-field feasibility audit "
              "of 25\u201330 historical RFQs, scored by the estimators "
              "against a written rubric, to replace these ranges with "
              "evidence from Khoory's own documents. That audit remains the "
              "right instrument, and its materials are drafted (protocol, "
              "rubric and scoring sheet in Appendix E), but it needs "
              "estimator time we could not commission for this paper."),
     "replace": ("We designed a field-by-field feasibility audit of "
                 "25\u201330 historical RFQs to replace these ranges with "
                 "evidence from Khoory's own documents. Its materials are "
                 "drafted (Appendix E), but it needs estimator time we could "
                 "not commission for this paper.")},
    {"find": ("As with the contractor reply, the manufacturer special-quote "
              "round trip on complex work is outside the design's control "
              "and is carried at its measured pace inside the fitted "
              "external waits."),
     "replace": ("The manufacturer special-quote round trip on complex work, "
                 "like the contractor reply, is outside the design's control "
                 "and carried at its measured pace.")},
    {"find": ("Routing stays cautious: 15 percent of Tier 1 inquiries "
              "release as auto-drafts and a quarter go out assisted; Tier 2 "
              "is one-fifth assisted; every Tier 3 quote stays with an "
              "engineer, worked in the pre-filled workspace."),
     "replace": ("Routing stays cautious: 15 percent of Tier 1 inquiries "
                 "release as auto-drafts and a quarter go out assisted, Tier "
                 "2 is one-fifth assisted, and every Tier 3 quote stays with "
                 "an engineer.")},

    # ---- Section 9 ----
    {"find": (" Throughput is roughly \u20ac17 million of won value per "
              "estimator per year."),
     "replace": ""},
    {"find": ("636 inquiries a year (the Table 4.2 monthly volumes "
              "annualized; the log holds 640)"),
     "replace": ("636 inquiries a year (the Table 4.2 monthly volumes "
                 "annualized, against 640 in the log)")},
    {"find": "full adoption, central case (S; run manifest in the public repository).",
     "replace": "full adoption, central case (S, run manifest in the public repository)."},
    {"find": ("the recovered volume is upside the pilot can log. It is left "
              "out of every number in this paper, which is the conservative "
              "direction."),
     "replace": ("the recovered volume is upside the pilot can log. It "
                 "enters no number in this paper.")},
    {"find": ("(E, management estimate; the \u20ac92,000 engineer-year is "
              "the build alone)"),
     "replace": ("(E, management estimate: the \u20ac92,000 engineer-year is "
                 "the build alone)")},
    {"find": ("\u20ac2.7 million at P50 and \u20ac4.3 million at P90; every "
              "one of the 20,000 draws clears the hurdle, and median payback "
              "is about four months (S; Exhibit 9.2)."),
     "replace": ("\u20ac2.7 million at P50 and \u20ac4.3 million at P90. "
                 "Every one of the 20,000 draws clears the hurdle, and "
                 "median payback is about four months (S, Exhibit 9.2).")},
    {"find": ("Phase 1 measures exactly that first: extraction accuracy on "
              "Khoory's own documents and the win-rate response on live "
              "inquiries (11.1)."),
     "replace": ("Phase 1 measures exactly that: live extraction accuracy "
                 "and the win-rate response (11.1).")},
    {"find": ("about \u20ac180, and about four calendar days, with the "
              "contractor's reply carried at its measured pace. The quote "
              "goes out a day inside the deadline (S)."),
     "replace": ("about \u20ac180, and about four calendar days. The quote "
                 "goes out a day inside the deadline (S).")},
    {"find": ("the margin at stake is roughly \u20ac1.4\u20132.6 million (S, "
              "register arithmetic: the D19 flagship value range at the Tier "
              "3 margin), and what the redesign buys is the deadline,"),
     "replace": ("the margin at stake is roughly \u20ac1.4\u20132.6 million "
                 "(S), and what the redesign buys is the deadline,")},

    # ---- Section 11 ----
    {"find": ("priced at roughly \u20ac30,000 (S: one quarter of the build "
              "engineer-year plus pilot-scale running costs) inside the "
              "\u20ac92,000 build budget."),
     "replace": ("priced at roughly \u20ac30,000 (S: a quarter engineer-year "
                 "plus pilot running costs) inside the \u20ac92,000 build "
                 "budget.")},
    {"find": ("automation rate (share of fields drafted without "
              "intervention, against the 8.2 variants); override rate "
              "(engineer corrections per quote, the flywheel\u2019s input "
              "and the adoption signal); extraction accuracy (field level, "
              "against the 5.2 range the case is priced on); cycle time "
              "median and P90 by tier (against Exhibit 8.1); win rate by "
              "tier (against the measured 2025 rates and, from Phase 2, the "
              "9.1 uplift); margin per quote (against the measured discount "
              "spread and the plus or minus 1 percent band); and error "
              "escapes (against the parity constraint of 8.2)."),
     "replace": ("automation rate (against the 8.2 variants); override rate "
                 "(the flywheel\u2019s input and the adoption signal); "
                 "extraction accuracy (against the 5.2 range); cycle time "
                 "median and P90 by tier (against Exhibit 8.1); win rate by "
                 "tier (against the 2025 rates and, from Phase 2, the 9.1 "
                 "uplift); margin per quote (against the discount spread and "
                 "the plus or minus 1 percent band); and error escapes "
                 "(against the 8.2 parity constraint).")},

    # ---- Section 13: vary the RQ paragraph openers ----
    {"find": ("The third asked what the transformation means for the "
              "distributor\u2019s position in the value chain. Section "
              "10\u2019s answer: automated quoting converts"),
     "replace": ("On the third question, the distributor\u2019s position in "
                 "the value chain, Section 10\u2019s answer is that "
                 "automated quoting converts")},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
