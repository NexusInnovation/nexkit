
# Contributing to Nexkit (Spec Kit)

Welcome — thank you for wanting to contribute. This document is a concise, step-by-step guide to get new developers up and running quickly: how to set up a local development environment, modify and test the project locally, publish changes, and create releases (with versioning guidance).

## Quick summary

- Setup: Install Python 3.11+, Git, the `uv` tool, and an editor (VS Code recommended). Create a fork and clone.
- Local dev: Use `uv` to sync dependencies, run the CLI during development, and use the included scripts to run tests and linters.
- Publish: Create a branch, commit changes, open a PR with tests/docs, and wait for review.
- Releases: The repository uses semantic-style versioning (major.minor.patch). The CI computes the next patch version automatically; bump major/minor manually when appropriate.

## 1) Prerequisites and environment setup

These instructions assume you are on Windows (PowerShell) but are similar for macOS/Linux.

1. Install Python 3.11 or later
	- Download and install from https://www.python.org/downloads/
	- Make sure `python --version` or `py -3 --version` shows 3.11+

2. Install Git
	- https://git-scm.com/downloads
	- Configure your name and email:
	  ```powershell
	  git config --global user.name "Your Name"
	  git config --global user.email "you@example.com"
	  ```

3. Install the `uv` tool (used by this repo for tasks)
	- `uv` is the package manager/runner used by this project. Follow https://docs.astral.sh/uv/ to install.
	- Verify with:
	  ```powershell
	  uv --version
	  ```

4. Install GitHub CLI (optional but recommended for release and workflow runs)
	- https://cli.github.com/
	- Authenticate: `gh auth login`

5. Clone the repository
	- Fork the repository on GitHub (recommended) then:
	  ```powershell
	  git clone https://github.com/<your-user>/nexkit.git
	  cd nexkit
	  ```

6. Create a virtual environment (optional but recommended)
	- Using venv:
	  ```powershell
	  python -m venv .venv
	  .\.venv\Scripts\Activate.ps1
	  ```

7. Install / sync project dependencies
	- The repo uses `uv` to manage setup tasks. Run:
	  ```powershell
	  uv sync
	  ```
	- Confirm CLI help works:
	  ```powershell
	  uv run nexkit --help
	  ```

## 2) Modify, run and test locally

A disciplined workflow keeps changes small, tested, and documented.

1. Create a feature branch
	```powershell
	git checkout -b feat/my-feature
	```

2. Make changes
	- Edit files in `src/nexkit/`, `templates/`, or scripts in `scripts/` as appropriate.
	- Keep changes focused: one logical change per branch/PR.

3. Run linters and unit checks
	- Project-specific checks are available via `uv` tasks. Run the repo's check task:
	  ```powershell
	  uv run nexkit check
	  ```
	- If you add Python code, run unit tests (if any exist) or add tests to `tests/`.

4. Run the CLI locally to exercise integration
	- There are small helper CLI commands bundled, for example:
	  ```powershell
	  uv run nexkit.specify --help
	  uv run nexkit.plan --help
	  ```
	- Use your editor's debugger or simple `print`/logging to validate logic.

5. Test templates and scripts
	- Templates are in `templates/`. If you changed templates, exercise them using the CLI or sample projects.
	- Scripts to build release artifacts are under `.github/workflows/scripts/`. Test them locally when appropriate but be careful: scripts that use `gh` will act on your authenticated GitHub account.

6. Write or update documentation
	- Update `README.md`, `docs/`, or `templates/` files if your changes affect the user experience.

7. Commit changes and push
	```powershell
	git add -A
	git commit -m "feat: short description of change"
	git push origin feat/my-feature
	```

## 3) Submit a Pull Request

1. Open a PR from your branch to `main` on the repository (or to the main repo if you have push access).
2. In the PR description:
	- Describe the change; show short examples if applicable.
	- Include testing steps and evidence that you ran the checks locally.
	- If you used AI assistance, disclose it (see policy in the repository).

3. Add reviewers and wait for CI to run
	- CI will run the `Create Release` workflow (only on main) and other checks. Make sure your changes are compatible.

4. Address review feedback: update code, tests, and docs as requested.

## 4) Publishing your update (merge & release process)

A. Merging the PR
- After reviews and passing CI, merge the PR into `main` using a merge commit or squash (follow repo conventions).

B. How releases are created
- The repository has a GitHub Actions workflow (`.github/workflows/release.yml`) that runs on pushes to `main` and on manual dispatch.
- It determines the next version by incrementing the patch number (vMAJOR.MINOR.PATCH) from the most recent tag.
- If the computed release tag already exists, the workflow normally skips release creation to avoid duplicates.

C. Creating a release manually or when you need to re-publish
- To create a release automatically: merge to `main` and the workflow will attempt to create a release for the computed version (if it does not already exist).
- To re-create the same release (for example, you need to re-upload assets), use the workflow_dispatch with `force_release=true`.
  - From the GitHub UI: Actions -> Create Release -> Run workflow -> set `force_release` to `true`.
  - Or using `gh`:
	 ```powershell
	 gh workflow run release.yml --ref main -f force_release=true
	 ```
  - This will delete the existing release (and the remote tag if present) and create a fresh release with the same tag and the newly generated assets.

D. When to bump major or minor version
- Patch (x.y.Z): default automatic increment. Use for bug fixes, minor improvements, or non-breaking changes. The workflow automatically increments the patch number.
- Minor (x.Y.z): bump the minor version when you add new features in a backward-compatible way or add new templates or CLI features that are additive.
- Major (X.y.z): bump the major version when you make incompatible changes (breaking changes to CLI behavior, removal of features, or API changes that will break existing users).

How to perform a manual major/minor bump
1. Decide the new version number and update `pyproject.toml` or other canonical version source if required by your change (the workflow will update `pyproject.toml` for releases, but for major/minor bumps it's clearer to update it in the PR and call that out in the PR body).
2. Add a note in the PR: why major/minor bumped and migration guidance for users.
3. Merge to `main`. The release workflow will still compute the next patch tag unless you explicitly create a release tag yourself — if you need a deterministic version (for major/minor), tag the commit manually and push the tag:
	```powershell
	git tag v2.0.0
	git push origin v2.0.0
	```
	The workflow will pick up tags and release as configured.

## 5) Additional tips and guardrails

- Keep changes atomic and tests small. Large PRs are harder to review.
- Document any user-facing changes in `docs/` and in the PR description.
- If you must re-create a release for any reason, prefer the `force_release` workflow path rather than manually deleting things on GitHub unless you understand the consequences.
- Avoid running release scripts (`.github/workflows/scripts/*`) against the real repo when testing locally unless you are comfortable with `gh` and tags; prefer running them in a fork or with a dry-run approach.

## 6) Troubleshooting

- Workflow skipped because release exists: either merge a new commit so the computed patch increments, or run the `Create Release` workflow with `force_release=true` (see above).
- Assets failed to upload: check the release workflow logs. You can re-run the workflow from the Actions UI or use `gh` to upload assets to an existing release.

## 7) Security & contribution rules

- Follow the Contributor Code of Conduct in `CODE_OF_CONDUCT.md`.
- Disclose any AI assistance in PRs according to the repository policy.
- Do not commit secrets. Use repository secrets for credentials in workflows.

## 8) Contacts and support

If you get stuck, open an issue describing the problem, include logs and commands you ran, and tag maintainers. Thank you for contributing!

---

This document was updated to give a clear, step-by-step onboarding flow for new developers: environment setup, local testing, publishing changes, and releases. If you'd like, I can also:

- Add a small `DEVELOPER.md` with exact `uv` task examples and sample `gh` commands tailored to this repo.
- Add a short checklist template for PRs to ensure consistent contributions.
