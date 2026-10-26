#!/usr/bin/env python3
"""Phase 2, pass 3: Sections 5-6 per the confirmed audit.

Section 5 (923 -> ~520, 4 subs -> 2): lit-review narrative cut; every
citation the paper leans on is kept. 5.2+5.3+5.4 merge into one sub.
Section 6 (1,009 -> ~770, 3 subs -> 2): option descriptions compressed
(the 2.1 cost restatement in Option A deduplicated); 6.3 folds into 6.2.
Cross-references to 5.3/5.4/6.3/4.4 renumbered.
"""
import sys

from doc_editor import run

EDITS = [
    # ---------------- Section 5 ----------------
    {"find": ("This paper draws on four bodies of work. A source appears "
              "here only because a later section leans on it; the aim is to "
              "establish what is already known so the paper's contribution "
              "stands on settled ground.\n"),
     "replace": ""},
    {"find": "5.1 Digitization of B2B distribution and the disintermediation debate",
     "replace": "5.1 Disintermediation: the case for moving first"},
    {"find": ("The oldest question this paper raises is whether digitizing a "
              "distributor's core function hastens the distributor's own "
              "removal. Early electronic-commerce research answered yes: "
              "online markets cut transaction costs and let manufacturers "
              "deal directly with buyers (Benjamin & Wigand, 1995). The "
              "counter-position followed immediately: intermediaries do more "
              "than pass product, and new electronic intermediaries appear "
              "even as old ones dissolve (Sarkar et al., 1995). Chircu and "
              "Kauffman (2000) reconciled the two as a cycle of "
              "intermediation\u2013disintermediation\u2013reintermediation: "
              "displaced incumbents can re-enter by absorbing the technology "
              "into the functions that made them valuable, provided they "
              "move before a substitute occupies the position. Two decades "
              "of wholesale-distribution practice broadly confirms the "
              "pattern: distribution consolidated and digitized rather than "
              "disappeared (Mudambi & Aggarwal, 2003), with the gains "
              "accruing to distributors that made their differentiating "
              "capability digital first."),
     "replace": ("Whether digitizing a distributor's core function hastens "
                 "the distributor's own removal is an old question with a "
                 "settled shape. Early electronic-commerce research "
                 "predicted disintermediation: online markets cut "
                 "transaction costs and let manufacturers deal directly with "
                 "buyers (Benjamin & Wigand, 1995). Sarkar et al. (1995) "
                 "countered that intermediaries do more than pass product, "
                 "and Chircu and Kauffman (2000) reconciled the two as a "
                 "cycle of intermediation, disintermediation and "
                 "reintermediation: displaced incumbents re-enter by "
                 "absorbing the technology into the functions that made them "
                 "valuable, provided they move before a substitute occupies "
                 "the position. Wholesale distribution has since "
                 "consolidated and digitized rather than disappeared "
                 "(Mudambi & Aggarwal, 2003)."),
     "unbold": True},
    {"find": ("The relevance is direct: this study proposes to digitize the "
              "first of the three pillars identified in Section 2, and the "
              "IDR framing turns that from an efficiency question into the "
              "strategic one Section 10 resolves: whether automating "
              "technical expertise makes the distributor the platform of "
              "record for its market, or merely writes the manual for its "
              "own replacement. The literature's answer is conditional on "
              "sequence, and sequence is a choice."),
     "replace": ("The framing does real work for this paper: it turns "
                 "automating technical expertise from an efficiency question "
                 "into the strategic one Section 10 resolves, whether the "
                 "distributor becomes the platform of record for its market "
                 "or writes the manual for its own replacement. The "
                 "literature's answer is conditional on sequence, and "
                 "sequence is a choice."),
     "unbold": True},
    {"find": "5.2 CPQ systems and their limits for engineered-to-spec product",
     "replace": "5.2 What the technology evidence does and does not support"},
    {"find": ("Configure-price-quote software is the commercial category "
              "closest to this paper's proposal: where a product family can "
              "be described by enumerable options and compatibility rules, a "
              "configurator reliably replaces expert intervention in the "
              "sales process (Forza & Salvador, 2002, 2007), offering guided "
              "configuration, rule-based pricing and automated quote "
              "assembly on top of structured inputs.\n"
              "The qualifier carries the weight: structured inputs. CPQ "
              "assumes the seller already knows, in machine-readable form, "
              "what the customer needs; engineered-to-order environments "
              "violate that at both ends, with requirements arriving as "
              "drawings and specifications rather than option selections, "
              "and the mapping to product running through engineering "
              "calculation rather than compatibility rules (Hicks et al., "
              "2000). A pump distributor's RFQ is a textbook instance. The "
              "make-to-order literature has long treated the enquiry stage "
              "as a competitive arena in its own right: Kingsman et al. "
              "(1996) model the probability of winning an order as a "
              "function of the price and the lead time quoted, the coupling "
              "Section 9 prices. That is why Section 6 treats CPQ as a "
              "component of the proposed design (the right machinery for "
              "pricing discipline and quote assembly) rather than as an "
              "alternative to it: what the category has never solved, and "
              "what this design must, is the unstructured front door."),
     "replace": ("Three streams of prior work set the boundaries of the "
                 "design.\n"
                 "Configure-price-quote systems automate quoting reliably "
                 "where a product can be described by enumerable options and "
                 "compatibility rules (Forza & Salvador, 2002, 2007), but "
                 "they assume structured inputs. Engineered-to-order "
                 "environments violate that assumption at both ends: "
                 "requirements arrive as drawings and specifications, and "
                 "the mapping to product runs through engineering "
                 "calculation (Hicks et al., 2000). The make-to-order "
                 "literature also treats the enquiry stage itself as a "
                 "competitive arena: Kingsman et al. (1996) model the "
                 "probability of winning an order as a function of the price "
                 "and lead time quoted, the coupling Section 9 prices. "
                 "Section 6 accordingly treats CPQ as a component for "
                 "pricing discipline and quote assembly, and the "
                 "unstructured front door as the problem this design must "
                 "solve."),
     "unbold": True},
    {"find": "5.3 AI document understanding: what the benchmarks do and do not promise\n",
     "replace": ""},
    {"find": ("Because this study fields no prototype, published evidence on "
              "machine reading of business documents is load-bearing: it "
              "supplies the priors that 8.1 maps onto the distributor's own "
              "document mix, and it must be reported with both its "
              "flattering and its unflattering sides. The flattering side is "
              "genuine: layout-aware and vision-language models have pushed "
              "the standard document-understanding benchmarks to levels out "
              "of reach five years ago, with the strongest pipelines "
              "answering well above 90% of items on the principal "
              "document-QA benchmark (Jaume et al., 2019; Kim et al., 2022; "
              "Mathew et al., 2021; Xu et al., 2020).\n"
              "The unflattering side matters more here. Benchmark corpora "
              "are dominated by curated, single-genre documents, while "
              "recent enterprise-extraction evaluations show accuracy "
              "degrading sharply as schemas widen and documents lengthen: "
              "models produce validly structured output whose values are "
              "wrong. The distributor's reality sits at the hard end of that "
              "spectrum: multi-column schedules scanned as images, "
              "specification extracts running to dozens of pages, units and "
              "symbols that differ by consultant. And one piece of "
              "arithmetic reframes even optimistic per-field accuracy: at "
              "95% per field, a twelve-field schema is fully correct only "
              "about 54% of the time (0.95\u00b9\u00b2). That arithmetic, "
              "not distrust of the models, is why the Section 7 design "
              "carries per-field confidence scores, validation gates and "
              "human review as structural features rather than as caution, "
              "and why the 8.1 audit exists: to establish where on the "
              "published spectrum this distributor's documents actually "
              "fall."),
     "replace": ("Machine reading of business documents supplies the "
                 "capability priors that 8.1 maps onto the distributor's own "
                 "document mix. The strongest pipelines now answer well "
                 "above 90% of items on the principal document-QA benchmarks "
                 "(Jaume et al., 2019; Kim et al., 2022; Mathew et al., "
                 "2021; Xu et al., 2020). Enterprise evaluations are less "
                 "flattering: accuracy degrades sharply as schemas widen and "
                 "documents lengthen, with models producing validly "
                 "structured output whose values are wrong, and the "
                 "distributor's documents sit at the hard end of that "
                 "spectrum. One piece of arithmetic reframes even the "
                 "optimistic figures: at 95% per field, a twelve-field "
                 "schema is fully correct only about 54% of the time "
                 "(0.95\u00b9\u00b2). That arithmetic is why the Section 7 "
                 "design carries per-field confidence scores, validation "
                 "gates and human review as structural features, and why the "
                 "8.1 audit exists."),
     "unbold": True},
    {"find": "5.4 Human-in-the-loop automation\n", "replace": ""},
    {"find": ("Four decades of human-factors research warns that the failure "
              "mode of partial automation is rarely the machine's error "
              "alone; it is the human's changed relationship to the task. "
              "Operators over-rely on automation that is usually right and "
              "abandon automation that has embarrassed them, in neither case "
              "calibrating to its actual reliability (Parasuraman & Riley, "
              "1997). Automation bias, the acceptance of a machine's "
              "suggestion in place of one's own vigilance, produces "
              "measurable errors even among trained professionals (Goddard "
              "et al., 2012), and strengthens when the human feels less "
              "accountable for the outcome (Skitka et al., 1999). The design "
              "response is to set the level of automation per function, "
              "deliberately (Parasuraman, Sheridan and Wickens, 2000).\n"
              "The routing design of 7.7 applies these findings directly: "
              "confidence is displayed so trust has something to calibrate "
              "against; uncertain fields arrive flagged, forcing engagement "
              "where it is needed; release is an explicit act with a name "
              "attached; and the automation level is set per tier and per "
              "function. The literature's uncomfortable implication is "
              "retained rather than argued away: a reviewer who approves "
              "ninety-nine good drafts is primed to approve the hundredth, "
              "and the value-gated release rules and override logging of 7.7 "
              "are the design's admission of it."),
     "replace": ("Partial automation also changes the human. Operators "
                 "over-rely on automation that is usually right and abandon "
                 "automation that has embarrassed them (Parasuraman & Riley, "
                 "1997). Automation bias produces measurable errors even "
                 "among trained professionals (Goddard et al., 2012), and "
                 "strengthens when the human feels less accountable for the "
                 "outcome (Skitka et al., 1999). The design response is to "
                 "set the level of automation per function, deliberately "
                 "(Parasuraman, Sheridan and Wickens, 2000). The routing of "
                 "7.7 applies these findings directly: confidence is "
                 "displayed so trust has something to calibrate against, "
                 "uncertain fields arrive flagged, release is an explicit "
                 "act with a name attached, and the automation level is set "
                 "per tier and per function. A reviewer who approves "
                 "ninety-nine good drafts is primed to approve the "
                 "hundredth, and the value-gated release rules and override "
                 "logging of 7.7 are the design's admission of it."),
     "unbold": True},

    # ---------------- Section 6 ----------------
    {"find": ("Each is described on its own terms and scored in 6.2; two of "
              "the rejected options survive inside the proposed design as "
              "components."),
     "replace": ("Each is described on its own terms and scored in 6.2. Two "
                 "of the rejected options survive inside the proposed design "
                 "as components.")},
    {"find": "6.1 Option set", "replace": "6.1 The option set"},
    {"find": ("Option A: hire more estimators. The baseline competitor is "
              "not technology at all: keep the process of Section 4 and add "
              "one or two estimators as volume grows. Its virtues are real: "
              "lowest cost, fastest to value, no implementation risk, no "
              "change management. Its limits are the arithmetic of 2.1: a "
              "qualified estimator costs about \u20ac22,000 a year (E), "
              "takes two to three months to hire and another three to four "
              "to reach full productivity, and adds capacity only in "
              "permanent, indivisible steps. Cycle time, error rates and "
              "the discount spread stay where Section 4 measured them, "
              "because the process itself is unchanged."),
     "replace": ("Option A: hire more estimators. The baseline competitor is "
                 "not technology at all: keep the process of Section 4 and "
                 "add one or two estimators as volume grows. Its virtues are "
                 "real: lowest cost, fastest to value, no implementation "
                 "risk, no change management. Its limits are the arithmetic "
                 "of 2.1: capacity arrives in permanent, indivisible steps, "
                 "and cycle time, error rates and the discount spread stay "
                 "where Section 4 measured them, because the process itself "
                 "is unchanged."),
     "bold": ["Option A: hire more estimators."], "unbold": True},
    {"find": ("Option B: manufacturer selection tools. Grundfos, Wilo, KSB "
              "and Xylem all publish selection software: the estimator "
              "enters a computed duty point and picks from the returned "
              "range instead of reading curves off the page. This is how "
              "most distributors, Khoory included, already work, so its "
              "gains are banked in the Section 4 baseline: the tools remove "
              "roughly 20 to 30 percent of manual effort at the selection "
              "step (E, estimator interviews) and make that step more "
              "reliable. They cannot reach intake, extraction, calculation "
              "or clarification, where the delay and most of the defects "
              "live, and each tool ranks only its publisher's range."),
     "replace": ("Option B: manufacturer selection tools. Grundfos, Wilo, "
                 "KSB and Xylem all publish selection software: the "
                 "estimator enters a computed duty point and picks from the "
                 "returned range. The branch already works this way, so the "
                 "gains are banked in the Section 4 baseline: the tools "
                 "remove roughly 20 to 30 percent of manual effort at the "
                 "selection step (E, estimator interviews). They cannot "
                 "reach intake, extraction, calculation or clarification, "
                 "where the delay and most of the defects live, and each "
                 "tool ranks only its publisher's range."),
     "bold": ["Option B: manufacturer selection tools."], "unbold": True},
    {"find": ("Option C: off-the-shelf CPQ. Configure-price-quote software "
              "automates the commercial tail: line-item assembly, pricing "
              "rules, discount approvals, document generation. As 5.2 "
              "established, the category assumes structured inputs and "
              "therefore solves the wrong end of this problem: it cannot "
              "read a specification, run a head-loss calculation or select "
              "a pump, and it addresses only around 10 to 15 percent of the "
              "touch time measured in Section 4 (E), at enterprise licence "
              "prices. It is rejected as an alternative and retained as a "
              "component: the pricing discipline it embodies reappears as "
              "the rules-based engine of 7.6."),
     "replace": ("Option C: off-the-shelf CPQ. Configure-price-quote "
                 "software automates the commercial tail: line-item "
                 "assembly, pricing rules, discount approvals, document "
                 "generation. As 5.2 established, the category assumes "
                 "structured inputs and solves the wrong end of this "
                 "problem: it addresses only around 10 to 15 percent of the "
                 "touch time measured in Section 4 (E), at enterprise "
                 "licence prices. It is rejected as an alternative and "
                 "retained as a component: its pricing discipline reappears "
                 "as the rules-based engine of 7.6."),
     "bold": ["Option C: off-the-shelf CPQ."], "unbold": True},
    {"find": ("It duplicates assets the manufacturers already maintain "
              "(curve data, selection logic), requires specialist "
              "engineering talent the business does not employ, and stakes "
              "the schedule on the hardest problems first, against the 5.3 "
              "evidence that extraction degrades exactly where this design "
              "would need it most. Nothing in the Section 4 baseline "
              "requires the ceiling; everything in Section 9 punishes the "
              "cost."),
     "replace": ("It duplicates assets the manufacturers already maintain "
                 "(curve data, selection logic), requires specialist "
                 "engineering talent the business does not employ, and "
                 "stakes the schedule on the hardest problems first, against "
                 "the 5.2 evidence that extraction degrades exactly where "
                 "this design would need it most. Nothing in the baseline "
                 "requires the ceiling, and everything in Section 9 punishes "
                 "the cost.")},
    {"find": ("the manufacturer selection APIs of Option B repurposed as "
              "services, the pricing discipline of Option C rebuilt as rules "
              "on Khoory's own data, and confidence-routed human review over "
              "all of it (Section 7). Nothing unproven is invented; the "
              "claim is in the assembly and the routing."),
     "replace": ("the Option B selection APIs repurposed as services, the "
                 "Option C pricing discipline rebuilt as rules on Khoory's "
                 "own data, and confidence-routed human review over all of "
                 "it (Section 7). Nothing unproven is invented: the claim is "
                 "in the assembly and the routing.")},
    {"find": "6.2 Decision matrix",
     "replace": "6.2 The decision matrix and the concession"},
    {"find": ("Section 9 prices that trade; 6.3 states the conditions under "
              "which A wins it."),
     "replace": ("Section 9 prices that trade, and the concession below "
                 "states the conditions under which A wins it.")},
    {"find": "6.3 The concession\n", "replace": ""},
    {"find": "the roughly \u20ac850,000 annual leak of 4.4 sits in error content",
     "replace": "the roughly \u20ac850,000 annual leak of 4.2 sits in error content"},

    # ---------------- cross-reference renumbering elsewhere ----------------
    {"find": "the 1.9%-of-revenue leak of 4.4; machine-learned price",
     "replace": "the 1.9%-of-revenue leak of 4.2; machine-learned price"},
    {"find": "published benchmark ranges reviewed in 5.3 and carried",
     "replace": "published benchmark ranges reviewed in 5.2 and carried"},
    {"find": "score below the pessimistic bound of the 5.3 range",
     "replace": "score below the pessimistic bound of the 5.2 range"},
    {"find": "automation bias (5.4); the design counters it",
     "replace": "automation bias (5.2); the design counters it"},
    {"find": "extraction accuracy (field level, against the 5.3 range the case is priced on)",
     "replace": "extraction accuracy (field level, against the 5.2 range the case is priced on)"},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
