# Copilot Instructions for nexkit

This file provides explicit instructions to GitHub Copilot for contributing to the nexkit project. Follow these guidelines to ensure code quality, maintainability, and alignment with Spec-Driven Development (SDD) principles.
## 0. Multi-Agent, CLI, and IDE Support
- The nexkit project must support a variety of CLI tools and IDEs. Instructions and code should be compatible across different environments and agent integrations.
- When implementing features, consider cross-platform compatibility and agent-specific requirements as described in AGENTS.md.

## 0.1 Templates and Deployment Targets
- The `templates/` folder contains generic artefacts that can be renamed and moved as needed for the target deployment environment.
- Not all deployment targets will support every feature or artefact defined in the templates. Adapt and trim features as required for the specific target.

## 0.2 Feature Support Variability
- Some agents, CLI tools, or IDEs may not support all features or conventions defined in the templates. Always check compatibility and document any limitations or required adjustments.

## 1. Spec-Driven Development Principles
- Prioritize clear, detailed specifications before implementation.
- Use and maintain provided templates and directory structures.
- Ensure all new features and changes are traceable to a specification.

## 2. Coding Standards
- Follow PEP8 for Python code style and formatting.
- Use descriptive variable, function, and class names.
- Include type hints and docstrings for all public functions and classes.
- Keep functions and classes small and focused.

## 3. Templates and Directory Conventions
Use the templates in the `templates/` directory for new files and features. These artefacts are generic and may be renamed or moved to suit the deployment target.
Maintain the existing directory structure; do not introduce new top-level folders without justification.
Place agent-specific files in their designated directories (see AGENTS.md). When adapting templates, ensure compatibility with the target CLI tool or IDE, and document any unsupported features.

## 4. Documentation and Comments
- Write clear, concise docstrings for all modules, classes, and functions.
- Add inline comments to explain complex logic or design decisions.
- Update documentation in `docs/` as needed for new features or changes.

## 5. Testing
- Write unit tests for all new code and features.
- Place tests in the appropriate `tests/unit/` or `tests/integration/` directories.
- Ensure all tests pass before submitting changes.

## 6. Security and Privacy
- Never hardcode secrets, credentials, or API keys. Use environment variables or configuration files.
- Follow best practices for handling sensitive data.
- Do not log or expose confidential information.

## 7. Prohibited Practices
- Do not commit generated files, secrets, or credentials.
- Avoid duplicating code; refactor and reuse existing functions where possible.
- Do not bypass code reviews or testing requirements.

## 8. Example Code Patterns
- Use context managers for file and resource handling.
- Prefer list comprehensions and generator expressions for concise data processing.
- Use logging instead of print statements for debug output.

## 9. Project-Specific Rules
- Update `CHANGELOG.md` and increment the version in `pyproject.toml` for any user-facing changes.
- Follow the guidance in `AGENTS.md` when adding or modifying agent support.
- Ensure compatibility with supported AI agents and their directory conventions.

---

By following these instructions, Copilot will help maintain the quality and consistency of the nexkit project. When in doubt, prefer clarity, maintainability, and adherence to SDD principles.