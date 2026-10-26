#!/usr/bin/env python3
"""Rebuild Exhibit 4.3 (root-cause driver tree) compact and legible.

Designed in points at the doc's 450 pt text width so fonts print at true
size. Four cause cards sized to their wrapped text feed the observed-outcome
card on the right. Content is unchanged from the previous exhibit: 41% of
defects from extraction, 1.5 h reading per inquiry, 86% queue share, 41 wh
median clarification loss, 38% loop share, ~3.1% of revenue leaked,
4-18% discount spread.
"""
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.textpath import TextPath

TEAL = "#16606b"
BAND = "#e9f1f2"
GREY = "#4d5d61"
INK = "#22333b"

W = 450.0
HEAD_FS, BODY_FS = 8.5, 7.5
LINE_H = 10.0

CAUSES = [
    ("RC1 \u00b7 Unstructured inputs",
     "Specs arrive as PDF, CAD and free-text email, and every field is "
     "re-keyed by hand. Drives 41% of defects and 1.5 h of reading per "
     "inquiry."),
    ("RC2 \u00b7 Serial expert bottleneck",
     "One estimator owns each inquiry end-to-end, so work waits for the "
     "person, not the task. 86% of elapsed time is queue, concentrated in "
     "engineering."),
    ("RC3 \u00b7 Clarification ping-pong",
     "Missing data is found mid-process, one gap at a time. A median 41\u00a0wh "
     "is lost per loop, and 38% of inquiries need at least "
     "one."),
    ("RC4 \u00b7 No pricing discipline",
     "Discounts are set case-by-case without reference points. The largest "
     "single margin leak, invisible because each decision looks reasonable "
     "alone."),
]

OUTCOME = ("Observed outcome",
           ["5 working days elapsed per quote, ~5.5 hours actually worked.",
            "Quality cost and discount leakage \u2248 3.1% of revenue.",
            "Discount spread 4\u201318% on like jobs."])

CARD_X, CARD_W = 0.0, 268.0
OUT_X, OUT_W = 304.0, 146.0
PAD, GAP = 8.0, 10.0

BOLD = FontProperties(weight="bold")
NORM = FontProperties()


def wrap(text, width_pt, size):
    for chars in range(70, 10, -1):
        lines = textwrap.wrap(text, chars, break_on_hyphens=False)
        if all(TextPath((0, 0), ln, size=size,
                        prop=NORM).get_extents().width <= width_pt
               for ln in lines):
            return lines
    raise ValueError(text)


def main():
    cause_lines = [(h, wrap(b, CARD_W - 2 * PAD, BODY_FS)) for h, b in CAUSES]
    n_body = max(len(ls) for _, ls in cause_lines)
    card_h = PAD + 13 + n_body * LINE_H + PAD - 2       # header + body

    out_stanzas = [wrap(s, OUT_W - 2 * PAD, BODY_FS) for s in OUTCOME[1]]
    out_lines = sum(len(s) for s in out_stanzas)
    out_h = PAD + 15 + out_lines * LINE_H + (len(out_stanzas) - 1) * 5 + PAD

    title_h = 20.0
    H = title_h + 4 * card_h + 3 * GAP + 6

    fig, ax = plt.subplots(figsize=(6.25, H / 72.0), dpi=300)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    ax.text(0, H - 8, "Root-cause driver tree", fontsize=9.5,
            fontweight="bold", color=TEAL, ha="left", va="center")

    tops = []
    y = H - title_h
    for (head, lines) in cause_lines:
        top = y
        ax.add_patch(FancyBboxPatch(
            (CARD_X + 1, top - card_h), CARD_W, card_h,
            boxstyle="round,pad=0.6,rounding_size=3", fc="white", ec=TEAL,
            lw=1.2, zorder=2))
        ax.text(CARD_X + PAD, top - PAD - 4, head, fontsize=HEAD_FS,
                fontweight="bold", color=TEAL, ha="left", va="center",
                zorder=3)
        for k, ln in enumerate(lines):
            ax.text(CARD_X + PAD, top - PAD - 15 - k * LINE_H, ln,
                    fontsize=BODY_FS, color=INK, ha="left", va="center",
                    zorder=3)
        tops.append(top)
        y -= card_h + GAP

    # outcome card, centred on the stack
    stack_mid = (tops[0] + (tops[-1] - card_h)) / 2
    ot = stack_mid + out_h / 2
    ax.add_patch(FancyBboxPatch(
        (OUT_X, ot - out_h), OUT_W - 1, out_h,
        boxstyle="round,pad=0.6,rounding_size=3", fc=BAND, ec=TEAL,
        lw=1.4, zorder=2))
    ax.text(OUT_X + PAD, ot - PAD - 5, OUTCOME[0], fontsize=HEAD_FS,
            fontweight="bold", color=TEAL, ha="left", va="center", zorder=3)
    yy = ot - PAD - 17
    for stanza in out_stanzas:
        for ln in stanza:
            ax.text(OUT_X + PAD, yy, ln, fontsize=BODY_FS, color=INK,
                    ha="left", va="center", zorder=3)
            yy -= LINE_H
        yy -= 5

    # arrows: each cause to an even landing on the outcome's left edge
    lands = [ot - out_h * (0.2 + 0.2 * i) for i in range(4)]
    for top, land in zip(tops, lands):
        ax.add_patch(FancyArrowPatch(
            (CARD_X + CARD_W + 3, top - card_h / 2), (OUT_X - 2, land),
            arrowstyle="-|>", mutation_scale=11, lw=1.3, color=GREY,
            shrinkA=0, shrinkB=0, zorder=1,
            connectionstyle="arc3,rad=0.0"))

    fig.savefig("simulator/figures/fig_drivertree.png",
                bbox_inches="tight", pad_inches=0.04, facecolor="white")
    print(f"written: simulator/figures/fig_drivertree.png ({W:g}x{H:g} pt)")


if __name__ == "__main__":
    main()
