#!/usr/bin/env python3
"""Phase 2, pass 4: Sections 7-9 per the confirmed audit.

Section 7 (1,549 -> ~1,060, 10 subs -> 3): 7.1+7.2+7.10 -> "7.1 Five
constraints and the projected process"; 7.3-7.8 -> "7.2 The architecture:
from intake to engineer release"; 7.9 -> 7.3. Phase detail in old 7.10 cut
as a duplicate of 11.1.
Section 8 (894 -> ~720, 4 subs -> 2): 8.3+8.4 fold into 8.2.
Section 9 (1,421 -> ~1,190, 6 subs -> 3): 9.1+9.2+9.3 -> 9.1; 9.4+9.5 ->
9.2; 9.6 -> 9.3. The elasticity sub's pre-statement of the floor-case
finding is cut as a duplicate of 9.2/9.3.
Cross-references renumbered across the paper. Image moves (Exhibits 8.1,
9.3 -> Appendix F) are in e4b.
"""
import sys

from doc_editor import run

EDITS = [
    # ================= SECTION 7 =================
    {"find": "7.1 Design principles, stated as constraints",
     "replace": "7.1 Five constraints and the projected process"},
    {"find": ("The proposed system, referred to hereafter as QuoteBench, is "
              "governed by five constraints, written as obligations rather "
              "than aspirations. First, automate extraction and calculation, "
              "and augment judgement: the system takes over the reading, "
              "transcription and arithmetic where Section 4.4 located 41% of "
              "defects, and presents judgement calls to a person. Second, no "
              "quote leaves below defined confidence without human review; "
              "in Phase 1 the gate is absolute."),
     "replace": ("QuoteBench is governed by five constraints, written as "
                 "obligations. First, automate extraction and calculation, "
                 "and augment judgement: the system takes over the reading, "
                 "transcription and arithmetic where Section 4.2 located 41% "
                 "of defects, and presents judgement calls to a person. "
                 "Second, no quote leaves below defined confidence without "
                 "human review. In Phase 1 the gate is absolute.")},
    {"find": ("the constraint that turns review burden into the flywheel of "
              "7.7."),
     "replace": ("the constraint that turns review burden into the flywheel "
                 "of 7.2.")},
    {"find": "7.2 The to-be process: a projected swimlane\n", "replace": ""},
    {"find": ("A projected Tier 2 inquiry would need roughly 25 minutes of "
              "human attention against the measured 5.5 hours, the "
              "difference redeployed rather than removed (9.2, 11.2)."),
     "replace": ("A projected Tier 2 inquiry would need roughly 25 minutes "
                 "of human attention against the measured 5.5 hours, the "
                 "difference redeployed rather than removed (9.1, 11.2). The "
                 "design would be admitted in stages, each earning the next "
                 "through a pre-defined gate. Thresholds are stated as "
                 "symbols because they are parameters the pilot exists to "
                 "determine, and the roadmap with kill criteria is the "
                 "subject of 11.1.")},
    {"find": "7.3 Intake and classification layer",
     "replace": "7.2 The architecture: from intake to engineer release"},
    {"find": ("Within minutes of arrival the intake layer classifies the "
              "inquiry into the 4.1 taxonomy [A1] and validates completeness "
              "against the 7.4 schema, producing a definitive list of gaps "
              "while the inquiry is minutes old. Missing fields trigger one "
              "consolidated clarification covering every gap at once [A3], "
              "where the as-is process finds gaps serially, at a median "
              "41-hour round trip each, and only after roughly 22 working "
              "hours of queueing and reading. When the reply arrives,"),
     "replace": ("Within minutes of arrival the intake layer classifies the "
                 "inquiry into the 4.1 taxonomy [A1] and validates "
                 "completeness against the extraction schema, producing a "
                 "definitive list of gaps while the inquiry is minutes old. "
                 "Missing fields trigger one consolidated clarification "
                 "covering every gap at once [A3], where the as-is process "
                 "finds gaps serially at a median 41-hour round trip each. "
                 "When the reply arrives,")},
    {"find": "7.4 Extraction layer\n", "replace": ""},
    {"find": ("Extraction converts unstructured documents into one canonical "
              "record, the twelve-field-per-system RFQ schema of Appendix G, "
              "using language and vision models to read specification "
              "extracts, schedules and email text. Each field carries a "
              "confidence score, and it is these scores, not the values, "
              "that drive the routing of 7.7. One boundary is stated now: "
              "native CAD parsing is out of scope for Phase 1. Where "
              "required fields exist only in a DWG file, the inquiry routes "
              "to an engineer with every extractable field pre-filled and "
              "the CAD-dependent fields flagged, so degradation is to "
              "assisted work rather than manual, and the 8.1 audit measures "
              "how often this occurs."),
     "replace": ("Extraction converts the documents into one canonical "
                 "record, the twelve-field-per-system RFQ schema of Appendix "
                 "G, using language and vision models. Each field carries a "
                 "confidence score, and the scores, not the values, drive "
                 "the routing below. Native CAD parsing is out of scope for "
                 "Phase 1: where required fields exist only in a DWG file, "
                 "the inquiry routes to an engineer with every extractable "
                 "field pre-filled and the CAD-dependent fields flagged, and "
                 "the 8.1 audit measures how often that occurs."),
     "unbold": True},
    {"find": "7.5 The product data layer: classification, storage and retrieval\n",
     "replace": ""},
    {"find": ("None of the above works if the system's knowledge of pumps "
              "lives inside a language model: models recall approximately, "
              "catalogues change monthly, and a quotation defensible under "
              "the audit constraint must rest on data that is exact, "
              "versioned and sourced. The design therefore separates "
              "reasoning from memory. Models read documents and orchestrate; "
              "a governed product database remembers: manufacturer data "
              "normalized into a typed hierarchy, hydraulic performance "
              "stored as curve data rather than prose, prices and lead times "
              "versioned with effective dates. The model never answers a "
              "product question from its own weights: retrieval runs "
              "structured filters first and semantic search second, and any "
              "response naming a model must carry the database key and data "
              "version it drew from, which is what keeps a quote "
              "reconstructible months later and correct the week after a "
              "price revision. The full specification of this layer "
              "(classification standard, storage architecture, retrieval "
              "tooling and ingestion pipeline) is given in Appendix J."),
     "replace": ("The system's knowledge of pumps does not live inside a "
                 "language model: models recall approximately, catalogues "
                 "change monthly, and a quotation defensible under the audit "
                 "constraint must rest on data that is exact, versioned and "
                 "sourced. Models read documents and orchestrate. A governed "
                 "product database remembers: manufacturer data in a typed "
                 "hierarchy, hydraulic performance as curve data, prices and "
                 "lead times versioned with effective dates. Any response "
                 "naming a model must carry the database key and data "
                 "version it drew from, which keeps a quote reconstructible "
                 "months later. The full specification of this layer is "
                 "Appendix J."),
     "unbold": True},
    {"find": "7.6 Calculation and decision layer: three separated engines\n",
     "replace": ""},
    {"find": ("Between a validated schema and a draft quote sit three "
              "engines, kept separate because they carry different "
              "uncertainty. The hydraulic engine is deterministic physics, "
              "not AI: static head plus friction and fitting losses by "
              "Darcy-Weisbach, cross-checked by Hazen-Williams, the same "
              "formulas the estimators apply by hand, encoded once; because "
              "this is settled engineering, the design's uncertainty lives "
              "entirely upstream in extraction, which is what the Section 8 "
              "audit measures. The selection engine is a constrained search: "
              "given a duty point it filters the 7.5 store, queries the "
              "manufacturer's selection API, and returns candidates ranked "
              "on efficiency, price and lead time, flagging duty points near "
              "a curve edge rather than accepting them silently [A5]; where "
              "several answers are defensible, Khoory's own history of "
              "chosen and winning selections breaks the tie, the Section 10 "
              "data asset used here as a sort order. The pricing engine is "
              "rules, not learning: cost-plus by family with a defined "
              "discount band and a reference price beside every discount "
              "decision, aimed at the 4\u201318% spread and the "
              "1.9%-of-revenue leak of 4.2; machine-learned price "
              "optimisation is deferred to Phase 3."),
     "replace": ("Between a validated schema and a draft quote sit three "
                 "engines, kept separate because they carry different "
                 "uncertainty. The hydraulic engine is deterministic "
                 "physics, not AI: Darcy-Weisbach cross-checked by "
                 "Hazen-Williams, the same formulas the estimators apply by "
                 "hand, encoded once, so the design's uncertainty lives "
                 "upstream in extraction. The selection engine is a "
                 "constrained search: given a duty point it filters the "
                 "product store, queries the manufacturer's selection API, "
                 "and returns candidates ranked on efficiency, price and "
                 "lead time, flagging duty points near a curve edge [A5]. "
                 "Where several answers are defensible, Khoory's own history "
                 "of winning selections breaks the tie. The pricing engine "
                 "is rules, not learning: cost-plus by family with a defined "
                 "discount band and a reference price beside every discount "
                 "decision, aimed at the 4\u201318% spread and the "
                 "1.9%-of-revenue leak of 4.2. Machine-learned price "
                 "optimisation is deferred to Phase 3."),
     "bold": ["The hydraulic engine is deterministic physics, not AI",
              "The selection engine is a constrained search",
              "The pricing engine is rules, not learning"],
     "unbold": True},
    {"find": "7.7 Human-in-the-loop design\n", "replace": ""},
    {"find": ("The preceding layers describe what the machine would do; this "
              "one decides what it is allowed to do. The routing is stated "
              "as logic:"),
     "replace": ("The preceding layers describe what the machine would do. "
                 "The routing decides what it is allowed to do:")},
    {"find": ("The thresholds C\u2081, C\u2082 and V\u2081 are design "
              "parameters, not findings; setting them is the work of the "
              "pilot in 11.1. Under this routing the estimator's role moves "
              "upward,"),
     "replace": ("The thresholds C\u2081, C\u2082 and V\u2081 are design "
                 "parameters. Setting them is the work of the pilot in "
                 "11.1. Under this routing the estimator moves upward,")},
    {"find": ("and freed capacity concentrates where margin is highest, a "
              "projected mechanism the pilot exists to observe."),
     "replace": "and freed capacity concentrates where margin is highest."},
    {"find": "7.8 Build, buy or partner\n", "replace": ""},
    {"find": ("Exhibit 7.2 (Appendix B) shows the layers assembled; Table "
              "7.1 (Appendix K) states the sourcing decision per component. "
              "The pattern: buy the probabilistic commodity,"),
     "replace": ("Exhibit 7.2 (Appendix B) shows the layers assembled, and "
                 "Table 7.1 (Appendix K) states the sourcing per component: "
                 "buy the probabilistic commodity,")},
    {"find": "7.9 The Innovo inquiry, to-be: a simulated walk-through",
     "replace": "7.3 The Innovo inquiry, to-be: a simulated walk-through"},
    {"find": ("flagged as an explicit conflict [A2]; at 16:53 a single "
              "consolidated clarification is on its way,"),
     "replace": ("flagged as an explicit conflict [A2]. At 16:53 a single "
                 "consolidated clarification is on its way,")},
    {"find": ("the review turns on the flagged selections; the senior's "
              "confirmation is two lines,"),
     "replace": ("the review turns on the flagged selections. The senior's "
                 "confirmation is two lines,")},
    {"find": ("Seven calendar days would become four; twenty-eight touch "
              "hours would become roughly fifteen (S: eleven to twenty "
              "across the 8.1 capability range): the review of a 75-pump "
              "draft rather than its manual construction; and neither "
              "near-miss of 4.5 would arise to be caught. These times are "
              "model outputs; the numbers they are compared with were "
              "measured, and closing that asymmetry is Section 8's job."),
     "replace": ("Seven calendar days would become four, and twenty-eight "
                 "touch hours roughly fifteen (S: eleven to twenty across "
                 "the 8.1 capability range): the review of a 75-pump draft "
                 "rather than its manual construction. Neither near-miss of "
                 "4.3 would arise to be caught. These times are model "
                 "outputs. The numbers they are compared with were measured, "
                 "and closing that asymmetry is Section 8's job.")},
    {"find": ("7.10 Phasing preview\n"
              "The design would be admitted in stages, each earning the next "
              "through a pre-defined gate. Phase 1 runs the pipeline in "
              "shadow, every quote human-released and scored against the "
              "estimators; Phase 1 is the pilot itself. Phase 2 opens "
              "auto-draft for Tier 1 only, gated on live extraction "
              "accuracy, override rates and zero escaped defects in shadow. "
              "Phase 3 makes assisted routing the Tier 2 default and "
              "revisits the deferred items (pricing optimization, CAD) on "
              "the strength of accumulated flywheel data. Thresholds are "
              "stated as symbols deliberately: they are parameters the "
              "pilot exists to determine, and the full roadmap with kill "
              "criteria is the subject of 11.1.\n"),
     "replace": ""},

    # ================= SECTION 8 =================
    {"find": "8.1 Capability evidence: what the automation could plausibly do",
     "replace": "8.1 Capability evidence from published benchmarks"},
    {"find": ("No system has been built, so nothing in this section is a "
              "measurement of a live tool; every capability figure is a "
              "simulation input,"),
     "replace": ("No system has been built, so nothing in this section is a "
                 "measurement of a live tool. Every capability figure is a "
                 "simulation input,")},
    {"find": ("It is therefore scheduled as the first activity of the Phase "
              "1 pilot (11.1); until it runs, the capability inputs stay on "
              "the published ranges. The consequence is stated once: if "
              "Khoory's"),
     "replace": ("It is scheduled as the first activity of the Phase 1 pilot "
                 "(11.1), and until it runs the capability inputs stay on "
                 "the published ranges. If Khoory's")},
    {"find": "8.2 Process simulation: calibration first, projection second",
     "replace": "8.2 Simulation: calibration, projection, validation"},
    {"find": ("The current build passes all fifteen (Exhibit F.1, Appendix "
              "F); the gate is enforced in code,"),
     "replace": ("The current build passes all fifteen (Exhibit F.1, "
                 "Appendix F). The gate is enforced in code,")},
    {"find": "with P90s falling in step (Exhibit 8.1); median engineer touch drops",
     "replace": ("with P90s falling in step (Exhibit 8.1, Appendix F). "
                 "Median engineer touch drops")},
    {"find": "the stress runs of 9.6 show the same two estimators absorbing",
     "replace": "the stress runs of 9.3 show the same two estimators absorbing"},
    {"find": ("which is a design constraint rather than a bonus: reviewer "
              "attention drops"),
     "replace": "which is a design constraint: reviewer attention drops"},
    {"find": "8.3 Expert & practitioner validation (validated design)\n",
     "replace": ""},
    {"find": ("Validation by the people involved is partly done and partly "
              "scheduled. The estimators challenged the swimlane, the tier "
              "taxonomy and the error audit during measurement, and two of "
              "their corrections (small jobs first, clarification "
              "overlapping other waits) became load-bearing calibration "
              "facts in 8.2. The contractor interviews (protocol in Appendix "
              "D) and a structured review of the Section 7 architecture are "
              "in progress; their scores and dissents will be reported here, "
              "and the routing thresholds they challenge are the same "
              "parameters the pilot re-measures."),
     "replace": ("Validation by the people involved is partly done and "
                 "partly scheduled. The estimators challenged the swimlane, "
                 "the tier taxonomy and the error audit during measurement, "
                 "and two of their corrections became the calibration facts "
                 "above. The contractor interviews (protocol in Appendix D) "
                 "and a structured review of the Section 7 architecture are "
                 "in progress. The routing thresholds they challenge are the "
                 "same parameters the pilot re-measures.")},
    {"find": "8.4 Honest synthesis\n", "replace": ""},
    {"find": ("What the evidence supports: the measured baseline and its "
              "costs (Section 4); the calibrated capacity arithmetic of 8.2; "
              "and roughly \u20ac210,000 a year of simulated benefit that "
              "does not depend on winning a single additional order (the "
              "labour, error and discounting effects of 9.2)."),
     "replace": ("What the evidence supports: the measured baseline and its "
                 "costs (Section 4); the calibrated capacity arithmetic "
                 "above; and roughly \u20ac210,000 a year of simulated "
                 "benefit that does not depend on winning a single "
                 "additional order (the labour, error and discounting "
                 "effects of 9.1).")},
    {"find": ("and above all the win-rate response to speed, which 9.5 shows "
              "carries the investment case. Each unproven item maps to a "
              "Phase 1 pilot measurement with a go/no-go gate in 11.1, and "
              "the floor case in 9.5 states"),
     "replace": ("and above all the win-rate response to speed, which 9.2 "
                 "shows carries the investment case. Each unproven item maps "
                 "to a Phase 1 pilot measurement with a go/no-go gate in "
                 "11.1, and the floor case in 9.2 states")},

    # ================= SECTION 9 =================
    {"find": "9.1 Baseline economics of the quoting function (measured)",
     "replace": "9.1 Baseline economics and the benefits waterfall"},
    {"find": ("The revenue those hours carry is stated, not derived: the "
              "branch's 2025 pump-only revenue was approximately AED 150 "
              "million, \u20ac34.5 million at the paper's conversion (M, "
              "management figure, D19),"),
     "replace": ("The revenue those hours carry is a stated management "
                 "figure: the branch's 2025 pump-only revenue was "
                 "approximately AED 150 million, \u20ac34.5 million at the "
                 "paper's conversion (M, D19),")},
    {"find": "9.2 Benefits waterfall (projected, tagged)\n", "replace": ""},
    {"find": ("The assumption is redeployment rather than redundancy; the "
              "hours move to Tier 3 work, declined inquiries and the "
              "clarification chase, which also defuses the change-management "
              "tension addressed in 11.2."),
     "replace": ("The assumption is redeployment: the hours move to Tier 3 "
                 "work, declined inquiries and the clarification chase "
                 "(11.2).")},
    {"find": ("with overall defect rates held at parity (8.2); the saving "
              "comes from the mix shifting away from expensive selection "
              "errors, not from a lower headline rate."),
     "replace": ("with overall defect rates held at parity (8.2). The saving "
                 "comes from the mix shifting away from expensive selection "
                 "errors.")},
    {"find": "the dominant bar and the least proven, gated next in 9.3.",
     "replace": "the dominant bar and the least proven, defended below."},
    {"find": "reached on the 7.10 ramp", "replace": "reached on the 11.1 ramp"},
    {"find": ("the recovered volume is upside the pilot can log; it is left "
              "out of every number in this paper,"),
     "replace": ("the recovered volume is upside the pilot can log. It is "
                 "left out of every number in this paper,")},
    {"find": "9.3 Validating the speed\u2013win elasticity\n", "replace": ""},
    {"find": ("Customer evidence: the contractor interviews of 4.6 (in "
              "progress, protocol in Appendix D) ask directly how speed "
              "weighs against price; the model takes no credit for anything "
              "they have not yet said."),
     "replace": ("Customer evidence: the contractor interviews of 4.4 (in "
                 "progress, protocol in Appendix D) ask directly how speed "
                 "weighs against price, and the model takes no credit for "
                 "anything they have not yet said.")},
    {"find": ("The model therefore carries the uplift as a range from zero "
              "to five percentage points of win rate with a central value of "
              "two (S); five points on a 27 percent Tier 2 base is an 18 "
              "percent relative gain, inside the ceiling the lost-tender "
              "estimate implies. The floor case of 9.5 sets it to zero "
              "outright. The stress runs add the most useful fact in the "
              "paper: the investment clears its hurdle even if speed turns "
              "out to be worth nothing at all, because the discounting and "
              "error effects carry the cost base on their own; the uplift "
              "decides how large the return is, not whether there is one "
              "(S)."),
     "replace": ("The model carries the uplift as a range from zero to five "
                 "percentage points of win rate with a central value of two "
                 "(S). Five points on a 27 percent Tier 2 base is an 18 "
                 "percent relative gain, inside the ceiling the lost-tender "
                 "estimate implies. The floor case of 9.2 sets it to zero "
                 "outright.")},
    {"find": "9.4 Cost model",
     "replace": "9.2 Costs and investment appraisal"},
    {"find": "Costs enter the model as ranges, and their sourcing is stated. Build:",
     "replace": "Costs enter the model as ranges. Build:"},
    {"find": ("carries an overrun tail to +30 percent, with 9.6 stressing to "
              "+60."),
     "replace": ("carries an overrun tail to +30 percent, with 9.3 stressing "
                 "to +60.")},
    {"find": ("plus inference and API usage at projected volume and "
              "licences; the usage component is provisional,"),
     "replace": ("plus inference and API usage at projected volume and "
                 "licences. The usage component is provisional,")},
    {"find": ("Every range is drawn as a distribution in 9.5, and the "
              "boundaries in 9.6 state"),
     "replace": ("Every range is drawn as a distribution below, and the "
                 "boundaries in 9.3 state")},
    {"find": "9.5 Investment appraisal under uncertainty\n", "replace": ""},
    {"find": ("the win-rate uplift of 9.3 and the cost ranges of 9.4, with "
              "benefits anchored to the calibrated process model of 8.2 and "
              "phased in on the 7.10 adoption ramp."),
     "replace": ("the win-rate uplift of 9.1 and the cost ranges above, with "
                 "benefits anchored to the calibrated process model of 8.2 "
                 "and phased in on the 11.1 adoption ramp.")},
    {"find": ("(the median exceeds 300 percent against a \u20ac92,000 "
              "build); the number that matters is the floor."),
     "replace": ("(the median exceeds 300 percent against a \u20ac92,000 "
                 "build). The number that matters is the floor.")},
    {"find": ("and a result this one-sided is an argument for testing the "
              "inputs, not for skipping the test."),
     "replace": "and a result this one-sided argues for testing the inputs."},
    {"find": "9.6 Sensitivity & unit economics",
     "replace": "9.3 Sensitivity and unit economics"},
    {"find": "Exhibit 9.3 ranks the levers one at a time.",
     "replace": "Exhibit 9.3 (Appendix F) ranks the levers one at a time."},
    {"find": ("and demand at one-fifth of the 2025 rate still clears; in the "
              "other direction,"),
     "replace": ("and demand at one-fifth of the 2025 rate still clears. In "
                 "the other direction,")},
    {"find": ("The pilot's kill criteria are therefore evidential rather "
              "than financial: the 11.1 gates guard the simulated inputs "
              "(live extraction accuracy, override rates, escaped defects) "
              "rather than an NPV threshold, alongside the operating point "
              "the simulator's search proposes:"),
     "replace": ("The pilot's kill criteria are evidential, not financial. "
                 "The 11.1 gates guard the simulated inputs (live extraction "
                 "accuracy, override rates, escaped defects) together with "
                 "the operating point the simulator proposes:")},
    {"find": ("with the contractor's reply carried at its measured pace; the "
              "quote goes out a day inside the deadline (S)."),
     "replace": ("with the contractor's reply carried at its measured pace. "
                 "The quote goes out a day inside the deadline (S).")},

    # ============ cross-references elsewhere ============
    {"find": "the pricing engine of Section 7.6 is designed against",
     "replace": "the pricing engine of Section 7.2 is designed against"},
    {"find": "reappears as the rules-based engine of 7.6.",
     "replace": "reappears as the rules-based engine of 7.2."},
    {"find": "The routing of 7.7 applies these findings directly",
     "replace": "The routing of 7.2 applies these findings directly"},
    {"find": "override logging of 7.7 are the design's admission of it",
     "replace": "override logging of 7.2 are the design's admission of it"},
    {"find": "which is where 7.7 routes it",
     "replace": "which is where 7.2 routes it"},
    {"find": "lands as a structured record (7.5)",
     "replace": "lands as a structured record (7.2)"},
    {"find": "selects across brands on the contractor\u2019s constraints (7.4)",
     "replace": "selects across brands on the contractor\u2019s constraints (7.2)"},
    {"find": "ingests the contractor\u2019s documents as they actually arrive (7.3)",
     "replace": "ingests the contractor\u2019s documents as they actually arrive (7.2)"},
    {"find": "product-agnostic by construction (7.3, 12.2)",
     "replace": "product-agnostic by construction (7.2, 12.2)"},
    {"find": "an abstraction with a second-vendor fallback (7.3)",
     "replace": "an abstraction with a second-vendor fallback (7.2)"},
    {"find": "on the strength of accumulated data (7.10).",
     "replace": "on the strength of accumulated data (7.1)."},
    {"find": "which is what turns the 40 percent demand surge of 9.6",
     "replace": "which is what turns the 40 percent demand surge of 9.3"},
    {"find": "largely fixed platform cost (9.4)",
     "replace": "largely fixed platform cost (9.2)"},
    {"find": "the redeployment promise of 9.2, made public before the pilot",
     "replace": "the redeployment promise of 9.1, made public before the pilot"},
    {"find": "and 9.3\u2019s evidence says the speed is worth paying for",
     "replace": "and 9.1\u2019s evidence says the speed is worth paying for"},
    {"find": ("because 9.6 found no single lever that sinks the case within "
              "its tested range; what can sink it is the capability evidence "
              "itself."),
     "replace": ("because 9.3 found no single lever that sinks the case "
                 "within its tested range. What can sink it is the "
                 "capability evidence itself.")},
    {"find": "the automation rates of 8.2 and 9.5 assume machine drafting",
     "replace": "the automation rates of 8.2 and 9.2 assume machine drafting"},
    {"find": ("touch time reverts toward its manual level and the labour "
              "benefit shrinks; the floor case of 9.5 absorbs even that."),
     "replace": ("touch time reverts toward its manual level and the labour "
                 "benefit shrinks. The floor case of 9.2 absorbs even "
                 "that.")},
    {"find": "and, from Phase 2, the 9.3 uplift",
     "replace": "and, from Phase 2, the 9.1 uplift"},
    {"find": "The speed\u2013win elasticity is triangulated, not measured (9.3).",
     "replace": "The speed\u2013win elasticity is triangulated, not measured (9.1)."},
    {"find": "still clears the 15 percent hurdle (9.5).",
     "replace": "still clears the 15 percent hurdle (9.2)."},
    {"find": "no single lever within its tested range sinks the case (9.6).",
     "replace": "no single lever within its tested range sinks the case (9.3)."},
    {"row_anchor": "Simulation models", "old_cell": "8.2, 9.5",
     "new_cell": "8.2, 9.2"},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
