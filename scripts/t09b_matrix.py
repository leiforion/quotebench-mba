#!/usr/bin/env python3
"""T09b — insert Table 6.1 (decision matrix) between the 6.2 intro and rationale.
Usage: python3 scripts/t09b_matrix.py [--apply]
"""
import sys
sys.path.insert(0, "scripts")
from doc_editor import get_service, snapshot, DOC_ID, find_text_range

apply = "--apply" in sys.argv
svc = get_service(write=apply)

ANCHOR = "Option A wins where a conservative reader looks first"
CAPTION = "Table 6.1. Option scoring, 1 (worst) to 5 (best); criteria are not equally weighted. Cost and implementation risk score five-year exposure; strategic optionality scores the transaction-data asset of Section 10.\n"

CELLS = [
    ["Criterion", "A \u2014 Hire", "B \u2014 Selection tools", "C \u2014 CPQ", "D \u2014 Full custom", "E \u2014 Hybrid (proposed)"],
    ["Cycle-time impact", "1", "2", "2", "5", "5"],
    ["Margin impact (errors, discounts, capacity)", "1", "2", "2", "5", "5"],
    ["Error-rate impact", "1", "2", "1", "4", "4"],
    ["Five-year cost (build + run)", "5", "4", "2", "1", "3"],
    ["Implementation risk", "5", "4", "3", "1", "3"],
    ["Strategic optionality (data asset)", "1", "1", "2", "5", "5"],
]

doc = svc.documents().get(documentId=DOC_ID).execute()
print("snapshot:", snapshot(doc))
rng, n = find_text_range(doc, ANCHOR)
if rng is None:
    print(f"FAIL: anchor -> {n} matches")
    sys.exit(1)
p = rng[0]
print(f"insert at {p}")
if not apply:
    print("DRY RUN.")
    sys.exit(0)

# batch 1: caption first, then table -> final order [TABLE][caption][rationale]
svc.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
    {"insertText": {"location": {"index": p}, "text": CAPTION}},
    {"insertTable": {"rows": 7, "columns": 6, "location": {"index": p}}},
]}).execute()
print("batch 1: table + caption inserted")

# batch 2: refetch, populate, style
doc = svc.documents().get(documentId=DOC_ID).execute()
empty = None
for item in doc["body"]["content"]:
    if "table" in item and item["table"]["rows"] == 7 and item["table"]["columns"] == 6:
        texts = []
        for row in item["table"]["tableRows"]:
            for cell in row["tableCells"]:
                t = ""
                for ce in cell["content"]:
                    if "paragraph" in ce:
                        t += "".join(el.get("textRun", {}).get("content", "")
                                     for el in ce["paragraph"].get("elements", []))
                texts.append(t.strip())
        if all(t == "" for t in texts):
            empty = item
assert empty is not None, "empty 7x6 table not found"

reqs = []
# caption paragraph: normal style, italic, not bold
cap_para = None
for item in doc["body"]["content"]:
    if "paragraph" in item:
        t = "".join(el.get("textRun", {}).get("content", "")
                    for el in item["paragraph"].get("elements", []))
        if t.startswith("Table 6.1. Option scoring"):
            cap_para = item
assert cap_para is not None
s, e = cap_para["startIndex"], cap_para["endIndex"]
reqs.append({"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": e},
             "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"}, "fields": "namedStyleType"}})
reqs.append({"updateTextStyle": {"range": {"startIndex": s, "endIndex": e - 1},
             "textStyle": {"bold": False, "italic": True}, "fields": "bold,italic"}})

cell_inserts = []
for r, row in enumerate(empty["table"]["tableRows"]):
    for c, cell in enumerate(row["tableCells"]):
        idx = cell["content"][0]["startIndex"]
        cell_inserts.append((idx, CELLS[r][c], r == 0))
cell_inserts.sort(key=lambda x: -x[0])
for idx, text, header in cell_inserts:
    reqs.append({"insertText": {"location": {"index": idx}, "text": text}})
    reqs.append({"updateTextStyle": {"range": {"startIndex": idx, "endIndex": idx + len(text)},
                 "textStyle": {"bold": header}, "fields": "bold"}})

svc.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
print(f"batch 2: {len(cell_inserts)} cells populated, caption styled")
