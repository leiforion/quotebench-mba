#!/usr/bin/env python3
"""D19 rebase: replace Exhibits 9.1-9.3 with the regenerated figures.

For each caption anchor, finds the inline image immediately above it, deletes
it and inserts the new PNG (uploaded to a transient public host; Docs copies
the image at insert time) at the same index, sized to ~6.1in width.
"""
import os
import struct
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")

from doc_editor import DOC_ID, get_service, flat_text, snapshot

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "simulator", "figures")
WIDTH_PT = 440.0

FIGS = [  # (png, caption anchor)
    ("fig_waterfall.png", "Exhibit 9.1. Projected annual benefits"),
    ("fig_npv_fan.png", "Exhibit 9.2. Five-year NPV at 12 percent across"),
    ("fig_tornado.png", "Exhibit 9.3. One-at-a-time sensitivity"),
]


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def upload(path):
    out = subprocess.run(
        ["curl", "-s", "-F", "reqtype=fileupload",
         "-F", f"fileToUpload=@{path}", "https://catbox.moe/user/api.php"],
        capture_output=True, text=True, check=True).stdout.strip()
    if not out.startswith("https://"):
        raise RuntimeError(f"upload failed: {out[:120]}")
    return out


def image_before(doc, caption_start):
    """The inlineObjectElement closest before caption_start."""
    best = None
    for item in doc["body"]["content"]:
        if "paragraph" not in item:
            continue
        for el in item["paragraph"].get("elements", []):
            if "inlineObjectElement" in el and el["endIndex"] <= caption_start:
                if best is None or el["startIndex"] > best[0]:
                    best = (el["startIndex"], el["endIndex"])
    return best


def main(apply=False):
    svc = get_service(write=apply)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    print(f"snapshot: {snapshot(doc)}")
    text, idxs = flat_text(doc)

    plan = []
    for png, anchor in FIGS:
        n = text.count(anchor)
        if n != 1:
            print(f"FAIL ({n} matches): {anchor!r}")
            return False
        cap_start = idxs[text.find(anchor)]
        img = image_before(doc, cap_start)
        if img is None or cap_start - img[1] > 40:
            print(f"FAIL: no adjacent image above {anchor!r} (img={img}, cap={cap_start})")
            return False
        path = os.path.join(FIG_DIR, png)
        w, h = png_size(path)
        plan.append((img, path, WIDTH_PT * h / w))
        print(f"ok   {png}: old image @[{img[0]},{img[1]}) above caption @{cap_start}")

    if not apply:
        print("DRY RUN — nothing uploaded or written.")
        return True

    # descending order so indices stay valid
    for (s, e), path, h_pt in sorted(plan, key=lambda p: -p[0][0]):
        url = upload(path)
        svc.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
            {"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}},
            {"insertInlineImage": {
                "location": {"index": s}, "uri": url,
                "objectSize": {
                    "width": {"magnitude": WIDTH_PT, "unit": "PT"},
                    "height": {"magnitude": h_pt, "unit": "PT"}}}},
        ]}).execute()
        print(f"replaced {os.path.basename(path)}")
    return True


if __name__ == "__main__":
    sys.exit(0 if main(apply="--apply" in sys.argv) else 1)
