"""Fixed-seed reproducibility protocol: every run writes a manifest with the
seed, git commit, and parameter-file checksums alongside its outputs."""
import datetime
import json
import os
import subprocess

from .config import BASE, params_checksum

RESULTS = os.path.join(BASE, "results")


def git_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=BASE,
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "no-git"


def write_manifest(kind, seed, years, extra=None):
    os.makedirs(RESULTS, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest = {
        "kind": kind,
        "timestamp": stamp,
        "seed": seed,
        "years": years,
        "git_commit": git_hash(),
        "params_checksum": params_checksum(),
    }
    if extra:
        manifest.update(extra)
    path = os.path.join(RESULTS, f"{kind}_{stamp}.json")
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    return path
