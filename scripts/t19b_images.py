#!/usr/bin/env python3
"""Insert the five simulator figures into the Doc, each directly above its
caption anchor. Uploads PNGs to Drive (service account), makes them
link-readable, and uses insertInlineImage sized to ~6.1in width.
"""
import os
import struct
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")

from google.oauth2 import service_account
from googleapiclient.discovery import build

from doc_editor import DOC_ID, flat_text, snapshot

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "simulator", "figures")
WIDTH_PT = 440.0

FIGS = [  # (png, caption anchor)
    ("fig_calibration.png", "Exhibit 8.1. Calibration gate:"),
    ("fig_cycletimes.png", "Exhibit 8.2. Simulated cycle-time distributions"),
    ("fig_waterfall.png", "Exhibit 9.1. Projected annual benefits"),
    ("fig_npv_fan.png", "Exhibit 9.2. Five-year NPV at 12 percent across"),
    # fig_tornado inserted in the first (crashed-after-insert) run
]


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def creds():
    return service_account.Credentials.from_service_account_file(
        os.path.join(BASE, "google_key.json"),
        scopes=["https://www.googleapis.com/auth/documents"])


def upload(path):
    """Transient public host: Docs copies the image into the document at
    insert time, so the URL only needs to live for this run."""
    out = subprocess.run(
        ["curl", "-s", "-F", "reqtype=fileupload",
         "-F", f"fileToUpload=@{path}", "https://catbox.moe/user/api.php"],
        capture_output=True, text=True, check=True).stdout.strip()
    if not out.startswith("https://"):
        raise RuntimeError(f"upload failed: {out[:120]}")
    return out


def main(apply=False):
    c = creds()
    docs = build("docs", "v1", credentials=c)
    doc = docs.documents().get(documentId=DOC_ID).execute()
    print(f"snapshot: {snapshot(doc)}")
    text, idxs = flat_text(doc)

    plan = []
    for png, anchor in FIGS:
        pos = text.find(anchor)
        n = text.count(anchor)
        if n != 1:
            print(f"FAIL ({n} matches): {anchor!r}")
            return False
        s = idxs[pos]
        path = os.path.join(FIG_DIR, png)
        w, h = png_size(path)
        plan.append((s, path, WIDTH_PT, WIDTH_PT * h / w))
        print(f"ok   {png} @{s}  ({w}x{h}px -> {WIDTH_PT:.0f}x{WIDTH_PT*h/w:.0f}pt)")

    if not apply:
        print("DRY RUN — nothing uploaded or written.")
        return True

    plan.sort(key=lambda p: -p[0])   # descending so indices stay valid
    for s, path, w_pt, h_pt in plan:
        uri = upload(path)
        reqs = [
            {"insertText": {"location": {"index": s}, "text": "\n"}},
            {"insertInlineImage": {
                "location": {"index": s}, "uri": uri,
                "objectSize": {
                    "width": {"magnitude": w_pt, "unit": "PT"},
                    "height": {"magnitude": h_pt, "unit": "PT"}}}},
        ]
        docs.documents().batchUpdate(documentId=DOC_ID,
                                     body={"requests": reqs}).execute()
        print(f"inserted {os.path.basename(path)}")
    print("APPLIED.")
    return True


if __name__ == "__main__":
    sys.exit(0 if main(apply="--apply" in sys.argv) else 1)
