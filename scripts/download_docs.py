#!/usr/bin/env python3
"""Download the paper (Google Doc) and P&L projection (spreadsheet) locally."""
import io
import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.path.join(BASE, "google_key.json")
OUT = os.path.join(BASE, "source_docs")
os.makedirs(OUT, exist_ok=True)

DOC_ID = "1XuVqXKpqiPj3FT5PhPtYTEqAr04RU0wbSHx0xgmCaGY"
SHEET_ID = "1c0zkBq99q-QMyIM_ZavoNNthPUTxDFuW"

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
drive = build("drive", "v3", credentials=creds)


def export(file_id, mime, out_path):
    req = drive.files().export_media(fileId=file_id, mimeType=mime)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    print(f"exported {out_path} ({len(buf.getvalue())} bytes)")


def download_raw(file_id, out_path):
    req = drive.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    print(f"downloaded {out_path} ({len(buf.getvalue())} bytes)")


for fid, label in [(DOC_ID, "paper"), (SHEET_ID, "pnl")]:
    meta = drive.files().get(fileId=fid, fields="id,name,mimeType,size").execute()
    print(json.dumps(meta, indent=2))

# Paper: markdown + docx
export(DOC_ID, "text/markdown", os.path.join(OUT, "paper.md"))
export(DOC_ID, "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
       os.path.join(OUT, "paper.docx"))

# P&L: could be a native Google Sheet or an uploaded xlsx
meta = drive.files().get(fileId=SHEET_ID, fields="mimeType,name").execute()
if meta["mimeType"] == "application/vnd.google-apps.spreadsheet":
    export(SHEET_ID, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
           os.path.join(OUT, "pnl_projection.xlsx"))
else:
    download_raw(SHEET_ID, os.path.join(OUT, "pnl_projection.xlsx"))
