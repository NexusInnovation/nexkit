#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}
if [[ "${FORCE_RELEASE:-false}" == "true" ]]; then
  echo "FORCE_RELEASE=true; deleting existing release (if any) and associated tag: $VERSION" >&2
  # Try to delete release and tag if they exist; ignore errors
  gh release view "$VERSION" >/dev/null 2>&1 && gh release delete "$VERSION" --yes || true
  git tag -l "$VERSION" >/dev/null 2>&1 && git push origin --delete "$VERSION" || true
fi

# Check if tag exists, if not create it
if ! git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "Creating tag $VERSION" >&2
  git tag "$VERSION"
  git push origin "$VERSION"
else
  echo "Tag $VERSION already exists" >&2
fi

gh release create "$VERSION" \
  .genreleases/nexkit-template-copilot-sh-"$VERSION".zip \
  .genreleases/nexkit-template-copilot-ps-"$VERSION".zip \
  .genreleases/nexkit-template-claude-sh-"$VERSION".zip \
  .genreleases/nexkit-template-claude-ps-"$VERSION".zip \
  .genreleases/nexkit-template-gemini-sh-"$VERSION".zip \
  .genreleases/nexkit-template-gemini-ps-"$VERSION".zip \
  .genreleases/nexkit-template-cursor-sh-"$VERSION".zip \
  .genreleases/nexkit-template-cursor-ps-"$VERSION".zip \
  .genreleases/nexkit-template-opencode-sh-"$VERSION".zip \
  .genreleases/nexkit-template-opencode-ps-"$VERSION".zip \
  .genreleases/nexkit-template-qwen-sh-"$VERSION".zip \
  .genreleases/nexkit-template-qwen-ps-"$VERSION".zip \
  .genreleases/nexkit-template-windsurf-sh-"$VERSION".zip \
  .genreleases/nexkit-template-windsurf-ps-"$VERSION".zip \
  .genreleases/nexkit-template-codex-sh-"$VERSION".zip \
  .genreleases/nexkit-template-codex-ps-"$VERSION".zip \
  .genreleases/nexkit-template-kilocode-sh-"$VERSION".zip \
  .genreleases/nexkit-template-kilocode-ps-"$VERSION".zip \
  .genreleases/nexkit-template-auggie-sh-"$VERSION".zip \
  .genreleases/nexkit-template-auggie-ps-"$VERSION".zip \
  .genreleases/nexkit-template-roo-sh-"$VERSION".zip \
  .genreleases/nexkit-template-roo-ps-"$VERSION".zip \
  .genreleases/nexkit-template-q-sh-"$VERSION".zip \
  .genreleases/nexkit-template-q-ps-"$VERSION".zip \
  --title "Nexkit Templates - $VERSION_NO_V" \
  --notes-file release_notes.md