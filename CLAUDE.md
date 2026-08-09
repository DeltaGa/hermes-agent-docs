# Hermes Agent Documentation Mirror

This repository contains automated mirrors of the Hermes Agent documentation
from https://hermes-agent.nousresearch.com/docs/.

The docs are periodically updated via GitHub Actions.

## For /docs Commands

When responding to /docs commands:

1. Read documentation files from the `docs/` directory only.
2. Use the directory structure to know available topics.
3. Do not edit files under `docs/` directly - they are overwritten by the
   update workflow and any manual edits will be lost.

## Files to ultrathink about

@scripts/
@.github/workflows/
@README.md
@docs_manifest.json