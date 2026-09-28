"""Capability layer: document quality, per-field extraction and confidence,
and the 7.7 routing. Pure draws, no simulation clock; sim/tobe.py owns time.

The confidence model is the load-bearing piece: scores correlate with
correctness (correct fields cluster near 1, wrong fields spread around 0.5),
so routing on minimum field confidence does real work and confidently-wrong
fields are rare but present - they are what the residual-defect model feeds on.
"""
from dataclasses import dataclass

import numpy as np

DOC_CLASSES = ("clean_digital", "scanned", "fragmented", "cad_dependent")


@dataclass
class DocsDraw:
    doc_class: str
    n_fields: int
    n_systems: int
    correct: np.ndarray       # bool per field (CAD-locked fields are False)
    confidence: np.ndarray    # float per field
    flagged: np.ndarray       # bool per field (confidence < flag threshold)

    @property
    def min_confidence(self):
        return float(self.confidence.min())

    @property
    def extracted_share(self):
        return float(self.correct.mean())


def _pick_weighted(rng, mix):
    """Sample a key from {key: prob} without np.random.choice's per-call array
    construction (this is on the hot path, once per inquiry)."""
    u = rng.random()
    cum = 0.0
    last = None
    for k, v in mix.items():
        cum += v
        last = k
        if u < cum:
            return k
    return last   # guard against float rounding on the final bucket


def draw_docs(rng, tier, pt, variant, extraction_override=None):
    mix = pt["doc_class_mix"][tier]
    doc_class = _pick_weighted(rng, mix)
    lo, hi = pt["systems_per_inquiry"][tier]
    n_systems = int(rng.integers(lo, hi + 1))
    n_fields = n_systems * pt["fields_per_system"]

    if extraction_override is not None:
        p_succ = extraction_override
    else:
        p_succ = pt["extraction_success"][doc_class][variant]

    n_locked = pt["cad_locked_fields_per_system"] * n_systems \
        if doc_class == "cad_dependent" else 0
    n_ext = n_fields - n_locked

    correct = rng.random(n_ext) < p_succ
    c = pt["confidence"]
    conf_correct = 1.0 - c["correct"]["eps_scale"] * rng.beta(
        c["correct"]["eps_beta_a"], c["correct"]["eps_beta_b"], n_ext)
    conf_wrong = rng.beta(c["wrong"]["beta_a"], c["wrong"]["beta_b"], n_ext)
    confidence = np.where(correct, conf_correct, conf_wrong)

    if n_locked:
        lo_c, hi_c = c["cad_locked_conf"]
        locked_conf = rng.uniform(lo_c, hi_c, n_locked)
        confidence = np.concatenate([confidence, locked_conf])
        correct = np.concatenate([correct, np.zeros(n_locked, dtype=bool)])

    flagged = confidence < pt["residual_defects"]["flag_threshold"]
    return DocsDraw(doc_class, n_fields, n_systems, correct, confidence, flagged)


def draw_value_eur(rng, tier, pt):
    band = pt["value_bands_eur"][tier]
    if tier == "tier3":
        mega = pt["value_bands_eur"]["mega"]
        if rng.random() < mega["per_year"] / mega["of_tier3_per_year"]:
            return float(rng.uniform(*mega["value_range"]))
    v = band["median"] * float(np.exp(band["sigma"] * rng.standard_normal()))
    return float(np.clip(v, band["min"], band["max"]))


def decide_route(rng, tier, value_eur, docs, pt, variant):
    """The 7.7 routing: auto-draft / assisted / manual. The business does not
    offer discounts, so auto-drafting is gated only on field confidence, tier
    and the value gate (no discount-band condition)."""
    r = pt["routing"]
    if (docs.min_confidence >= r["C1"] and tier == "tier1"
            and value_eur < r["V1_eur"]):
        return "auto"
    if tier in ("tier1", "tier2") and docs.min_confidence >= r["C2"]:
        return "assisted"
    return "manual"   # Tier 3, CAD-dependent, low confidence -> senior review


def draw_asis_defects(rng, tier, pt, incidence_mult=1.0):
    """Cluster model for the manual lane: BASE-19 incidence, classes
    co-occurring per the 4.4 chain (calibrated to BASE-28/29).

    incidence_mult (<=1) scales the overall defect incidence: the to-be manual
    lane passes 1 - (manual prefill credit) so validated AI prefill lowers the
    error rate even for manually-produced quotes; the as-is baseline passes 1.0
    (unchanged)."""
    d = pt["asis_defects"]
    if rng.random() >= d["p_defective"][tier] * incidence_mult:
        return []
    return [cls for cls, p in d["class_given_defective"].items()
            if rng.random() < p]


def draw_system_defects(rng, docs, reviewer, route, pt, error_mult,
                        class_mult=None):
    """Residual defects in the auto/assisted lanes: wrong fields that survive
    review, plus small system rates for calc/selection/pricing.

    class_mult (per-class, <=1) scales the deterministic system rates: the
    to-be model passes 1 - software_defect_reduction so the calc engine,
    reference catalogue and rules-based pricing cut those error classes."""
    cm = class_mult or {}
    rd = pt["residual_defects"]
    defects = []
    wrong = ~docs.correct
    if wrong.any():
        if route == "auto":
            miss_p = rd["reviewer_miss"]["auto_one_click"][reviewer]
            miss = rng.random(int(wrong.sum())) < min(1.0, miss_p * error_mult)
            survived = miss.any()
        else:
            survived = False
            for flag in docs.flagged[wrong]:
                key = "flagged" if flag else "unflagged"
                p = min(1.0, rd["reviewer_miss"][key][reviewer] * error_mult)
                if rng.random() < p:
                    survived = True
                    break
        if survived:
            defects.append("extraction")
    if rng.random() < rd["calc_rate_system"] * cm.get("calculation", 1.0):
        defects.append("calculation")
    if rng.random() < rd["selection_rate_system"] * cm.get("selection", 1.0):
        defects.append("selection")
    if rng.random() < rd["pricing_rate_system"] * cm.get("pricing", 1.0):
        defects.append("pricing")
    return defects
