"""SIM-1 calibration gate. Every assertion maps to a measured register row;
tolerance ±10% (±8% on annual volume). The CLI refuses to run to-be scenarios
while any of these fail.
"""
import pytest

from sim.asis import AsIsModel, TIERS
from sim.config import load_asis, is_fitted

TOL = 0.10


@pytest.fixture(scope="module")
def summary():
    p = load_asis()
    assert is_fitted(p), "run `python -m sim fit` first"
    res = AsIsModel(p, seed=42).run(years=12)
    return p, res.summary(p["hourly_rate_eur"])


@pytest.mark.parametrize("tier", TIERS)
def test_cycle_median(summary, tier):
    p, s = summary
    tgt = p["calibration_targets"]["cycle_median_wh"][tier]
    assert abs(s["cycle_median_wh"][tier] - tgt) <= TOL * tgt


@pytest.mark.parametrize("tier", TIERS)
def test_cycle_p90(summary, tier):
    p, s = summary
    tgt = p["calibration_targets"]["cycle_p90_wh"][tier]
    assert abs(s["cycle_p90_wh"][tier] - tgt) <= TOL * tgt


@pytest.mark.parametrize("tier", TIERS)
def test_touch_median(summary, tier):
    p, s = summary
    tgt = p["calibration_targets"]["touch_median_h"][tier]
    assert abs(s["touch_median_h"][tier] - tgt) <= TOL * tgt


@pytest.mark.parametrize("tier", TIERS)
def test_cost_per_quote(summary, tier):
    p, s = summary
    tgt = p["calibration_targets"]["cost_per_quote_eur"][tier]
    assert abs(s["cost_per_quote_eur"][tier] - tgt) <= TOL * tgt


def test_annual_volume(summary):
    p, s = summary
    tgt = p["calibration_targets"]["annual_inquiries"]
    assert abs(s["annual_inquiries"] - tgt) <= 0.08 * tgt


def test_queue_share(summary):
    p, s = summary
    lo = p["calibration_targets"]["queue_share_pct"]["low"]
    hi = p["calibration_targets"]["queue_share_pct"]["high"]
    for t in TIERS:
        assert lo <= s["queue_share_pct"][t] <= hi


def test_utilization_feasible(summary):
    _, s = summary
    assert 0.4 < s["utilization"] < 1.0
