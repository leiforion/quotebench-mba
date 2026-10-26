#!/usr/bin/env python3
"""Replace the Exhibit 4.3 driver-tree image (Appendix B) with the
regenerated compact version (simulator/figures/fig_drivertree.png),
hosted via catbox, sized to the 450 pt text width.
"""
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")

from PIL import Image

from doc_editor import DOC_ID, get_service, snapshot
from e2b_images import paragraphs

PNG = "../simulator/figures/fig_drivertree.png"
CAPTION = "Exhibit 4.3."


def main(apply):
    out = subprocess.run(
        ["curl", "-s", "-F", "reqtype=fileupload",
         "-F", f"fileToUpload=@{PNG}", "https://catbox.moe/user/api.php"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert out.startswith("https://"), f"upload failed: {out[:120]}"
    print("hosted:", out)

    w, h = Image.open(PNG).size
    width_pt = 450.0
    height_pt = round(width_pt * h / w, 1)
    print(f"png {w}x{h}px -> {width_pt}x{height_pt}pt")

    svc = get_service(write=apply)
    doc = svc.documents().get(documentId=DOC_ID).execute()
    print("snapshot:", snapshot(doc))
    paras = paragraphs(doc)
    cap = [p for p in paras if p[2].startswith(CAPTION)]
    assert len(cap) == 1, f"caption matches: {len(cap)}"
    cs = cap[0][0]

    el = None
    for item in doc["body"]["content"]:
        if "paragraph" not in item or item["startIndex"] >= cs:
            continue
        for pe in item["paragraph"].get("elements", []):
            if "inlineObjectElement" in pe:
                el = pe
    assert el is not None, "no image element before caption"
    s, e = el["startIndex"], el["endIndex"]
    assert cs - e <= 2, f"image not adjacent to caption ({e} .. {cs})"
    print(f"old image element @[{s},{e})")
    if not apply:
        print("DRY RUN.")
        return

    reqs = [
        {"insertInlineImage": {
            "location": {"index": s}, "uri": out,
            "objectSize": {
                "width": {"magnitude": width_pt, "unit": "PT"},
                "height": {"magnitude": height_pt, "unit": "PT"}}}},
        # old image element shifted by the 1 inserted char
        {"deleteContentRange": {"range": {"startIndex": s + 1,
                                          "endIndex": e + 1}}},
    ]
    svc.documents().batchUpdate(documentId=DOC_ID,
                                body={"requests": reqs}).execute()
    print("APPLIED.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
