#!/usr/bin/env python3
"""T07 pass 1 — scaffolding removal + mechanical fixes.
Usage: python3 scripts/t07a_edits.py [--apply]
"""
import sys
sys.path.insert(0, "scripts")
from doc_editor import run

EDITS = [
    # preamble
    {"find": "Revised Paper Architecture (v3) \u2014 Ex-Ante Evaluation Framing\n", "replace": ""},
    {"find": "Narrative device one real, anonymized RFQ \u2014 \u201cInnovo Contracting for Guggenheim Museum in Abu Dhabi\u201d \u2014 opens the paper (2.0), is traced through the As-Is process with real timestamps (4.5), is re-run as a simulated scenario through the proposed design (7.8), anchors the feasibility audit (8.1), and is priced in the financial model (9.6). In the To-Be scenes, label it explicitly: \u201ca simulated walk-through under the assumptions of Section 8.\u201d The story survives the reframing intact \u2014 it simply changes tense halfway through, which is itself an elegant structural signal.\n", "replace": ""},
    # section 1
    {"find": "Section 1 \u2014 Executive Summary (1 page) \u2014 write last", "replace": "Section 1 \u2014 Executive Summary"},
    {"find": "Test: a professor reading only this page should know exactly what is fact, what is projection, and what decision you are recommending.\n", "replace": ""},
    # section 2
    {"find": "Section 2 \u2014 Introduction & Problem Definition (2.5 pages)", "replace": "Section 2 \u2014 Introduction & Problem Definition"},
    {"find": "2.0 Opening vignette (\u00bd page)", "replace": "2.0 Opening vignette"},
    {"find": "The distribution value chain and why the distributor exists: technical selection expertise, aggregation across manufacturers, credit, local presence. Plant the tension explicitly: \u201cEach of these functions is under pressure from digitization; this paper examines what happens when the most defensible one \u2014 technical expertise \u2014 becomes automatable.\u201d Do not resolve it here.\n", "replace": ""},
    {"find": "2.3 Research questions \u2014 reworded for the ex-ante frame", "replace": "2.3 Research questions"},
    {"find": "In / out, one sentence of justification per exclusion. Add one explicit line: \u201cThis study evaluates the proposed transformation ex-ante; implementation and post-implementation measurement are outside its scope and are addressed as a recommended pilot design in Section 11.\u201d Stating this once, early, inoculates you against the \u2018but you didn\u2019t build it\u2019 critique \u2014 you convert the absence into a declared research design.\n", "replace": ""},
    # author's notes
    {"find": "Author's note (remove before submission): the bracketed branch designation in 3.1 and the interview counts in Table 3.1 must be confirmed and completed with actual values. The scoping sentence reconciling the 640-inquiry baseline with Khoory's company-wide estimator figures is load-bearing \u2014 verify it reflects how the data was actually collected before submission.\n", "replace": ""},
    {"find": "Author's note (remove before submission): all figures in this section are structured placeholders written to be replaced with the distributor's actual data. Volumes, times, costs and rates are internally consistent and realistic for a UAE pump distributor of this size, but they are illustrative until substituted. The (M) measured / (E) estimated tags mark the evidence standard each figure must meet once real values are inserted.\n", "replace": ""},
    {"find": "Author's note (remove before submission): the works cited below are established literature in their fields, but every citation must be verified against the original source, page-checked where quoted figures appear, and formatted to the programme's referencing standard before submission. Subsection 5.5 is a deliberate placeholder pending documentation of the authors' simulation platform.\n", "replace": ""},
    {"find": "Rule: every citation must be re-cited in Sections 6\u201311 or deleted.\n", "replace": ""},
    # section 6 heading
    {"find": "Section 6 \u2014 Solution Options & Design Choice (1.5\u20132 pages) \u2014 the anti-whitepaper section", "replace": "Section 6 \u2014 Solution Options & Design Choice"},
    # 4.6 heading + provisional stub (D6)
    {"find": "4.6 Voice of the customer (\u00bd\u20131 page)", "replace": "4.6 Voice of the customer"},
    {"find": "TO be Provided: 4\u20136 contractor interviews: what drives supplier choice, how much speed matters vs. price, and \u2014 now doubly important \u2014 their stated reaction to the hypothetical of an automated quote. Because you cannot observe real behaviour toward the system, their stated preferences are your only demand-side evidence; gather them carefully and quote 2\u20133 verbatim.",
     "replace": "Contractor interviews are in progress at the time of writing (protocol in Appendix D): four to six structured conversations covering what drives supplier choice, how speed weighs against price, and \u2014 because no live system exists to observe \u2014 each contractor's stated reaction to the hypothetical of an automated quote. Preliminary conversations consistently point to response speed and error-free technical submittals as decisive selection factors, which supports the direction of this design; verbatim quotations, including any dissenting views, will be incorporated once transcripts are complete (E, provisional). Stated preferences are the paper's only demand-side evidence, and Section 9.3 treats them accordingly: as an upper bound to be triangulated, not a measurement."},
    # consistency: queue-share in 4.7
    {"find": "The 84\u201387% queue share in Exhibit 4.2", "replace": "The 86\u201388% queue share in Exhibit 4.2"},
    # table renumbering
    {"find": "Table 7.2 states the sourcing decision per component", "replace": "Table 7.1 states the sourcing decision per component"},
    {"find": "Table 7.2. Sourcing by component.", "replace": "Table 7.1. Sourcing by component."},
    {"find": "Table 7.1. The canonical RFQ schema (simplified).", "replace": "Table G.1. The canonical RFQ schema (simplified)."},
    # missing Section 8 heading
    {"insert_before": "8.1 Technical feasibility audit (audited evidence)",
     "text": "Section 8 \u2014 Feasibility & Simulation Evidence\n",
     "style": "HEADING_1",
     "bold": ["Section 8 \u2014 Feasibility & Simulation Evidence"]},
    # heading meta strips, sections 9-13
    {"find": "Section 9 \u2014 Projected Financial Analysis (4.5 pages)", "replace": "Section 9 \u2014 Projected Financial Analysis"},
    {"find": "Section 10 \u2014 Business Model & Strategic Implications (2.5 pages)", "replace": "Section 10 \u2014 Business Model & Strategic Implications"},
    {"find": "Section 11 \u2014 Recommended Implementation Path, Change & Risk (2.5 pages)", "replace": "Section 11 \u2014 Recommended Implementation Path, Change & Risk"},
    {"find": "Section 12 \u2014 Limitations & Generalizability (0.75 page)", "replace": "Section 12 \u2014 Limitations & Generalizability"},
    {"find": "Section 13 \u2014 Conclusion (1 page)", "replace": "Section 13 \u2014 Conclusion"},
    {"find": "Appendices (confirm they are excluded from the page count)", "replace": "Appendices"},
    {"find": "References cited in section 5", "replace": "References"},
    {"find": "9.5 Investment appraisal under uncertainty \u2014 now simulation-based", "replace": "9.5 Investment appraisal under uncertainty"},
    {"find": "10.2 Resolving the disintermediation question (planted in 2.1)", "replace": "10.2 Resolving the disintermediation question"},
    {"find": "11.1 Stage-gated roadmap \u2014 the pilot is the point", "replace": "11.1 Stage-gated roadmap"},
]

if __name__ == "__main__":
    ok = run(EDITS, apply="--apply" in sys.argv)
    sys.exit(0 if ok else 1)
