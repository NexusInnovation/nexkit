#!/usr/bin/env bash
set -euo pipefail

# check-release-exists.sh
# Check if a GitHub release already exists for the given version
# Usage: check-release-exists.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

if [[ "${FORCE_RELEASE:-false}" == "true" ]]; then
  echo "FORCE_RELEASE is set to true; treating release as non-existent for creation" >&2
  echo "exists=false" >> $GITHUB_OUTPUT
  exit 0
fi

if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "exists=true" >> $GITHUB_OUTPUT
  echo "Release $VERSION already exists, skipping..."
else
  echo "exists=false" >> $GITHUB_OUTPUT
  echo "Release $VERSION does not exist, proceeding..."
fi