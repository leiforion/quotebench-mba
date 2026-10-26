#!/usr/bin/env python3
"""Insert the O9 author annotation (actual branch revenue) into Section 9.1."""
import sys

from doc_editor import run

NOTE = ("\n[AUTHORS TO CONFIRM — O9: the simulator derives the revenue base from "
        "registered values: EUR ~22.2M quoted / ~5.6M won per year (~AED 97M / 25M), "
        "including two flagship-scale quotes per year (D17). This level is pinned by "
        "the measured tier value shares (12/41/47, BASE-11) and the Tier 1 value cap "
        "(BASE-12); it cannot go materially higher without contradicting them. "
        "Confirm the branch's actual 2025 pump-only revenue. If it differs "
        "materially, BASE-11/12 must be re-measured and Section 9 rebased.]")

EDITS = [{
    "find": "Annual fully-loaded quoting cost, revenue throughput per engineer, "
            "quantified leakage (errors + discounting), all from 4.3/4.4; no new numbers.",
    "replace": "Annual fully-loaded quoting cost, revenue throughput per engineer, "
               "quantified leakage (errors + discounting), all from 4.3/4.4; no new numbers."
               + NOTE,
    "bold": ["[AUTHORS TO CONFIRM — O9:"],
}]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
