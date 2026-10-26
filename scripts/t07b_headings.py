#!/usr/bin/env python3
"""T07 pass 2 — normalize heading styles.
H1 for 'Section N —' titles, Appendices, References; H2 for 'N.M' subsections;
TITLE for the paper title line.
Usage: python3 scripts/t07b_headings.py [--apply]
"""
import re
import sys
sys.path.insert(0, "scripts")
from doc_editor import get_service, snapshot, DOC_ID

H1_RE = re.compile(r"^Section \d{1,2} \u2014 ")
H2_RE = re.compile(r"^\d{1,2}\.\d{1,2} \S")

apply = "--apply" in sys.argv
svc = get_service(write=apply)
doc = svc.documents().get(documentId=DOC_ID).execute()
snap = snapshot(doc)
print("snapshot:", snap)

reqs = []
for item in doc["body"]["content"]:
    if "paragraph" not in item:
        continue
    p = item["paragraph"]
    text = "".join(el.get("textRun", {}).get("content", "") for el in p.get("elements", [])).rstrip("\n")
    if not text.strip():
        continue
    cur = p.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    target = None
    if H1_RE.match(text) or text in ("Appendices", "References"):
        target = "HEADING_1"
    elif H2_RE.match(text) and len(text) < 90:
        target = "HEADING_2"
    elif text.startswith("Digital Transformation of the RFQ Process"):
        target = "TITLE"
    if target and target != cur:
        s = item["startIndex"]
        e = item["endIndex"]
        print(f"{cur:>12} -> {target:<10} {text[:70]!r}")
        reqs.append({"updateParagraphStyle": {
            "range": {"startIndex": s, "endIndex": e},
            "paragraphStyle": {"namedStyleType": target},
            "fields": "namedStyleType"}})

print(f"\n{len(reqs)} style updates")
if apply and reqs:
    svc.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
    print("APPLIED.")
elif not apply:
    print("DRY RUN.")
