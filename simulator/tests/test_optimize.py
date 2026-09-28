"""SIM-5 gates: selection and constraint logic (pure functions, no DES)."""
from sim.optimize import select_optimum


def row(c1, c2, p50, p10h, defects, cap=0.092):
    return {"c1": c1, "c2": c2, "p50": p50,
            "p10_hurdle": p10h, "defect_rate": defects, "defect_cap": cap}


def test_picks_best_feasible():
    rows = [row(0.90, 0.75, 200000, 10000, 0.085),
            row(0.85, 0.65, 260000, 12000, 0.089),
            row(0.85, 0.65, 240000, -5000, 0.089)]   # tail fails
    best, binding = select_optimum(rows)
    assert best["p50"] == 260000
    assert binding["n_feasible"] == 2
    assert binding["tail_rejected"] == 1
    assert binding["constraint_binds_at_optimum"] is False


def test_reports_binding_constraint():
    rows = [row(0.90, 0.75, 200000, 10000, 0.085),
            row(0.85, 0.65, 300000, 15000, 0.110)]   # best point too risky
    best, binding = select_optimum(rows)
    assert best["p50"] == 200000
    assert binding["defects_rejected"] == 1
    assert binding["constraint_binds_at_optimum"] is True
    assert binding["foregone_p50_eur"] == 100000


def test_no_feasible_point():
    rows = [row(0.90, 0.75, 200000, -1000, 0.085),
            row(0.85, 0.65, 300000, 15000, 0.150)]
    best, binding = select_optimum(rows)
    assert best is None
    assert binding["n_feasible"] == 0
