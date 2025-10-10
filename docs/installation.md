# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows; PowerShell scripts now supported without WSL)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), or [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init .
# or use the --here flag
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init --here
```

### Nexkit AI Agent

You can proactively choose your AI agent during initialization:

```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <project_name> --ai claude
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <project_name> --ai gemini
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <project_name> --ai copilot
```

### Nexkit Script Type (Shell vs PowerShell)

All automation scripts now have both Bash (`.sh`) and PowerShell (`.ps1`) variants.

Auto behavior:
- Windows default: `ps`
- Other OS default: `sh`
- Interactive mode: you'll be prompted unless you pass `--script`

Force a specific script type:
```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <project_name> --script sh
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <project_name> --script ps
```

### Global Installation (Optional)

If you plan to use the tool frequently, you can install it globally:

```bash
uv tool install git+https://github.com/NexusInnovation/nexkit.git
```

Then run:
```bash
nexkit init <project_name>
nexkit check  # to verify your system has all requirements
```
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
If you're in a corporate environment or don't want to install dependencies:

```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <project_name> --ai claude --ignore-agent-tools
```
```

## Verification

After initialization, you should see the following commands available in your AI agent:

**Core Commands:**
- `/nexkit.constitution` - Create project principles
- `/nexkit.specify` - Create specifications
- `/nexkit.plan` - Generate implementation plans  
- `/nexkit.tasks` - Break down into actionable tasks
- `/nexkit.implement` - Execute implementation

**Optional Commands:**
- `/nexkit.clarify` - Clarify underspecified areas
- `/nexkit.analyze` - Cross-artifact consistency analysis
- `/nexkit.checklist` - Generate quality checklists
- `/nexkit.commit` - Generate intelligent commit messages
- `/nexkit.implement-workitem` - Quick implementation with Azure DevOps work items
- `/nexkit.refine-workitem` - Add refinement to existing user stories

The `.nexkit/scripts` directory will contain both `.sh` and `.ps1` scripts.

## Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```
