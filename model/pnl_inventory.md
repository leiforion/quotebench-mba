# P&L Workbook Inventory — "QuoteBench P&L Leif.xlsx"

Downloaded 6 Sep 2026 from Drive (uploaded Excel file, not a native Sheet).
Internal title: **"Quomate | Software Business P&L"**. Two tabs, both AED.

## Tab 1 — Assumptions (A1:G40)

| Block | Contents | Hard-coded / formula |
|---|---|---|
| Pricing (per customer, AED/yr) | Small distributor: 120,000 sub + 50,000 setup · Mid: 200,000 + 90,000 · Large group: 320,000 + 140,000 | Hard-coded |
| Churn | 8% of prior active base per year | Hard-coded |
| New customers per year (by tier, Y1–Y5) | Small: 1/4/6/5/5 · Mid: 1/3/6/5/6 · Large: 1/1/2/2/2 · Total: 3/8/14/12/13 | Hard-coded; totals formula |
| Active customers EOY | ROUND(prior × 0.92) + new → totals 3/11/25/35/46 | Formula. Note: ROUND makes churn vanish at small counts (e.g., 1 → 1) |
| Cost of revenue / active customer | AED 32,000/yr — cell note: "AI/API inference, hosting, selection API, support**??**" | Hard-coded, authors' own "??" |
| Onboarding cost / new customer | AED 18,000 — note: "Catalogue load, ERP integration, training**??**" | Hard-coded, "??" |
| One-time MVP build (Y1) | AED 400,000 | Hard-coded |
| Opex (stepped, Y1–Y5, AED) | Founder draw (2): 120k→900k · Eng & product: 180k→1.9M · CS & support: 0→620k · S&M: 60k→780k · Tools: 40k→250k · Legal/admin: 50k→300k | Hard-coded |
| Discount rate | 20% | Hard-coded |

## Tab 2 — P&L (A1:G55) — all lines link to Assumptions

| Line | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Subscription revenue | 640,000 | 2,040,000 | 4,600,000 | 6,520,000 | 8,640,000 |
| Setup revenue | 280,000 | 610,000 | 1,120,000 | 980,000 | 1,070,000 |
| **Total revenue** | 920,000 | 2,650,000 | 5,720,000 | 7,500,000 | 9,710,000 |
| Total cost of revenue | 150,000 | 496,000 | 1,052,000 | 1,336,000 | 1,706,000 |
| **Gross profit (margin)** | 770,000 (84%) | 2,154,000 (81%) | 4,668,000 (82%) | 6,164,000 (82%) | 8,004,000 (82%) |
| Total opex | 450,000 | 1,620,000 | 2,900,000 | 3,880,000 | 4,750,000 |
| MVP build | 400,000 | — | — | — | — |
| **Net profit (pre-tax)** | −80,000 | 534,000 | 1,768,000 | 2,284,000 | 3,254,000 |
| Cumulative | −80,000 | 454,000 | 2,222,000 | 4,506,000 | 7,760,000 |

Key metrics: 5-yr NPV @20% = AED 3,736,490 (≈ **€859,393** at 0.23); Y5 ARR =
AED 8,640,000 (≈ €1,987,200); valuation view at 4/6/8/10× ARR = AED 34.6M–86.4M
(≈ €7.9M–19.9M). Payback: during Year 2.

Model mechanics notes: no tax, no working capital, no cash-flow timing beyond
annual buckets; NPV formula discounts Y1 as end-of-year-1 (build cost not treated
as t=0); churn is cosmetic at Y1–Y2 customer counts due to ROUND.

## New conflicts (extends the C1–C16 ledger in improvements.md)

| # | Conflict | Detail | Resolution path |
|---|---|---|---|
| **C17** | **Business-model frame mismatch — the big one** | The paper's Section 9 outline is a *distributor-internal* investment appraisal (benefits waterfall of savings, hurdle rate, stage-gated pilot for Khoory). The workbook models a *SaaS vendor* (Quomate) selling subscriptions to many distributors, with founder draws and an ARR-multiple valuation. Two different investment cases with different NPVs, different risks, different Monte Carlo drivers | **Resolved (D7, 6 Sep):** the software is Khoory's own ("Khoory's QuoteBench"); Section 9 = internal case; this workbook becomes the 10.3 licensing-option illustration. Phase 4 builds the internal driver model for Section 9 and the Monte Carlo |
| C18 | Currency | Workbook entirely AED; decision D1 mandates EUR at 0.23 | Convert workbook (or its successor model) on the same rate as the paper |
| C19 | Build cost | Workbook MVP = AED 400k (≈ €92k); paper 9.4 wants vendor-referenced build estimates with a +30% overrun scenario and describes a substantial custom build (extraction, product DB, engines, workspace). No source or reconciliation for 400k | Source the estimate per 9.4's own standard; align the MC build-cost distribution around it |
| C20 | Product naming | Workbook title "Quomate"; file name "QuoteBench"; the paper names no product | **Resolved (D7):** "Khoory's QuoteBench" — introduce the name once in Section 7 and use it thereafter; "Quomate" is retired |
| C21 | Monte Carlo driver mismatch | Paper 9.5 names three uncertain inputs: automation rate (8.1), win-rate uplift (9.3), build cost (9.4). None of these are drivers in the workbook, whose uncertainties are customer adds, churn, pricing, and unit costs | Depends on C17. If Section 9 is the internal case, a new driver-level model is needed (the workbook doesn't contain one); if venture case, the MC samples the workbook's drivers and the paper's three inputs enter via willingness-to-pay/adoption logic |
| C22 | Discount/hurdle rate | Workbook uses 20% with no justification; paper 9.5 requires "discount rate justified" and a named hurdle rate; paper 1.3 references clearing "the hurdle rate" | Write the justification (venture-stage 20% is defensible for a SaaS case; a distributor internal case would use Khoory's WACC + risk premium — again hinges on C17) |
| C23 | Margin conflation risk | Workbook gross margin ~82%; paper Table 4.2 gross margins 14–21% (distributor product margins). Different entities — never compare or cite together without labels | Style rule for Section 9/10 drafting |
| C24 | Unvalidated unit costs | The two cost-of-revenue drivers carry the authors' own "??" notes (32k/customer, 18k/onboarding) | Source or bound them before the MC; they set gross margin |

## What the Monte Carlo will need (preview, given C17 outcome)

- **Internal case (paper as drafted):** rebuild from `assumptions.csv` — benefits
  waterfall drivers (touch-hour reduction × loaded rate, error-cost elimination,
  discount-leakage recovery, win-rate uplift × margin, capacity value) vs. build/run
  costs. Distributions: automation rate (8.1 audit), win-rate uplift (floored 0),
  build cost (C19 ± overrun).
- **Venture case (workbook):** distributions over new-customer adds by tier, churn,
  realized pricing, cost-of-revenue per customer, MVP cost; output NPV / ARR / EV
  percentiles. Note the two cases share the automation-rate uncertainty — it drives
  the product's value proposition in both.
