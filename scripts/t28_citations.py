#!/usr/bin/env python3
"""T16: resolve citation placeholders and gaps G2/G13.

- 3.3 PLACEHOLDER -> Law (2015), Robinson (2014) for DES practice; Hertz
  (1964) as the Monte Carlo investment-case precedent.
- 5.1 uncited practice claim -> Mudambi & Aggarwal (2003) (G13).
- 5.2 + 9.3 -> Kingsman et al. (1996) strike-rate literature: win probability
  as a function of price and quoted lead time (kills the G2 phantom).
- References: delete the ExtractBench scaffolding note; insert five verified
  entries alphabetically; italics pass for journal/book names.
All entries verified against publisher records 6 Sep.
"""
import sys
import time

from doc_editor import run, get_service, DOC_ID, find_text_range

R_HERTZ = ("Hertz, D. B. (1964). Risk analysis in capital investment. "
           "Harvard Business Review, 42(1), 95\u2013106.")
R_KINGSMAN = ("Kingsman, B., Hendry, L., Mercer, A., & de Souza, A. (1996). "
              "Responding to customer enquiries in make-to-order companies: "
              "Problems and solutions. International Journal of Production "
              "Economics, 46\u201347, 219\u2013231.")
R_LAW = ("Law, A. M. (2015). Simulation modeling and analysis (5th ed.). "
         "McGraw-Hill Education.")
R_MUDAMBI = ("Mudambi, S., & Aggarwal, R. (2003). Industrial distributors: "
             "Can they survive in the new economy? Industrial Marketing "
             "Management, 32(4), 317\u2013325.")
R_ROBINSON = ("Robinson, S. (2014). Simulation: The practice of model "
              "development and use (2nd ed.). Palgrave Macmillan.")

ITALICS = [
    (R_HERTZ, "Harvard Business Review, 42"),
    (R_KINGSMAN, "International Journal of Production Economics, 46\u201347"),
    (R_LAW, "Simulation modeling and analysis"),
    (R_MUDAMBI, "Industrial Marketing Management, 32"),
    (R_ROBINSON, "Simulation: The practice of model development and use"),
]

EDITS = [
    # ---- 3.3 simulation-methods citations
    {"find": ("The approach follows established practice in operations "
              "simulation. [PLACEHOLDER: two to three citations situating "
              "discrete-event and Monte Carlo simulation of service "
              "operations, plus precedents for simulation-based investment "
              "cases, ; the simulator's modelling approach, calibration and "
              "validation logic go to Appendix F.]"),
     "replace": ("The approach follows established practice: discrete-event "
                 "models of service operations are standard instruments of "
                 "operations analysis (Law, 2015; Robinson, 2014), and Monte "
                 "Carlo analysis of capital investments has been orthodox "
                 "since Hertz (1964). The simulator's modelling approach, "
                 "calibration and validation logic go to Appendix F."),
     "unbold": True},
    # ---- 5.1 distribution-industry source (G13)
    {"find": ("Two decades of wholesale-distribution practice broadly "
              "confirms the pattern: distribution consolidated and digitized "
              "rather than disappeared, with the gains accruing"),
     "replace": ("Two decades of wholesale-distribution practice broadly "
                 "confirms the pattern: distribution consolidated and "
                 "digitized rather than disappeared (Mudambi & Aggarwal, "
                 "2003), with the gains accruing"),
     "unbold": True},
    # ---- 5.2 strike-rate literature (grounds the 9.3 leg)
    {"find": ("A pump distributor's RFQ is a textbook instance. That is why "
              "Section 6 treats CPQ"),
     "replace": ("A pump distributor's RFQ is a textbook instance. The "
                 "make-to-order literature has long treated the enquiry "
                 "stage as a competitive arena in its own right: Kingsman "
                 "et al. (1996) model the probability of winning an order "
                 "as a function of the price and the lead time quoted, the "
                 "coupling Section 9 prices. That is why Section 6 treats "
                 "CPQ"),
     "unbold": True},
    # ---- 9.3 phantom citation fixed (G2)
    {"find": ("Industry evidence: the response-time literature reviewed in "
              "Section 5 supports a positive but modest effect."),
     "replace": ("Industry evidence: the make-to-order bidding literature "
                 "reviewed in 5.2 models win probability as a function of "
                 "price and quoted lead time (Kingsman et al., 1996), "
                 "supporting a positive but modest effect."),
     "unbold": True},
    # ---- References: drop the scaffolding note, insert verified entries
    {"find": ("[Recent enterprise-extraction evaluation work on schema-scale "
              "degradation, e.g. ExtractBench (arXiv, 2026); verify "
              "preferred citation and add benchmark comparison sources "
              "here.]\n"),
     "replace": ""},
    {"find": ("Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation "
              "bias: A systematic review of frequency, effect mediators, and "
              "mitigators. Journal of the American Medical Informatics "
              "Association, 19(1), 121\u2013127."),
     "replace": ("Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). "
                 "Automation bias: A systematic review of frequency, effect "
                 "mediators, and mitigators. Journal of the American Medical "
                 "Informatics Association, 19(1), 121\u2013127.\n"
                 + R_HERTZ),
     "unbold": True},
    {"find": ("OCR-free document understanding transformer. In Computer "
              "Vision \u2013 ECCV 2022 (pp. 498\u2013517). Springer."),
     "replace": ("OCR-free document understanding transformer. In Computer "
                 "Vision \u2013 ECCV 2022 (pp. 498\u2013517). Springer.\n"
                 + R_KINGSMAN + "\n" + R_LAW),
     "unbold": True},
    {"find": ("DocVQA: A dataset for VQA on document images. In Proceedings "
              "of the IEEE/CVF Winter Conference on Applications of Computer "
              "Vision (WACV) (pp. 2200\u20132209). IEEE."),
     "replace": ("DocVQA: A dataset for VQA on document images. In "
                 "Proceedings of the IEEE/CVF Winter Conference on "
                 "Applications of Computer Vision (WACV) (pp. "
                 "2200\u20132209). IEEE.\n" + R_MUDAMBI),
     "unbold": True},
    {"find": ("A model for types and levels of human interaction with "
              "automation. IEEE Transactions on Systems, Man, and "
              "Cybernetics, Part A: Systems and Humans, 30(3), "
              "286\u2013297."),
     "replace": ("A model for types and levels of human interaction with "
                 "automation. IEEE Transactions on Systems, Man, and "
                 "Cybernetics, Part A: Systems and Humans, 30(3), "
                 "286\u2013297.\n" + R_ROBINSON),
     "unbold": True},
]


def italicize(apply):
    svc = get_service(write=apply)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    reqs, ok = [], True
    for entry, span in ITALICS:
        rng, n = find_text_range(doc, entry)
        if rng is None:
            print(f"FAIL entry ({n}): {entry[:50]!r}")
            ok = False
            continue
        off = entry.find(span)
        s = rng[0] + off
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": s, "endIndex": s + len(span)},
            "textStyle": {"italic": True}, "fields": "italic"}})
        print(f"italic ok: {span[:50]!r}")
    if not ok or not apply:
        return ok
    svc.documents().batchUpdate(documentId=DOC_ID,
                                body={"requests": reqs}).execute()
    print("italics APPLIED")
    return True


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    if not run(EDITS, apply=apply):
        sys.exit(1)
    if apply:
        time.sleep(1)
        italicize(apply)
    else:
        print("(italics pass runs after --apply)")
