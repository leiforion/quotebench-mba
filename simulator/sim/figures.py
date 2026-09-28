"""SIM-6: export the four paper figures, sized for the Doc (6.5in wide).

  figures/fig_calibration.png   measured vs simulated gate table
  figures/fig_cycletimes.png    cycle-time distributions, as-is vs to-be
  figures/fig_npv_fan.png       NPV@12% Monte Carlo distribution + percentiles
  figures/fig_tornado.png       one-at-a-time NPV@12% sensitivity
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .config import BASE, load_asis, load_econ, load_tobe
from .economics import build_anchors, mc_from_anchors
from .stress import fin_centrals, tornado
from .tobe import ToBeModel

FIG_DIR = os.path.join(BASE, "figures")
TIERS = ("tier1", "tier2", "tier3")
GREY, BLUE = "#8a8a8a", "#1f5fa8"


def _save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path}")
    return path


def fig_calibration(gate_rows):
    """gate_rows: (metric, tier, measured, simulated, verdict)."""
    fig, ax = plt.subplots(figsize=(6.5, 0.32 * len(gate_rows) + 0.8))
    ax.axis("off")
    table = ax.table(
        cellText=[[m, t, str(me), str(si), v] for m, t, me, si, v in gate_rows],
        colLabels=["Metric", "Tier", "Measured", "Simulated", "Gate"],
        loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.25)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#cccccc")
        if r == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#eef2f7")
        elif c == 4 and "PASS" in cell.get_text().get_text():
            cell.set_text_props(color="#1a7a2e")
    ax.set_title("Calibration gate: measured baseline vs simulated as-is",
                 fontsize=10, pad=10)
    return _save(fig, "fig_calibration.png")


def fig_cycletimes(asis_recs, tobe_recs):
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.4), sharey=False)
    labels = {"tier1": "Tier 1 (simple)", "tier2": "Tier 2 (standard)",
              "tier3": "Tier 3 (engineered)"}
    for ax, tier in zip(axes, TIERS):
        a = [r.cycle_wh for r in asis_recs if r.tier == tier]
        b = [r.cycle_wh for r in tobe_recs if r.tier == tier]
        hi = np.percentile(a, 98)
        bins = np.linspace(0, hi, 32)
        ax.hist(a, bins=bins, density=True, alpha=0.55, color=GREY,
                label="as-is")
        ax.hist(b, bins=bins, density=True, alpha=0.55, color=BLUE,
                label="to-be")
        ax.axvline(np.median(a), color=GREY, lw=1.2, ls="--")
        ax.axvline(np.median(b), color=BLUE, lw=1.2, ls="--")
        ax.set_title(labels[tier], fontsize=9)
        ax.set_xlabel("cycle time (working hours)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.set_yticks([])
    axes[0].legend(fontsize=8, frameon=False)
    fig.suptitle("Quote cycle-time distributions: as-is vs to-be (central case)",
                 fontsize=10)
    fig.tight_layout()
    return _save(fig, "fig_cycletimes.png")


def fig_waterfall(medians):
    """9.2 benefits waterfall from the P&L benefit medians (EUR/yr). The
    business offers no discounts, so there is no pricing-recovery bar."""
    labels = ["Engineering\ncapacity", "Error\ncost",
              "Win-rate\nuplift", "Total\n(central)"]
    vals = [medians["labour_redeploy"], medians["quality_savings"],
            medians["win_uplift_margin"]]
    total = sum(vals)
    n = len(vals)
    fig, ax = plt.subplots(figsize=(6.5, 2.8))
    left = 0.0
    for i, v in enumerate(vals):
        ax.bar(i, v / 1000, bottom=left / 1000, color=BLUE, alpha=0.8, width=0.6)
        ax.text(i, (left + v / 2) / 1000, f"{v/1000:,.0f}k", ha="center",
                va="center", fontsize=8, color="white", weight="bold")
        left += v
    ax.bar(n, total / 1000, color="#2e7d46", alpha=0.85, width=0.6)
    ax.text(n, total / 2000, f"{total/1000:,.0f}k", ha="center", va="center",
            fontsize=8, color="white", weight="bold")
    ax.set_xticks(range(n + 1))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("EUR thousands / year", fontsize=8)
    ax.tick_params(labelsize=8)
    ax.set_title("Projected annual benefits at full adoption, central case "
                 "(all simulated)", fontsize=10)
    fig.tight_layout()
    return _save(fig, "fig_waterfall.png")


def fig_npv_fan(npv12):
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    ax.hist(npv12 / 1000, bins=80, color=BLUE, alpha=0.7, density=True)
    for p, lab in ((10, "P10"), (50, "P50"), (90, "P90")):
        v = np.percentile(npv12, p) / 1000
        ax.axvline(v, color="#333333", lw=1.1, ls="--")
        ax.text(v, ax.get_ylim()[1] * 0.95, f" {lab}: {v:,.0f}k",
                fontsize=8, va="top")
    ax.axvline(0, color="#b03030", lw=1.4)
    ax.set_xlabel("five-year NPV at 12% (EUR thousands)", fontsize=9)
    ax.set_yticks([])
    ax.set_title("NPV distribution, 20,000 Monte Carlo draws", fontsize=10)
    fig.tight_layout()
    return _save(fig, "fig_npv_fan.png")


def fig_tornado(tor, base_npv):
    items = sorted(tor.items(), key=lambda kv: kv[1][1] - kv[1][0])
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    for i, (name, (lo, hi)) in enumerate(items):
        ax.barh(i, (hi - lo) / 1000, left=lo / 1000, color=BLUE, alpha=0.75,
                height=0.55)
    ax.axvline(base_npv / 1000, color="#333333", lw=1.1, ls="--",
               label=f"central case ({base_npv/1000:,.0f}k)")
    ax.axvline(0, color="#b03030", lw=1.4)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([k for k, _ in items], fontsize=8.5)
    ax.set_xlabel("NPV@12% (EUR thousands), one-at-a-time low/high", fontsize=9)
    ax.set_title("Sensitivity tornado", fontsize=10)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.tight_layout()
    return _save(fig, "fig_tornado.png")


def export_all(seed=42, jobs=None):
    from .report import gate_rows
    pa, pt, pe = load_asis(), load_tobe(), load_econ()

    print("figures: calibration table...")
    fig_calibration(gate_rows(seed=seed))

    print("figures: cycle-time distributions (1 seed, 8y)...")
    asis_res = ToBeModel(pt, pa, seed=seed, degraded=True).run(years=8)
    tobe_res = ToBeModel(pt, pa, variant="central", seed=seed).run(years=8)
    fig_cycletimes(asis_res.records, tobe_res.records)

    print("figures: anchors + Monte Carlo (npv fan, tornado)...")
    from .infra import cost_model
    infra_annual = cost_model()["annual_full_eur"]
    asis, anchors, scale = build_anchors(pe, pt, pa, jobs=jobs)
    mc = mc_from_anchors(pe, asis, anchors, scale, seed=seed,
                         return_draws=True, infra_annual_eur=infra_annual)
    fig_npv_fan(mc["npv12_draws"])
    fig_waterfall(mc["benefit_medians"])
    tor = tornado(pe, asis, anchors, scale, infra_annual_eur=infra_annual)
    base_npv = np.median(mc["npv12_draws"])
    fig_tornado(tor, base_npv)
    print("done.")
