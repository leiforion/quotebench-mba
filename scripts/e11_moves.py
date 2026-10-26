#!/usr/bin/env python3
"""Page-recovery moves per author approval: Exhibit 9.2 (NPV fan) to
Appendix F between Exhibits 8.1 and 9.3, and Table 6.1 (option matrix) to
Appendix K between Tables 4.4 and 7.1. Body references were repointed by
e10_readability.py.
"""
import sys
import time
import warnings

warnings.filterwarnings("ignore")

from doc_editor import DOC_ID, get_service, snapshot
from e2b_images import catbox

CAP_92 = "Exhibit 9.2. Five-year NPV at 12 percent"
ANCHOR_F = "Exhibit 8.1. Simulated cycle-time distributions"
CAP_61 = "Table 6.1. Option scoring"
ANCHOR_K = "Table 4.4."


def para_text(item):
    return "".join(el.get("textRun", {}).get("content", "")
                   for el in item["paragraph"].get("elements", []))


def paras(doc):
    return [it for it in doc["body"]["content"] if "paragraph" in it]


def cell_texts(table_item):
    rows = []
    for row in table_item["table"]["tableRows"]:
        r = []
        for cell in row["tableCells"]:
            t = ""
            for ce in cell["content"]:
                if "paragraph" in ce:
                    t += para_text(ce)
            r.append(t.strip())
        rows.append(r)
    return rows


def main(apply):
    svc = get_service(write=apply)

    def fetch():
        return svc.documents().get(documentId=DOC_ID).execute()

    def batch(reqs):
        svc.documents().batchUpdate(documentId=DOC_ID,
                                    body={"requests": reqs}).execute()
        time.sleep(0.4)

    doc = fetch()
    print("snapshot:", snapshot(doc))

    # ---------- Exhibit 9.2 ----------
    ps = paras(doc)
    cap = [p for p in ps if para_text(p).startswith(CAP_92)]
    assert len(cap) == 1, f"9.2 caption matches: {len(cap)}"
    cs, ce = cap[0]["startIndex"], cap[0]["endIndex"]
    cap_text = para_text(cap[0]).rstrip("\n")
    img = None
    for p in ps:
        if p["endIndex"] <= cs:
            for el in p["paragraph"].get("elements", []):
                if "inlineObjectElement" in el:
                    img = (p, el)
    ip, iel = img
    assert cs - ip["endIndex"] <= 1 and ip["endIndex"] - ip["startIndex"] <= 2, \
        "9.2 image paragraph not standalone/adjacent"
    obj = doc["inlineObjects"][iel["inlineObjectElement"]["inlineObjectId"]]
    emb = obj["inlineObjectProperties"]["embeddedObject"]
    uri, size = emb["imageProperties"]["contentUri"], emb["size"]

    dest = [p for p in ps if para_text(p).startswith(ANCHOR_F)]
    assert len(dest) == 1, f"F anchor matches: {len(dest)}"
    d = dest[0]["endIndex"]
    print(f"9.2: image @[{ip['startIndex']},{ip['endIndex']}) caption "
          f"@[{cs},{ce}) -> insert @{d}")

    # ---------- Table 6.1 ----------
    prev_table = None
    body_tbl = body_cap = None
    for item in doc["body"]["content"]:
        if "table" in item:
            prev_table = item
        elif "paragraph" in item and para_text(item).startswith(CAP_61):
            body_tbl, body_cap = prev_table, item
    assert body_tbl is not None, "Table 6.1 not found"
    cells = cell_texts(body_tbl)
    rows, cols = body_tbl["table"]["rows"], body_tbl["table"]["columns"]
    cap61_text = para_text(body_cap).rstrip("\n")
    k_caps = [p for p in ps if para_text(p).startswith(ANCHOR_K)]
    k_anchor = k_caps[-1]  # Appendix K copy is the last match
    assert k_anchor["startIndex"] > body_cap["startIndex"], "K anchor not in appendix"
    kd = k_anchor["endIndex"]
    print(f"6.1: table {rows}x{cols} @[{body_tbl['startIndex']},"
          f"{body_tbl['endIndex']}) caption @[{body_cap['startIndex']},"
          f"{body_cap['endIndex']}) -> insert @{kd}")
    if not apply:
        print("DRY RUN.")
        return

    # ---- apply 9.2 move (insert in appendix, delete body originals) ----
    def move_img(image_uri):
        batch([
            {"insertText": {"location": {"index": d},
                            "text": "\n" + cap_text + "\n"}},
            {"insertInlineImage": {"location": {"index": d},
                                   "uri": image_uri, "objectSize": size}},
            {"updateTextStyle": {
                "range": {"startIndex": d + 2,
                          "endIndex": d + 2 + len(cap_text)},
                "textStyle": {"italic": True, "bold": False},
                "fields": "italic,bold"}},
            {"deleteContentRange": {"range": {"startIndex": cs, "endIndex": ce}}},
            {"deleteContentRange": {"range": {"startIndex": ip["startIndex"],
                                              "endIndex": ip["endIndex"]}}},
        ])
    try:
        move_img(uri)
    except Exception as e:
        print(f"  contentUri rejected ({str(e)[:80]}); rehosting")
        move_img(catbox(uri))
    print("Exhibit 9.2 moved to Appendix F.")

    # ---- apply 6.1 move: recreate in K, then delete body original ----
    doc = fetch()
    k_caps = [p for p in paras(doc) if para_text(p).startswith(ANCHOR_K)]
    kd = k_caps[-1]["endIndex"]
    batch([{"insertText": {"location": {"index": kd},
                           "text": cap61_text + "\n"}},
           {"insertTable": {"rows": rows, "columns": cols,
                            "location": {"index": kd}}}])
    doc = fetch()
    empty = None
    for item in doc["body"]["content"]:
        if "table" in item and item["table"]["rows"] == rows \
                and item["table"]["columns"] == cols \
                and all(t == "" for r in cell_texts(item) for t in r):
            empty = item
    assert empty is not None, "new empty table not found"
    ins = []
    for r, row in enumerate(empty["table"]["tableRows"]):
        for c, cell in enumerate(row["tableCells"]):
            if cells[r][c]:
                ins.append((cell["content"][0]["startIndex"], cells[r][c], r == 0))
    ins.sort(key=lambda x: -x[0])
    reqs = []
    for idx, text, header in ins:
        reqs.append({"insertText": {"location": {"index": idx}, "text": text}})
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": idx, "endIndex": idx + len(text)},
            "textStyle": {"bold": header, "italic": False},
            "fields": "bold,italic"}})
    batch(reqs)
    # style the K caption copy (last match), then delete the body originals
    doc = fetch()
    matches = [p for p in paras(doc) if para_text(p).startswith(CAP_61)]
    capk = matches[-1]
    batch([{"updateParagraphStyle": {
                "range": {"startIndex": capk["startIndex"],
                          "endIndex": capk["endIndex"]},
                "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                "fields": "namedStyleType"}},
           {"updateTextStyle": {
                "range": {"startIndex": capk["startIndex"],
                          "endIndex": capk["endIndex"] - 1},
                "textStyle": {"bold": False, "italic": True},
                "fields": "bold,italic"}}])
    doc = fetch()
    prev_table = None
    body_tbl = body_cap = None
    for item in doc["body"]["content"]:
        if "table" in item:
            prev_table = item
        elif "paragraph" in item and para_text(item).startswith(CAP_61):
            if body_tbl is None:
                body_tbl, body_cap = prev_table, item
    batch([{"deleteContentRange": {"range": {"startIndex": body_cap["startIndex"],
                                             "endIndex": body_cap["endIndex"]}}},
           {"deleteContentRange": {"range": {"startIndex": body_tbl["startIndex"],
                                             "endIndex": body_tbl["endIndex"]}}}])
    print("Table 6.1 moved to Appendix K.")
    print("APPLIED.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
