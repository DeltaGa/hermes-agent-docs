[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Update](https://img.shields.io/github/last-commit/DeltaGa/hermes-agent-docs/main.svg?label=docs%20updated)](https://github.com/DeltaGa/hermes-agent-docs/commits/main)

# Hermes Agent Documentation v1.0.0

## Automated Mirror of the Official Docs

**Version:** 1.0.0  
**Release Date:** August 9, 2026  
**Source:** [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)  
**Live Site:** [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)

---

## Table of Contents

- [Overview](#overview)
- [Purpose](#purpose)
- [Source](#source)
- [How Updates Work](#how-updates-work)
- [Manual Sync](#manual-sync)
- [Repository Layout](#repository-layout)
- [Author](#author)

---

## Overview

An automated mirror of the Hermes Agent documentation. The official documentation lives in the source repository under `website/docs/` and is published to [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/). This repository mirrors that documentation as plain Markdown files so it can be read, searched, diffed, and consumed by tools and agents.

### Key Capabilities

- **Automatic updates** - A GitHub Actions workflow fetches the latest documentation every three hours
- **Byte-for-byte fidelity** - The mirror is identical to the upstream source; no content is rewritten or transformed
- **Full tree preservation** - The complete directory structure and file extensions are preserved
- **Dependency-free fetching** - The fetch script uses only the Python standard library
- **Manual trigger** - The update workflow can be run on demand from the Actions tab

---

## Purpose

The live documentation site serves rendered HTML. This repository provides the same content as plain Markdown so that:

- Documentation can be read and searched locally
- Changes over time are visible as a git diff
- Tools and agents can ingest the docs directly as files

---

## Source

- **Upstream repository:** [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **Source path:** `website/docs/`
- **Branch:** `main`
- **Local mirror:** `docs/`

The mirror is byte-for-byte identical to the upstream source.

---

## How Updates Work

A GitHub Actions workflow runs every three hours and fetches the latest documentation from the upstream repository:

1. Reads the upstream `website/docs/` tree from the GitHub API.
2. Downloads each file and writes it into `docs/`.
3. Removes files that were deleted upstream.
4. Commits and pushes when anything changed.

The workflow can also be triggered manually from the Actions tab.

| Component | Purpose |
|-----------|---------|
| `.github/workflows/update-docs.yml` | Update workflow |
| `scripts/fetch_hermes_docs.py` | Fetch script |
| `docs_manifest.json` | Tracks the last-fetched hash of every file |

---

## Manual Sync

Run the fetch script locally to pull the latest documentation:

```bash
python scripts/fetch_hermes_docs.py
```

---

## Repository Layout

```
hermes-agent-docs/
├── docs/                 # Mirrored documentation (matches upstream website/docs/)
├── .github/workflows/    # GitHub Actions workflow for automatic updates
├── scripts/              # Fetch script
├── docs_manifest.json    # Per-file content hashes from the last sync
└── README.md             # This file
```

---

## License

The mirrored documentation content is owned by [Nous Research](https://nousresearch.com) and licensed under the MIT License, as published in the upstream [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) repository. The supporting files in this repository are licensed under the MIT License; see [LICENSE](LICENSE).

---

## Author

**Tchicdje Kouojip Joram Smith (DeltaGa)**  
Email: dev.github.tkjoramsmith@outlook.com  
GitHub: [https://github.com/DeltaGa](https://github.com/DeltaGa)

---

© 2026 DeltaGa. All rights reserved.