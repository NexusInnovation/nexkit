# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Nexkit** is a CLI tool that bootstraps projects for Spec-Driven Development (SDD). It enables AI coding agents (Claude Code, GitHub Copilot, Gemini, Cursor, Windsurf, etc.) to collaborate with developers in a structured specification-to-implementation workflow.

**Core Philosophy**: Specifications become executable artifacts that directly generate working implementations, flipping traditional development where code is king and specs are discarded scaffolding.

## Development Commands

### Environment Setup

```bash
# This project uses uv for Python package management
# Install uv first: https://docs.astral.sh/uv/

# Install dependencies
uv sync

# Run the CLI during development
uv run nexkit --help
uv run nexkit init test-project --ai claude
uv run nexkit check
```

### Testing

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_gitignore.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src/nexkit --cov-report=html
```

### Building and Installation

```bash
# Build the package
uv build

# Install locally for testing (persistent installation)
uv tool install --force --editable .

# Test the installed version
nexkit --help
nexkit init test-project

# Uninstall
uv tool uninstall nexkit
```

## Architecture

### Source Code Structure

```
src/nexkit/
├── __init__.py        - Main CLI application (1,514 lines)
│                        • StepTracker: Progress renderer for initialization
│                        • CLI commands: init, check, add-exclusion, remove-exclusion
│                        • Template download/extraction from GitHub releases
│                        • MCP server detection and configuration
│                        • Tool detection (git, claude, gemini, etc.)
└── gitignore.py       - Git exclusion management (499 lines)
                         • Safe .gitignore section manipulation
                         • Atomic file operations with temp files
                         • Tracked file detection and cleanup guidance
```

### Template System

Templates are **not embedded** in the package - they are downloaded from GitHub releases as ZIP files. This allows:
- Templates to evolve independently of CLI updates
- Agent-specific customizations (different templates for Claude vs Copilot vs Cursor)
- Better version management

**Template Variants**:
- `nexkit-template-{ai}-{script}.zip` (e.g., `nexkit-template-claude-sh.zip`)
- `{ai}`: claude, copilot, gemini, cursor, windsurf, qwen, opencode, codex, etc.
- `{script}`: sh (bash/zsh) or ps (PowerShell)

**Template Contents**:
```
templates/
├── commands/                  - AI agent slash command definitions
│   ├── constitution.md        - Create project principles
│   ├── specify.md            - Generate specifications
│   ├── plan.md               - Create implementation plans
│   ├── tasks.md              - Break down into tasks
│   ├── implement.md          - Execute implementation
│   ├── clarify.md            - Structured clarification workflow
│   ├── analyze.md            - Cross-artifact consistency
│   ├── checklist.md          - Quality validation checklists
│   ├── commit.md             - Intelligent commit generation
│   ├── implement-workitem.md - Azure DevOps integration
│   └── refine-workitem.md    - Work item refinement
├── spec-template.md          - Feature specification structure
├── plan-template.md          - Implementation plan structure
├── tasks-template.md         - Task breakdown structure
└── vscode-settings.json      - Recommended VS Code settings
```

### Scripts System (Dual Implementation)

Scripts are deployed to user projects in **both bash and PowerShell variants** for cross-platform support:

```
scripts/
├── bash/
│   ├── common.sh                - Core utilities (path resolution, git detection)
│   ├── create-new-feature.sh    - Creates feature branch and spec directory
│   ├── setup-plan.sh            - Initializes plan.md and related files
│   ├── check-prerequisites.sh   - Validates spec/plan/tasks existence
│   └── update-agent-context.sh  - Updates agent-specific context files
└── powershell/
    └── [equivalent .ps1 files]
```

**Key Script Patterns**:
- Scripts output JSON when called with `--json` flag for reliable parsing
- Scripts check `NEXKIT_FEATURE` environment variable before git
- Non-git repository support via directory naming fallback

### Feature Branch Naming Convention

**Pattern**: `###-feature-name` (e.g., `001-user-auth`, `002-payment-system`)

**Purpose**:
- Automatic feature directory discovery in `specs/`
- Ordering and numbering
- Non-Git fallback (via directory names when git unavailable)

**Enforcement**: Scripts validate and error if pattern not followed (unless `NEXKIT_FEATURE` env var is set)

### MCP (Model Context Protocol) Integration

Nexkit detects and configures MCP servers:

1. **@azure-devops/mcp** - Azure DevOps integration
   - Configured at **project-level** (`.vscode/mcp.json`)
   - Requires: org name, tenant ID, project name
   - Uses azcli authentication

2. **@upstash/context7-mcp** - Context management (user-level)
3. **@modelcontextprotocol/server-sequential-thinking** - Structured reasoning (user-level)

**Configuration Locations**:
- User-level: `~/.config/Code/User/mcp.json` (Linux/Mac) or `%APPDATA%/Code/User/mcp.json` (Windows)
- Project-level: `.vscode/mcp.json` (for Azure DevOps with org-specific settings)

## Key Architectural Decisions

### 1. Template Downloading vs Embedding
Templates are pulled from GitHub releases rather than embedded in the package. This allows templates to evolve without CLI updates and enables agent-specific variants.

### 2. Dual Script System (Bash + PowerShell)
Both script variants are deployed to projects. Users choose during `nexkit init`. Both output identical JSON for parsing reliability.

### 3. JSON Output from Shell Scripts
Scripts output structured JSON when called with `--json` flag. This ensures reliable parsing by AI agents without shell parsing issues.

**Example**:
```bash
create-new-feature.sh --json "Build a photo album app"
# Outputs: {"BRANCH_NAME": "001-photo-album", "SPEC_FILE": "/path/specs/001-photo-album/spec.md", ...}
```

### 4. Atomic .gitignore Operations
`.gitignore` modifications use write-to-temp-then-rename pattern to prevent corruption. Boundary markers (`# BEGIN nexkit exclusions` / `# END nexkit exclusions`) enable safe section removal.

### 5. Non-Git Repository Support
Via `NEXKIT_FEATURE` environment variable, Nexkit can work without git by discovering the latest feature directory via naming convention.

### 6. Claude Local Path Priority
After `claude migrate-installer`, the executable moves to `~/.claude/local/claude`. Nexkit prioritizes this path for proper detection.

## Release Process

Releases are automated via GitHub Actions (`.github/workflows/release.yml`):

1. Triggered on push to `main` branch (paths: `memory/`, `scripts/`, `templates/`, `src/`)
2. Version is auto-incremented based on latest tag
3. Creates template ZIP variants for all AI agent + script combinations
4. Generates release notes from commits
5. Creates GitHub release with all template ZIPs attached

**Manual release**: Use workflow dispatch with `force_release: true` to recreate existing releases.

## Environment Variables

- `GH_TOKEN` / `GITHUB_TOKEN`: GitHub API authentication for template downloads
- `NEXKIT_FEATURE`: Override feature detection for non-Git repos (set to feature directory name like `001-photo-albums`)
- `APPDATA`: Windows VS Code settings folder (for mcp.json)

**Setting NEXKIT_FEATURE**: Must be set in the context of the AI agent before using nexkit commands.

## Project Structure After Initialization

When users run `nexkit init my-project`, the resulting structure is:

```
my-project/
├── .nexkit/
│   ├── memory/
│   │   └── constitution.md           # Project principles
│   ├── scripts/
│   │   ├── bash/                     # Helper scripts
│   │   └── powershell/
│   ├── specs/
│   │   └── [001-feature-name]/       # Per-feature specs
│   │       ├── spec.md               # Feature specification
│   │       ├── plan.md               # Implementation plan
│   │       ├── tasks.md              # Task breakdown
│   │       ├── research.md           # Technical decisions
│   │       ├── data-model.md         # Entity definitions
│   │       ├── quickstart.md         # Integration examples
│   │       ├── checklists/           # Quality checklists
│   │       └── contracts/            # API specifications
│   └── templates/
│       ├── spec-template.md
│       ├── plan-template.md
│       └── ...
├── .github/
│   └── prompts/                      # AI agent slash commands
│       ├── nexkit.constitution.md
│       ├── nexkit.specify.md
│       └── ...
└── [project source code]
```

## Workflow: Spec-Driven Development

The typical user workflow involves these phases:

1. **Initialize project**: `nexkit init my-project --ai claude`
2. **Work with your AI agent**: Develop specifications and implementation plans collaboratively
3. **Execute implementation**: Use `/nexkit.implement` to implement from specifications
4. **Commit work**: Use `/nexkit.commit` to generate intelligent commit messages
5. **Azure DevOps integration**: Use `/nexkit.implement-workitem` and `/nexkit.refine-workitem` for work item management

## Dependencies

**Core** (from `pyproject.toml`):
- `typer`: CLI framework
- `rich`: Terminal styling and progress
- `httpx[socks]`: HTTP client for GitHub API
- `platformdirs`: Cross-platform config directories
- `readchar`: Cross-platform keyboard input
- `truststore>=0.10.4`: SSL certificate management

**Runtime** (detected but not required):
- `git`: Version control (recommended)
- `npm`: For MCP server installation
- AI agent CLIs: `claude`, `gemini`, `qwen`, `cursor-agent`, `windsurf`, etc.

## Code Style and Conventions

- Python 3.11+ required
- Use type hints where beneficial
- Shell scripts should be POSIX-compliant (bash) or PowerShell Core compatible
- All user-facing output should avoid emojis (for broader terminal compatibility)
- Progress indicators use circles (●, ○) and colors instead of emojis
- JSON output from scripts must be parseable without shell escaping issues

## Testing Patterns

Tests are organized in `tests/`:
- `tests/unit/` - Unit tests for individual modules
- `tests/integration/` - End-to-end git interaction tests

**Test fixtures** create temporary git repositories:
```python
@pytest.fixture
def temp_repo(tmp_path):
    """Create temporary git repo for testing"""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    subprocess.run(["git", "init"], cwd=repo_path, ...)
    return repo_path
```

## Important Notes

### When Modifying Templates
Templates are deployed to user projects and also shipped in GitHub releases. If you modify templates:
1. Update the template files in `templates/`
2. Ensure changes are backward-compatible or document breaking changes
3. Test with multiple AI agents (Claude, Copilot, Gemini) if applicable
4. Push to `main` to trigger automatic release creation

### When Modifying Scripts
Scripts are copied to user projects during initialization. Changes to scripts:
1. Update both bash (`scripts/bash/`) and PowerShell (`scripts/powershell/`) variants
2. Ensure JSON output format remains consistent
3. Test on both Unix-like systems and Windows
4. Document any new `--json` output fields

### When Adding New AI Agent Support
1. Add agent detection to `check()` command in `src/nexkit/__init__.py`
2. Create template variant: `nexkit-template-{agent}-sh.zip` and `nexkit-template-{agent}-ps.zip`
3. Update release workflow to include new agent in template packaging
4. Add to supported agents table in README.md

### Security Considerations
The CLI displays a security notice about excluding agent credential folders (`.specify/`, `.github/prompts/`) from git. This prevents accidental credential exposure in public repositories.
