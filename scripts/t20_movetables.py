#!/usr/bin/env python3
"""T19 (script t20): move detail tables to Appendix K and the calibration
exhibit to an Appendix F extract; leave bridge sentences in the body.

Moves: Tables 3.1, 4.1, 4.3, 4.4, 7.1 -> Appendix K; Exhibit 8.1 image ->
Appendix F as Exhibit F.1. Keeps Table 4.2 and Table 6.1 in the body.
"""
import sys
import time

sys.path.insert(0, "scripts")
from doc_editor import get_service, snapshot, DOC_ID, run as run_edits

APPLY = "--apply" in sys.argv
TABLES = ["Table 3.1.", "Table 4.1.", "Table 4.3.", "Table 4.4.", "Table 7.1."]
CAL_URI = "https://files.catbox.moe/pgdadr.png"   # fig_calibration.png (785x787)

K_HEAD = "Appendix K (extract): Detail tables\n"
K_INTRO = ("Reference tables relocated from the body; numbering unchanged. "
           "Each is cited from its home section.\n")
F_HEAD = "Appendix F (extract): Simulation calibration\n"
F_INTRO = ("The simulator's methodology, parameters, seeds and run manifests "
           "are in the public repository ([repository URL]). The calibration "
           "gate below is the summary evidence behind 8.2: the as-is model "
           "must reproduce the measured 2025 baseline before any projection "
           "is run.\n")
F_CAPTION = ("Exhibit F.1. Calibration gate: measured 2025 baseline versus "
             "the simulated as-is process; all checks pass within tolerance "
             "(S; seed 42, run manifests in the public repository).\n")


def para_text(item):
    return "".join(el.get("textRun", {}).get("content", "")
                   for el in item["paragraph"].get("elements", []))


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


def find_sources(doc):
    """caption prefix -> (table_item, caption_item)."""
    out = {}
    prev_table = None
    for item in doc["body"]["content"]:
        if "table" in item:
            prev_table = item
        elif "paragraph" in item:
            t = para_text(item)
            for pref in TABLES:
                if t.startswith(pref) and prev_table is not None:
                    out[pref] = (prev_table, item)
    return out


def find_para_start(doc, prefix):
    for item in doc["body"]["content"]:
        if "paragraph" in item and para_text(item).startswith(prefix):
            return item["startIndex"]
    raise RuntimeError(f"anchor not found: {prefix!r}")


def style_reqs(doc, prefix, style, italic=False):
    for item in doc["body"]["content"]:
        if "paragraph" in item and para_text(item).startswith(prefix):
            s, e = item["startIndex"], item["endIndex"]
            reqs = [{"updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e},
                "paragraphStyle": {"namedStyleType": style},
                "fields": "namedStyleType"}}]
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "textStyle": {"bold": False, "italic": italic},
                "fields": "bold,italic"}})
            return reqs
    raise RuntimeError(f"style anchor not found: {prefix!r}")


def main():
    svc = get_service(write=APPLY)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    print("snapshot:", snapshot(doc))

    sources = find_sources(doc)
    for pref in TABLES:
        tbl, cap = sources[pref]
        dims = (tbl["table"]["rows"], tbl["table"]["columns"])
        print(f"{pref:<12} {dims[0]}x{dims[1]}  table @[{tbl['startIndex']},"
              f"{tbl['endIndex']})  caption @[{cap['startIndex']},{cap['endIndex']})")
    p_ref = find_para_start(doc, "References")
    p_g = find_para_start(doc, "Appendix G (extract)")
    print(f"References @ {p_ref}; Appendix G heading @ {p_g}")
    if not APPLY:
        print("DRY RUN.")
        return

    def batch(reqs):
        svc.documents().batchUpdate(documentId=DOC_ID,
                                    body={"requests": reqs}).execute()
        time.sleep(0.4)

    def fetch():
        return svc.documents().get(documentId=DOC_ID).execute()

    # --- 1. Appendix K heading + intro (above References)
    batch([{"insertText": {"location": {"index": p_ref},
                           "text": K_HEAD + K_INTRO}}])
    doc = fetch()
    batch(style_reqs(doc, "Appendix K (extract)", "HEADING_2")
          + style_reqs(doc, "Reference tables relocated", "NORMAL_TEXT"))
    print("Appendix K skeleton in")

    # --- 2. recreate each table above References
    for pref in TABLES:
        doc = fetch()
        tbl, cap = find_sources(doc)[pref]
        cells = cell_texts(tbl)
        rows, cols = tbl["table"]["rows"], tbl["table"]["columns"]
        cap_text = para_text(cap).rstrip("\n") + "\n"
        p = find_para_start(doc, "References")
        batch([{"insertText": {"location": {"index": p}, "text": cap_text}},
               {"insertTable": {"rows": rows, "columns": cols,
                                "location": {"index": p}}}])
        # populate the new (empty) table
        doc = fetch()
        empty = None
        for item in doc["body"]["content"]:
            if "table" in item and item["table"]["rows"] == rows \
                    and item["table"]["columns"] == cols:
                if all(t == "" for r in cell_texts(item) for t in r):
                    empty = item
        assert empty is not None, f"empty {rows}x{cols} not found for {pref}"
        reqs = []
        ins = []
        for r, row in enumerate(empty["table"]["tableRows"]):
            for c, cell in enumerate(row["tableCells"]):
                if cells[r][c]:
                    ins.append((cell["content"][0]["startIndex"],
                                cells[r][c], r == 0))
        ins.sort(key=lambda x: -x[0])
        for idx, text, header in ins:
            reqs.append({"insertText": {"location": {"index": idx}, "text": text}})
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": idx, "endIndex": idx + len(text)},
                "textStyle": {"bold": header, "italic": False},
                "fields": "bold,italic"}})
        batch(reqs)
        # caption style: the copy sitting in Appendix K is the LAST match
        doc = fetch()
        matches = [it for it in doc["body"]["content"]
                   if "paragraph" in it and para_text(it).startswith(pref)]
        capk = matches[-1]
        s, e = capk["startIndex"], capk["endIndex"]
        batch([{"updateParagraphStyle": {
                    "range": {"startIndex": s, "endIndex": e},
                    "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                    "fields": "namedStyleType"}},
               {"updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": e - 1},
                    "textStyle": {"bold": False, "italic": True},
                    "fields": "bold,italic"}}])
        print(f"recreated {pref} in Appendix K")

    # --- 3. Appendix F extract with the calibration image
    doc = fetch()
    p_g = find_para_start(doc, "Appendix G (extract)")
    batch([{"insertText": {"location": {"index": p_g},
                           "text": F_HEAD + F_INTRO + F_CAPTION}}])
    doc = fetch()
    batch(style_reqs(doc, "Appendix F (extract)", "HEADING_2")
          + style_reqs(doc, "The simulator's methodology", "NORMAL_TEXT")
          + style_reqs(doc, "Exhibit F.1.", "NORMAL_TEXT", italic=True))
    doc = fetch()
    p_cap = find_para_start(doc, "Exhibit F.1.")
    batch([{"insertText": {"location": {"index": p_cap}, "text": "\n"}},
           {"insertInlineImage": {
               "location": {"index": p_cap}, "uri": CAL_URI,
               "objectSize": {
                   "width": {"magnitude": 440, "unit": "PT"},
                   "height": {"magnitude": 441, "unit": "PT"}}}}])
    print("Appendix F extract with calibration image in")

    # --- 4. delete originals (tables + captions + old Exhibit 8.1)
    doc = fetch()
    dels = []
    src = find_sources(doc)
    for pref in TABLES:
        # first match = body original (Appendix K copies come later in doc)
        prev_table = None
        for item in doc["body"]["content"]:
            if "table" in item:
                prev_table = item
            elif "paragraph" in item and para_text(item).startswith(pref):
                dels.append((prev_table["startIndex"], item["endIndex"]))
                break
    # old Exhibit 8.1: image paragraph + caption paragraph in Section 8
    content = doc["body"]["content"]
    for i, item in enumerate(content):
        if "paragraph" in item and para_text(item).startswith("Exhibit 8.1."):
            img_para = content[i - 1]
            dels.append((img_para["startIndex"], item["endIndex"]))
            break
    dels.sort(key=lambda d: -d[0])
    batch([{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}}
           for s, e in dels])
    print(f"deleted {len(dels)} original blocks")
    print("STRUCTURAL MOVES DONE — now run bridge edits")


if __name__ == "__main__":
    main()
