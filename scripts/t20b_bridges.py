#!/usr/bin/env python3
"""T19 bridges: pointer sentences where the moved tables stood, and
cross-reference updates (Appendix K / Exhibit F.1). Also adds K to the
appendix list.
"""
import sys

from doc_editor import run

EDITS = [
    # 3.2 — Table 3.1 bridge
    {"find": "Table 3.1 lists every source of evidence the paper draws on, what each supplies, and the section where it does its work. No other data enters the analysis.",
     "replace": "Seven sources of evidence carry the paper and no other data enters the analysis: the 2025 RFQ log, three weeks of direct observation, the 120-quotation defect audit, internal and contractor interviews, the planned feasibility audit and the simulation models. Table 3.1 (Appendix K) itemizes what each supplies and where it does its work.",
     "unbold": True},
    # 4.2 — Table 4.1 bridge
    {"find": "The inversion in the last two rows matters: Tier 3 supplies",
     "replace": "The tiers are defined by pump count, data completeness at receipt and value band; the full criteria and 2025 mix are Table 4.1 (Appendix K). The inversion in that mix is what matters: Tier 3 supplies",
     "unbold": True},
    # 4.3 — reference to moved 4.1
    {"find": "Third, and read together with the value shares in Table 4.1: the business earns",
     "replace": "Third, and read together with the value shares of 4.2: the business earns"},
    # 4.4 — Table 4.3 bridge
    {"find": "surfaced four distinct classes of error. They differ not only in frequency but in when they are discovered,",
     "replace": "surfaced four distinct classes of error; the full taxonomy with frequencies and unit costs is Table 4.3 (Appendix K). Extraction errors are the most frequent (41% of defects, on 9% of inquiries), selection errors the most expensive (about \u20ac1,840 each), and calculation errors carry the site-failure tail beyond \u20ac5,750 (E). The classes differ not only in frequency but in when they are discovered,",
     "unbold": True},
    # 4.5 — Table 4.4 bridge
    {"find": "Table 4.4 reconstructs its path through the office, timestamped from the mailbox records and the estimators' logs.",
     "replace": "Table 4.4 (Appendix K) reconstructs its path step by step, timestamped from the mailbox records and the estimators' logs: received Thursday evening and unread overnight, first touched late Friday morning, the consolidated clarification not sent until Saturday afternoon, and the contractor's Tuesday reply then sitting unread in the same shared mailbox that delayed the start.",
     "unbold": True},
    # 7.8 — Table 7.1 pointer
    {"find": "Exhibit 7.2 (Appendix B) shows the layers assembled; Table 7.1 states the sourcing decision per component.",
     "replace": "Exhibit 7.2 (Appendix B) shows the layers assembled; Table 7.1 (Appendix K) states the sourcing decision per component."},
    # 6.2 — reference to moved 7.1
    {"find": "E's buy-partner-build sourcing (Table 7.1) confines custom work",
     "replace": "E's buy-partner-build sourcing (Table 7.1, Appendix K) confines custom work"},
    # 8.2 — calibration exhibit now lives in Appendix F
    {"find": "The current build passes all fifteen (Exhibit 8.1); the gate is enforced in code",
     "replace": "The current build passes all fifteen (Exhibit F.1, Appendix F); the gate is enforced in code"},
    # Appendices list — add K
    {"find": "K: Detail tables" if False else "J: Product data layer. Technical specification: classification standard, storage architecture, retrieval tooling and ingestion pipeline.",
     "replace": "J: Product data layer. Technical specification: classification standard, storage architecture, retrieval tooling and ingestion pipeline.\nK: Detail tables relocated from the body (Tables 3.1, 4.1, 4.3, 4.4, 7.1); numbering unchanged.",
     "bold": ["K:"]},
]

if __name__ == "__main__":
    run(EDITS, apply="--apply" in sys.argv)
