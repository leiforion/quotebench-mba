#!/usr/bin/env python3
"""T05 — propagate canonical numbers (conflicts C1–C15, C20) into the Doc.

Sources: model/conflict_resolutions.md, model/decisions.md (D1, D7–D11).
Usage: python3 scripts/t05_edits.py [--apply]
"""
import sys
sys.path.insert(0, "scripts")
from doc_editor import run

EDITS = [
    # --- C2 + C3: Tier 2 definition & effort (2.2) ---
    {"find": "A standard inquiry, ten to twenty pumps across up to three product types, takes an estimator roughly one full working day: reading the specification and CAD files, running head loss calculations, selecting the model, and pricing it.",
     "replace": "A standard inquiry — three to twelve pumps across one or two applications — takes an estimator around five and a half hours of concentrated work: reading the specification and CAD files, running head loss calculations, selecting the model, and pricing it."},

    # --- C4 + C5: large-inquiry size & effort (2.2) ---
    {"find": "Large, multi-application inquiries well over one hundred pumps stretch this to four or five working days and require pulling multiple estimators simultaneously, depending on the deadline the project demands, sometimes as tight as two to three days.",
     "replace": "The largest inquiries — several dozen pumps across multiple applications; the Innovo package ran to seventy-five — demand twenty-five to thirty hours of estimating effort and require pulling multiple estimators simultaneously, against deadlines sometimes as tight as two to three days."},

    # --- C15: tag the 15% lost-tender figure (2.2) ---
    {"find": "Timing costs real business, an estimated 15% of tenders are lost specifically due to late or rushed quotes, concentrated in two situations",
     "replace": "Timing costs real business: an estimated 15% of tenders are lost specifically to late or rushed quotes (E, sales and management interviews; treated as an upper bound and triangulated in 9.3), concentrated in two situations"},

    # --- C1 + C7: estimator cost and loaded rate ---
    {"find": "A fully loaded estimator costs the business approximately AED 96,000 a year.",
     "replace": "A fully loaded estimator costs the business approximately \u20ac22,000 a year."},
    {"find": "a qualified estimator costs around AED 96,000 a year",
     "replace": "a qualified estimator costs around \u20ac22,000 a year"},
    {"find": "At a fully loaded rate of AED 52 per hour, applied to both estimation and sales time (E, from payroll and headcount records), the median inquiry carries roughly AED 286 of direct labour before any overhead allocation, a figure developed by tier in 4.3.",
     "replace": "At a fully loaded rate of \u20ac12 per hour \u2014 \u20ac22,000 a year spread over roughly 1,840 productive hours \u2014 applied to both estimation and sales time (E, from payroll and headcount records), the median inquiry carries roughly \u20ac66 of direct labour before any overhead allocation, a figure developed by tier in 4.3."},

    # --- C8: branch-volume reconciliation (3.1 + 2.2), per D9 ---
    {"find": "Khoory operates 16 estimators across its UAE branches, handling on the order of twelve inquiries per estimator-week. The empirical baseline of Section 4 was measured at a single branch \u2014 [the Abu Dhabi estimation office] \u2014 whose 640 inquiries in 2025 constitute the study population;",
     "replace": "Khoory operates 16 estimators across its UAE branches, each handling on the order of twelve inquiries a week across all the product lines the company distributes. The empirical baseline of Section 4 was measured at a single branch \u2014 [the Abu Dhabi estimation office] \u2014 whose 640 pump RFQs in 2025 constitute the study population, the slice of that workload within this paper's product scope;"},
    {"find": "Khoory carries 16 estimators across all branches, each handling roughly 12 RFQs a week.",
     "replace": "Khoory carries 16 estimators across all branches, each handling roughly 12 RFQs a week across the company's full product range."},

    # --- C6: error rate restated in inquiry terms (2.2) ---
    {"find": "Errors are not rare. In a typical quotation covering around ten pump line items, one or two will typically contain a mistake, wrong model selection, wrong pricing, or a missed specification requirement.",
     "replace": "Errors are not rare. Across the 2025 quotation audit, roughly one standard inquiry in nine went out containing at least one defect \u2014 a wrong model, a wrong price, or a missed specification requirement \u2014 rising to one in five on the largest, most valuable work."},

    # --- C9: queue-share range (Exhibit 4.2 caption) ---
    {"find": "The queue share is remarkably stable \u2014 between 84% and 87% \u2014 regardless of complexity (M).",
     "replace": "The queue share is remarkably stable \u2014 between 86% and 88% \u2014 regardless of complexity (M)."},

    # --- C1: error-cost table (4.4) ---
    {"find": "AED 600 rework; occasional full requote",
     "replace": "\u20ac140 rework; occasional full requote"},
    {"find": "AED 1,900; site failure cases exceed AED 25,000",
     "replace": "\u20ac440; site failure cases exceed \u20ac5,750"},
    {"find": "AED 8,000 avg. (returns, re-orders, commissioning delay)",
     "replace": "\u20ac1,840 avg. (returns, re-orders, commissioning delay)"},
    {"find": "AED 3,200 direct margin loss",
     "replace": "\u20ac740 direct margin loss"},

    # --- C1: routing threshold (7.7) ---
    {"find": "value < AED V\u2081",
     "replace": "value < \u20acV\u2081"},

    # --- C1: Table 4.2 label ---
    {"find": "Direct cost per quote (AED)",
     "replace": "Direct cost per quote (\u20ac)"},

    # --- C1: conversion statement (3.2) ---
    {"find": "Table 3.1 lists every source of evidence the paper draws on, what each supplies, and the section where it does its work. No other data enters the analysis.",
     "replace": "Table 3.1 lists every source of evidence the paper draws on, what each supplies, and the section where it does its work. No other data enters the analysis. All monetary figures in this paper are stated in euros, converted from UAE dirhams at AED 1 = \u20ac0.23; the underlying records are dirham-denominated."},

    # --- C14: tag Option B / Option C percentages (6.1) ---
    {"find": "The selection software removes around 20 to 30 percent of the manual effort, mainly the curve reading and model matching that used to be done by hand.",
     "replace": "The selection software removes around 20 to 30 percent of the manual effort (E, estimator interviews), mainly the curve reading and model matching that used to be done by hand."},
    {"find": "So an off-the-shelf CPQ tool only solves around 10 to 15 percent of the problem we are trying to solve. It automates the sending of the quotation, but everything before that stays manual.",
     "replace": "So an off-the-shelf CPQ tool addresses only around 10 to 15 percent of the touch time measured in Section 4 (E) \u2014 the pricing and quote-assembly tail. It automates the sending of the quotation, but everything before that stays manual."},

    # --- C13: source the 22-hour claim (7.3) ---
    {"find": "instead of after 22 hours of triage and reading",
     "replace": "instead of after the roughly 22 working hours of queueing and reading the as-is process needs (the 14-hour assignment median of 4.1 plus a day of reading)"},

    # --- C20: name the system (7.1), per D7 ---
    {"find": "Five constraints govern the design, written as obligations rather than aspirations.",
     "replace": "The proposed system \u2014 referred to hereafter as QuoteBench \u2014 is governed by five constraints, written as obligations rather than aspirations."},

    # --- C11 + C12: re-time the to-be Innovo walk-through (7.9), per D8 ---
    {"find": "Friday, 11:05: the contractor replies; the system merges the thread, re-validates, runs the head-loss calculations, filters the product store, queries the selection API, and holds a draft quote \u2014 models ranked, the booster duty point flagged near its curve edge, prices in band \u2014 by 11:12. It is waiting on someone, rather than someone waiting on it, and that inversion is the whole design. At 14:00, the estimator's first free slot, the twenty-minute review turns on the flagged selection; the senior's confirmation is two lines, one alternate is added, the discount stays in band [A6, A7]. At 15:10 Friday the quote would go out, with the estimator's name on it per 11.3. Seven calendar days would become one; 5.5 touch hours would become roughly 25 minutes; and neither near-miss of 4.5 would arise to be caught.",
     "replace": "The contractor's reply is the one interval no redesign controls, so it is carried over at its measured pace: the request is seen on Friday and answered Monday morning. Within minutes of the reply the system has merged the thread, re-validated, run the head-loss calculations, filtered the product store, queried the selection API, and holds a draft quote \u2014 models ranked, the booster duty point flagged near its curve edge, prices in band. It is waiting on someone, rather than someone waiting on it. At 14:00 Monday, the estimator's first free slot, the review turns on the flagged selections; the senior's confirmation is two lines, one alternate is added, the discount stays in band [A6, A7]. At 15:10 Monday the quote would go out with the estimator's name on it per 11.3 \u2014 a day ahead of the deadline instead of two days late. Seven calendar days would become four; twenty-eight touch hours would become roughly [2.5\u20133, pending the Section 8 simulation] \u2014 the review of a 75-pump draft rather than its manual construction; and neither near-miss of 4.5 would arise to be caught."},

    # --- Table 4.1: thresholds to EUR + typo ---
    {"row_anchor": "Project value", "old_cell": "< AED 40k", "new_cell": "< \u20ac9k"},
    {"row_anchor": "Project value", "old_cell": "AED 40k \u2013 350k", "new_cell": "\u20ac9k \u2013 \u20ac80k"},
    {"row_anchor": "Project value", "old_cell": "> AED 350k", "new_cell": "> \u20ac80k"},
    {"row_anchor": "Pumps requested", "old_cell": "3\u201312, upto 2 applications", "new_cell": "3\u201312, up to 2 applications"},

    # --- Table 4.2: cost row to EUR ---
    {"row_anchor": "Direct cost per quote", "old_cell": "109", "new_cell": "25"},
    {"row_anchor": "Direct cost per quote", "old_cell": "286", "new_cell": "66"},
    {"row_anchor": "Direct cost per quote", "old_cell": "593", "new_cell": "137"},

    # --- Table 4.4: chronology rebuild (C10) ---
    {"row_anchor": "Contractor replies (weekend plus Monday in between)", "old_cell": "~41 h", "new_cell": "~2.5 working days"},
    {"row_anchor": "Pricing and discount debated across the package", "old_cell": "Fri", "new_cell": "Thu"},
    {"row_anchor": "Pricing and discount debated across the package", "old_cell": "4.0 h", "new_cell": "1.0 h"},
    {"row_anchor": "Quotation assembled and issued", "old_cell": "Thu (next)", "new_cell": "Thu evening"},
    {"row_anchor": "Quotation assembled and issued", "old_cell": "6.0 h", "new_cell": "\u2014"},
]

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    ok = run(EDITS, apply=apply)
    sys.exit(0 if ok else 1)
