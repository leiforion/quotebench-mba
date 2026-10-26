#!/usr/bin/env python3
"""T15c — de-academicize the setup: compress Section 3, cut meta-commentary,
reduce 'ex-ante' to definitional uses, active first person where the authors acted.
Usage: python3 scripts/t15c_tone.py [--apply]
"""
import sys
sys.path.insert(0, "scripts")
from doc_editor import run

EDITS = [
    # ---------- 2.4 depth of evaluation ----------
    {"find": "This is an ex-ante study: no software has been built and no pilot run. The analysis rests on",
     "replace": "No software has been built and no pilot run; the paper evaluates the investment before it is made. The analysis rests on"},

    # ---------- 3.1 ----------
    {"find": "This study is a prospective, ex-ante evaluation of a proposed process transformation. Nothing described in Sections 6 through 8 has been built, and the paper claims otherwise nowhere. Its claim is narrower: that the transformation can be evaluated to a decision-grade standard before a line of code exists, with the discipline applied to any capital investment: measure the current state, design the alternative from established components, model its behaviour, and subject the assumptions to structured challenge.",
     "replace": "Nothing in this paper has been built yet; the study is what investment appraisal calls an ex-ante evaluation. We evaluate the proposed transformation the way a board evaluates any capital request: measure the current process, design the alternative from proven components, model what it would do, and stress the assumptions until they hold or break."},
    {"find": "Four components carry the evaluation: an empirical baseline of the current quoting process, measured rather than recalled (Section 4); a design synthesis assembled from components whose individual behaviour is documented, so that the novelty lies in the assembly rather than in any unproven part (Section 7); a simulation of the future state, combining a process model for cycle time and capacity with a financial model that converts its outputs into a probabilistic investment case (Sections 8 and 9); and expert and customer validation, in which the estimators and contractors are used not as sources of enthusiasm but as adversaries of the design's assumptions (8.1, 8.3, 4.6).",
     "replace": "Four components carry the evaluation: a measured baseline of the current quoting process (Section 4); a design assembled from components whose behaviour is already documented, so the novelty lies in the assembly and not in any unproven part (Section 7); a simulation of the future state, a process model for cycle time and capacity plus a financial model that turns its outputs into an investment case stated as ranges (Sections 8 and 9); and validation by the people involved: we use the estimators and the contractors to challenge the design's assumptions, not to endorse them (8.1, 8.3, 4.6).",
     "bold": ["measured baseline", "design", "simulation of the future state", "validation by the people involved"]},
    {"find": "One scoping statement belongs here because every number downstream depends on it. Khoory operates 16 estimators across its UAE branches, each handling on the order of twelve inquiries a week across all the product lines the company distributes. The empirical baseline of Section 4 was measured at a single branch, [the Abu Dhabi estimation office], whose 640 pump RFQs in 2025 constitute the study population, the slice of that workload within this paper's product scope; company-wide figures appear only where Section 9 scales the branch-level findings, and are labelled as such when they do. Measuring one branch deeply was preferred to measuring all branches thinly: the simulation of Section 8 needs step-level timings that only observation can supply, and observation does not spread.",
     "replace": "One scoping point matters for every number downstream. Khoory operates 16 estimators across its UAE branches, each handling around twelve inquiries a week across all product lines. We measured a single branch, [the Abu Dhabi estimation office], whose 640 pump RFQs in 2025 are the study population; company-wide figures appear only where Section 9 scales the branch findings, and are labelled when they do. We chose to measure one branch deeply rather than all branches thinly, because the Section 8 simulation needs step-level timings that only direct observation can supply."},
    {"find": "Every quantitative claim in the paper carries one of three tags, used without exception. Measured means read directly from records or timestamped observation. Audited means produced by the structured feasibility study of 8.1, scored by estimators against a written rubric on real historical documents. Simulated means an output of the process or financial model, traceable to a named assumption in Appendix A. The vocabulary is the paper's contract with its reader: at any sentence, it should be unambiguous which kind of knowledge is being offered.",
     "replace": "Every quantitative claim in the paper carries one of three tags. Measured means read from records or timestamped observation. Audited means produced by the structured feasibility study of 8.1, scored by estimators against a written rubric on real historical documents. Simulated means an output of the process or financial model, traceable to a named assumption in Appendix A.",
     "bold": ["Measured", "Audited", "Simulated"]},

    # ---------- 3.3 ----------
    {"find": "Two models do the projective work of this paper, and one rule governs both: a model earns the right to project a future it has not seen only by first reproducing a past that was measured.",
     "replace": "Two models do the projective work, under one rule: a model earns the right to project a future only by first reproducing the past we measured."},
    {"find": "The process model represents the branch operation as a flow of inquiries through the steps of Exhibit 4.1: arrivals by tier at measured 2025 rates, touch times from the observed step distributions, estimator capacity as the constraint, queue discipline as observed, with large inquiries modelled as pre-emption because that is what the Innovo case shows happens. It runs on the authors' operations-simulation platform (5.5). Before any to-be scenario is run, the model must reproduce the measured as-is baseline (median and P90 cycle time by tier, within a stated tolerance), and the calibration error is reported in 8.2, because it is the number that separates simulation from arithmetic. Only then are to-be scenarios run across the audited automation range, reporting cycle time, utilization and capacity as distributions.",
     "replace": "The process model replays the branch operation of Exhibit 4.1: arrivals by tier at 2025 rates, touch times from the observed step distributions, estimator capacity as the constraint, and queue discipline as observed, with large inquiries modelled as pre-emption because the Innovo case shows that is what happens. It runs on the authors' operations-simulation platform (5.5) and must reproduce the measured baseline (median and P90 cycle time by tier, within a stated tolerance) before any to-be scenario is run; the calibration error appears in 8.2. To-be scenarios then run across the audited automation range and report cycle time, utilization and capacity as distributions.",
     "bold": ["The process model"]},
    {"find": "The financial model converts those projections into an investment case by Monte Carlo, because the honest state of knowledge in an ex-ante study is a set of ranges. Three uncertain inputs are treated as distributions: the automation rate, bounded by the 8.1 audit; the win-rate uplift from faster quoting, triangulated in 9.3 and floored at zero in the conservative case; and the build cost (9.4). Sampling across these produces five-year NPV at P10, P50 and P90 with the probability of clearing the hurdle rate. Every input distribution is documented in Appendix C; no parameter enters the model that the Appendix A register does not name.",
     "replace": "The financial model converts those projections into five-year NPV by Monte Carlo, because what we honestly have are ranges, not points. Three inputs dominate and are drawn as distributions: the automation rate, bounded by the 8.1 audit; the win-rate uplift from faster quoting, triangulated in 9.3 and floored at zero in the conservative case; and the build cost (9.4). Results are reported at P10, P50 and P90 with the probability of clearing the hurdle rate; every input distribution is documented in Appendix C and named in the Appendix A register.",
     "bold": ["The financial model"]},

    # ---------- 3.4 ----------
    {"find": "Three limitations are acknowledged now and treated fully in Section 12. The baseline is one branch of one distributor, measured over one year, and the deep-observation sample behind the step timings is 22 inquiries. The future state is simulated and audited, not observed: no live extraction accuracy, engineer adoption, or contractor behaviour has been measured, and the pilot recommended in Section 11 exists precisely to supply what this design cannot. And the demand-side evidence (how much speed is worth in won tenders) rests on triangulated history and stated preferences rather than experiment, which is why the financial model floors that benefit at zero before it claims anything else.",
     "replace": "Three limits of method are stated here and treated fully in Section 12: the baseline is one branch of one distributor over one year, with 22 deeply observed inquiries; the future state is simulated and audited, not observed, which is what the Section 11 pilot exists to fix; and the demand-side evidence on what speed is worth rests on history and stated preferences, which is why the financial model floors that benefit at zero."},

    # ---------- Section 4 ----------
    {"find": "three weeks of direct observation, during which 22 inquiries were timestamped from arrival to quotation (M)",
     "replace": "three weeks of direct observation in which we timestamped 22 inquiries from arrival to quotation (M)"},
    {"find": "so every 2025 inquiry was classified retrospectively into three tiers by pump count, data completeness at receipt, and project value",
     "replace": "so we classified every 2025 inquiry retrospectively into three tiers by pump count, data completeness at receipt, and project value"},

    # ---------- Section 5 intro ----------
    {"find": "Each is treated instrumentally (a source appears here only because a later section leans on it), and the review's purpose is to establish what is already known so that the paper's contribution stands on settled ground.",
     "replace": "A source appears here only because a later section leans on it; the aim is to establish what is already known so the paper's contribution stands on settled ground."},

    # ---------- 6.3 ----------
    {"find": "What the rejected options do better deserves plain statement.",
     "replace": "The rejected options do some things better."},

    # ---------- Section 7 preamble ----------
    {"find": "Evidence status: everything in this section is a proposal; nothing has been built. To-be times and behaviours are projections, each carrying the ID of the Appendix A assumption that supplies its value, established by the audit and simulation of Section 8. Figures carried over from Section 4 remain measured. Exhibits 7.1\u20137.3 are placed in Appendix B and referenced from the text; the RFQ schema table is in Appendix G.",
     "replace": "Everything in this section is a proposal: to-be times and behaviours are projections, each tagged with the Appendix A assumption that supplies its value, while figures carried over from Section 4 remain measured. Exhibits 7.1\u20137.3 are in Appendix B; the RFQ schema table is in Appendix G.",
     "unbold": True},

    # ---------- 7.9 meta trim ----------
    {"find": "The conditional tense is deliberate, because these times are model outputs, but the contrast is with numbers that were measured, and closing that asymmetry is Section 8's job.",
     "replace": "These times are model outputs; the numbers they are compared with were measured, and closing that asymmetry is Section 8's job."},
]

if __name__ == "__main__":
    ok = run(EDITS, apply="--apply" in sys.argv)
    sys.exit(0 if ok else 1)
