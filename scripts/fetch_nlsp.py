"""Fetch the NASA bed rest Case Report Form datasets from the NASA Life Sciences Portal.

    python scripts/fetch_nlsp.py

Open downloads: no account, no request form, no click-through. All daily vitals, fluid,
meal, symptom and medication logs for UTMB Campaigns 1, 3 and 11 (CFT70) sit under one
experiment, "Case Report Form". Files land in data/raw/nlsp/<folder>/ (gitignored) and
data/manifests/nlsp.json records each file's UUID, size and SHA-256.

Idempotent: a file already on disk with the expected size is re-hashed, not re-downloaded.
The API approach follows the open project MiladBahariQaragoz/BedrestToMars.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
API = "https://nlsp.nasa.gov/api/v1"
EXPERIMENT = "eeb9bd34-bdd4-5115-b139-adf2c9927962"  # "Case Report Form"
DEST = REPO_ROOT / "data" / "raw" / "nlsp"
MANIFEST = REPO_ROOT / "data" / "manifests" / "nlsp.json"
HEADERS = {"User-Agent": "bedrest-research-client/1.0"}
PAUSE_SECONDS = 0.15


def _get(url: str, retries: int = 3) -> requests.Response:
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=90)
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2.0 * (attempt + 1))
    raise AssertionError("unreachable")


def fetch() -> dict:
    tree = _get(f"{API}/data/lsda_experiment/{EXPERIMENT}/full").json()
    folders = tree["related"]["datasets"]
    files, downloaded = [], 0
    for folder in sorted(folders, key=lambda f: f["label"]):
        folder_dir = DEST / folder["label"]
        folder_dir.mkdir(parents=True, exist_ok=True)
        entries = folder.get("children") or []
        for entry in sorted(entries, key=lambda e: e["label"]):
            name = entry["label"] if "." in entry["label"] else f"{entry['label']}.csv"
            target = folder_dir / name
            expected = int(entry.get("file_size") or 0)
            if not (target.exists() and target.stat().st_size == expected):
                target.write_bytes(_get(f"{API}/files/{entry['key']}/download").content)
                downloaded += 1
                time.sleep(PAUSE_SECONDS)
            files.append({
                "folder": folder["label"], "file": name, "uuid": entry["key"],
                "bytes": target.stat().st_size,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            })
        print(f"  {folder['label']:<40} {len(entries):>3} files")

    manifest = {
        "source": API, "experiment": EXPERIMENT, "experiment_title": tree["record"].get("experiment_title"),
        "accessed": time.strftime("%Y-%m-%d"), "files": files,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    total = sum(f["bytes"] for f in files)
    print(f"{downloaded} downloaded, {len(files) - downloaded} already present, "
          f"{len(files)} files, {total / 1024:.0f} KB -> {MANIFEST.relative_to(REPO_ROOT)}")
    return manifest


if __name__ == "__main__":
    fetch()
