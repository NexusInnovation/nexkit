# GitHub Release Workflow Fix

## Problem Description

The GitHub Actions release workflow was skipping release creation when changes were pushed to `main`, but would create duplicate releases when tags were manually pushed.

### Symptom
- Push to `main` → Release creation skipped
- Manually push tag `v0.1.6` → Creates release for `v0.1.6`
- Next push to `main` → Increments to `v0.1.7` and creates another release

## Root Cause

The `gh release create` command **automatically creates a git tag** when creating a release. This caused a race condition:

1. When the workflow runs normally:
   - It calculates next version (e.g., v0.1.5)
   - Checks if release exists (it doesn't)
   - Runs `gh release create v0.1.5` which automatically creates the tag
   
2. When you manually push a tag:
   - Tag already exists in the repository
   - The workflow's version calculation sees this tag
   - Creates a release for that tag
   - On next push, it increments and creates another release

The issue was that **tags were being created implicitly** by `gh release create` rather than explicitly by the workflow.

## Solution

### Fix 1: Use `git tag` Instead of `git describe`

Modified `.github/workflows/scripts/get-next-version.sh` to use `git tag -l --sort=-v:refname` which:
- Lists **all** tags regardless of commit ancestry
- Sorts by version number (handles v0.0.10 > v0.0.9 correctly)
- Always finds the truly latest tag

```bash
# Get the latest tag using version sort
LATEST_TAG=$(git tag -l --sort=-v:refname | head -n 1)
if [ -z "$LATEST_TAG" ]; then
  LATEST_TAG="v0.0.0"
fi
```

### Fix 2: Explicit Tag Fetching

Added explicit tag fetch step in `.github/workflows/release.yml`:

```yaml
- name: Fetch all tags
  run: |
    git fetch --tags --force
```

### Fix 3: Explicit Tag Creation

Modified `.github/workflows/scripts/create-github-release.sh` to create tags before release:

```bash
# Check if tag exists, if not create it
if ! git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "Creating tag $VERSION" >&2
  git tag "$VERSION"
  git push origin "$VERSION"
else
  echo "Tag $VERSION already exists" >&2
fi

gh release create "$VERSION" \
  # ... rest of the command
```

## Expected Behavior After Fix

1. **Normal push to `main`** (with v0.0.9 as latest tag):
   - Workflow explicitly fetches all tags
   - `get-next-version.sh` finds v0.0.9 (latest by version sort)
   - Calculates next version: v0.0.10
   - Checks if release v0.0.10 exists (it doesn't)
   - Creates tag v0.0.10 and pushes it
   - Creates release v0.0.10
   - ✅ Release created successfully

2. **Manual tag push**:
   - If you manually push tag v0.0.11
   - Next workflow run finds v0.0.11 as latest
   - Calculates v0.0.12 as next version
   - Creates release v0.0.12
   - ✅ No duplicate releases, proper increment

3. **Subsequent pushes**:
   - Each push increments from the actual latest tag
   - No skipped releases due to tag ancestry issues
   - ✅ Version increments correctly

## Testing the Fix

To verify the fix works:

1. Make a change to a tracked file (e.g., in `src/`, `templates/`, etc.)
2. Commit and push to `main`
3. Check that the workflow runs and creates a release
4. Verify that only one release is created per version

## Prevention

- Don't manually create tags unless necessary
- If you do create a tag manually, ensure it doesn't conflict with the auto-versioning scheme
- Use the `workflow_dispatch` with `force_release: true` if you need to recreate a release

## Related Files

- `.github/workflows/release.yml` - Main workflow definition
- `.github/workflows/scripts/create-github-release.sh` - Release creation script (FIXED)
- `.github/workflows/scripts/get-next-version.sh` - Version calculation
- `.github/workflows/scripts/check-release-exists.sh` - Release existence check
