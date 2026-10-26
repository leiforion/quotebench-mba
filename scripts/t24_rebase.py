#!/usr/bin/env python3
"""D19 rebase: restate the paper at the actual 2025 revenue base.

Authors (6 Sep): branch pump-only revenue ~AED 150M won (EUR ~34.5M), average
gross margin 24% on revenue. Simulator rebased (x6.125 on all value
parameters; margins 18.5/22.5/27.8; BASE-30 unit costs value-scaled; BASE-31
pct target retired). New headline: NPV P10/P50/P90 = 1.49/2.82/4.40 M EUR,
every draw clears the hurdle, floor case POSITIVE (+342k @12%).

Edits: exec summary paras 1+3; 3.1 single-branch statement (G1); Tables 3.1,
4.1, 4.2, 4.3 (cells + captions); 4.4 leakage prose; 6.3 concession rewrite
(G1); 8.4 cost-only bundle; 9.1 rewrite + O9 note deletion; 9.2 waterfall;
9.3 elasticity verdict; 9.5 appraisal + floor; 9.6 tornado/kill/Innovo (G8).
"""
import sys

from doc_editor import run

EDITS = [
    # ---- Executive summary
    {"find": ("Between 6 and 19 percent of quotations carry at least one "
              "defect, and the function leaks about five times its "
              "\u20ac33,000 running cost: roughly \u20ac67,000 a year to "
              "quality failures and \u20ac106,000 to unmanaged discounting."),
     "replace": ("Between 6 and 19 percent of quotations carry at least one "
                 "defect, and against the branch\u2019s \u20ac34.5 million of "
                 "won pump orders the function leaks about twenty-five times "
                 "its \u20ac33,000 running cost: roughly \u20ac177,000 a year "
                 "to quality failures and \u20ac673,000 to unmanaged "
                 "discounting."),
     "unbold": True},
    {"find": ("Across 20,000 Monte Carlo draws at a 12 percent discount rate, "
              "five-year NPV runs from \u20ac94,000 (P10) through \u20ac260,000 "
              "(P50) to \u20ac457,000 (P90), with median payback of 1.6 years "
              "and a 98.5 percent probability of clearing the 15 percent "
              "hurdle. The floor case is negative: with the win-rate uplift "
              "at zero and extraction at its pessimistic bound, NPV is minus "
              "\u20ac83,000. The investment is a bet that faster, cleaner "
              "quotes win work, and the pilot tests that bet first."),
     "replace": ("Across 20,000 Monte Carlo draws at a 12 percent discount "
                 "rate, five-year NPV runs from \u20ac1.5 million (P10) "
                 "through \u20ac2.8 million (P50) to \u20ac4.4 million (P90), "
                 "clearing the 15 percent hurdle in every draw, with median "
                 "payback of about four months. The floor case also clears: "
                 "with the win-rate uplift at zero, extraction at its "
                 "pessimistic bound and the build 30 percent over, NPV is "
                 "still about \u20ac0.3 million on discount discipline and "
                 "error reduction alone. The remaining risk is not the "
                 "arithmetic but the evidence under it: every capability "
                 "input is simulated, and the pilot exists to test those "
                 "inputs before the build is approved."),
     "unbold": True},
    # ---- 3.1 single-branch statement (fixes the G1 promise)
    {"find": ("whose 640 pump RFQs in 2025 are the study population; "
              "company-wide figures appear only where Section 9 scales the "
              "branch findings, and are labelled when they do."),
     "replace": ("whose 640 pump RFQs in 2025 are the study population; every "
                 "figure in the paper, including the Section 9 investment "
                 "case, is single-branch, and no company-wide scaling is "
                 "used."),
     "unbold": True},
    # ---- Table 3.1 (Appendix K): internal interviews row
    {"row_anchor": "Internal interviews",
     "old_cell": "Loaded costs, hiring lead times, lost-tender estimate, discounting behaviour",
     "new_cell": "Loaded costs, hiring lead times, lost-tender estimate, discounting behaviour, 2025 revenue and margin"},
    {"row_anchor": "Internal interviews",
     "old_cell": "2.2, 4.4, 9.4",
     "new_cell": "2.2, 4.4, 9.1, 9.4"},
    # ---- Table 4.1 (Appendix K): value bands restated
    {"row_anchor": "Project value", "old_cell": "< \u20ac9k", "new_cell": "< \u20ac56k"},
    {"row_anchor": "Project value", "old_cell": "\u20ac9k \u2013 \u20ac80k", "new_cell": "\u20ac56k \u2013 \u20ac493k"},
    {"row_anchor": "Project value", "old_cell": "> \u20ac80k", "new_cell": "> \u20ac493k"},
    {"find": "Table 4.1. Segmentation criteria and 2025 mix. n = 640 inquiries.",
     "replace": ("Table 4.1. Segmentation criteria and 2025 mix, n = 640 "
                 "inquiries. Value bands restated against the branch\u2019s "
                 "actual 2025 revenue (E, D19); volume and value shares are "
                 "measured (M).")},
    # ---- Table 4.2: margins restated
    {"row_anchor": "Gross margin", "old_cell": "14%", "new_cell": "18.5%"},
    {"row_anchor": "Gross margin", "old_cell": "17%", "new_cell": "22.5%"},
    {"row_anchor": "Gross margin", "old_cell": "21%", "new_cell": "27.8%"},
    {"row_anchor": "Gross margin", "old_cell": "M", "new_cell": "E"},
    {"find": ("defect rates were estimated by auditing a stratified sample of "
              "120 quotations against source documents."),
     "replace": ("defect rates were estimated by auditing a stratified sample "
                 "of 120 quotations against source documents. Gross margins "
                 "restate the measured tier pattern to the branch\u2019s "
                 "stated 24 percent average on revenue (D19).")},
    # ---- 4.4 prose
    {"find": ("selection errors the most expensive (about \u20ac1,840 each), "
              "and calculation errors carry the site-failure tail beyond "
              "\u20ac5,750 (E)."),
     "replace": ("selection errors the most expensive (about \u20ac11,300 "
                 "each), and calculation errors carry the site-failure tail "
                 "beyond \u20ac35,000 (E)."),
     "unbold": True},
    {"find": ("Summed across the year, the traceable cost of the four classes "
              "comes to roughly 1.2% of revenue (E)."),
     "replace": ("Summed across the year, the traceable cost of the four "
                 "classes comes to roughly \u20ac177,000, about 0.5% of "
                 "revenue (E). Unit costs are stated at the branch\u2019s "
                 "actual 2025 order values: the audit\u2019s original "
                 "estimates were made against order sizes about six times "
                 "smaller than the revenue reconciliation later established, "
                 "and a defect on a larger order costs proportionally more "
                 "(D19)."),
     "unbold": True},
    {"find": ("the foregone margin is roughly 1.9% of revenue annually (E), "
              "half again as large as all four error classes combined, and "
              "invisible precisely because no single decision was wrong."),
     "replace": ("the foregone margin is roughly 1.9% of revenue annually "
                 "(E, about \u20ac673,000), nearly four times all four error "
                 "classes combined, and invisible precisely because no single "
                 "decision was wrong."),
     "unbold": True},
    {"find": ("Together, quality cost and discount leakage run to about 3.1% "
              "of revenue, the figure the pricing engine of Section 7.6 is "
              "designed against."),
     "replace": ("Together, quality cost and discount leakage run to about "
                 "2.5% of revenue, roughly \u20ac850,000 a year, the figure "
                 "the pricing engine of Section 7.6 is designed against."),
     "unbold": True},
    # ---- Table 4.3 (Appendix K): unit costs restated
    {"row_anchor": "Extraction / transcription",
     "old_cell": "\u20ac140 rework; occasional full requote",
     "new_cell": "\u20ac860 rework; occasional full requote"},
    {"row_anchor": "Head-loss worked from wrong pipe",
     "old_cell": "\u20ac440; site failure cases exceed \u20ac5,750",
     "new_cell": "\u20ac2,680; site failure cases exceed \u20ac35,000"},
    {"row_anchor": "duty point at curve edge",
     "old_cell": "\u20ac1,840 avg. (returns, re-orders, commissioning delay)",
     "new_cell": "\u20ac11,270 avg. (returns, re-orders, commissioning delay)"},
    {"row_anchor": "Wrong list price",
     "old_cell": "\u20ac740 direct margin loss",
     "new_cell": "\u20ac4,510 direct margin loss"},
    {"find": ("Categories are not mutually exclusive on a given inquiry; "
              "frequencies count inquiries where the class appears."),
     "replace": ("Categories are not mutually exclusive on a given inquiry; "
                 "frequencies count inquiries where the class appears. Unit "
                 "costs restated to actual 2025 order values (D19).")},
    # ---- 6.3 concession rewrite (fixes G1's multi-branch dependency)
    {"find": ("The arithmetic has a crossover. At the measured tier mix the "
              "average inquiry carries about 4.3 touch hours (M, Table 4.2), "
              "roughly \u20ac52 of labour at the loaded rate, so below "
              "roughly 1,000\u20131,300 pump RFQs a year (the span of the "
              "pre-audit automation range) the touch time automation could "
              "redeploy would not cover the system's amortized build cost "
              "(\u20ac92,000, one internal engineer-year) and its running "
              "costs (developed in 9.4), and hiring would dominate on cost "
              "as well as risk (S, register arithmetic; refined in 9.5). The "
              "measured single-branch volume of 640 sits below that line: "
              "the case for Option E rests explicitly on multi-branch "
              "deployment (9.1) and on the benefits hiring cannot buy at any "
              "volume: error elimination, discount discipline and response "
              "speed (9.2)."),
     "replace": ("On touch time alone, hiring even wins the arithmetic: at "
                 "the measured tier mix the average inquiry carries about "
                 "4.3 touch hours (M, Table 4.2), roughly \u20ac52 of labour "
                 "at the loaded rate, so at 640 RFQs a year the labour the "
                 "automation could redeploy (about \u20ac17,000 a year) does "
                 "not cover the system's amortized build cost (\u20ac92,000, "
                 "one internal engineer-year) and its running costs "
                 "(developed in 9.4). What decides the comparison is what "
                 "hiring cannot buy at any volume: the roughly \u20ac850,000 "
                 "annual leak of 4.4 sits in error content and discount "
                 "variance, and adding hands to an unchanged process "
                 "recovers none of it (9.2)."),
     "unbold": True},
    # ---- 8.4 cost-only bundle
    {"find": ("and roughly \u20ac53,000 a year of simulated benefit that does "
              "not depend on winning a single additional order"),
     "replace": ("and roughly \u20ac210,000 a year of simulated benefit that "
                 "does not depend on winning a single additional order"),
     "unbold": True},
    # ---- 9.1 rewrite
    {"find": ("The quoting function is cheap to run and expensive to get "
              "wrong. Direct quoting cost is about \u20ac33,000 a year: 636 "
              "inquiries at \u20ac25, \u20ac66 and \u20ac136 per quote by "
              "tier (E), absorbing about 2,780 engineer hours. Throughput is "
              "roughly \u20ac2.8 million of won value per estimator per "
              "year. The leakage is larger than the labour: quality failures "
              "cost about 1.2 percent of revenue (E, \u20ac67,000 on the "
              "derived base) and unmanaged discounting another 1.9 percent "
              "(E, \u20ac106,000), so the office leaks about five times what "
              "it costs to operate. The revenue base behind those "
              "percentages is derived rather than read from accounts (D13): "
              "tier volumes, value bands and win rates already in the "
              "register compound to \u20ac22.2 million quoted and \u20ac5.6 "
              "million won per year (S), including two flagship-scale "
              "projects a year (D17)."),
     "replace": ("The quoting function is cheap to run and expensive to get "
                 "wrong. Direct quoting cost is about \u20ac33,000 a year: "
                 "636 inquiries at \u20ac25, \u20ac66 and \u20ac137 per "
                 "quote by tier (E), absorbing about 2,780 engineer hours. "
                 "The revenue those hours carry is stated, not derived: the "
                 "branch's 2025 pump-only revenue was approximately AED 150 "
                 "million, \u20ac34.5 million at the paper's conversion (M, "
                 "management figure, D19), and the simulator's value model "
                 "reproduces it with about \u20ac136 million quoted implied "
                 "by the measured win rates (S), including two "
                 "flagship-scale projects a year (D17). Throughput is "
                 "roughly \u20ac17 million of won value per estimator per "
                 "year. The leakage dwarfs the labour: quality failures "
                 "cost about 0.5 percent of revenue (E, \u20ac177,000 at "
                 "the restated unit costs) and unmanaged discounting "
                 "another 1.9 percent (E, \u20ac673,000), so the office "
                 "leaks about twenty-five times what it costs to operate."),
     "unbold": True},
    # ---- O9 note deletion
    {"find": ("[AUTHORS TO CONFIRM \u2014 O9: the simulator derives the "
              "revenue base from registered values: EUR ~22.2M quoted / "
              "~5.6M won per year (~AED 97M / 25M), including two "
              "flagship-scale quotes per year (D17). This level is pinned by "
              "the measured tier value shares (12/41/47, BASE-11) and the "
              "Tier 1 value cap (BASE-12); it cannot go materially higher "
              "without contradicting them. Confirm the branch's actual 2025 "
              "pump-only revenue. If it differs materially, BASE-11/12 must "
              "be re-measured and Section 9 rebased.]\n"),
     "replace": ""},
    # ---- 9.2 waterfall
    {"find": ("Error cost, \u20ac8,000 a year (S): escaped-defect cost on won "
              "orders at the register's unit costs, with overall defect "
              "rates held at parity (8.2);"),
     "replace": ("Error cost, \u20ac20,000 a year (S): escaped-defect cost on "
                 "won orders at the restated unit costs, with overall defect "
                 "rates held at parity (8.2);"),
     "unbold": True},
    {"find": ("Discounting discipline, \u20ac28,000 a year (S): the sleeper. "
              "Quoting inside a reference band recovers part of the measured "
              "4\u201318 percent spread on comparable work (M);"),
     "replace": ("Discounting discipline, \u20ac174,000 a year (S): at the "
                 "actual revenue base this is the anchor benefit, larger "
                 "than labour and errors together by a factor of five. "
                 "Quoting inside a reference band recovers part of the "
                 "measured 4\u201318 percent spread on comparable work (M);"),
     "unbold": True},
    {"find": ("Win-rate uplift, \u20ac96,000 a year (S): the dominant bar and "
              "the least proven, gated next in 9.3."),
     "replace": ("Win-rate uplift, \u20ac779,000 a year (S): the dominant bar "
                 "and the least proven, gated next in 9.3."),
     "unbold": True},
    {"find": ("The central total is about \u20ac150,000 a year at full "
              "adoption, reached on the 7.10 ramp."),
     "replace": ("The central total is about \u20ac990,000 a year at full "
                 "adoption, reached on the 7.10 ramp."),
     "unbold": True},
    # ---- 9.3 elasticity verdict
    {"find": ("The stress runs add the most useful fact in the paper: the "
              "investment clears its hurdle if speed is worth as little as "
              "0.2 percentage points of win rate, one-tenth of the central "
              "estimate, and fails only if it is worth almost nothing at "
              "all (S)."),
     "replace": ("The stress runs add the most useful fact in the paper: the "
                 "investment clears its hurdle even if speed turns out to be "
                 "worth nothing at all, because the discounting and error "
                 "effects carry the cost base on their own; the uplift "
                 "decides how large the return is, not whether there is one "
                 "(S)."),
     "unbold": True},
    # ---- 9.5 appraisal
    {"find": ("Five-year NPV comes out at \u20ac94,000 at P10, \u20ac260,000 "
              "at P50 and \u20ac457,000 at P90; the probability of clearing "
              "the hurdle is 98.5 percent, median IRR is 69 percent, and "
              "median payback is 1.6 years (S; Exhibit 9.2)."),
     "replace": ("Five-year NPV comes out at \u20ac1.5 million at P10, "
                 "\u20ac2.8 million at P50 and \u20ac4.4 million at P90; "
                 "every one of the 20,000 draws clears the hurdle, and "
                 "median payback is about four months (S; Exhibit 9.2). At "
                 "this scale the internal rate of return stops being "
                 "informative (the median exceeds 300 percent against a "
                 "\u20ac92,000 build); the number that matters is the "
                 "floor."),
     "unbold": True},
    {"find": ("The floor case matters most. Set extraction to the pessimistic "
              "bound, the win uplift to zero and the build 30 percent over, "
              "and benefits fall to about \u20ac42,000 a year against the "
              "same cost base: NPV is minus \u20ac83,000 at 12 percent and "
              "minus \u20ac88,000 at the hurdle. The project does not clear "
              "on cost, error and discounting alone. This investment is a "
              "bet that faster, cleaner quotes win at least some additional "
              "work, cushioned by operating savings that cover most of the "
              "downside. The evidence that de-risks the bet is what Phase 1 "
              "of the pilot measures first: extraction accuracy on Khoory's "
              "own documents and the win-rate response on live inquiries "
              "(11.1)."),
     "replace": ("The floor case matters most. Set extraction to the "
                 "pessimistic bound, the win uplift to zero and the build 30 "
                 "percent over, and benefits still run about \u20ac180,000 a "
                 "year: NPV is \u20ac342,000 at 12 percent and \u20ac304,000 "
                 "at the hurdle. The project clears on cost, error and "
                 "discounting alone. That reverses the burden the case "
                 "carries: the question is no longer whether the economics "
                 "survive a disappointing pilot, but whether the capability "
                 "assumptions under them survive contact with Khoory's own "
                 "documents. Every input above the measured baseline is "
                 "simulated, and a result this one-sided is an argument for "
                 "testing the inputs, not for skipping the test. Phase 1 "
                 "measures exactly that first: extraction accuracy on "
                 "Khoory's own documents and the win-rate response on live "
                 "inquiries (11.1)."),
     "unbold": True},
    # ---- 9.6 tornado + kill criteria + Innovo stake (fixes G8)
    {"find": ("Exhibit 9.3 ranks the levers one at a time. The win uplift "
              "dominates: its zero-to-five-point range moves NPV by "
              "\u20ac650,000, six times the next lever (extraction "
              "capability, \u20ac101,000); pricing adoption, run cost, build "
              "overrun and change cost together move less than extraction "
              "alone. The same stress runs turn the ranking into thresholds "
              "a board can hold us to: at central values elsewhere, the case "
              "fails at the hurdle only if the uplift falls below 0.2 "
              "percentage points, the build exceeds 3.3 times plan, run "
              "costs exceed \u20ac83,000 a year, or demand halves; "
              "extraction quality and pricing adoption have no failure "
              "boundary on their own (S). These boundaries reappear as pilot "
              "kill criteria in 11.1, alongside"),
     "replace": ("Exhibit 9.3 ranks the levers one at a time. The win uplift "
                 "dominates: its zero-to-five-point range moves NPV by "
                 "\u20ac5.3 million, thirteen times the next lever (pricing "
                 "adoption, \u20ac0.4 million), with extraction capability "
                 "close behind and run cost, build overrun and change cost "
                 "together barely visible. The same stress runs return a "
                 "finding a marginal case could not: within every tested "
                 "range, no single lever kills the case at the hurdle. The "
                 "uplift at zero still clears (\u20ac0.43 million at the "
                 "hurdle), the build at six times plan still clears, run "
                 "costs at \u20ac200,000 a year still clear, and demand at "
                 "one-fifth of the 2025 rate still clears (S). The pilot's "
                 "kill criteria are therefore evidential rather than "
                 "financial: the 11.1 gates guard the simulated inputs "
                 "(live extraction accuracy, override rates, escaped "
                 "defects) rather than an NPV threshold, alongside"),
     "unbold": True},
    {"find": ("On a package of this size the margin at stake is roughly "
              "\u20ac200,000\u2013300,000 (M), and what the redesign buys is "
              "the deadline,"),
     "replace": ("On a package of this size the margin at stake is roughly "
                 "\u20ac1.4\u20132.6 million (S, register arithmetic: the "
                 "D19 flagship value range at the Tier 3 margin), and what "
                 "the redesign buys is the deadline,"),
     "unbold": True},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
