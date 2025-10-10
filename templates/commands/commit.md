---
description: Intelligent commit workflow that analyzes changes, extracts work item context, and creates meaningful commit messages.
model: GPT-5 mini (copilot)
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

Execute the following comprehensive commit workflow:

## Phase 1: Analyze Pending Changes

1. **Get Repository Status**
   - Use `get_changed_files` to analyze the current git state
   - Identify staged vs unstaged changes
   - Document the scope and nature of modifications

2. **Analyze Change Content**
   - Use sequential-thinking to understand the purpose and impact of changes
   - Categorize changes by type (feature, bugfix, refactor, docs, test, etc.)
   - Identify affected components and systems
   - Assess the logical grouping of changes

## Phase 2: Extract Work Item Context

3. **Extract Work Item Reference from Branch**
   - Parse the current branch name to extract work item ID
   - Common patterns: `feature/12345-description`, `bugfix/12345-description`, `task/12345-description`
   - Extract numeric work item ID from branch name

4. **Fetch Work Item Details** 
   - **IF work item ID is found in branch name**:
     - Use `mcp_azure-devops_wit_get_work_item` with:
       - Current project
       - Work item ID from branch name
       - Include fields: title, description, work item type, state, acceptance criteria
     - Extract key context: purpose, requirements, acceptance criteria
   - **IF no work item ID found**:
     - Proceed with change analysis only
     - Note in commit message that no work item reference was found

## Phase 3: Generate Commit Message

5. **Create Structured Commit Message**
   - **Format**: `<type>(<scope>): <description>`
   - **Types**: feat, fix, refactor, docs, test, chore, style, perf
   - **Scope**: Component/module affected (e.g., api, frontend, infrastructure)
   - **Description**: Clear, concise summary (50 chars or less)

6. **Add Detailed Body (if needed)**
   - **Line 2**: Blank line
   - **Line 3+**: Detailed explanation including:
     - What was changed and why
     - Work item context (if available)
     - Breaking changes (if any)
     - Related work items or references

7. **Follow Conventional Commits Format**
   ```
   type(scope): description

   Detailed explanation of the change.
   
   - Key change 1
   - Key change 2
   
   Work Item: #12345 - Title from work item
   
   BREAKING CHANGE: Description of breaking change (if applicable)
   ```

## Phase 4: Execute Commit

8. **Analyze Staging Status**
   - Use `run_in_terminal` with `git status` to check current state
   - Parse output to identify:
     - "Changes to be committed" section (staged files)
     - "Changes not staged for commit" section (modified but unstaged files)
     - "Untracked files" section (new files not yet tracked)

9. **Commit Strategy Decision**
   - **IF there are staged changes ("Changes to be committed" section exists)**:
     - Commit ONLY staged changes
     - Do NOT run `git add` - respect existing staging decisions
     - Warn user about any unstaged changes remaining
   - **IF no staged changes but unstaged/untracked files exist**:
     - Only then use `git add .` to stage all changes
     - Ask user confirmation before staging (optional)
   - **IF no changes to commit**:
     - Inform user and exit

10. **Execute Git Commit**
    - Use `run_in_terminal` to execute git commit with generated message
    - Command: `git commit -m "commit message"`
    - **IMPORTANT**: Use `-m` flag to avoid opening editor
    - Verify commit was successful

10. **Post-Commit Summary**
    - Display commit hash and message
    - Show what was committed (files and change summary)
    - Note any remaining unstaged changes
    - Suggest next steps if appropriate

## Error Handling

- **Branch name parsing fails**: Proceed without work item context
- **Work item not found**: Log warning and proceed with git analysis only  
- **No changes to commit**: Inform user and suggest staging changes with `git add`
- **Git status parsing fails**: Fall back to `git status --porcelain` for simpler parsing
- **Git commit fails**: Display error and suggest resolution steps
- **Mixed staging states**: Respect existing staged files, never use `git add` when staged files exist

## Example Output Format

```
✅ Commit Analysis Complete
📋 Work Item: #12345 - Add user authentication feature
📝 Commit Message: feat(auth): implement user login with Azure AD

� Git Status Analysis:
- Staged files: 3 files ready for commit
- Unstaged files: 2 files modified but not staged
- Strategy: Committing staged files only

�🔄 Committing staged changes...
✅ Commit successful: abc1234 - feat(auth): implement user login with Azure AD

📊 Summary:
- Files committed: 3 staged files
- Remaining unstaged: 2 files (run 'git status' to see details)
- Tip: Review unstaged changes and stage manually if needed
```

Remember: This prompt respects existing staging decisions and never uses `git add` when there are already staged files, maintaining clean commit history with meaningful, contextual commit messages derived from both code analysis and work item details.