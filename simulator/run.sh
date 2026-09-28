#!/usr/bin/env bash
# One-command reproduction: venv, dependencies, calibration, gates, every
# report and figure used by the paper.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt

python -m sim fit
pytest -q
python -m sim report calibration
python -m sim tobe
python -m sim pnl
python -m sim stress
python -m sim optimize --no-register
python -m sim figures
