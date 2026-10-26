# QuoteBench Branch Simulator

A discrete-event simulation of a pump distributor's RFQ quoting operation,
built for the paper *Digital Transformation of the RFQ Process in Commercial
Pump Distribution*. It simulates the branch one inquiry at a time: arrivals by
complexity tier at measured 2025 rates, estimators as resources with skill
profiles, queues and pre-emption as observed, then the economics of every
simulated quote, aggregated into a projected P&L and a five-year investment
case under uncertainty.

## What it claims, and what it does not

- The **as-is model is calibrated, not assumed**: it must reproduce the
  measured 2025 baseline (cycle-time medians and P90s by tier, touch hours,
  queue share, cost per quote) within ±10% before any to-be scenario will run.
  The gate is enforced in code and in the test suite.
- The **to-be capability assumptions are generated, not audited**: extraction
  performance is seeded from published document-AI benchmark ranges, spread by
  document-quality class and engineer skill. No live system exists; nothing
  here is a measurement of one.
- All monetary values are EUR (AED converted at EUR 1 = AED 4.25).

## Quick start

```bash
./run.sh          # venv, dependencies, calibration, tests, all reports, figures
```

Or step by step:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m sim fit                  # calibrate as-is parameters (writes data/)
python -m sim report calibration   # measured vs simulated, with gate verdict
pytest                             # the same gates as assertions (41 tests)

python -m sim tobe                 # to-be projection vs the calibrated baseline
python -m sim designs              # compare the three Tier-3 designs (D24)
python -m sim pnl                  # P&L + 20,000-draw five-year investment case
python -m sim stress               # 8 adverse scenarios, tornado, kill criteria
python -m sim optimize             # search the C1/C2 routing operating point (dual gate)
python -m sim figures              # export the four paper figures (figures/)
```

Every run writes a manifest to `results/` (seed, git commit, parameter
checksums), so any number in the paper can be traced to the exact run that
produced it. Default seeds reproduce the published figures.

## Headline outputs (seed 42)

Revenue basis = **branch** (D21): the AED 150M (~€35.3M) 2025 pump revenue is
the Abu Dhabi *branch*. Company revenue is **derived** from the as-is DES anchor
at company volume (~€303M), and per-defect error cost scales with each quote's
value. The calibration gate is unchanged (the process model is value-independent).

- Company revenue (derived): **~€304M**; as-is quality (error) cost **~€1.41M
  = 0.46% of revenue**, value-proportional so it concentrates in high-value work:
  Tier 1 7% / Tier 2 37% / **Tier 3 56%** (the majority, vs 41% of won value).
- **Defects use one (material) definition** (D24): wrong model / wrong price /
  missed spec, so as-is and to-be are comparable. The as-is material rate
  **reproduces the paper's audit** (BASE-19 6/11/19%, 9.2% company). Company
  any-defect 9.2% → 8.0%; **material 9.2% → 4.9%**. Material rate falls in
  **every** tier (as-is → to-be): T1 5.9 → 3.7%, T2 11.3 → 7.5%, **T3 18.9 → 3.3%**.
- Surviving misreads on **hydraulically critical fields** are priced as the
  calculation/selection defects they become in the engines (D24 propagation),
  not cheap extraction typos. Error cut by tier (cost): T1 39% / T2 36% /
  **T3 78%**, total **60%** (€1.41M → €0.57M).
- **Tier-3 design (c)** adopted (engines + full review + mandatory source
  verification of critical fields). The three designs were compared under the
  corrected pricing; (c) meets both gates at the lowest total cost. Design (b)
  (engines + full review, no verification) fails the material gate (T3 24.9% >
  as-is 15.9%) and *raises* T3 error cost (−8%), so it cannot be used.
- Annual benefit at full adoption: **€2.51M at the win-uplift mode** (capacity
  redeployment €203k, error reduction €847k, win-rate uplift €1.46M, defect-killed
  bid inert) vs **€2.68M at the Monte Carlo median**. The paper reports the
  **central/mode €2.51M** (coherent with stress base + floor); NPV below comes
  from the full Monte Carlo.
- Capacity (Section 8.2): automation of touch time **56%** (to-be ~10,940 vs
  as-is ~24,900 engineer hours); the same 16 estimators can absorb **~128% more
  inquiry volume** at equal touch load. Cycle-time medians fall T1 18 → 1.7 h,
  T2 39 → 12 h, T3 88 → 55 h (working hours).
- Five-year NPV at 12%: **P10 €4.42M / P50 €6.98M / P90 €10.02M**;
  P(clears the 15% hurdle) 100%; median IRR ~437%; payback ~0.2 years.
- **Dual escape gate** (D24): to-be **error cost ≤ as-is** AND no tier's
  **material defect rate** above as-is. All 12 routing points are feasible;
  neither gate binds at the optimum.
- The conservative case (pessimistic extraction + critical share, zero speed-win
  elasticity, +30% build) **clears** the hurdle on cost + error savings alone
  (NPV@12% **+€1.45M** — capacity €132k + error €534k). Rule E (floor break-even)
  not triggered.
- Kill criteria: no single stressor drives the case below the 15% hurdle in the
  tested ranges. The multi-office-rollout scenario (change cost ×8 = €144k) is
  cost-only and leaves annual benefits unchanged.
- Tornado: most sensitive to the win-rate uplift (0–5pp), then extraction
  quality; the critical-field-share assumption moves NPV little (~€15k) because
  source verification neutralises it; build / change / run costs move it least.
- Tier 3 engineer touch: ~5.4 h median (incl. critical-field verification), with
  the Innovo-scale job (as-is ~28 h) simulating to ~13 h to-be (7.2 walkthrough).
- Optimizer recommendation: confidence thresholds **C1 = 0.85, C2 = 0.80**,
  under the D24 dual gate (value-proportional cost + per-tier material defect);
  neither constraint binds — the NPV-best point is also the defect-safe point.

## Layout

- `sim/asis.py` — as-is discrete-event engine (SimPy)
- `sim/fit.py` — auto-calibration of the residual-queue parameters
- `sim/tobe.py`, `sim/capability.py` — to-be engine: document quality,
  per-field extraction and confidence, routing (auto / assisted / manual),
  graceful degradation to the as-is process
- `sim/economics.py` — per-quote economics, Monte Carlo investment case
- `sim/stress.py`, `scenarios/*.yaml` — named adverse scenarios, tornado,
  kill-criteria bisection
- `sim/optimize.py` — constrained grid search over the design's thresholds
- `sim/report.py`, `sim/figures.py` — calibration exhibit, paper figures
- `data/parameters_*.yaml` — every parameter with its evidence source
- `data/register_snapshot.csv` — anonymized snapshot of the paper's
  assumptions register (id, value, unit, evidence tag)
- `tests/` — calibration, to-be, economics, stress and optimizer gates
- `results/` — run manifests (gitignored); `figures/` — exported figures
