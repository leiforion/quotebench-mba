# Digital Transformation of the RFQ Process in Commercial Pump Distribution: INSEAD EMBA Final Project

# **Section 1: Executive Summary**

Khoory’s Abu Dhabi estimation office turned 640 pump RFQs into quotations in 2025 at measured median cycle times of 18, 39 and 88 working hours by complexity tier. Only 2.1 to 11.4 of those hours are engineering work. The rest is queueing. Between 6 and 19 percent of quotations carry at least one defect, and the function leaks about twenty-five times its €33,000 running cost, mostly to unmanaged discounting. We propose QuoteBench, an automated quoting system: a document-extraction and pricing layer that drafts every quote and routes each by confidence, so engineers review rather than retype and judgement concentrates on the inquiries that need it.

No prototype exists. Capability inputs come from published document-AI benchmarks, fed through a process simulation that reproduced the 2025 baseline on fifteen checks before projecting anything. In the simulated central case, median cycle time falls to 2, 9 and 56 working hours by tier and engineer touch time roughly halves. Benefits reach about €990,000 a year at full adoption, of which about €210,000 does not depend on winning a single additional order. Five-year NPV runs from €1.4 million (P10) to €4.3 million (P90) across 20,000 Monte Carlo draws, and every draw clears the 15 percent hurdle. No single lever within its tested range sinks the case, even with the win-rate uplift set to zero. QuoteBench also converts the branch’s inquiry flow into structured transaction data that neither manufacturers nor marketplaces hold, the distributor’s defensible position as the channel digitizes.

**We recommend building QuoteBench in strategic phases designed to prevent over-committing.** Spend is released gate by gate as evidence replaces simulation. Phase 1 is a three-month shadow-mode pilot on one inquiry tier costing roughly €30,000 (S), opening with the feasibility audit of 25–30 historical RFQs on Khoory’s own documents, inside a total build budget of €92,000. Every gate carries pre-committed kill criteria set on evidence (live extraction accuracy, engineer override rates, escaped defects), and a breached gate reverts the recommendation to hiring.

# **Section 2: Introduction & Problem Definition**

The RFQ from Innovo Contracting for the Guggenheim Abu Dhabi lands on a Thursday evening at the Abu Dhabi branch of M.A.H.Y. Khoory, a UAE pump distributor: roughly 75 pumps across five applications, from booster sets to chilled water, with the quote due the following Tuesday. Khoory is competing against Grundfos, Xylem, Wilo and Lowara, and against at least one other distributor quoting the same Grundfos range it carries. The job will be won or lost on price and speed of response as much as on brand.

Worked properly, an inquiry this size is close to twenty-eight hours of estimating work, and the branch has two estimators. Line managers bring both in over the weekend on overtime and borrow a third from another desk. It is not enough. The quote goes out two days late, seven calendar days after receipt. Innovo's senior management escalates to Khoory's leadership, and a face-to-face meeting is needed to settle the relationship. Khoory still wins the project, but not on the strength of this quotation. The paper returns to what that near-failure cost and why it keeps happening.

## **2.1 The technical-expertise function: slow, capacity-bound, error-prone**

A distributor exists in this chain because the manufacturer cannot do what the distributor does. Three functions justify the position: technical expertise, credit, and local presence for testing, commissioning and warranty support. Credit and presence are largely fixed costs of being in the market. Technical expertise is the costliest and the one under examination here. Every RFQ means reading consultant specifications, CAD files and drawings, extracting flow, head and efficiency requirements, running head-loss calculations, and working out which model across a manufacturer's full range fits the site. It needs trained estimators, it scales with volume and complexity, and it is what nearly failed under pressure in the Innovo inquiry. The paper asks whether the reading, the calculations and the model selection can be digitized without losing the judgment that makes them valuable.

At Khoory the function shows three symptoms.

**Speed.** A standard inquiry of three to twelve pumps takes an estimator around five and a half hours of concentrated work. The largest inquiries (the Innovo package ran to seventy-five pumps) demand twenty-five to thirty hours and several estimators at once, against deadlines sometimes as tight as two to three days. They arrive roughly once a month but cannot be staffed as if routine. An estimated 15% of tenders are lost specifically to late or rushed quotes (E, sales and management interviews, treated as an upper bound and triangulated in 9.3), concentrated among first-time customers with no relationship to buy patience.

**Cost.** Khoory carries 16 estimators across all branches, each handling roughly 12 RFQs a week. A fully loaded estimator costs the business approximately €22,000 a year, and a qualified replacement takes two to three months to hire and a further three to four to become productive. Estimator capacity is a hard constraint: it directly determines how fast the business can take on new sales and new customers, independent of demand.

**Quality.** Across the 2025 quotation audit, roughly one standard inquiry in nine went out containing at least one defect (a wrong model, a wrong price, or a missed specification requirement), rising to one in five on the largest, most valuable work. Section 4.2 develops the error taxonomy and its cost.

## **2.2 Research questions and scope**

•    **RQ1: **What process architecture could automate the RFQ process while preserving quote quality, and what evidence supports its technical feasibility? (Sections 6 to 8)

•    **RQ2: **What is the projected financial impact of the proposed transformation, and how robust is that projection under uncertainty? (Section 9)

•    **RQ3: **What are the strategic implications for the distributor’s position in the value chain, and what implementation path best manages the risks? (Sections 10 and 11)

**The scope is deliberately narrow.**

**Product.** Pumps only, where the technical selection burden is heaviest. Valves, HVAC and Khoory's other product lines are the natural extension once the system is proven.

**Geography.** The UAE only, where the volume and the pain concentrate today. GCC specifications closely mirror the UAE market, so regional expansion is a near-term step.

**Process.** The technical workflow from RFQ receipt through quote generation. The commercial negotiation between quote and LOI is excluded: the paper automates the distributor's technical-judgment function, not its deal-making.

**Depth.** No software has been built and no pilot run. The paper evaluates the investment before it is made, on a calibrated simulation of the current process, an audited feasibility assessment and a financial projection under uncertainty (Sections 6–9). A live pilot is recommended in Section 11 and has not been conducted.

# Section 3: Methodology

## 3.1 Research design and evidence base

Nothing in this paper has been built yet. The study is an ex-ante evaluation: we assess the proposed transformation the way a board assesses any capital request. Measure the current process, design the alternative from proven components, model what it would do, and stress the assumptions until they hold or break.

Four components carry the evaluation: a **measured baseline** of the current quoting process (Section 4); a **design** assembled from components whose behaviour is already documented (Section 7); a **simulation of the future state**, covering cycle time, capacity and the investment case as ranges (Sections 8 and 9); and **validation** by the estimators and contractors, who challenge the design's assumptions (8.2, 4.4).

One scoping point matters for every number downstream. We measured a single branch, the Abu Dhabi estimation office, whose 640 pump RFQs in 2025 are the study population. Every figure in the paper, including the Section 9 investment case, is single-branch, and no company-wide scaling is used. We measured one branch deeply because the Section 8 simulation needs step-level timings that only direct observation can supply.

Every quantitative claim in the paper carries one of three tags. **Measured** means read from records or timestamped observation. **Estimated** means derived from sampled data or structured interviews. **Simulated** means an output of the process or financial model, traceable to a named assumption in Appendix A.

Seven sources of evidence carry the paper and no other data enters the analysis: the 2025 RFQ log, three weeks of direct observation, the 120-quotation defect audit, internal and contractor interviews, the planned feasibility audit and the simulation models. Table 3.1 (Appendix K) itemizes what each supplies and where it does its work. All monetary figures are stated in euros, converted from the dirham-denominated records at AED 1 = €0.23.

## 3.2 Simulation method and its limits

Two models do the projective work, under one rule: a model earns the right to project a future only by first reproducing the past we measured.

**The process model** replays the branch operation of Exhibit 4.1: arrivals by tier at 2025 rates, touch times from the observed step distributions, estimator capacity as the constraint, and large inquiries as pre-emption, which is what the Innovo case shows happens. It is a discrete-event simulation built for this study. The full code, parameters, seeds and run manifests are public at [repository URL] (Appendix F), so every simulated number in this paper can be reproduced to the digit. The model must reproduce the measured baseline before any to-be scenario is run (8.2). To-be scenarios then run across the capability ranges of 8.1 and report cycle time, utilization and capacity as distributions.

**The financial model** converts those projections into five-year NPV by Monte Carlo, because the inputs arrive as ranges. Three dominate and are drawn as distributions: the extraction capability, spanning the published ranges mapped in 8.1; the win-rate uplift from faster quoting, triangulated in 9.1 and floored at zero in the conservative case; and the build cost (9.2). Results are reported at P10, P50 and P90: one outcome in ten falls below the P10 value, half below the P50, and nine in ten below the P90. Input distributions are documented in Appendix C and named in the Appendix A register.

Both models follow established practice: discrete-event models of service operations are standard instruments of operations analysis (Law, 2015; Robinson, 2014), and Monte Carlo analysis of capital investments has been orthodox since Hertz (1964).

Three limits of method are stated here and treated fully in Section 12: the baseline is one branch of one distributor over one year, with 22 deeply observed inquiries; the future state is simulated and audited, not observed, which is what the Section 11 pilot exists to fix; and the demand-side evidence on what speed is worth rests on history and stated preferences, which is why the financial model floors that benefit at zero.

# Section 4: Current State Analysis

Three sources anchor this section: the 2025 inquiry log (640 pump RFQs, M); three weeks of direct observation in which we timestamped 22 inquiries from arrival to quotation (M); and the finance ledger of credit notes and rework traceable to quotation defects (M). Figures that could not be read directly from records were estimated from sampled data or structured interviews and are tagged (E).

An inquiry arrives as an email carrying some combination of a specification extract, a pump schedule (often a scanned image), a riser diagram, and occasionally a CAD file. From there it passes through nine steps and five roles before a quotation goes back out. Exhibit 4.1 maps the path, annotating each step with touch time and queue time.[IMAGE]

*Exhibit 4.1. Median values across the 22 observed inquiries (M). The clarification and management approval loops occur on a subset of inquiries. Their queue times are medians within that subset.*

The exhibit carries the section's central finding: the median case consumed 5.5 hours of work spread over 39 working hours of elapsed time (M). Six hours out of every seven, nobody was working on the inquiry at all: it was waiting to be assigned, waiting in an estimator's personal queue, waiting on the contractor's answer, waiting for a discount approval. The work is not slow. The waiting is.

Three steps account for most of the queueing: assignment (a median 14 working hours before an estimator picks the inquiry up), the clarification loop (a median 41 working hours for the contractor's answer, during which the process cannot move), and pricing approval. Each is a handover between people, and each handover is a queue. The cost side is simpler: at a fully loaded €12 per hour (E, payroll records), the median inquiry carries about €66 of direct cost, developed by tier in Table 4.2.

## 4.1 Segmentation and baseline performance

A single replacement circulator and a three-building museum package have nothing in common except the mailbox they arrive in, so we classified every 2025 inquiry retrospectively into three tiers by pump count, data completeness at receipt, and project value. Two staff members classified independently, agreeing on 91% of inquiries (E). The taxonomy carries through the paper: Section 7 routes by it, Section 8 samples by it, and Section 9 builds its benefits by it.

The full criteria and 2025 mix are Table 4.1 (Appendix K). The inversion in that mix is what matters: Tier 3 supplies one inquiry in eight but nearly half the quoted value, so the commercially decisive inquiries are exactly where the process is slowest, the documents messiest, and the expertise thinnest. A redesign that only worked for simple inquiries would automate the 12% of value that least needs help.

Table 4.2 consolidates the baseline. Every subsequent claim of improvement in this paper is a claim against one of these cells.

| **Metric** | **Tier 1** | **Tier 2** | **Tier 3** | **Tag** |
|---|---|---|---|---|
| Inquiries per month | 29 | 18 | 6 | M |
| Median cycle time (working hours) | 18 | 39 | 88 | M |
| P90 cycle time (working hours) | 34 | 71 | 162 | M |
| Touch time per inquiry (hours) | 2.1 | 5.5 | 11.4 | M |
| Direct cost per quote (€) | 25 | 66 | 137 | E |
| Inquiries with ≥1 defect | 6% | 11% | 19% | E |
| Win rate | 34% | 27% | 22% | M |
| Gross margin on won quotes | 18.5% | 22.5% | 27.8% | E |

*Table 4.2. Baseline metrics by tier, 2025. Tag: M means measured from records or timestamped observation, E means estimated from sampled data or interviews (3.1). Cost per quote combines touch hours at loaded rates with a per-inquiry licence allocation. Defect rates were estimated by auditing a stratified sample of 120 quotations against source documents. Gross margins restate the measured tier pattern to the branch’s stated 24 percent average on revenue.*

## 4.2 Error taxonomy and the cost of poor quality

The audit of 120 sampled quotations, cross-checked against the credit-note ledger, surfaced four distinct classes of error. The full taxonomy with frequencies and unit costs is Table 4.3 (Appendix K). Extraction errors are the most frequent (41% of defects, on 9% of inquiries), selection errors the most expensive (about €11,300 each), and calculation errors carry the site-failure tail beyond €35,000 (E). Discovery timing drives cost far more than the mistake itself: an extraction error caught at internal review costs an hour of rework, while the same error caught at commissioning costs a return shipment, a site visit, and a measure of trust.

Summed across the year, the traceable cost of the four classes comes to roughly €177,000, about 0.5% of revenue (E). Unit costs are restated at the branch's actual 2025 order values, since a defect on a larger order costs proportionally more. The chain matters as much as the total: nearly every calculation and selection error began life as an extraction problem, so attacking the point of entry starves much of the downstream taxonomy.

The larger leak never appears in an error report, because each instance looks like a reasonable commercial decision. Discounts are set case by case with no reference point in front of the pricer: matched 2025 quotations show discounts on comparable Tier 2 work ranging from 4% to 18% (M), not because the jobs differed but because the days did. Against the median like-for-like discount, the foregone margin is roughly 1.9% of revenue annually (E, about €673,000), nearly four times all four error classes combined, and invisible precisely because no single decision was wrong. Together, quality cost and discount leakage run to about 2.5% of revenue, roughly €850,000 a year, the figure the pricing engine of Section 7.2 is designed against.

## 4.3 The Innovo inquiry: Guggenheim Abu Dhabi, as-is

The numbers above describe the process in aggregate. The Innovo inquiry that opened this paper shows what they feel like from inside. By the criteria of 4.1 it was a large Tier 3 inquiry: a specification extract running to dozens of pages, schedules scanned as images, and riser diagrams across several buildings. Table 4.4 (Appendix K) reconstructs its path from the mailbox records and the estimators' logs: unread overnight, first touched late Friday, the consolidated clarification not sent until Saturday afternoon, the contractor's reply then sitting unread in the same shared mailbox.

Seven calendar days from receipt to quotation, and twenty-eight hours of work across three estimators and a weekend of overtime, well above the Tier 3 median of Table 4.2. The process could not absorb a job this size inside the deadline, however many people were thrown at it.

It also nearly went wrong, twice. A static head read from the wrong drawing would have undersized the booster set for the taller building. It was caught only because an odd duty point prompted a second look. The contractor's reply also sat unread for a stretch, because nothing in the process flags a waiting inquiry when its answer arrives. The quotation was late, and it nearly went out wrong, on a marquee project.

## 4.4 Root causes and the customer's view

Compressing the evidence of this section yields four root causes, shown as a driver tree in Exhibit 4.3 (Appendix B). Each demands a different remedy, and a design that fixes three while ignoring the fourth forfeits much of the gain.

**Unstructured inputs. **Every technical fact the process needs arrives locked inside a PDF, a scan, or a sentence in an email, and is released only by an estimator reading and re-keying it. This is where 1.5 hours of every Tier 2 inquiry goes, and where 41% of defects begin. The Innovo near-miss was this cause in miniature.

**The serial expert bottleneck. **One estimator owns an inquiry end to end, so work waits for a person rather than a task, and the scarcest expertise, held by two people for chilled water, sets the pace for the most valuable inquiries. The 86–88% queue share in Exhibit 4.2 (Appendix B) is the signature of serial ownership.

**Clarification ping-pong. **Gaps in the data are discovered mid-process, one at a time, each triggering a round trip to the contractor at a median cost of 41 working hours. Nothing alerts anyone when the answer lands. Thirty-eight percent of inquiries need at least one loop (M), and complex inquiries often need two.

**No pricing discipline. **Discounts are set without reference points, producing a 4–18% spread on comparable work and the largest single leak in the system. Unlike the other three causes, this one costs nothing in time, only money, quietly, on jobs that were won.

These four causes are the requirements specification for everything that follows. The intake and extraction layer of Section 7 exists because of the first; confidence-based routing and parallel task design because of the second; automated completeness checks and clarification tracking because of the third; and the rules-based pricing engine because of the fourth. The measured current state is the design brief.

The customer's view supports the diagnosis. Contractor interviews are in progress (protocol in Appendix D): four to six structured conversations covering what drives supplier choice, how speed weighs against price, and each contractor's stated reaction to an automated quote. Preliminary conversations point to response speed and error-free technical submittals as decisive selection factors (E, provisional). Verbatim quotations will be incorporated once transcripts are complete. Stated preferences are the paper's only demand-side evidence, and 9.3 treats them as an upper bound to be triangulated.

# Section 5: Literature & Industry Context

## 5.1 Disintermediation: the case for moving first

Whether digitizing a distributor's core function hastens the distributor's own removal is an old question with a settled shape. Early electronic-commerce research predicted disintermediation: online markets cut transaction costs and let manufacturers deal directly with buyers (Benjamin & Wigand, 1995). Sarkar et al. (1995) countered that intermediaries do more than pass product, and Chircu and Kauffman (2000) reconciled the two as a cycle of intermediation, disintermediation and reintermediation: displaced incumbents re-enter by absorbing the technology into the functions that made them valuable, provided they move before a substitute occupies the position. Wholesale distribution has since consolidated and digitized rather than disappeared (Mudambi & Aggarwal, 2003).

The framing does real work for this paper: it turns automating technical expertise from an efficiency question into the strategic one Section 10 resolves, whether the distributor becomes the platform of record for its market or writes the manual for its own replacement. The literature's answer is conditional on sequence, and sequence is a choice.

## 5.2 What the technology evidence does and does not support

Three streams of prior work set the boundaries of the design.

Configure-price-quote systems automate quoting reliably where a product can be described by enumerable options and compatibility rules (Forza & Salvador, 2002, 2007), but they assume structured inputs. Engineered-to-order environments violate that assumption at both ends: requirements arrive as drawings and specifications, and the mapping to product runs through engineering calculation (Hicks et al., 2000). The make-to-order literature also treats the inquiry stage itself as a competitive arena: Kingsman et al. (1996) model the probability of winning an order as a function of the price and lead time quoted, the coupling Section 9 prices. Section 6 accordingly treats CPQ as a component for pricing discipline and quote assembly, and the unstructured front door as the problem this design must solve.

Machine reading of business documents supplies the capability priors that 8.1 maps onto the distributor's own document mix. The strongest pipelines now answer well above 90% of items on the principal document-QA benchmarks (Jaume et al., 2019; Kim et al., 2022; Mathew et al., 2021; Xu et al., 2020). Enterprise evaluations are less flattering: accuracy degrades sharply as schemas widen and documents lengthen, with models producing validly structured output whose values are wrong, and the distributor's documents sit at the hard end of that spectrum. One piece of arithmetic reframes even the optimistic figures: at 95% per field, a twelve-field schema is fully correct only about 54% of the time (0.95¹²). That arithmetic is why the Section 7 design carries per-field confidence scores, validation gates and human review as structural features, and why the 8.1 audit exists.

Partial automation also changes the human. Operators over-rely on automation that is usually right and abandon automation that has embarrassed them (Parasuraman & Riley, 1997). Automation bias produces measurable errors even among trained professionals (Goddard et al., 2012), and strengthens when the human feels less accountable for the outcome (Skitka et al., 1999). The design response is to set the level of automation per function, deliberately (Parasuraman, Sheridan and Wickens, 2000). The routing of 7.2 applies these findings directly: confidence is displayed so trust has something to calibrate against, uncertain fields arrive flagged, release is an explicit act with a name attached, and the automation level is set per tier and per function. A reviewer who approves ninety-nine good drafts is primed to approve the hundredth, and the value-gated release rules and override logging of 7.2 are the design's admission of it.

# **Section 6: Solution Options & Design Choice**

## **6.1 The option set**

Five options span the realistic range, from adding headcount to building everything. Each is described on its own terms and scored in 6.2. Two of the rejected options survive inside the proposed design as components.

**Option A: hire more estimators.** The baseline competitor is not technology at all: keep the process of Section 4 and add one or two estimators as volume grows. Its virtues are real: lowest cost, fastest to value, no implementation risk, no change management. Its limits are the arithmetic of 2.1: capacity arrives in permanent, indivisible steps, and cycle time, error rates and the discount spread stay where Section 4 measured them, because the process itself is unchanged.

**Option B: manufacturer selection tools.** Grundfos, Wilo, KSB and Xylem all publish selection software: the estimator enters a computed duty point and picks from the returned range. The branch already works this way, so the gains are banked in the Section 4 baseline: the tools remove roughly 20 to 30 percent of manual effort at the selection step (E, estimator interviews). They cannot reach intake, extraction, calculation or clarification, where the delay and most of the defects live, and each tool ranks only its publisher's range.

**Option C: off-the-shelf CPQ.** Configure-price-quote software automates the commercial tail: line-item assembly, pricing rules, discount approvals, document generation. As 5.2 established, the category assumes structured inputs and solves the wrong end of this problem: it addresses only around 10 to 15 percent of the touch time measured in Section 4 (E), at enterprise licence prices. It is rejected as an alternative and retained as a component: its pricing discipline reappears as the rules-based engine of 7.2.

**Option D: full custom AI platform.** Building everything in-house (bespoke extraction models, proprietary hydraulic and selection engines, CAD interpretation from day one) carries the highest capability ceiling and the highest exposure. It duplicates assets the manufacturers already maintain (curve data, selection logic), requires specialist engineering talent the business does not employ, and stakes the schedule on the hardest problems first, against the 5.2 evidence that extraction degrades exactly where this design would need it most. Nothing in the baseline requires the ceiling, and everything in Section 9 punishes the cost.

**Option E: the proposed hybrid.** QuoteBench assembles proven components under Khoory's own orchestration: foundation-model extraction bought as a commodity, a deterministic in-house calculation engine, the Option B selection APIs repurposed as services, the Option C pricing discipline rebuilt as rules on Khoory's own data, and confidence-routed human review over all of it (Section 7). Nothing unproven is invented: the claim is in the assembly and the routing. It is the only option that attacks all four root causes of 4.4 at once, and the only one that accumulates a compounding asset while it works: the transaction data of Section 10.

## **6.2 The decision matrix and where hiring wins**

Table 6.1 (Appendix K) scores the five options against the six criteria the investment decision turns on, from 1 (worst) to 5 (best). The criteria are not equally weighted, and the scores are argued rather than averaged.

Option A wins where a conservative reader looks first: it is the cheapest and the least likely to fail, and the matrix says so. What it cannot do is move cycle time, error rate or the discount spread. D and E dominate the impact criteria and separate on cost and risk: D pays a premium to rebuild what can be bought or borrowed, while E's buy-partner-build sourcing (Table 7.1, Appendix K) confines custom work to thin, auditable layers. B and C score as what they are: useful components mistaken for solutions when deployed alone. The decision therefore reduces to A versus E: certainty and linearity against operational transformation carrying genuine implementation risk. Section 9 prices that trade, and the closing paragraph states the conditions under which A wins it.

The rejected options do some things better. Option A is faster to first value than anything proposed here (an estimator hired in March is quoting by summer), and hiring is reversible in a way build spend is not. On touch time alone, hiring even wins the arithmetic: the average inquiry carries about 4.3 touch hours (M, Table 4.2), roughly €52 of labour, so the labour the automation could redeploy (about €17,000 a year) does not cover the amortized build (€92,000) and running costs (9.2). What decides the comparison is what hiring cannot buy at any volume: the roughly €850,000 annual leak of 4.2 sits in error content and discount variance, and adding hands to an unchanged process recovers none of it (9.2). The commitment is conditional in both directions: if the 8.1 audit returns automation rates materially below its central range, or the pilot of 11.1 breaches its kill criteria, Option A is not this paper's fallback but its recommendation.

# Section 7: Proposed To-Be Process & Solution Architecture

Everything in this section is a proposal: to-be times and behaviours are projections, each traceable to a named assumption in the Appendix A register, while figures carried over from Section 4 remain measured. Exhibits 7.1–7.3 are in Appendix B; the RFQ schema table is in Appendix G.

## 7.1 Five constraints and the projected process

QuoteBench is governed by five constraints. **Automate the mechanical, augment the judgement:** the system takes over the reading, transcription and arithmetic where Section 4.2 located 41% of defects, and presents the judgement calls to a person.

**Nothing ships unreviewed below confidence:** no quote leaves below defined confidence without human review, and in Phase 1 the gate is absolute.

**Every automated decision is auditable:** each extracted field, calculation input, ranked option and price is logged with source, confidence and timestamp, feeding the liability analysis of 11.2.

**Fail back to the manual process:** on any failure, the inquiry drops into the Section 4 manual process with partial work attached.

**Every correction is training data:** every human correction is captured as labelled data, the constraint that turns review burden into the flywheel of 7.2.

Exhibit 7.1 (Appendix B) mirrors the as-is map lane for lane, with one addition: a System lane into which six of the nine steps migrate, running in minutes. The queues are not compressed but removed: a runtime has no inbox. What remains of elapsed time is one internal queue (the engineer's next free review slot, a projected 2.5-hour median) and one external wait (the contractor's reply, carried over unchanged from measurement). A projected Tier 2 inquiry would need roughly 25 minutes of human attention against the measured 5.5 hours, the difference redeployed (9.1, 11.2). The design would be admitted in stages, each earning the next through a pre-defined gate. Thresholds are stated as symbols because they are parameters the pilot exists to determine, and the roadmap with kill criteria is the subject of 11.1.

## 7.2 The architecture: from intake to engineer release

Within minutes of arrival the intake layer classifies the inquiry into the 4.1 taxonomy and validates completeness against the extraction schema, so every gap is known while the inquiry is minutes old. Missing fields trigger one consolidated clarification covering every gap at once, where the as-is process finds gaps serially at a median 41-hour round trip each. When the reply arrives, the layer recognises the thread, merges it and resumes, closing the gap that left Innovo's answer sitting unread in a mailbox.

Extraction converts the documents into one canonical record, the twelve-field-per-system RFQ schema of Appendix G, using language and vision models. Each field carries a confidence score, and the scores, not the values, drive the routing below. Native CAD parsing is out of scope for Phase 1: where required fields exist only in a DWG file, the inquiry routes to an engineer with every extractable field pre-filled and the CAD-dependent fields flagged, and the 8.1 audit measures how often that occurs.

The system's knowledge of pumps does not live inside a language model: models recall approximately, catalogues change monthly, and a quotation defensible under the audit constraint must rest on data that is exact, versioned and sourced. Models read documents and orchestrate. A governed product database remembers: manufacturer data in a typed hierarchy, hydraulic performance as curve data, prices and lead times versioned with effective dates. Any response naming a model must carry the database key and data version it drew from, which keeps a quote reconstructible months later. The full specification of this layer is Appendix J.

Between a validated schema and a draft quote sit three engines, kept separate because they carry different uncertainty. **The hydraulic engine is deterministic physics, not AI**: Darcy-Weisbach cross-checked by Hazen-Williams, the same formulas the estimators apply by hand, encoded once, so the design's uncertainty lives upstream in extraction. **The selection engine is a constrained search**: given a duty point it filters the product store, queries the manufacturer's selection API, and returns candidates ranked on efficiency, price and lead time, flagging duty points near a curve edge. Where several answers are defensible, Khoory's own history of winning selections breaks the tie. **The pricing engine is rules, not learning**: cost-plus by family with a defined discount band and a reference price beside every discount decision, aimed at the 4–18% spread and the 1.9%-of-revenue leak of 4.2. Machine-learned price optimisation is deferred to Phase 3.

The preceding layers describe what the machine would do. The routing decides what it is allowed to do:

IF   min. field confidence ≥ C₁ AND tier = 1 AND value < €V₁ AND discount in band

THEN auto-draft quote → engineer one-click release

ELIF tier ≤ 2 AND min. field confidence ≥ C₂

THEN engineer workspace: pre-filled schema, flagged uncertainties, ranked options

ELSE full engineer workspace + senior review (Tier 3, CAD-dependent, low confidence)

The thresholds C₁, C₂ and V₁ are design parameters. Setting them is the work of the pilot in 11.1. Under this routing the estimator moves upward, to exception-handler and advisor, owning the flagged uncertainties and the Tier 3 work that needs judgement (11.2). Constraint five powers the correction flywheel of Exhibit 7.3 (Appendix B): corrections become labelled data, accuracy rises, routing admits more inquiries to the assisted paths, and freed capacity concentrates where margin is highest. Error containment closes the loop: value-gated release regardless of confidence, escalation for out-of-band discounts, an immutable audit log, and a single switch back to manual. Whose signature a quote carries is taken up in 11.2.

Exhibit 7.2 (Appendix B) shows the layers assembled, and Table 7.1 (Appendix K) states the sourcing per component: buy the probabilistic commodity, partner for domain logic the manufacturer maintains, build only the thin layers that encode Khoory's process and data, which is where defensibility lives.

## 7.3 The Innovo inquiry, to-be: a simulated walk-through

What follows is a simulated scenario: the inquiry of Section 4.3 processed under the proposed design, with step times drawn from the Section 8 assumptions. Nothing in it has happened.

Thursday, 16:40: the email lands and intake opens it within the minute: classified, valued, in band. By 16:52 extraction has populated the schema and validation has found the same gaps a human found on day two, with the riser ambiguity flagged as an explicit conflict. At 16:53 a single consolidated clarification is on its way, thirteen minutes after receipt instead of 22 working hours. The contractor's reply, the one interval no redesign controls, is carried at its measured pace: seen Friday, answered Monday morning. Within minutes of the reply the system has merged the thread, re-validated, and run the calculations and selection queries. It now holds a draft quote: models ranked, the booster duty point flagged near its curve edge, prices in band. At 14:00 Monday, the estimator's first free slot, the review turns on the flagged selections. The senior's confirmation is two lines, one alternate is added, the discount stays in band. At 15:10 Monday the quote would go out with the estimator's name on it (11.2), a day ahead of the deadline instead of two days late. Twenty-eight hours of manual construction would become the review of a 75-pump draft (S), and Section 9.3 prices the difference. Neither near-miss of 4.3 would arise to be caught. These times are model outputs. The numbers they are compared with were measured, and closing that asymmetry is Section 8's job.

# Section 8: Feasibility & Simulation Evidence

## **8.1 Capability evidence from published benchmarks**

No system has been built, so nothing in this section is a measurement of a live tool. Every capability figure is a simulation input, tagged S and registered in Appendix A. What we could ground, we did. The mix of document quality that arrives at the desk (clean digital PDFs, scanned schedules, email fragments, CAD-dependent inquiries) is estimated by tier from the 640-inquiry log and the 22 inquiries we observed end to end. The extraction performance the design could plausibly achieve on each document class is taken from the published benchmark ranges reviewed in 5.2 and carried as three variants: pessimistic, central, optimistic. Engineer skill and inquiry complexity spread those figures further, drawn inquiry by inquiry, so no single accuracy number is load-bearing.

We designed a field-by-field feasibility audit of 25–30 historical RFQs to replace these ranges with evidence from Khoory's own documents. Its materials are drafted (Appendix E), but it needs estimator time we could not commission for this paper. It is scheduled as the first activity of the Phase 1 pilot (11.1), and until it runs the capability inputs stay on the published ranges. If Khoory's documents score materially below the pessimistic bound, Section 9 weakens, and the pilot's first gate is built to catch it.

## **8.2 Simulation: calibration, projection, validation**

The simulator described in 3.2 replays the branch one inquiry at a time. Before it may project anything, it must reproduce the 2025 baseline it was built from: median and P90 cycle times by tier, touch hours, cost per quote, annual volume, queue share of elapsed time and estimator utilization, fifteen checks in all, each within ten percent of the measured value. The current build passes all fifteen (Exhibit F.1, Appendix F). The gate is enforced in code, and every to-be number in this paper is locked behind it.

Calibrating taught us three things about the office that no interview surfaced: the estimators work small jobs first, which is why Tier 1 waits stay short at 68 percent utilization; assignment delay is queueing, not procedure; and clarification waiting overlaps other queues rather than adding to them. Each finding changed the model before it passed.

With the baseline earned, the Section 7 design runs under the 8.1 capability ranges. In the central case, median cycle time falls from 18 to about 2 working hours for Tier 1, from 39 to 9 for Tier 2 and from 88 to 56 for Tier 3, with P90s falling in step (Exhibit 8.1, Appendix F). Median engineer touch drops from 2.1 to 0.8 hours, 5.5 to 2.7 and 11.4 to 6.2 by tier (S). The manufacturer special-quote round trip on complex work, like the contractor reply, is outside the design's control and carried at its measured pace. Routing stays cautious: 15 percent of Tier 1 inquiries release as auto-drafts and a quarter go out assisted, Tier 2 is one-fifth assisted, and every Tier 3 quote stays with an engineer. Engineering hours on quoting fall from about 2,780 to about 1,380 a year at unchanged volume, and the stress runs of 9.3 show the same two estimators absorbing a 40 percent demand surge that breaks the as-is desk. Escaped defects hold at parity with the baseline (a simulated 9.2 percent of inquiries against the measured 9.1 percent), which is a design constraint: reviewer attention drops on machine-drafted work, and the routing thresholds are set so the two effects cancel.

The degradation requirement of 7.1 also holds: with extraction forced to zero, the model reproduces the as-is baseline, so a failed capability assumption returns the office to today's process rather than to something worse.

Validation by the people involved is partly done and partly scheduled. The estimators challenged the swimlane, the tier taxonomy and the error audit during measurement, and two of their corrections became the calibration facts above. The contractor interviews (protocol in Appendix D) and a structured review of the Section 7 architecture are in progress. The routing thresholds they challenge are the same parameters the pilot re-measures.

What the evidence supports: the measured baseline and its costs (Section 4); the calibrated capacity arithmetic above; and roughly €210,000 a year of simulated benefit that does not depend on winning a single additional order (the labour, error and discounting effects of 9.1). What remains unproven: extraction accuracy on Khoory's own documents; contractor acceptance of faster, system-assembled quotes; engineer adoption of the review workspace; and above all the win-rate response to speed, which 9.2 shows carries the investment case. Each unproven item maps to a Phase 1 pilot measurement with a go/no-go gate in 11.1, and the floor case in 9.2 states what happens if the pilot returns the pessimistic answer.

# **Section 9: Projected Financial Analysis**

## **9.1 Baseline economics and the benefits waterfall**

The quoting function is cheap to run and expensive to get wrong. Direct quoting cost is about €33,000 a year: 636 inquiries a year (the Table 4.2 monthly volumes annualized, against 640 in the log) at €25, €66 and €137 per quote by tier (E), absorbing about 2,780 engineer hours. The revenue those hours carry is a stated management figure: the branch's 2025 pump-only revenue was approximately AED 150 million, €34.5 million at the paper's conversion (M). Working backwards through the measured win rates, winning that much implies roughly €136 million of value quoted each year (S), including two flagship-scale projects. The leakage dwarfs the labour: quality failures cost about 0.5 percent of revenue (E, €177,000 at the restated unit costs) and unmanaged discounting another 1.9 percent (E, €673,000), so the office leaks about twenty-five times what it costs to operate.

Exhibit 9.1 shows the projected annual benefit at full adoption, central case, as four bars that do not overlap by construction: each is computed on its own base.

Engineering capacity, €17,000 a year (S): about 1,400 hours valued at the loaded rate, not at revenue. The assumption is redeployment: the hours move to Tier 3 work, declined inquiries and the clarification chase (11.2).

Error cost, €20,000 a year (S): escaped-defect cost on won orders at the restated unit costs, with overall defect rates held at parity (8.2). The saving comes from the mix shifting away from expensive selection errors.

Discounting discipline, €174,000 a year (S): at the actual revenue base this is the anchor benefit, larger than labour and errors together by a factor of five. Quoting inside a reference band recovers part of the measured 4–18 percent spread on comparable work (M); we count only the 40–90 percent of that recovery that pricing governance is assumed to enforce.

Win-rate uplift, €779,000 a year (S): the dominant bar and the least proven, defended below.

[IMAGE]

**Exhibit 9.1.** Projected annual benefits at full adoption, central case (S).

The central total is about €990,000 a year at full adoption, reached on the 11.1 ramp. A fifth benefit is possible but unevidenced: if capacity constraints suppress intake today, the recovered volume is upside the pilot can log. It enters no number in this paper.

The speed-win elasticity is the single most attackable assumption, so it is triangulated and then floored. Internal evidence: sales attribute about 15 percent of lost tenders to late or rushed quotes (E), an upper bound on what speed can recover. Customer evidence: the contractor interviews of 4.4 (in progress, protocol in Appendix D) ask directly how speed weighs against price, and the model takes no credit for anything they have not yet said. Industry evidence: the make-to-order bidding literature reviewed in 5.2 models win probability as a function of price and quoted lead time (Kingsman et al., 1996), supporting a positive but modest effect. The model carries the uplift as a range from zero to five percentage points of win rate with a central value of two (S). Five points on a 27 percent Tier 2 base is an 18 percent relative gain, inside the ceiling the lost-tender estimate implies. The floor case of 9.2 sets it to zero outright.

## **9.2 Costs and investment appraisal**

Costs enter the model as ranges. Build: €92,000, priced as one internal software-engineer year. We have no build experience of our own, so this is an analogy price rather than a vendor quotation, and the Monte Carlo carries an overrun tail to +30 percent, with 9.3 stressing to +60. Run: €45,000–65,000 a year: platform maintenance and upkeep at about €40,000 (E, management estimate: the €92,000 engineer-year is the build alone), plus inference and API usage at projected volume and licences. The usage component is provisional, and vendor quotations replace it before any build decision. Change: €10,000–30,000 once, for training and the transition productivity dip. Every range is drawn as a distribution below, and the boundaries in 9.3 state how far any of them may grow before the case dies.

The financial model runs 20,000 Monte Carlo draws over the ranges established above: extraction capability across the 8.1 variants, the win-rate uplift of 9.1 and the cost ranges above, with benefits anchored to the calibrated process model of 8.2 and phased in on the 11.1 adoption ramp. We discount at 12 percent as a WACC proxy and test approval against a 15 percent hurdle. Five-year NPV comes out at €1.4 million at P10, €2.7 million at P50 and €4.3 million at P90. Every one of the 20,000 draws clears the hurdle, and median payback is about four months (S; Exhibit 9.2, Appendix F). At this scale the internal rate of return stops being informative (the median exceeds 300 percent against a €92,000 build). The number that matters is the floor.

The floor case matters most. Set extraction to the pessimistic bound, the win uplift to zero and the build 30 percent over, and benefits still run about €180,000 a year: NPV is €226,000 at 12 percent and €197,000 at the hurdle. The project clears on cost, error and discounting alone. That reverses the burden the case carries: the question is no longer whether the economics survive a disappointing pilot, but whether the capability assumptions under them survive contact with Khoory's own documents. Every input above the measured baseline is simulated, and a result this one-sided argues for testing the inputs. Phase 1 measures exactly that: live extraction accuracy and the win-rate response (11.1).

## **9.3 Sensitivity and unit economics**

Exhibit 9.3 (Appendix F) ranks the levers one at a time. The win uplift dominates: its zero-to-five-point range moves NPV by €5.3 million, thirteen times the next lever (pricing adoption, €0.4 million), with extraction capability close behind and run cost, build overrun and change cost together barely visible. The same stress runs return a finding a marginal case could not: within every tested range, no single lever kills the case at the hurdle. The uplift at zero still clears (€0.33 million at the hurdle), the build at six times plan still clears, run costs at €200,000 a year still clear, and demand at one-fifth of the 2025 rate still clears. In the other direction, the 40 percent demand surge that breaks the as-is desk raises annual benefits to about €1.2 million (S). The pilot's kill criteria are evidential, not financial. The 11.1 gates guard the simulated inputs (live extraction accuracy, override rates, escaped defects) together with the operating point the simulator proposes: auto-draft threshold 0.85, assisted threshold 0.70 and a discount band of plus or minus 1 percent (S, proposed; the pilot validates all three).

The Innovo inquiry closes its loop here. As measured in 4.3: 28 touch hours across three estimators, about €340 of direct cost, seven calendar days, issued two days late. As simulated at the central case, applying the 8.2 Tier 3 ratios: roughly 15 touch hours (11 to 20 across the capability range), about €180, and about four calendar days. The quote goes out a day inside the deadline (S). The €160 of processing saved is beside the point. On a package of this size the margin at stake is roughly €1.4–2.6 million (S), and what the redesign buys is the deadline, plus the absence of the two near-misses that almost turned a late quote into a wrong one.

# **Section 10: Business Model & Strategic Implications**

## **10.1 The business-model shift: from expertise to data**

Set side by side, the as-is and to-be business model canvases (the one-page map of how the branch creates, delivers and captures value) differ in only three of their nine blocks, and they are the ones that matter. Key activities shift from producing quotations to handling exceptions and curating the product data layer: the work moves from transcription to judgement, which is where 7.2 routes it. Cost structure shifts from variable labour that scales with inquiry volume to a largely fixed platform cost (9.2), which is what turns the 40 percent demand surge of 9.3 from a breaking load into an operating gain. The deepest change is in key resources. Today the branch’s scarce asset is engineer expertise, and it walks out the door with every resignation (2.1). Under QuoteBench the compounding asset is proprietary transaction data: every RFQ, selection, price and win/loss outcome lands as a structured record (7.2), and the correction flywheel of 7.1 (Exhibit 7.3) converts daily operations into training data. Competitors can hire estimators. They cannot buy the branch’s inquiry history.

## **10.2 Resolving the disintermediation question and the options beyond it**

The disintermediation question planted in 2.1 can now be answered with the paper’s own evidence. Three futures compete. In the first, manufacturers automate selection and quotation and go direct: pump makers already publish sizing tools, and nothing prevents one from wrapping them in a quoting front end. In the second, contractors self-serve through those manufacturer tools, and the distributor’s technical function is not captured by anyone. It simply stops being paid for. In the third, the distributor automates first and becomes the platform of record for its market: the layer through which multi-brand inquiries are specified, priced and won.

Moving first makes the third future attainable for three reasons grounded in the design. Neutrality: a manufacturer’s tool sizes its own pumps, while QuoteBench selects across brands on the contractor’s constraints (7.2), and neutrality is what a manufacturer cannot credibly offer. Embedded workflow: the system ingests the contractor’s documents as they actually arrive (7.2), fragmented, scanned and incomplete, which is the form the manufacturers’ clean-input configurators refuse (5.2); whoever absorbs that mess owns the relationship. Compounding data: the correction flywheel of 7.1 (Exhibit 7.3) turns every routed inquiry into labelled training data, so the first mover’s accuracy advantage widens with every quote. This is the reintermediation move of Chircu and Kauffman (2000): absorb the technology into the function that made the intermediary valuable, before a substitute occupies the position.

The concession is genuine: the first future wins anyway under stateable conditions. If selection commoditizes to the point that contractors trust single-brand tools, if a manufacturer subsidizes direct quoting to buy the channel, or if the distributor’s own automation stalls while 640 inquiries a year keep queueing, then the window closes. Section 11’s stage gates are therefore strategic as well as financial: each phase that clears keeps the reintermediation option alive, and the moment they stop clearing, the conclusion is that this market’s automation will be done to the distributor rather than by it.

Three options open once the platform runs. All are options, not commitments, and none enters a Section 9 number. Quotes-as-a-product: a guaranteed two-hour response on standard configurations, sold as a service level rather than granted as a favour. The simulated Tier 1 cycle time of 2 working hours (8.2) would make the promise printable, and 9.1’s evidence says the speed is worth paying for. A contractor self-service portal: the same intake and selection layers exposed directly for simple configurations, with the branch’s engineers behind the escalation path.

Licensing is the third and least obvious: the extraction and routing layers are product-agnostic by construction (7.2, 12), and a valve or switchgear distributor in a non-competing market faces the same document mess. Each option would monetize the platform beyond one branch’s P&L. None is needed for the investment to clear.

# **Section 11: Recommended Implementation Path, Change & Risk**

## **11.1 Stage gates, kill criteria and the dashboard**

Phase 1 is the validation experiment this paper could not run, priced at roughly €30,000 (S: a quarter engineer-year plus pilot running costs) inside the €92,000 build budget. For three months the pipeline runs in shadow on Tier 2, the most common inquiry and the richest document mix: the system drafts every quote, the draft is scored against the version the estimator actually releases, and nothing reaches a contractor unreviewed. The phase opens with the feasibility audit of Appendix E (25–30 historical RFQs scored field by field), the instrument 8.1 defers. The gates are evidential because 9.3 found no single lever that sinks the case within its tested range. What can sink it is the capability evidence itself. Gate 1, after the audit: if Khoory’s documents score below the pessimistic bound of the 5.2 range, stop before any build spend. Gate 2, after roughly fifty shadow inquiries: live extraction accuracy at or above the pessimistic variant, an engineer override rate falling month on month, and zero would-be escaped defects against the released versions. Breach any of these and the recommendation reverts to Option A, the hire, with €30,000 spent buying that answer early. Phase 2 opens auto-draft for Tier 1 behind the same accuracy gates and begins measuring the win-rate response against the 2025 baseline, the one input shadow mode cannot test. Phase 3 makes assisted routing the Tier 2 default and revisits the deferred items (pricing optimization, CAD) on the strength of accumulated data (7.1).

The pilot and any rollout run on seven indicators, each mapped to the simulation output it validates or refutes: automation rate (against the 8.2 variants); override rate (the flywheel’s input and the adoption signal); extraction accuracy (against the 5.2 range); cycle time median and P90 by tier (against Exhibit 8.1); win rate by tier (against the 2025 rates and, from Phase 2, the 9.1 uplift); margin per quote (against the discount spread and the plus or minus 1 percent band); and error escapes (against the 8.2 parity constraint). Targets tighten by phase, and every number the dashboard produces replaces a simulated input with a measured one.

## **11.2 Adoption, liability and trust**

Change is sized to a six-person office, so we apply ADKAR, the change model that moves one person through awareness, desire, knowledge, ability and reinforcement, at the level it operates: the individual estimator. Awareness is built on the leak, not the tool: the roughly €850,000 of 4.2 is shared with the estimators as the problem statement, because nobody defends a status quo that discounts away many times their salary. Desire rests on the redeployment promise of 9.1, made public before the pilot starts: the automation removes retyping, not engineers, and the senior estimator’s job migrates toward the hardest projects and the exception queue. Knowledge comes from co-design: the estimators score the shadow quotes, tune the audit rubric of Appendix E, and set the first routing thresholds, so the system’s judgement is visibly calibrated against theirs. Ability is the shadow quarter itself: three months in the review workspace with no release pressure. Reinforcement is the KPI change, from quotes produced, which rewards the queue, to win rate and margin per quote (11.1), which rewards what the branch sells. The known failure mode is automation bias (5.2). The design counters it by displaying confidence per field and making override a single click that feeds the flywheel.

Who signs an automated quote is unresolved, and the paper treats it conservatively. The working rule, priced into every projection, is that an engineer releases every quotation whatever lane drafted it (7.2): the automation rates of 8.2 and 9.2 assume machine drafting, never machine release, so the rule places no new ceiling on them. Whether professional-indemnity cover or UAE practice additionally requires full re-verification of Tier 1 auto-drafts, rather than review and release, is a fact question we could not close. It is a named Phase 1 legal check. If the answer is re-verification, Tier 1 touch time reverts toward its manual level and the labour benefit shrinks. The floor case of 9.2 absorbs even that. Contractor-facing trust is designed in: every quote states its review status, and complex quotes carry the responsible engineer’s name.

## **11.3 Risk register**

Seven risks, each with likelihood, impact, mitigation and an owner. Technical, documents messier than the published benchmarks (likelihood medium, impact high): the feasibility audit runs before any build and the pessimistic variant is already priced; owner, build lead. Commercial, contractors discounting system-assembled quotes (medium, medium): review-status labelling, engineer names on complex work, and the in-progress contractor interviews; owner, sales manager. Organizational, estimator attrition during transition (medium, high): the public redeployment promise and the senior’s ownership of the exception queue; owner, branch manager. Legal, mis-specification liability (low, high): the engineer-release rule and the 11.2 legal check; owner, management with counsel. Vendor and model dependency (medium, medium): the extraction layer is bought behind an abstraction with a second-vendor fallback (7.2); owner, build lead. Data protection, contractor documents in third-party models (low, medium): in-tenant processing and no training on client documents without consent; owner, build lead. Model risk, the simulation itself being wrong (medium, high): the calibration gate of 8.2, shadow-mode scoring against reality, and kill criteria that do not depend on the model being right; owner, the authors.

# **Section 12: Limitations & Generalizability**

The limitations are structural and we state them without qualification. The study evaluates the investment before anything is built: no part of QuoteBench exists and no implementation evidence is offered. The projections rest on a calibrated simulation fed by published benchmark ranges, not observed performance, and the feasibility audit that would ground extraction capability in Khoory’s own documents is designed but not yet run. Contractor evidence is thin: interviews are in progress, and what contractors say they value may differ from what they do when a system-assembled quote actually arrives. The speed-win elasticity is triangulated, not measured (9.1). The revenue base is a management figure and the tier value bands are re-derived from it rather than independently measured (9.1). CAD-dependent inquiries are out of scope entirely. These limitations define precisely the evidentiary agenda of the Phase 1 pilot in Section 11: each maps to a gate, a metric or a named check, which is what an ex-ante case can do about its own weaknesses.

Two things generalize. The numbers do not. The architecture pattern (probabilistic intake, a deterministic engineering core, and confidence-based routing that reserves people for the hardest cases) transfers to any engineered-product distribution business whose quoting runs on document extraction plus catalogue logic: valves, switchgear, HVAC equipment. So does the method: measure the baseline, register every assumption, calibrate a simulation against the measured state, and let a pilot attack the weakest inputs first. The specific economics, a 24 percent margin on €34.5 million of pump revenue through one six-person office, belong to one branch in one market and travel nowhere.

# **Section 13: Conclusion**

The first research question asked what process architecture could automate RFQ handling while preserving quote quality, and what evidence supports its feasibility. The answer is the layered design of Section 7: probabilistic extraction quarantined behind confidence scores, a deterministic selection core, and routing that sends every uncertain field to an engineer, with every quote released by one. Its feasibility rests on published benchmark ranges carried as three variants (8.1) and on a process simulation that reproduced the measured 2025 baseline on fifteen checks before projecting anything (8.2). In the simulated central case, median cycle time falls from 18, 39 and 88 working hours by tier to 2, 9 and 56, with engineer touch time roughly halved.

The second asked the projected financial impact and its robustness. The simulated central case is about €990,000 a year at full adoption on the branch’s stated €34.5 million revenue, led by discounting discipline and the win-rate uplift. Simulated five-year NPV spans €1.4 to €4.3 million from P10 to P90, and the floor case, with the uplift at zero and extraction at its pessimistic bound, still clears the 15 percent hurdle (9.2). Across eight stress scenarios and six boundary searches, no single lever within its tested range sinks the case (9.3). What remains uncertain is the inputs beneath the arithmetic, which no simulation can settle.

On the third question, the distributor’s position in the value chain, Section 10’s answer is that automated quoting converts inquiry flow into proprietary transaction data, the one asset in this channel that neither manufacturers nor marketplaces hold, and the reintermediation condition from the literature, moving before a substitute occupies the position, is satisfiable today and will not remain so indefinitely.

We therefore recommend what Section 1 promised: building QuoteBench in stage-gated phases that commit spend only as evidence accumulates. Phase 1 comes first, a three-month €30,000 shadow-mode pilot with pre-committed kill criteria, opening with the feasibility audit on Khoory’s own documents (11.1). Every number above the measured baseline is simulated. The pilot is priced at what it costs to replace the most important simulations with facts.

If the pilot returns what the simulation projects, the Innovo inquiry of Section 2 would read differently the next time it arrives: the same RFQ, one day instead of seven, reviewed by an engineer whose expertise is spent on the ten hardest projects on her desk rather than the forty easiest, and a flagship package quoted inside its deadline instead of against it. That future is worth a €30,000 experiment to prove.

# **Appendices**

•    **A: Assumptions Register.** Build before writing anything else; single owner; every number traces here, tagged measured / audited / simulated.

•    **B: **Full-size process maps (As-Is / proposed To-Be).

•    **C: **Financial model with full assumptions, Monte Carlo input distributions, scenario and sensitivity tables.

•    **D: **Interview guides + anonymized summaries (internal and contractor).

•    **E: **Feasibility audit protocol, scoring rubric, and full results table (replaces the v2 PoC appendix).

•    **F: **Process simulation model description, parameters, and calibration results.

•    **G: **RFQ data schema (proposed) and a worked extraction example, hand-constructed from Innovo.

•    **H: **Full risk register.

•    **I: **Dual Business Model Canvas, full size.

•   **J**: Product data layer. Technical specification: classification standard, storage architecture, retrieval tooling and ingestion pipeline.

•   **K:** Detail tables relocated from the body (Tables 3.1, 4.1, 4.3, 4.4, 7.1); numbering unchanged.

## **Appendix B (extract): Section 4 and Section 7 Exhibits**

[IMAGE]

*Exhibit 4.2. Touch and queue medians by inquiry tier (tiers defined in 4.1). The queue share is remarkably stable, between 86% and 88%, regardless of complexity (M).*

[IMAGE]

*Exhibit 4.3. Four root causes behind the observed cycle times, quality costs and margin leakage. Each maps to a specific element of the proposed design in Section 7.*

Exhibit 7.1. Projected to-be process for a Tier 2 inquiry. Every System-lane time is a simulation output; the bracketed ID names the Appendix A assumption that carries it. The contractor's reply time is the one interval no redesign controls, shown at its measured Section 4 value.

Exhibit 7.2. The proposed architecture. Probabilistic components (sand) are bought; deterministic, rules and data components (white) are built; the selection engine partners with the manufacturer's curve APIs. The dashed return path is the flywheel of Exhibit 7.3.

Exhibit 7.3. The correction flywheel. Constraint five of 7.1 makes every human intervention a labelled training example; accuracy rises, routing admits more inquiries to assisted and auto-draft paths, and freed capacity concentrates on complex, high-margin work. Projected mechanism; the pilot observes its first turn.

## Appendix F (extract): Simulation calibration

The simulator's methodology, parameters, seeds and run manifests are in the public repository ([repository URL]). The calibration gate below is the summary evidence behind 8.2: the as-is model must reproduce the measured 2025 baseline before any projection is run.

[IMAGE]

*Exhibit F.1. Calibration gate: measured 2025 baseline versus the simulated as-is process; all checks pass within tolerance (S; seed 42, run manifests in the public repository).*

## [IMAGE]

## ***Exhibit 8.1. Simulated cycle-time distributions by tier, as-is versus to-be central case, dashed lines marking medians (S).***

## [IMAGE]

## *Exhibit 9.2. Five-year NPV at 12 percent across 20,000 draws, with P10, P50 and P90 marked (S).*

## [IMAGE]

## ***Exhibit 9.3. One-at-a-time sensitivity of five-year NPV at 12 percent (S).***

## **Appendix G (extract): Canonical RFQ Schema**

| **#** | **Field** | **Type** | **Required** | **Typical source** |
|---|---|---|---|---|
| 1 | Contractor & project identity | text | Yes | Email header / body |
| 2 | System type (booster, circulation, transfer, chilled water) | enum | Yes | Schedule / spec |
| 3 | Number of distinct hydraulic systems | integer | Yes | Schedule / drawings |
| 4 | Design flow rate, per system (m³/h) | number | Yes | Schedule |
| 5 | Static head / vertical rise, per system (m) | number | Yes | Riser diagram |
| 6 | Pipe run length (m) | number | Yes | Drawings / spec |
| 7 | Pipe diameter and material | number + enum | Yes | Spec |
| 8 | Fittings summary (bends, valves, strainers) | structured list | Yes | Drawings / default profile |
| 9 | Fluid and temperature | enum + number | Yes | Spec |
| 10 | Power supply (voltage / phase) | enum | Yes | Spec |
| 11 | Required delivery date | date | No | Email body |
| 12 | Attachments manifest & per-field confidence | metadata | system | Generated |

Table G.1. The canonical RFQ schema (simplified). Fields 4–8 repeat per hydraulic system on multi-system inquiries. Field 12 is generated by the extraction layer and is the input to the confidence router of 7.7.

## **Appendix J (extract): Product Data Layer Technical Specification**

**Classification.** Manufacturer data is normalized at ingestion into a four-level hierarchy (family, range, model, configuration), with each configuration carrying typed attributes in four groups: hydraulic (performance stored as Q–H, efficiency, power and NPSH point arrays or curve coefficients, never as prose), mechanical (materials, seal type, orientation, connections), electrical (voltage, phase, IE class), and commercial (list price, lead time, supersession chain). Attribute naming follows the ETIM classification standard where the manufacturer supplies it, with a mapping table for house conventions, so that a model designation means exactly one thing to every layer of the system, and remains comparable if further manufacturers are added later.

**Storage.** Two stores, chosen by data type. Parametric and curve data sit in a relational database (PostgreSQL): feasibility questions (which configurations deliver 46 m³/h at 38 m head, in cast iron, at 400 V) are exact filters that must return the same answer every time, and SQL guarantees it. Unstructured technical content (specification sheets, application notes, installation constraints) is chunked, embedded and held in a vector index (pgvector, in the same database) for semantic retrieval when the reviewer or the clarification drafter needs supporting text. Curve data decides this architecture: selection quality depends on interpolating real curves, which is arithmetic on stored coefficients, not language.

**Retrieval.** The model is granted tools (a structured query against the relational store, semantic search over the vector index, and the manufacturer's live selection API of 7.6), and its outputs are schema-constrained, so any response naming a model must carry the database key and data version it drew from. Structured filters run first, semantic retrieval second: narrow, then read. Every record carries source and effective date, and each quote references the price-list and curve versions it used. An ingestion pipeline from manufacturer feeds refreshes the store; a record that cannot name its source does not enter it.

## Appendix K (extract): Detail tables

Reference tables relocated from the body; numbering unchanged. Each is cited from its home section.

| **Source** | **Scope** | **What it supplies** | **Used in** | **Tag** |
|---|---|---|---|---|
| RFQ log analysis | 640 inquiries, Jan–Dec 2025, single branch | Volumes, tier mix, cycle times, win rates, discount spreads | 4.1–4.4, 9.1 | M |
| Time-and-motion observation | 22 inquiries shadowed end-to-end over 3 weeks; both branch estimators | Step-level touch and queue times; the swimlane of Exhibit 4.1; simulation parameters | 4.1, 8.2 | M |
| Quotation defect audit | Stratified sample of 120 quotations checked against source documents; credit-note ledger | Error taxonomy, defect frequencies, cost of poor quality | 4.4 | E |
| Internal interviews | 6 structured interviews: estimators, sales, branch and line management | Loaded costs, hiring lead times, lost-tender estimate, discounting behaviour, 2025 revenue and margin | 2.2, 4.4, 9.1, 9.4 | E |
| Contractor interviews | [4–6] interviews, in progress (protocol in Appendix D) | Drivers of supplier choice; speed-vs-price weighting; stated reaction to automated quoting | 4.6, 9.3 | E |
| Feasibility audit sample | 25–30 historical RFQs across tiers, scored field-by-field per the 8.1 rubric | Pilot instrument (Appendix E): replaces the simulated capability ranges with evidence from Khoory's own documents | 8.1, 11.1 | planned |
| Simulation models | Discrete-event process model + financial Monte Carlo; code, parameters, seeds and manifests published (Appendix F) | Projected cycle time, capacity and utilization; NPV distribution | 8.2, 9.2 | S |

*Table 3.1. Evidence base of the study. Tags: M measured, E estimated from sampled data or structured interview, S simulated. The feasibility audit is a planned pilot instrument, not yet evidence. The contractor interview count is bracketed pending completion.*

| **Criterion** | **Tier 1: Simple** | **Tier 2: Standard** | **Tier 3: Complex** |
|---|---|---|---|
| Pumps requested | 1–2, One application | 3–12, up to 2 applications | >12, or multiple systems / buildings (Multiple applications) |
| Data completeness at receipt | Complete, or trivially completable | Partial; typically one clarification | Substantially incomplete; drawings required |
| Typical content | Replacement unit, small booster set | Single building or package | Chilled water, multi-building, special quotes to manufacturer |
| Project value | < €56k | €56k – €493k | > €493k |
| Share of inquiry volume (M) | 55% | 33% | 12% |
| Share of quoted value (M) | 12% | 41% | 47% |

*Table 4.1. Segmentation criteria and 2025 mix, n = 640 inquiries. Value bands restated against the branch’s actual 2025 revenue (E, D19); volume and value shares are measured (M).*

| **Error class** | **What it looks like** | **Share of defects (E)** | **Frequency (E)** | **Typical unit cost (E)** |
|---|---|---|---|---|
| Extraction / transcription | Flow, head or model data mis-read or re-keyed wrongly from PDF, scan or drawing | 41% | 9% of inquiries | €860 rework; occasional full requote |
| Calculation | Head-loss worked from wrong pipe length, material or fitting count; sizing off as a result | 17% | 3.5% of inquiries | €2,680; site failure cases exceed €35,000 |
| Selection | Feasible but wrong model: duty point at curve edge, wrong configuration for the application | 23% | 5% of inquiries | €11,270 avg. (returns, re-orders, commissioning delay) |
| Pricing / commercial | Wrong list price, missed cost update, arithmetic in the discount line | 19% | 4% of inquiries | €4,510 direct margin loss |

*Table 4.3. Error taxonomy from the 120-quotation audit and 2025 credit-note ledger. Categories are not mutually exclusive on a given inquiry; frequencies count inquiries where the class appears. Unit costs restated to actual 2025 order values (D19).*

| **When** | **What happened** | **Touch** | **Waiting** |
|---|---|---|---|
| Thu 16:30 | Inquiry received; sits unread overnight in the shared mailbox | – | – |
| Fri 10:15 | Triaged and assigned to an estimator | 0.3 h | 17.5 h |
| Fri – Sat | Specification, schedules and drawings read across all five applications; schedules transcribed by hand; gaps found on two systems, static head ambiguous between risers and flow missing for the transfer set | 6.0 h | 0.5 h |
| Sat 14:00 | Consolidated clarification drafted and sent to the contractor | 0.7 h | 0.3 h |
| Tue 11:20 | Contractor replies (weekend plus Monday in between); reply read and filed | – | ~2.5 working days |
| Tue – Wed | Head-loss calculations for all five systems | 7.0 h | 1.5 h |
| Wed – Thu | Model selection in the manufacturer software across 75 pumps; several booster and chilled-water duty points fall near the curve edge | 8.0 h | 3.0 h |
| Thu | Senior estimator pulled in to confirm the curve-edge selections; booster set re-checked after a static-head reading is questioned | 3.0 h | 2.0 h |
| Thu | Pricing and discount debated across the package between sales and estimation | 2.0 h | 1.0 h |
| Thu evening | Quotation assembled and issued, two days after the Tuesday deadline | 1.0 h | – |

*Table 4.4. The Innovo inquiry, timestamped from mailbox records and the estimators' logs (M). Touch total: 28 hours. Elapsed: seven calendar days, quote issued two days past the deadline.*

| **Criterion** | **A: Hire** | **B: Selection tools** | **C: CPQ** | **D: Full custom** | **E: Hybrid (proposed)** |
|---|---|---|---|---|---|
| Cycle-time impact | 1 | 2 | 2 | 5 | 5 |
| Margin impact (errors, discounts, capacity) | 1 | 2 | 2 | 5 | 5 |
| Error-rate impact | 1 | 2 | 1 | 4 | 4 |
| Five-year cost (build + run) | 5 | 4 | 2 | 1 | 3 |
| Implementation risk | 5 | 4 | 3 | 1 | 3 |
| Strategic optionality (data asset) | 1 | 1 | 2 | 5 | 5 |

*Table 6.1. Option scoring, 1 (worst) to 5 (best). Cost and implementation risk score five-year exposure, and strategic optionality scores the transaction-data asset of Section 10.*

| **Capability** | **Approach** | **Rationale** |
|---|---|---|
| Document & email extraction | Buy (foundation-model API) + build schema/validation layer | Models are a fast-moving commodity; owning the schema keeps the system model-agnostic |
| Intake, classification, clarification | Build (thin orchestration) | Encodes the 4.2 taxonomy and completeness rules |
| Product data layer (7.5) | Build (PostgreSQL + pgvector, managed hosting) | Normalization, versioning and history are the substrate of the Section 10 data asset |
| Hydraulic engine | Build (deterministic rules) | Settled formulas; must be auditable line by line |
| Pump selection | Partner (manufacturer curve/selection APIs) | Grundfos maintains the curves; rebuilding invites divergence |
| Pricing engine | Build (rules + ERP integration) | Bands and cost data are Khoory's own; recovers the 1.9% leak |
| Review workspace & routing | Build | The 7.7 design is the differentiating asset |
| Audit log, identity, monitoring | Buy (standard components) | Undifferentiated; shortens the path to pilot |
| CAD parsing | Defer (out of Phase 1) | Hardest problem, lowest early payoff |

*Table 7.1. Sourcing by component. The build column is intentionally thin: orchestration, rules, data and workspace.*

# **References**

Benjamin, R., & Wigand, R. (1995). Electronic markets and virtual value chains on the information superhighway. *Sloan Management Review, 36*(2), 62–72.

Chircu, A. M., & Kauffman, R. J. (2000). Reintermediation strategies in business-to-business electronic commerce. *International Journal of Electronic Commerce, 4*(4), 7–42.

Forza, C., & Salvador, F. (2002). Managing for variety in the order acquisition and fulfilment process: The contribution of product configuration systems. *International Journal of Production Economics, 76*(1), 87–98.

Forza, C., & Salvador, F. (2007). *Product information management for mass customization*. Palgrave Macmillan.

Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation bias: A systematic review of frequency, effect mediators, and mitigators. Journal of the American Medical Informatics Association, 19(1), 121–127.

Hertz, D. B. (1964). Risk analysis in capital investment. *Harvard Business Review, 42*(1), 95–106.

Hicks, C., McGovern, T., & Earl, C. F. (2000). Supply chain management: A strategic issue in engineer to order manufacturing. *International Journal of Production Economics, 65*(2), 179–190.

Jaume, G., Ekenel, H. K., & Thiran, J.-P. (2019). FUNSD: A dataset for form understanding in noisy scanned documents. In *2019 International Conference on Document Analysis and Recognition Workshops (ICDARW)* (Vol. 2, pp. 1–6). IEEE.

Kim, G., Hong, T., Yim, M., Nam, J., Park, J., Yim, J., Hwang, W., Yun, S., Han, D., & Park, S. (2022). OCR-free document understanding transformer. In Computer Vision – ECCV 2022 (pp. 498–517). Springer.

Kingsman, B., Hendry, L., Mercer, A., & de Souza, A. (1996). Responding to customer enquiries in make-to-order companies: Problems and solutions. *International Journal of Production Economics, 46–47*, 219–231.

Law, A. M. (2015). *Simulation modeling and analysis* (5th ed.). McGraw-Hill Education.

Mathew, M., Karatzas, D., & Jawahar, C. V. (2021). DocVQA: A dataset for VQA on document images. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) (pp. 2200–2209). IEEE.

Mudambi, S., & Aggarwal, R. (2003). Industrial distributors: Can they survive in the new economy? *Industrial Marketing Management, 32*(4), 317–325.

Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors, 39*(2), 230–253.

Parasuraman, R., Sheridan, T. B., & Wickens, C. D. (2000). A model for types and levels of human interaction with automation. IEEE Transactions on Systems, Man, and Cybernetics, Part A: Systems and Humans, 30(3), 286–297.

Robinson, S. (2014). *Simulation: The practice of model development and use* (2nd ed.). Palgrave Macmillan.

Sarkar, M. B., Butler, B., & Steinfield, C. (1995). Intermediaries and cybermediaries: A continuing role for mediating players in the electronic marketplace. *Journal of Computer-Mediated Communication, 1*(3).

Skitka, L. J., Mosier, K. L., & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies, 51*(5), 991–1006.

Xu, Y., Li, M., Cui, L., Huang, S., Wei, F., & Zhou, M. (2020). LayoutLM: Pre-training of text and layout for document image understanding. In *Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 1192–1200). ACM.

