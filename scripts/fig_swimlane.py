#!/usr/bin/env python3
"""Regenerate Exhibit 4.1 (as-is RFQ swimlane) legibly at print size.

Designed at 6.25 x 4.5 in (the doc's ~450 pt text width) so fonts render at
their true point size when printed. Each box is sized from its measured text
extents plus padding, and boxes are staggered rather than column-aligned so
every label sits fully inside its box with clear gaps between boxes.
Values are the Tier 2 medians from the observation study, identical to the
previous exhibit: touch sums to 5.5 h (BASE-17), assignment queue 14 wh
(BASE-25), clarification wait 41 wh (BASE-24), 38% loop share (BASE-26).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.textpath import TextPath

TEAL = "#16606b"
BAND = "#e9f1f2"
ORANGE = "#c96a1f"
GREY = "#4d5d61"
INK = "#22333b"

LANES = ["Management", "Pricing", "Engineering", "Sales", "Contractor"]
LANE_Y = {name: i for i, name in enumerate(LANES)}  # bottom -> top

X_RANGE = 10.45          # axis units across 450 pt of print width
PT = 450.0 / X_RANGE     # points per axis unit
PAD_PT = 13.0            # horizontal padding inside a box, total
NAME_FS, SUB_FS, TIME_FS = 7.0, 6.7, 6.7

# id: (x_centre, lane, name_lines, touch, queue, kind)
BOXES = {
    "rfq":      (0.95, "Contractor", ["RFQ sent", "(email, PDF, CAD)"], None, None, "endpoint"),
    "receive":  (0.95, "Sales", ["Receive & log"], 0.2, 3.5, "main"),
    "triage":   (2.80, "Sales", ["Triage & assign"], 0.3, 14, "main"),
    "read":     (2.94, "Engineering", ["Read & extract", "specs, drawings"], 1.5, 6, "main"),
    "clarify":  (4.92, "Engineering", ["Clarification", "request"], 0.4, 41, "main"),
    "replies":  (4.92, "Contractor", ["Contractor", "replies"], None, None, "loop"),
    "headloss": (6.90, "Engineering", ["Head-loss", "calculation"], 1.0, 9, "main"),
    "select":   (8.87, "Engineering", ["Model selection", "(mfr. software)"], 0.8, 4, "main"),
    "pricing":  (8.87, "Pricing", ["Pricing &", "discount"], 0.5, 11, "main"),
    "approval": (8.87, "Management", ["Approval", "(high value)"], 0.2, 8, "loop"),
    "assemble": (9.55, "Sales", ["Assemble &", "send quote"], 0.6, 5, "main"),
    "quote":    (9.55, "Contractor", ["Quote received"], None, None, "endpoint"),
}

BH, YC = 0.78, 0.44
BOLD = FontProperties(weight="bold")
NORM = FontProperties()


def text_w(s, size, bold=True):
    return TextPath((0, 0), s, size=size,
                    prop=BOLD if bold else NORM).get_extents().width


def box_w(bid):
    x, lane, lines, touch, queue, kind = BOXES[bid]
    widths = [text_w(lines[0], NAME_FS if kind != "endpoint" else 7.4)]
    for extra in lines[1:]:
        widths.append(text_w(extra, NAME_FS if kind != "endpoint" else SUB_FS,
                             bold=(kind != "endpoint")))
    if touch is not None:
        widths.append(text_w(f"queue {queue:g} h", TIME_FS, bold=False))
        widths.append(text_w(f"touch {touch:g} h", TIME_FS, bold=False))
    return (max(widths) + PAD_PT) / PT


def centre(bid):
    x, lane = BOXES[bid][0], BOXES[bid][1]
    return x, LANE_Y[lane] + YC


def edge(bid, side):
    x, y = centre(bid)
    w = box_w(bid)
    return {"top": (x, y + BH / 2), "bottom": (x, y - BH / 2),
            "left": (x - w / 2, y), "right": (x + w / 2, y)}[side]


def arrow(ax, p, q, dashed=False):
    ax.add_patch(FancyArrowPatch(
        p, q, arrowstyle="-|>", mutation_scale=10, shrinkA=2, shrinkB=2,
        lw=1.4, color=ORANGE if dashed else GREY,
        linestyle=(0, (3.5, 2.2)) if dashed else "solid", zorder=3))


def main():
    # sanity: gaps within each lane
    by_lane = {}
    for bid, spec in BOXES.items():
        by_lane.setdefault(spec[1], []).append(bid)
    for lane, ids in by_lane.items():
        ids.sort(key=lambda b: BOXES[b][0])
        for a, b in zip(ids, ids[1:]):
            gap = (BOXES[b][0] - box_w(b) / 2) - (BOXES[a][0] + box_w(a) / 2)
            print(f"{lane:12s} {a:>8s}|{b:<8s} gap {gap * PT:5.1f} pt")
            assert gap * PT > 8, f"boxes {a}/{b} too close"

    fig, ax = plt.subplots(figsize=(6.25, 4.5), dpi=300)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(-0.05, X_RANGE)
    ax.set_ylim(-0.30, 5.62)
    ax.axis("off")

    for name, i in LANE_Y.items():
        if i % 2 == 0:
            ax.axhspan(i, i + 1, color=BAND, zorder=0)
        ax.plot([-0.05, X_RANGE], [i, i], color="#c3d2d4", lw=0.6, zorder=1)
        ax.text(0.08, i + 0.91, name.upper(), fontsize=6.4, fontweight="bold",
                color=TEAL, ha="left", va="center", alpha=0.85)
    ax.plot([-0.05, X_RANGE], [5, 5], color="#c3d2d4", lw=0.6, zorder=1)

    for bid, (x, lane, lines, touch, queue, kind) in BOXES.items():
        _, y = centre(bid)
        w = box_w(bid)
        contractor = lane == "Contractor"
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - BH / 2), w, BH,
            boxstyle="round,pad=0.012,rounding_size=0.05",
            fc="#fdf6ef" if contractor else "white",
            ec=ORANGE if contractor else TEAL, lw=1.15,
            linestyle=(0, (3.5, 2.2)) if kind == "loop" else "solid",
            zorder=2))
        if touch is None:
            if len(lines) > 1:
                ax.text(x, y + 0.12, lines[0], ha="center", va="center",
                        fontsize=7.4, fontweight="bold", color=INK, zorder=4)
                ax.text(x, y - 0.16, lines[1], ha="center", va="center",
                        fontsize=SUB_FS, color=INK, zorder=4)
            else:
                ax.text(x, y, lines[0], ha="center", va="center",
                        fontsize=7.4, fontweight="bold", color=INK, zorder=4)
        else:
            ax.text(x, y + 0.18, "\n".join(lines), ha="center", va="center",
                    fontsize=NAME_FS, fontweight="bold", color=INK,
                    linespacing=1.15, zorder=4)
            ax.text(x, y - 0.185, f"touch {touch:g} h\nqueue {queue:g} h",
                    ha="center", va="center", fontsize=TIME_FS, color=GREY,
                    linespacing=1.25, zorder=4)

    # main flow
    arrow(ax, edge("rfq", "bottom"), edge("receive", "top"))
    arrow(ax, edge("receive", "right"), edge("triage", "left"))
    arrow(ax, edge("triage", "bottom"), edge("read", "top"))
    arrow(ax, edge("read", "right"), edge("clarify", "left"))
    arrow(ax, edge("clarify", "right"), edge("headloss", "left"))
    arrow(ax, edge("headloss", "right"), edge("select", "left"))
    arrow(ax, edge("select", "bottom"), edge("pricing", "top"))
    arrow(ax, edge("pricing", "right"), edge("assemble", "bottom"))
    arrow(ax, edge("assemble", "top"), edge("quote", "bottom"))

    # clarification loop (38% of inquiries)
    xc, _ = centre("clarify")
    ct = edge("clarify", "top")
    cb = edge("replies", "bottom")
    arrow(ax, (xc - 0.22, ct[1]), (xc - 0.22, cb[1]), dashed=True)
    arrow(ax, (xc + 0.22, cb[1]), (xc + 0.22, ct[1]), dashed=True)
    ax.text(xc + 0.42, (ct[1] + cb[1]) / 2 + 0.26, "38% of\ninquiries",
            fontsize=6.4, style="italic", color=ORANGE, ha="left",
            va="center", linespacing=1.15)

    # approval loop
    arrow(ax, edge("pricing", "bottom"), edge("approval", "top"), dashed=True)
    arrow(ax, edge("approval", "right"), edge("assemble", "bottom"),
          dashed=True)

    ax.text(-0.05, 5.36, "As-is RFQ process (median working hours per step)",
            fontsize=9.0, fontweight="bold", color=TEAL, ha="left",
            va="center")
    ax.text(X_RANGE, -0.16, "touch = someone working on the inquiry \u00b7 "
            "queue = the inquiry waiting \u00b7 dashed = subset of inquiries",
            fontsize=6.4, color=GREY, ha="right", va="center")

    fig.savefig("simulator/figures/fig_swimlane_asis.png",
                bbox_inches="tight", pad_inches=0.04, facecolor="white")
    print("written: simulator/figures/fig_swimlane_asis.png")


if __name__ == "__main__":
    main()
