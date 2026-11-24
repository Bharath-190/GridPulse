#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$ROOT_DIR/data/external/PV-Generation-Dataset"
REPO_URL="https://github.com/upb-nlp/PV-Generation-Dataset.git"

mkdir -p "$(dirname "$TARGET_DIR")"
if [[ -d "$TARGET_DIR/.git" ]]; then
  echo "Dataset repository already exists: $TARGET_DIR"
  echo "Update it with: git -C '$TARGET_DIR' pull --ff-only"
  exit 0
fi

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: Git is required. Install Git and rerun this script." >&2
  exit 1
fi

git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$TARGET_DIR"
git -C "$TARGET_DIR" sparse-checkout set site_a site_b

echo
echo "Dataset downloaded to: $TARGET_DIR"
echo "Next: python scripts/validate_primary_dataset.py --dataset-dir '$TARGET_DIR'"
