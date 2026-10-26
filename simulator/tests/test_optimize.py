"""SIM-5 gates: selection and constraint logic (pure functions, no DES)."""
from sim.optimize import select_optimum


ASIS_MAT = {"tier1": 0.05, "tier2": 0.095, "tier3": 0.159}


def row(c1, c2, p50, p10h, error_cost, cap=1_000_000, mat=None, asis_mat=None):
    # D24 dual gate: error COST <= as-is cap AND no tier's material defect rate
    # above as-is. Default mat is comfortably below the as-is caps.
    return {"c1": c1, "c2": c2, "p50": p50, "p10_hurdle": p10h,
            "error_cost": error_cost, "error_cap": cap, "defect_rate": 0.10,
            "mat_by_tier": mat or {"tier1": 0.03, "tier2": 0.06, "tier3": 0.03},
            "asis_mat": asis_mat or ASIS_MAT}


def test_picks_best_feasible():
    rows = [row(0.90, 0.75, 200000, 10000, 600000),
            row(0.85, 0.65, 260000, 12000, 700000),
            row(0.85, 0.65, 240000, -5000, 700000)]   # tail fails
    best, binding = select_optimum(rows)
    assert best["p50"] == 260000
    assert binding["n_feasible"] == 2
    assert binding["tail_rejected"] == 1
    assert binding["constraint_binds_at_optimum"] is False


def test_reports_binding_constraint():
    rows = [row(0.90, 0.75, 200000, 10000, 600000),
            row(0.85, 0.65, 300000, 15000, 1_200_000)]  # best point over cost cap
    best, binding = select_optimum(rows)
    assert best["p50"] == 200000
    assert binding["cost_rejected"] == 1
    assert binding["constraint_binds_at_optimum"] is True
    assert binding["foregone_p50_eur"] == 100000


def test_no_feasible_point():
    rows = [row(0.90, 0.75, 200000, -1000, 600000),
            row(0.85, 0.65, 300000, 15000, 1_500_000)]
    best, binding = select_optimum(rows)
    assert best is None
    assert binding["n_feasible"] == 0


def test_material_dual_gate_rejects_tier_above_asis():
    """D24: a point that clears cost + tail but ships MORE material defects than
    as-is in any tier is rejected by the dual gate."""
    good = row(0.90, 0.75, 200000, 10000, 600000)
    bad = row(0.85, 0.65, 300000, 15000, 600000,
              mat={"tier1": 0.03, "tier2": 0.06, "tier3": 0.20})  # tier3 > as-is
    best, binding = select_optimum([good, bad])
    assert best["p50"] == 200000              # the NPV-higher point is rejected
    assert binding["material_rejected"] == 1
    assert binding["constraint_binds_at_optimum"] is True
