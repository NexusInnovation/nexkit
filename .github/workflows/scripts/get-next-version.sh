#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Calculate the next version based on the latest git tag and output GitHub Actions variables
# Usage: get-next-version.sh

# Debug: Show all tags
echo "All tags:" >&2
git tag -l --sort=-v:refname | head -n 5 >&2

# Get the latest tag, or use v0.0.0 if no tags exist
# Use git tag with version sort instead of git describe to get the actual latest tag
# regardless of commit ancestry (important in CI where tags might be created after commits)
LATEST_TAG=$(git tag -l --sort=-v:refname | head -n 1)
if [ -z "$LATEST_TAG" ]; then
  LATEST_TAG="v0.0.0"
fi
echo "Latest tag found: $LATEST_TAG" >&2
echo "latest_tag=$LATEST_TAG" >> $GITHUB_OUTPUT

# Extract version number and increment
VERSION=$(echo $LATEST_TAG | sed 's/v//')
IFS='.' read -ra VERSION_PARTS <<< "$VERSION"
MAJOR=${VERSION_PARTS[0]:-0}
MINOR=${VERSION_PARTS[1]:-0}
PATCH=${VERSION_PARTS[2]:-0}

echo "Version parts - Major: $MAJOR, Minor: $MINOR, Patch: $PATCH" >&2

# Increment patch version
PATCH=$((PATCH + 1))
NEW_VERSION="v$MAJOR.$MINOR.$PATCH"

echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
echo "New version will be: $NEW_VERSION"