<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🌱 NexKit</h1>
    <h3><em>Build high-quality software faster.</em></h3>
</div>

<p align="center">
    <strong>An effort to allow organizations to focus on product scenarios rather than writing undifferentiated code with the help of Spec-Driven Development.</strong>
</p>

<p align="center">
    <a href="https://github.com/NexusInnovation/nexkit/actions/workflows/release.yml"><img src="https://github.com/NexusInnovation/nexkit/actions/workflows/release.yml/badge.svg" alt="Release"/></a>
    <a href="https://github.com/NexusInnovation/nexkit/stargazers"><img src="https://img.shields.io/github/stars/NexusInnovation/nexkit?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/NexusInnovation/nexkit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/NexusInnovation/nexkit" alt="License"/></a>
    <a href="https://nexusinnovation.github.io/nexkit/"><img src="https://img.shields.io/badge/docs-GitHub_Pages-blue" alt="Documentation"/></a>
</p>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [🤔 What is Spec-Driven Development?](#-what-is-spec-driven-development)
- [🔧 Prerequisites](#-prerequisites)
  - [Required](#required)
  - [Platform Support](#platform-support)
- [⚡ Get started](#-get-started)
  - [1. Install Nexkit](#1-install-nexkit)
    - [Option 1: Persistent Installation (Recommended)](#option-1-persistent-installation-recommended)
    - [Option 2: One-time Usage](#option-2-one-time-usage)
  - [2. Start building](#2-start-building)
- [📽️ Video Overview](#️-video-overview)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Nexkit CLI Reference](#-nexkit-cli-reference)
  - [Commands](#commands)
  - [`nexkit init` Arguments \& Options](#nexkit-init-arguments--options)
  - [Examples](#examples)
  - [Available Slash Commands](#available-slash-commands)
  - [Environment Variables](#environment-variables)
- [📚 Core philosophy](#-core-philosophy)
- [🌟 Development phases](#-development-phases)
- [🎯 Experimental goals](#-experimental-goals)
  - [Technology independence](#technology-independence)
  - [Enterprise constraints](#enterprise-constraints)
  - [User-centric development](#user-centric-development)
  - [Creative \& iterative processes](#creative--iterative-processes)
- [📖 Learn more](#-learn-more)
- [📋 Detailed process](#-detailed-process)
  - [**STEP 1:** Establish project principles](#step-1-establish-project-principles)
  - [**STEP 1:** Start building](#step-1-start-building)
  - [**STEP 3:** Refine and clarify requirements](#step-3-refine-and-clarify-requirements)
  - [**STEP 2:** Implementation](#step-2-implementation)
- [🔍 Troubleshooting](#-troubleshooting)
  - [Git Credential Manager on Linux](#git-credential-manager-on-linux)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

## 🤔 What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them.

## 🔧 Prerequisites

Before installing Nexkit, ensure you have the following prerequisites installed:

### Required

1. **[uv](https://docs.astral.sh/uv/)** - Fast Python package and project manager (required for installing Nexkit)

   Install `uv` using one of these methods:

   **macOS/Linux:**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **Windows:**

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   **Using pip:**

   ```bash
   pip install uv
   ```

   **Using pipx:**

   ```bash
   pipx install uv
   ```

2. **[Python 3.11+](https://www.python.org/downloads/)** - Python runtime (uv can also install Python for you)

3. **[Git](https://git-scm.com/downloads)** - Version control system

4. **AI coding agent** - Choose one of:
   - [Claude Code](https://www.anthropic.com/claude-code)
   - [GitHub Copilot](https://code.visualstudio.com/)
   - [Gemini CLI](https://github.com/google-gemini/gemini-cli)
   - [Cursor](https://cursor.sh/)
   - [Qwen CLI](https://github.com/QwenLM/qwen-code)
   - [opencode](https://opencode.ai/)
   - [Codex CLI](https://github.com/openai/codex)
   - [Windsurf](https://windsurf.com/)
   - [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/)

### Platform Support

- **Linux/macOS** - Fully supported
- **Windows** - Use PowerShell or WSL2

If you encounter issues with an agent, please open an issue so we can refine the integration.

## ⚡ Get started

### 1. Install Nexkit

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install nexkit --from git+https://github.com/NexusInnovation/nexkit.git
```

Then use the tool directly:

```bash
nexkit init <PROJECT_NAME>
nexkit check
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

### 2. Start building

After initializing your project with `nexkit init`, your AI coding agent will have access to custom prompts and workflows that help structure your development process. Simply describe what you want to build, and your agent will guide you through creating specifications, implementation plans, and working code.

For detailed step-by-step instructions and best practices, see our [comprehensive guide](./spec-driven.md).

## 📽️ Video Overview

Want to see Nexkit in action? Watch our [video overview](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)!

[![Nexkit video header](/media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🤖 Supported AI Agents

| Agent                                                                                | Support | Notes                                                                                                                                     |
| ------------------------------------------------------------------------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [Claude Code](https://www.anthropic.com/claude-code)                                 | ✅       |                                                                                                                                           |
| [GitHub Copilot](https://code.visualstudio.com/)                                     | ✅       |                                                                                                                                           |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli)                            | ✅       |                                                                                                                                           |
| [Cursor](https://cursor.sh/)                                                         | ✅       |                                                                                                                                           |
| [Qwen Code](https://github.com/QwenLM/qwen-code)                                     | ✅       |                                                                                                                                           |
| [opencode](https://opencode.ai/)                                                     | ✅       |                                                                                                                                           |
| [Windsurf](https://windsurf.com/)                                                    | ✅       |                                                                                                                                           |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)                                    | ✅       |                                                                                                                                           |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)                              | ✅       |                                                                                                                                           |
| [Roo Code](https://roocode.com/)                                                     | ✅       |                                                                                                                                           |
| [Codex CLI](https://github.com/openai/codex)                                         | ✅       |                                                                                                                                           |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️       | Amazon Q Developer CLI [does not support](https://github.com/aws/amazon-q-developer-cli/issues/3064) custom arguments for slash commands. |

## 🔧 Nexkit CLI Reference

The `nexkit` command supports the following options:

### Commands

| Command | Description                                                                                                                            |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `init`  | Initialize a new Nexkit project from the latest template                                                                               |
| `check` | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |

### `nexkit init` Arguments & Options

| Argument/Option        | Type     | Description                                                                                                                                |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory)                                         |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, or `q` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                                                                                |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                                                                                            |
| `--no-git`             | Flag     | Skip git repository initialization                                                                                                         |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one                                                                  |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation)                                                           |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                                                                                |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                                                                                           |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)                                                                  |

### Examples

```bash
# Basic project initialization
nexkit init my-project

# Initialize with specific AI assistant
nexkit init my-project --ai claude

# Initialize with Cursor support
nexkit init my-project --ai cursor

# Initialize with Windsurf support
nexkit init my-project --ai windsurf

# Initialize with PowerShell scripts (Windows/cross-platform)
nexkit init my-project --ai copilot --script ps

# Initialize in current directory
nexkit init . --ai copilot
# or use the --here flag
nexkit init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
nexkit init . --force --ai copilot
# or 
nexkit init --here --force --ai copilot

# Skip git initialization
nexkit init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
nexkit init my-project --ai claude --debug

# Use GitHub token for API requests (helpful for corporate environments)
nexkit init my-project --ai claude --github-token ghp_your_token_here

# Check system requirements
nexkit check
```

### Available Slash Commands

After running `nexkit init`, your AI coding agent will have access to these slash commands for structured development:

| Command             | Description                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| `/nexkit.implement` | Quick implementation workflow using Azure DevOps work item information             |
| `/nexkit.refine`    | Add refinement context to existing user stories via related improvement work items |
| `/nexkit.commit`    | Generate intelligent commit messages and commit staged code with work item context |

### Environment Variables

| Variable         | Description                                                                                                                                                                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NEXKIT_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches. Must be set in the context of the agent you're working with. |

## 📚 Core philosophy

Spec-Driven Development is a structured process that emphasizes:

- **Intent-driven development** where specifications define the "_what_" before the "_how_"
- **Rich specification creation** using guardrails and organizational principles
- **Multi-step refinement** rather than one-shot code generation from prompts
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

## 🌟 Development phases

| Phase                                    | Focus                    | Key Activities                                                                                                                                                     |
| ---------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **0-to-1 Development** ("Greenfield")    | Generate from scratch    | <ul><li>Start with high-level requirements</li><li>Generate specifications</li><li>Plan implementation steps</li><li>Build production-ready applications</li></ul> |
| **Creative Exploration**                 | Parallel implementations | <ul><li>Explore diverse solutions</li><li>Support multiple technology stacks & architectures</li><li>Experiment with UX patterns</li></ul>                         |
| **Iterative Enhancement** ("Brownfield") | Brownfield modernization | <ul><li>Add features iteratively</li><li>Modernize legacy systems</li><li>Adapt processes</li></ul>                                                                |

## 🎯 Experimental goals

Our research and experimentation focus on:

### Technology independence

- Create applications using diverse technology stacks
- Validate the hypothesis that Spec-Driven Development is a process not tied to specific technologies, programming languages, or frameworks

### Enterprise constraints

- Demonstrate mission-critical application development
- Incorporate organizational constraints (cloud providers, tech stacks, engineering practices)
- Support enterprise design systems and compliance requirements

### User-centric development

- Build applications for different user cohorts and preferences
- Support various development approaches (from vibe-coding to AI-native development)

### Creative & iterative processes

- Validate the concept of parallel implementation exploration
- Provide robust iterative feature development workflows
- Extend processes to handle upgrades and modernization tasks

## 📖 Learn more

- **[Complete Spec-Driven Development Methodology](./spec-driven.md)** - Deep dive into the full process
- **[Detailed Walkthrough](#-detailed-process)** - Step-by-step implementation guide

---

## 📋 Detailed process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

You can use the Nexkit CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
nexkit init <project_name>
```

Or initialize in the current directory:

```bash
nexkit init .
# or use the --here flag
nexkit init --here
# Skip confirmation when the directory already has files
nexkit init . --force
# or
nexkit init --here --force
```

![Nexkit CLI bootstrapping a new project in the terminal](./media/nexkit_cli.gif)

You will be prompted to select the AI agent you are using. You can also proactively choose it directly in the terminal:

```bash
nexkit init <project_name> --ai claude
nexkit init <project_name> --ai gemini
nexkit init <project_name> --ai copilot

# Or in current directory:
nexkit init . --ai claude
nexkit init . --ai codex

# or use --here flag
nexkit init --here --ai claude
nexkit init --here --ai codex

# Force merge into a non-empty current directory
nexkit init . --force --ai claude

# or
nexkit init --here --force --ai claude
```

The CLI will check if you have Claude Code, Gemini CLI, Cursor CLI, Qwen CLI, opencode, Codex CLI, or Amazon Q Developer CLI installed. If you do not, or you prefer to get the templates without checking for the right tools, use `--ignore-agent-tools` with your command:

```bash
nexkit init <project_name> --ai claude --ignore-agent-tools
```

### **STEP 1:** Establish project principles

Go to the project folder and run your AI agent. In our example, we're using `claude`.

![Bootstrapping Claude Code environment](./media/bootstrap-claude-code.gif)

You will know that things are configured correctly if you can interact with your AI agent and access the custom prompts and workflows provided by Nexkit.

### **STEP 1:** Start building

Describe what you want to build to your AI agent. Be as explicit as possible about _what_ you are trying to build and _why_.

An example prompt:

```text
Develop Taskify, a team productivity platform. It should allow users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. In this initial phase for this feature,
let's call it "Create Taskify," let's have multiple users but the users will be declared ahead of time, predefined.
I want five users in two different categories, one product manager and four engineers. Let's create three
different sample projects. Let's have the standard Kanban columns for the status of each task, such as "To Do,"
"In Progress," "In Review," and "Done." There will be no login for this application as this is just the very
first testing thing to ensure that our basic features are set up. For each task in the UI for a task card,
you should be able to change the current status of the task between the different columns in the Kanban work board.
You should be able to leave an unlimited number of comments for a particular card. You should be able to, from that task
card, assign one of the valid users. When you first launch Taskify, it's going to give you a list of the five users to pick
from. There will be no password required. When you click on a user, you go into the main view, which displays the list of
projects. When you click on a project, you open the Kanban board for that project. You're going to see the columns.
You'll be able to drag and drop cards back and forth between different columns. You will see any cards that are
assigned to you, the currently logged in user, in a different color from all the other ones, so you can quickly
see yours. You can edit any comments that you make, but you can't edit comments that other people made. You can
delete any comments that you made, but you can't delete comments anybody else made.
```

After this prompt is entered, you should see Claude Code kick off the planning and spec drafting process. Claude Code will also trigger some of the built-in scripts to set up the repository.

Once this step is completed, you should have a new branch created (e.g., `001-create-taskify`), as well as a new specification in the `specs/001-create-taskify` directory.

The produced specification should contain a set of user stories and functional requirements, as defined in the template.

At this stage, your project folder contents should resemble the following:

```text
└── .nexkit
    ├── memory
    │	 └── constitution.md
    ├── scripts
    │	 ├── check-prerequisites.sh
    │	 ├── common.sh
    │	 ├── create-new-feature.sh
    │	 ├── setup-plan.sh
    │	 └── update-claude-md.sh
    ├── specs
    │	 └── 001-create-taskify
    │	     └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

### **STEP 3:** Refine and clarify requirements

With the baseline specification created, clarify any requirements that need more detail.

Work iteratively with your AI agent to refine and clarify:
- Discuss unclear or ambiguous requirements
- Ask questions about edge cases and scenarios
- Validate assumptions and constraints
- Ensure all acceptance criteria are well-defined

It's important to use the interaction with your AI agent as an opportunity to clarify and ask questions - **do not treat its first attempt as final**. Work collaboratively to refine the solution.

### **STEP 2:** Implementation

Work with your AI agent to implement your feature. The agent will help you:
- Write clean, maintainable code following project conventions
- Create appropriate tests
- Handle errors and edge cases
- Follow best practices for your chosen technology stack

>[!IMPORTANT]
>The AI agent may execute local CLI commands (such as `dotnet`, `npm`, etc.) - make sure you have the required tools installed on your machine.

Once the implementation is complete, test the application and resolve any runtime errors. You can share error messages with your AI agent for assistance.

</details>

---

## 🔍 Troubleshooting

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

## 👥 Maintainers

- Eric De Carufel ([@decarufe](https://github.com/decarufe))

## 💬 Support

For support, please open a [GitHub issue](https://github.com/NexusInnovation/nexkit/issues/new). We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

## 🙏 Acknowledgements

This project is heavily influenced by and based on the work and research of [John Lam](https://github.com/jflam).

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
