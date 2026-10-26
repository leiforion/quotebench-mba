#!/usr/bin/env python3
"""Fetch the paper via the Google Docs API and convert to Markdown.

Saves:
  source_docs/paper.json  - raw Docs API payload (for later write-back mapping)
  source_docs/paper.md    - readable/editable markdown conversion
"""
import json
import os
import re
import warnings

warnings.filterwarnings("ignore")

from google.oauth2 import service_account
from googleapiclient.discovery import build

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "source_docs")
os.makedirs(OUT, exist_ok=True)
DOC_ID = "1XuVqXKpqiPj3FT5PhPtYTEqAr04RU0wbSHx0xgmCaGY"

creds = service_account.Credentials.from_service_account_file(
    os.path.join(BASE, "google_key.json"),
    scopes=["https://www.googleapis.com/auth/documents.readonly"],
)
docs = build("docs", "v1", credentials=creds)
doc = docs.documents().get(documentId=DOC_ID).execute()

with open(os.path.join(OUT, "paper.json"), "w") as f:
    json.dump(doc, f, indent=1)

HEADING_MAP = {
    "TITLE": "#",
    "SUBTITLE": "##",
    "HEADING_1": "#",
    "HEADING_2": "##",
    "HEADING_3": "###",
    "HEADING_4": "####",
    "HEADING_5": "#####",
    "HEADING_6": "######",
}

lists = doc.get("lists", {})
footnotes = doc.get("footnotes", {})


def render_text_run(el):
    tr = el.get("textRun")
    if tr is None:
        if "footnoteReference" in el:
            fid = el["footnoteReference"]["footnoteId"]
            num = el["footnoteReference"].get("footnoteNumber", "?")
            return f"[^{num}]"
        if "inlineObjectElement" in el:
            return "[IMAGE]"
        if "horizontalRule" in el:
            return "\n---\n"
        return ""
    text = tr.get("content", "")
    style = tr.get("textStyle", {})
    stripped = text.rstrip("\n")
    trailing = "\n" if text.endswith("\n") else ""
    if not stripped:
        return text
    if style.get("link"):
        url = style["link"].get("url", "")
        stripped = f"[{stripped}]({url})"
    if style.get("bold") and style.get("italic"):
        stripped = f"***{stripped}***"
    elif style.get("bold"):
        stripped = f"**{stripped}**"
    elif style.get("italic"):
        stripped = f"*{stripped}*"
    return stripped + trailing


def render_paragraph(p):
    parts = [render_text_run(el) for el in p.get("elements", [])]
    text = "".join(parts).rstrip("\n")
    style = p.get("paragraphStyle", {})
    named = style.get("namedStyleType", "NORMAL_TEXT")
    prefix = ""
    if "bullet" in p:
        b = p["bullet"]
        nest = b.get("nestingLevel", 0)
        lid = b["listId"]
        glyph = ""
        lprops = lists.get(lid, {}).get("listProperties", {}).get("nestingLevels", [])
        if nest < len(lprops) and lprops[nest].get("glyphType") not in (None, "GLYPH_TYPE_UNSPECIFIED"):
            glyph = "1. "
        else:
            glyph = "- "
        prefix = "  " * nest + glyph
    elif named in HEADING_MAP:
        prefix = HEADING_MAP[named] + " "
    if not text.strip():
        return ""
    return prefix + text


def render_table(t):
    rows = []
    for row in t.get("tableRows", []):
        cells = []
        for cell in row.get("tableCells", []):
            cell_text = []
            for ce in cell.get("content", []):
                if "paragraph" in ce:
                    cell_text.append(
                        "".join(render_text_run(el) for el in ce["paragraph"].get("elements", [])).strip()
                    )
            cells.append(" ".join(ct for ct in cell_text if ct).replace("|", "\\|"))
        rows.append("| " + " | ".join(cells) + " |")
    if rows:
        ncols = rows[0].count("|") - 1
        rows.insert(1, "|" + "---|" * ncols)
    return "\n".join(rows)


out_lines = []
for item in doc["body"]["content"]:
    if "paragraph" in item:
        line = render_paragraph(item["paragraph"])
        out_lines.append(line)
    elif "table" in item:
        out_lines.append(render_table(item["table"]))
        out_lines.append("")
    elif "sectionBreak" in item:
        continue

# footnote bodies
if footnotes:
    out_lines.append("\n---\n## Footnotes\n")
    for fid, fn in footnotes.items():
        texts = []
        for ce in fn.get("content", []):
            if "paragraph" in ce:
                texts.append("".join(render_text_run(el) for el in ce["paragraph"].get("elements", [])).strip())
        out_lines.append(f"[{fid}]: " + " ".join(texts))

md = "\n\n".join(l for l in out_lines if l is not None)
md = re.sub(r"\n{3,}", "\n\n", md)

with open(os.path.join(OUT, "paper.md"), "w") as f:
    f.write(md)

words = len(re.findall(r"\b\w+\b", md))
print(f"Title: {doc.get('title')}")
print(f"Markdown saved: {len(md)} chars, ~{words} words")
