# Quick Start Guide

This guide will help you get started with Spec-Driven Development using Nexkit.

> NEW: All automation scripts now provide both Bash (`.sh`) and PowerShell (`.ps1`) variants. The `nexkit` CLI auto-selects based on OS unless you pass `--script sh|ps`.

## The Quick Start Process

### 1. Install Nexkit

Initialize your project depending on the coding agent you're using:

```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <PROJECT_NAME>
```

Pick script type explicitly (optional):
```bash
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <PROJECT_NAME> --script ps  # Force PowerShell
uvx --from git+https://github.com/NexusInnovation/nexkit.git nexkit init <PROJECT_NAME> --script sh  # Force POSIX shell
```

### 2. Start Building

Describe what you want to build to your AI agent. Focus on the **what** and **why**. Your agent will guide you through creating specifications, implementation plans, and working code using the available slash commands and workflows.

## Example: Building Taskify

Here's a complete example of building a team productivity platform. Describe your requirements to your AI agent:

```text
Develop Taskify, a team productivity platform. It should allow users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. Include standard Kanban columns (To Do, 
In Progress, In Review, Done) with drag-and-drop functionality.
```

Your AI agent will guide you through the development process, helping you refine requirements and implement the solution.

## Key Principles

- **Be explicit** about what you're building and why
- **Iterate and refine** with your AI agent
- **Work collaboratively** - don't treat the first attempt as final
- **Let the AI agent guide** the implementation process

## Next Steps

- Read the complete methodology for in-depth guidance
- Check out more examples in the repository
- Explore the source code on GitHub
