#!/usr/bin/env python3
"""Index-based Google Docs editor.

Edit types:
  {"find": "...", "replace": "..."}          exact unique text match anywhere
  {"row_anchor": "...", "old_cell": "...",   table cell whose stripped text == old_cell,
   "new_cell": "..."}                        in the row whose text contains row_anchor
"""
import json
import os
import sys
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

from google.oauth2 import service_account
from googleapiclient.discovery import build

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC_ID = "1XuVqXKpqiPj3FT5PhPtYTEqAr04RU0wbSHx0xgmCaGY"


def get_service(write=False):
    scope = "https://www.googleapis.com/auth/documents" if write else \
            "https://www.googleapis.com/auth/documents.readonly"
    creds = service_account.Credentials.from_service_account_file(
        os.path.join(BASE, "google_key.json"), scopes=[scope])
    return build("docs", "v1", credentials=creds)


def snapshot(doc):
    d = os.path.join(BASE, "source_docs", "snapshots")
    os.makedirs(d, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(d, f"paper_{ts}.json")
    with open(path, "w") as f:
        json.dump(doc, f)
    return path


def flat_text(doc):
    """Concatenated body text with per-char doc indices."""
    chars, idxs = [], []

    def walk(content):
        for item in content:
            if "paragraph" in item:
                for el in item["paragraph"].get("elements", []):
                    tr = el.get("textRun")
                    if tr:
                        start = el["startIndex"]
                        for i, ch in enumerate(tr["content"]):
                            chars.append(ch)
                            idxs.append(start + i)
            elif "table" in item:
                for row in item["table"]["tableRows"]:
                    for cell in row["tableCells"]:
                        walk(cell["content"])
    walk(doc["body"]["content"])
    return "".join(chars), idxs


def find_text_range(doc, needle):
    text, idxs = flat_text(doc)
    hits = []
    pos = text.find(needle)
    while pos != -1:
        hits.append(pos)
        pos = text.find(needle, pos + 1)
    if len(hits) != 1:
        return None, len(hits)
    p = hits[0]
    start = idxs[p]
    end = idxs[p + len(needle) - 1] + 1
    # sanity: contiguous range
    if end - start != len(needle):
        return None, -1  # spans structural boundary
    return (start, end), 1


def cell_ranges(doc):
    """Yield (row_text, cell_text_stripped, cell_start, cell_end_of_text)."""
    out = []
    for item in doc["body"]["content"]:
        if "table" not in item:
            continue
        for row in item["table"]["tableRows"]:
            row_texts = []
            cells = []
            for cell in row["tableCells"]:
                t = ""
                first_start, last_end = None, None
                for ce in cell["content"]:
                    if "paragraph" in ce:
                        for el in ce["paragraph"].get("elements", []):
                            tr = el.get("textRun")
                            if tr:
                                if first_start is None:
                                    first_start = el["startIndex"]
                                last_end = el["endIndex"]
                                t += tr["content"]
                row_texts.append(t)
                cells.append((t, first_start, last_end))
            row_full = " | ".join(row_texts)
            for (t, s, e) in cells:
                out.append((row_full, t, s, e))
    return out


def build_requests(doc, edits, log):
    reqs = []
    ok = True
    for ed in edits:
        if "insert_before" in ed:
            rng, n = find_text_range(doc, ed["insert_before"])
            if rng is None:
                log.append(f"FAIL ({n} matches): insert_before {ed['insert_before'][:60]!r}")
                ok = False
                continue
            s, _ = rng
            log.append(f"ok   insert @{s}: {ed['text'][:60]!r}")
            reqs.append(("ins", s, s, ed["text"], ed.get("bold", []), ed.get("style"), ed.get("unbold", False)))
        elif "find" in ed:
            rng, n = find_text_range(doc, ed["find"])
            if rng is None:
                log.append(f"FAIL ({n} matches): {ed['find'][:80]!r}")
                ok = False
                continue
            s, e = rng
            log.append(f"ok   text @[{s},{e}): {ed['find'][:60]!r} -> {ed['replace'][:60]!r}")
            reqs.append(("del", s, e, ed["replace"], ed.get("bold", []), None, ed.get("unbold", False)))
        else:
            found = [c for c in cell_ranges(doc)
                     if ed["row_anchor"] in c[0] and c[1].strip() == ed["old_cell"]]
            if len(found) != 1:
                log.append(f"FAIL ({len(found)} matches): cell {ed['old_cell']!r} in row ~{ed['row_anchor'][:50]!r}")
                ok = False
                continue
            _, t, s, e = found[0]
            # keep the final newline of the cell: delete [s, e-1)
            log.append(f"ok   cell @[{s},{e-1}): {ed['old_cell']!r} -> {ed['new_cell']!r}")
            reqs.append(("del", s, e - 1, ed["new_cell"], [], None, False))
    # descending order so indices stay valid
    reqs.sort(key=lambda r: -r[1])
    api_reqs = []
    for _, s, e, repl, bold, style, unbold in reqs:
        if e > s:
            api_reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}})
        if repl:
            api_reqs.append({"insertText": {"location": {"index": s}, "text": repl}})
            if bold or unbold:
                # deterministic styling: clear bold across the insertion, then re-bold spans
                api_reqs.append({"updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": s + len(repl.rstrip("\n"))},
                    "textStyle": {"bold": False}, "fields": "bold"}})
            for sub in bold:
                off = repl.find(sub)
                if off >= 0:
                    api_reqs.append({"updateTextStyle": {
                        "range": {"startIndex": s + off, "endIndex": s + off + len(sub)},
                        "textStyle": {"bold": True}, "fields": "bold"}})
            if style:
                api_reqs.append({"updateParagraphStyle": {
                    "range": {"startIndex": s, "endIndex": s + len(repl)},
                    "paragraphStyle": {"namedStyleType": style}, "fields": "namedStyleType"}})
    return api_reqs, ok


def run(edits, apply=False):
    svc = get_service(write=apply)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    snap = snapshot(doc)
    log = [f"snapshot: {snap}", f"revision: {doc.get('revisionId', '?')[:24]}"]
    api_reqs, ok = build_requests(doc, edits, log)
    print("\n".join(log))
    print(f"\n{len(api_reqs)} API requests; all edits matched: {ok}")
    if not apply:
        print("DRY RUN — nothing written.")
        return ok
    if not ok:
        print("Aborting apply: unmatched edits.")
        return False
    svc.documents().batchUpdate(documentId=DOC_ID, body={"requests": api_reqs}).execute()
    print("APPLIED.")
    return True
