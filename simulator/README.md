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
- All monetary values are EUR (AED converted at 0.23).

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
pytest                             # the same gates as assertions (36 tests)

python -m sim tobe                 # to-be projection vs the calibrated baseline
python -m sim pnl                  # P&L + 20,000-draw five-year investment case
python -m sim stress               # 8 adverse scenarios, tornado, kill criteria
python -m sim optimize             # search C1/C2/discount-band operating point
python -m sim figures              # export the four paper figures (figures/)
```

Every run writes a manifest to `results/` (seed, git commit, parameter
checksums), so any number in the paper can be traced to the exact run that
produced it. Default seeds reproduce the published figures.

## Headline outputs (seed 42)

- Five-year NPV at 12%: **P10 €94k / P50 €260k / P90 €457k**;
  P(clears the 15% hurdle) 98.5%; median IRR 69%; payback 1.6 years.
- The conservative case (pessimistic extraction, zero speed-win elasticity,
  +30% build) **does not clear** the hurdle (−€88k): the case needs either
  some win-rate response to speed or central-range extraction.
- Kill boundaries: the case fails only if the speed-win uplift is below
  ~0.2pp, build exceeds ~3.3× plan, run costs exceed ~€83k/yr, or demand
  halves. Extraction quality and pricing adoption have no failure boundary
  alone.
- Optimizer recommendation: confidence thresholds C1 = 0.85, C2 = 0.70 and a
  ±1% discount band, subject to the constraint that the to-be process ships
  no more defects than the as-is baseline (it binds, at a cost of ~€0.5k).

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
