#!/usr/bin/env python3
"""Mirror Hermes Agent documentation from the upstream Nous Research repository.

Fetches the `website/docs` tree of `NousResearch/hermes-agent` and mirrors it
verbatim into the `docs/` directory of this repository, preserving the full
directory structure and file extensions. A manifest tracks the upstream blob
SHA of every file so that unchanged files are left untouched and files that
disappeared upstream are removed.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UPSTREAM_OWNER = "NousResearch"
UPSTREAM_REPO = "hermes-agent"
UPSTREAM_BRANCH = "main"
UPSTREAM_DOCS_PATH = "website/docs"

API_TREE_URL = (
    f"https://api.github.com/repos/{UPSTREAM_OWNER}/{UPSTREAM_REPO}"
    f"/git/trees/{UPSTREAM_BRANCH}?recursive=1"
)
RAW_BASE = (
    f"https://raw.githubusercontent.com/{UPSTREAM_OWNER}/{UPSTREAM_REPO}"
    f"/{UPSTREAM_BRANCH}/{UPSTREAM_DOCS_PATH}/"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
MANIFEST_FILE = REPO_ROOT / "docs_manifest.json"

USER_AGENT = "hermes-agent-docs-mirror/1.0"
MAX_RETRIES = 4
RETRY_BACKOFF_SECONDS = 3
RAW_RATE_LIMIT_DELAY_SECONDS = 0.2


def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        try:
            return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"files": {}}


def save_manifest(manifest: dict, touch_timestamp: bool) -> None:
    if touch_timestamp:
        manifest["last_updated"] = datetime.now(timezone.utc).isoformat()
    manifest["source"] = {
        "owner": UPSTREAM_OWNER,
        "repo": UPSTREAM_REPO,
        "branch": UPSTREAM_BRANCH,
        "path": UPSTREAM_DOCS_PATH,
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def http_get(url: str) -> bytes:
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def discover_upstream_files() -> dict[str, str]:
    payload = json.loads(http_get(API_TREE_URL))
    prefix = f"{UPSTREAM_DOCS_PATH}/"
    blobs = {}
    for entry in payload.get("tree", []):
        if entry.get("type") != "blob":
            continue
        path = entry.get("path", "")
        if path.startswith(prefix):
            blobs[path[len(prefix):]] = entry.get("sha", "")
    if not blobs:
        raise RuntimeError("No documentation files found upstream")
    return dict(sorted(blobs.items()))


def fetch_file(relative_path: str) -> bytes:
    return http_get(RAW_BASE + relative_path)


def write_file(relative_path: str, upstream_sha: str, content: bytes, manifest: dict) -> bool:
    target = DOCS_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    manifest.setdefault("files", {})[relative_path] = {
        "sha": upstream_sha,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
    return True


def remove_obsolete_files(current_files: set[str], manifest: dict) -> list[str]:
    removed = []
    previous = set(manifest.get("files", {}).keys())
    for relative_path in previous - current_files:
        target = DOCS_DIR / relative_path
        if target.exists():
            target.unlink()
            removed.append(relative_path)
            manifest["files"].pop(relative_path, None)
    return removed


def prune_empty_directories(root: Path) -> None:
    for directory in sorted((p for p in root.rglob("*") if p.is_dir()), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass


def main() -> int:
    manifest = load_manifest()
    upstream_shas = discover_upstream_files()
    current_files = set(upstream_shas)

    updated = []
    for relative_path, upstream_sha in upstream_shas.items():
        previous = manifest.get("files", {}).get(relative_path, {}).get("sha")
        if previous == upstream_sha and (DOCS_DIR / relative_path).exists():
            continue
        content = fetch_file(relative_path)
        write_file(relative_path, upstream_sha, content, manifest)
        updated.append(relative_path)
        time.sleep(RAW_RATE_LIMIT_DELAY_SECONDS)

    removed = remove_obsolete_files(current_files, manifest)
    prune_empty_directories(DOCS_DIR)
    save_manifest(manifest, touch_timestamp=bool(updated) or bool(removed))

    print(f"upstream_files={len(upstream_shas)}")
    print(f"updated={len(updated)}")
    print(f"removed={len(removed)}")
    if updated:
        print("updated_detail=" + ", ".join(updated))
    if removed:
        print("removed_detail=" + ", ".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())