#!/usr/bin/env python3
"""D18: convert all citations and the reference list to APA 7th.

In text: ampersand in parenthetical two-author citations; "et al." for three
or more; same-author works joined by comma; multi-work citations ordered
alphabetically. Narrative citations keep "and" (APA rule). Reference list:
full author lists (no "et al."), "&" before final author, sentence-case
titles, italicized journal/book/proceedings names + volume (styled in pass 2).
Author lists for Kim (2022) / Xu (2020) reconstructed from the published
papers; T16 verifies. Also fixes a D12 leftover ("the 8.1 audit") in 5.3.
"""
import sys
import time

from doc_editor import run, get_service, DOC_ID, find_text_range

REFS = [
    ("Benjamin, R. and Wigand, R. (1995). Electronic markets and virtual value chains on the information superhighway. Sloan Management Review, 36(2), 62\u201372.",
     "Benjamin, R., & Wigand, R. (1995). Electronic markets and virtual value chains on the information superhighway. Sloan Management Review, 36(2), 62\u201372.",
     "Sloan Management Review, 36"),
    ("Chircu, A.M. and Kauffman, R.J. (2000). Reintermediation strategies in business-to-business electronic commerce. International Journal of Electronic Commerce, 4(4), 7\u201342.",
     "Chircu, A. M., & Kauffman, R. J. (2000). Reintermediation strategies in business-to-business electronic commerce. International Journal of Electronic Commerce, 4(4), 7\u201342.",
     "International Journal of Electronic Commerce, 4"),
    ("Forza, C. and Salvador, F. (2002). Managing for variety in the order acquisition and fulfilment process: the contribution of product configuration systems. International Journal of Production Economics, 76(1), 87\u201398.",
     "Forza, C., & Salvador, F. (2002). Managing for variety in the order acquisition and fulfilment process: The contribution of product configuration systems. International Journal of Production Economics, 76(1), 87\u201398.",
     "International Journal of Production Economics, 76"),
    ("Forza, C. and Salvador, F. (2007). Product Information Management for Mass Customization. Palgrave Macmillan.",
     "Forza, C., & Salvador, F. (2007). Product information management for mass customization. Palgrave Macmillan.",
     "Product information management for mass customization"),
    ("Goddard, K., Roudsari, A. and Wyatt, J.C. (2012). Automation bias: a systematic review of frequency, effect mediators, and mitigators. Journal of the American Medical Informatics Association, 19(1), 121\u2013127.",
     "Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation bias: A systematic review of frequency, effect mediators, and mitigators. Journal of the American Medical Informatics Association, 19(1), 121\u2013127.",
     "Journal of the American Medical Informatics Association, 19"),
    ("Hicks, C., McGovern, T. and Earl, C.F. (2000). Supply chain management: a strategic issue in engineer to order manufacturing. International Journal of Production Economics, 65(2), 179\u2013190.",
     "Hicks, C., McGovern, T., & Earl, C. F. (2000). Supply chain management: A strategic issue in engineer to order manufacturing. International Journal of Production Economics, 65(2), 179\u2013190.",
     "International Journal of Production Economics, 65"),
    ("Jaume, G., Ekenel, H.K. and Thiran, J.-P. (2019). FUNSD: a dataset for form understanding in noisy scanned documents. ICDAR Workshops.",
     "Jaume, G., Ekenel, H. K., & Thiran, J.-P. (2019). FUNSD: A dataset for form understanding in noisy scanned documents. In 2019 International Conference on Document Analysis and Recognition Workshops (ICDARW) (Vol. 2, pp. 1\u20136). IEEE.",
     "2019 International Conference on Document Analysis and Recognition Workshops (ICDARW)"),
    ("Kim, G. et al. (2022). OCR-free document understanding transformer (Donut). European Conference on Computer Vision.",
     "Kim, G., Hong, T., Yim, M., Nam, J., Park, J., Yim, J., Hwang, W., Yun, S., Han, D., & Park, S. (2022). OCR-free document understanding transformer. In Computer Vision \u2013 ECCV 2022 (pp. 498\u2013517). Springer.",
     "Computer Vision \u2013 ECCV 2022"),
    ("Mathew, M., Karatzas, D. and Jawahar, C.V. (2021). DocVQA: a dataset for VQA on document images. IEEE/CVF WACV.",
     "Mathew, M., Karatzas, D., & Jawahar, C. V. (2021). DocVQA: A dataset for VQA on document images. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) (pp. 2200\u20132209). IEEE.",
     "Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)"),
    ("Parasuraman, R. and Riley, V. (1997). Humans and automation: use, misuse, disuse, abuse. Human Factors, 39(2), 230\u2013253.",
     "Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. Human Factors, 39(2), 230\u2013253.",
     "Human Factors, 39"),
    ("Parasuraman, R., Sheridan, T.B. and Wickens, C.D. (2000). A model for types and levels of human interaction with automation. IEEE Transactions on Systems, Man, and Cybernetics, Part A, 30(3), 286\u2013297.",
     "Parasuraman, R., Sheridan, T. B., & Wickens, C. D. (2000). A model for types and levels of human interaction with automation. IEEE Transactions on Systems, Man, and Cybernetics, Part A: Systems and Humans, 30(3), 286\u2013297.",
     "IEEE Transactions on Systems, Man, and Cybernetics, Part A: Systems and Humans, 30"),
    ("Sarkar, M.B., Butler, B. and Steinfield, C. (1995). Intermediaries and cybermediaries: a continuing role for mediating players in the electronic marketplace. Journal of Computer-Mediated Communication, 1(3).",
     "Sarkar, M. B., Butler, B., & Steinfield, C. (1995). Intermediaries and cybermediaries: A continuing role for mediating players in the electronic marketplace. Journal of Computer-Mediated Communication, 1(3).",
     "Journal of Computer-Mediated Communication, 1"),
    ("Skitka, L.J., Mosier, K.L. and Burdick, M. (1999). Does automation bias decision-making? International Journal of Human-Computer Studies, 51(5), 991\u20131006.",
     "Skitka, L. J., Mosier, K. L., & Burdick, M. (1999). Does automation bias decision-making? International Journal of Human-Computer Studies, 51(5), 991\u20131006.",
     "International Journal of Human-Computer Studies, 51"),
    ("Xu, Y. et al. (2020). LayoutLM: pre-training of text and layout for document image understanding. ACM SIGKDD.",
     "Xu, Y., Li, M., Cui, L., Huang, S., Wei, F., & Zhou, M. (2020). LayoutLM: Pre-training of text and layout for document image understanding. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 1192\u20131200). ACM.",
     "Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining"),
]

INTEXT = [
    ("(Benjamin and Wigand, 1995)", "(Benjamin & Wigand, 1995)"),
    ("(Sarkar, Butler and Steinfield, 1995)", "(Sarkar et al., 1995)"),
    ("(Hicks, McGovern and Earl, 2000)", "(Hicks et al., 2000)"),
    ("(Forza and Salvador, 2002; 2007)", "(Forza & Salvador, 2002, 2007)"),
    ("(Xu et al., 2020; Kim et al., 2022; Mathew et al., 2021; Jaume et al., 2019)",
     "(Jaume et al., 2019; Kim et al., 2022; Mathew et al., 2021; Xu et al., 2020)"),
    ("(Parasuraman and Riley, 1997)", "(Parasuraman & Riley, 1997)"),
    ("(Goddard, Roudsari and Wyatt, 2012)", "(Goddard et al., 2012)"),
    ("(Skitka, Mosier and Burdick, 1999)", "(Skitka et al., 1999)"),
    # D12 leftover in 5.3
    ("it supplies the priors the 8.1 audit maps onto the distributor's own document mix",
     "it supplies the priors that 8.1 maps onto the distributor's own document mix"),
]

EDITS = ([{"find": o, "replace": n} for o, n in INTEXT]
         + [{"find": o, "replace": n, "unbold": True} for o, n, _ in REFS])


def italicize(apply):
    """Pass 2: italicize journal/book/proceedings name + volume per APA."""
    svc = get_service(write=apply)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    reqs, ok = [], True
    for _, new, span in REFS:
        # find the span inside the new reference entry (entry text is unique)
        rng, n = find_text_range(doc, new)
        if rng is None:
            print(f"FAIL entry ({n}): {new[:60]!r}")
            ok = False
            continue
        off = new.find(span)
        s = rng[0] + off
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": s, "endIndex": s + len(span)},
            "textStyle": {"italic": True}, "fields": "italic"}})
        print(f"italic ok: {span[:60]!r}")
    if not ok or not apply:
        print("italics: DRY RUN or failures; not applied" if not apply else "aborted")
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
