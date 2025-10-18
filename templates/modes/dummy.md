# Dummy Mode

This is a generic template for creating custom AI assistant modes. This file demonstrates the structure and can be customized for specific use cases.

## Purpose

This mode serves as an example template that can be adapted to create specialized conversation contexts or assistant behaviors for different tasks.

## Description

A placeholder mode that demonstrates the basic structure. Replace this content with your specific mode's purpose, instructions, and behavior guidelines.

## Instructions

When operating in this mode, the AI assistant should:

1. **Follow Project Context**: Always consider the project structure, coding standards, and existing patterns
2. **Maintain Consistency**: Ensure all suggestions align with the project's established conventions
3. **Be Thorough**: Provide complete, working solutions rather than partial implementations
4. **Consider Best Practices**: Apply industry best practices and security guidelines
5. **Test-Driven**: Encourage writing tests alongside implementation

## Behavior Guidelines

- **Communication Style**: Clear, concise, and professional
- **Code Quality**: Prioritize maintainability, readability, and performance
- **Documentation**: Include inline comments and docstrings where appropriate
- **Error Handling**: Always consider edge cases and error scenarios
- **Dependencies**: Minimize external dependencies when possible

## Example Use Cases

This mode can be customized for various scenarios:

- Feature development with specific architectural patterns
- Bug fixing with emphasis on root cause analysis
- Code review focused on specific quality criteria
- Refactoring with performance optimization goals
- Documentation generation following project standards

## Customization Notes

To adapt this template for your specific needs:

1. **Rename the file** to match your mode's purpose (e.g., `feature-dev.md`, `code-review.md`)
2. **Update the Purpose section** with your mode's specific goal
3. **Modify Instructions** to reflect the desired behavior
4. **Add specific guidelines** relevant to your use case
5. **Include examples** that illustrate the expected output

## Agent-Specific Deployment

This template is designed to be agent-agnostic and will be deployed to the appropriate location based on your chosen AI assistant:

- **GitHub Copilot**: `.github/chatmodes/*.chatmode.md`
- **Claude Code**: `.claude/modes/*.md`
- **Gemini CLI**: `.gemini/modes/*.toml` (converted format)
- **Cursor**: `.cursor/modes/*.md`
- **Qwen Code**: `.qwen/modes/*.toml` (converted format)
- **opencode**: `.opencode/modes/*.md`
- **Codex**: `.codex/modes/*.md`
- **Windsurf**: `.windsurf/modes/*.md`
- **Kilo Code**: `.kilocode/modes/*.md`
- **Auggie**: `.augment/modes/*.md`
- **Amazon Q**: `.amazonq/modes/*.md`

---

**Note**: This is a template file. Customize it to create modes that suit your specific workflow and requirements.
