"""Auto-calibration of the as-is residual-queue parameters.

Six knobs (residual queue median and sigma per tier) against six targets
(cycle median and P90 per tier, BASE-15/16). Damped iterative updates:
medians move additively toward the target gap, sigmas move on the log-ratio
of P90s. Touch, cost per quote and queue share follow from the same fits and
are asserted by the test suite rather than tuned separately.
"""
import math

from .asis import AsIsModel, TIERS
from .config import load_asis, save_fitted


def fit(years=6, iterations=16, verbose=True):
    p = load_asis()
    tgt_med = p["calibration_targets"]["cycle_median_wh"]
    tgt_p90 = p["calibration_targets"]["cycle_p90_wh"]

    # initial guess: whatever noticing + touch + a few hours of desk queue
    # do not explain
    med = {t: max(0.3, tgt_med[t] - p["notice_delay"]["median_wh"]
                  - p["touch_median_h"][t] - 4.0)
           for t in TIERS}
    sig = {t: 0.9 for t in TIERS}

    for i in range(iterations):
        p["fitted"] = {
            "residual_queue_median_wh": {t: float(med[t]) for t in TIERS},
            "residual_queue_sigma": {t: float(sig[t]) for t in TIERS},
        }
        s = AsIsModel(p, seed=1000 + i).run(years=years)
        summ = s.summary(p["hourly_rate_eur"])
        worst = 0.0
        for t in TIERS:
            e_med = summ["cycle_median_wh"][t] - tgt_med[t]
            r_p90 = summ["cycle_p90_wh"][t] / tgt_p90[t]
            worst = max(worst, abs(e_med) / tgt_med[t], abs(math.log(r_p90)))
            med[t] = max(0.3, med[t] - 0.7 * e_med)
            sig[t] = min(2.2, max(0.15, sig[t] - 0.5 * math.log(r_p90)))
        if verbose:
            print(f"iter {i:2d}  worst rel err {worst:5.1%}  "
                  + "  ".join(f"{t}: med {summ['cycle_median_wh'][t]:5.1f}/{tgt_med[t]}"
                              f" p90 {summ['cycle_p90_wh'][t]:6.1f}/{tgt_p90[t]}"
                              for t in TIERS))
        if worst < 0.04:
            break

    fitted = {
        "residual_queue_median_wh": {t: round(float(med[t]), 2) for t in TIERS},
        "residual_queue_sigma": {t: round(float(sig[t]), 3) for t in TIERS},
    }
    save_fitted(fitted)
    from .manifest import write_manifest
    write_manifest("fit", seed=1000, years=years, extra={"fitted": fitted})
    if verbose:
        print("fitted parameters written to data/fitted_asis.yaml")
    p["fitted"] = fitted
    return p
