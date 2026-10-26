#!/usr/bin/env python3
"""Move Exhibits 4.2 and 4.3 (image + caption) from the Section 4 body to
Appendix B, preserving image size by reusing the doc's own contentUri.
Processes one exhibit per batch, re-fetching the doc between batches.
"""
import subprocess
import sys
import tempfile
import warnings

warnings.filterwarnings("ignore")

from googleapiclient.discovery import build

from doc_editor import DOC_ID, get_service, snapshot

DEST_ANCHOR = "Exhibit 7.1. Projected to-be process for a Tier 2 inquiry."

MOVES = [
    # (caption-start match in body, new caption text at destination)
    ("Exhibit 4.3. Four root causes behind the observed cycle times",
     "Exhibit 4.3. Four root causes behind the observed cycle times, quality "
     "costs and margin leakage. Each maps to a specific element of the "
     "proposed design in Section 7."),
    ("Exhibit 4.2. Touch and queue medians by inquiry tier",
     "Exhibit 4.2. Touch and queue medians by inquiry tier (tiers defined in "
     "4.1). The queue share is remarkably stable, between 86% and 88%, "
     "regardless of complexity (M)."),
]


def paragraphs(doc):
    """(start, end, text, image_object_id_or_None) per body paragraph."""
    out = []
    for item in doc["body"]["content"]:
        if "paragraph" not in item:
            continue
        t, img = "", None
        for el in item["paragraph"].get("elements", []):
            if "textRun" in el:
                t += el["textRun"]["content"]
            if "inlineObjectElement" in el:
                img = el["inlineObjectElement"]["inlineObjectId"]
        out.append((item["startIndex"], item["endIndex"], t, img))
    return out


def catbox(url):
    """Fallback: rehost an image the Docs fetcher refuses."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        subprocess.run(["curl", "-sL", "-o", f.name, url], check=True)
        out = subprocess.run(
            ["curl", "-s", "-F", "reqtype=fileupload",
             "-F", f"fileToUpload=@{f.name}", "https://catbox.moe/user/api.php"],
            capture_output=True, text=True, check=True).stdout.strip()
    if not out.startswith("https://"):
        raise RuntimeError(f"rehost failed: {out[:120]}")
    return out


def move_one(svc, cap_match, new_caption, apply, dest_anchor=DEST_ANCHOR):
    doc = svc.documents().get(documentId=DOC_ID).execute()
    paras = paragraphs(doc)

    cap = [p for p in paras if p[2].startswith(cap_match)]
    dest = [p for p in paras if p[2].startswith(dest_anchor)]
    assert len(cap) == 1, f"caption matches: {len(cap)} for {cap_match[:40]}"
    assert len(dest) == 1, "destination anchor not unique"
    cs, ce, _, _ = cap[0]
    # nearest preceding paragraph that carries an inline image
    imgs = [p for p in paras if p[3] and p[1] <= cs]
    assert imgs, "no image paragraph before caption"
    im = imgs[-1]
    assert cs - im[1] <= 2, f"image not adjacent to caption ({im[1]} .. {cs})"
    obj = doc["inlineObjects"][im[3]]["inlineObjectProperties"]["embeddedObject"]
    uri = obj["imageProperties"]["contentUri"]
    size = obj["size"]
    s_ins = dest[0][0]
    print(f"{cap_match[:24]}: image @[{im[0]},{im[1]}) caption @[{cs},{ce}) "
          f"-> insert @{s_ins}")
    if not apply:
        return

    def batch(image_uri):
        reqs = [
            {"insertText": {"location": {"index": s_ins},
                            "text": "\n" + new_caption + "\n"}},
            {"insertInlineImage": {"location": {"index": s_ins},
                                   "uri": image_uri, "objectSize": size}},
            {"updateTextStyle": {
                "range": {"startIndex": s_ins + 2,
                          "endIndex": s_ins + 2 + len(new_caption)},
                "textStyle": {"italic": True}, "fields": "italic"}},
            {"deleteContentRange": {"range": {"startIndex": cs, "endIndex": ce}}},
            {"deleteContentRange": {"range": {"startIndex": im[0], "endIndex": im[1]}}},
        ]
        svc.documents().batchUpdate(documentId=DOC_ID,
                                    body={"requests": reqs}).execute()

    try:
        batch(uri)
    except Exception as e:
        print(f"  contentUri rejected ({str(e)[:80]}); rehosting")
        batch(catbox(uri))
    print("  moved.")


def main(apply):
    svc = get_service(write=apply)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    print(f"snapshot: {snapshot(doc)}")
    for cap_match, new_caption in MOVES:
        move_one(svc, cap_match, new_caption, apply)
    print("APPLIED." if apply else "DRY RUN.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
