"""
Git exclusion management for nexkit projects.

This module provides functionality to add and remove nexkit-specific
exclusion patterns from .gitignore files, helping users manage whether
nexkit files are tracked in version control.
"""

import subprocess
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


# Constants
NEXKIT_SECTION_MARKER = "# Nexkit - Spec-Driven Development Tools"
NEXKIT_SECTION_END_MARKER = "# End Nexkit exclusions"

NEXKIT_PATTERNS = [
    ".specify/",
    "specs/",
    ".github/prompts/nexkit.*",
]


# Exceptions
class GitIgnoreError(Exception):
    """Base exception for git exclusion operations."""
    pass


class NotGitRepositoryError(GitIgnoreError):
    """Raised when path is not in a git repository."""
    pass


class GitNotInstalledError(GitIgnoreError):
    """Raised when git is not installed or not in PATH."""
    pass


# Data Classes
@dataclass
class ExclusionResult:
    """Result of add/remove exclusion operations."""
    success: bool
    message: str
    gitignore_path: Path
    patterns_affected: List[str]
    already_configured: bool
    tracked_files: List[Path]
    git_root: Path


@dataclass
class ExclusionStatus:
    """Status of nexkit exclusion in a repository."""
    is_excluded: bool
    has_gitignore: bool
    missing_patterns: List[str]
    tracked_files: List[Path]
    requires_cleanup: bool
    git_root: Path
    gitignore_path: Optional[Path]


# Core Functions
def is_git_repository(path: Path) -> bool:
    """
    Check if a path is within a git repository.
    
    Args:
        path: Path to check (can be any path, will search upwards)
    
    Returns:
        True if path is in a git repository, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        # git not installed
        return False
    except Exception:
        return False


def get_git_root(path: Path) -> Optional[Path]:
    """
    Get the root directory of a git repository.
    
    Args:
        path: Path within repository
    
    Returns:
        Absolute path to repository root, or None if not in a git repository
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    except Exception:
        return None


def get_tracked_nexkit_files(repo_path: Path) -> List[Path]:
    """
    Get list of nexkit files currently tracked by git.
    
    Args:
        repo_path: Path to repository (any path within repo)
    
    Returns:
        List of relative paths (from repo root) of tracked nexkit files
    
    Raises:
        NotGitRepositoryError: If not in a git repository
        GitNotInstalledError: If git is not available
    """
    if not is_git_repository(repo_path):
        raise NotGitRepositoryError("Not a git repository")
    
    git_root = get_git_root(repo_path)
    if not git_root:
        raise NotGitRepositoryError("Cannot determine git repository root")
    
    tracked_files = []
    
    # Check each pattern
    patterns_to_check = [".specify", "specs", ".github/prompts"]
    
    for pattern in patterns_to_check:
        try:
            result = subprocess.run(
                ["git", "ls-files", pattern],
                cwd=git_root,
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout.strip():
                files = result.stdout.strip().split("\n")
                tracked_files.extend([Path(f) for f in files if f])
        except FileNotFoundError:
            raise GitNotInstalledError("Git is not installed or not in PATH")
        except subprocess.CalledProcessError:
            # Pattern not found or error - continue
            continue
    
    return tracked_files


def has_nexkit_section(gitignore_path: Path) -> bool:
    """
    Check if .gitignore contains nexkit exclusion section.
    
    Args:
        gitignore_path: Path to .gitignore file
    
    Returns:
        True if nexkit section exists, False otherwise
    """
    if not gitignore_path.exists():
        return False
    
    try:
        content = gitignore_path.read_text(encoding="utf-8")
        return NEXKIT_SECTION_MARKER in content
    except Exception:
        return False


def get_nexkit_section_content() -> str:
    """
    Generate the complete nexkit exclusion section content.
    
    Returns:
        Formatted section with markers and patterns
    """
    lines = [
        "",
        NEXKIT_SECTION_MARKER,
        "# Generated by: nexkit add-exclusion",
        "# To remove: nexkit remove-exclusion",
        "",
    ]
    
    lines.extend(NEXKIT_PATTERNS)
    lines.append("")
    lines.append(NEXKIT_SECTION_END_MARKER)
    lines.append("")
    
    return "\n".join(lines)


def add_nexkit_exclusions(repo_path: Path) -> ExclusionResult:
    """
    Add nexkit exclusion patterns to repository's .gitignore file.
    
    Args:
        repo_path: Path to repository (can be any path within repo)
    
    Returns:
        ExclusionResult with operation details
    
    Raises:
        NotGitRepositoryError: If not in a git repository
        GitNotInstalledError: If git is not available
        PermissionError: If cannot read or write .gitignore
        OSError: If file operation fails
    """
    # Validate git repository
    if not is_git_repository(repo_path):
        raise NotGitRepositoryError(
            "Not a git repository. Initialize git first with: git init"
        )
    
    git_root = get_git_root(repo_path)
    if not git_root:
        raise NotGitRepositoryError("Cannot determine git repository root")
    
    gitignore_path = git_root / ".gitignore"
    
    # Check if already configured
    if has_nexkit_section(gitignore_path):
        tracked = get_tracked_nexkit_files(repo_path)
        return ExclusionResult(
            success=True,
            message="Nexkit exclusions already configured",
            gitignore_path=gitignore_path,
            patterns_affected=[],
            already_configured=True,
            tracked_files=tracked,
            git_root=git_root,
        )
    
    # Read existing content
    existing_content = ""
    if gitignore_path.exists():
        try:
            existing_content = gitignore_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            raise OSError(f".gitignore file encoding issue: {e}")
    
    # Prepare new content
    nexkit_section = get_nexkit_section_content()
    
    # Ensure proper spacing
    if existing_content and not existing_content.endswith("\n"):
        existing_content += "\n"
    
    new_content = existing_content + nexkit_section
    
    # Atomic write using temporary file
    temp_file = gitignore_path.with_name(gitignore_path.name + '.tmp')
    try:
        temp_file.write_text(new_content, encoding="utf-8")
        temp_file.replace(gitignore_path)  # Atomic on POSIX and Windows
    except PermissionError as e:
        if temp_file.exists():
            temp_file.unlink()
        raise PermissionError(
            f"Cannot write to .gitignore: {e}. Check file permissions."
        )
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        raise OSError(f"Failed to update .gitignore: {e}")
    
    # Check for tracked files
    tracked = get_tracked_nexkit_files(repo_path)
    
    return ExclusionResult(
        success=True,
        message="Successfully added nexkit exclusions to .gitignore",
        gitignore_path=gitignore_path,
        patterns_affected=NEXKIT_PATTERNS.copy(),
        already_configured=False,
        tracked_files=tracked,
        git_root=git_root,
    )


def remove_nexkit_exclusions(repo_path: Path) -> ExclusionResult:
    """
    Remove nexkit exclusion section from repository's .gitignore file.
    
    Args:
        repo_path: Path to repository (can be any path within repo)
    
    Returns:
        ExclusionResult with operation details
    
    Raises:
        NotGitRepositoryError: If not in a git repository
        PermissionError: If cannot read or write .gitignore
        OSError: If file operation fails
    """
    # Validate git repository
    if not is_git_repository(repo_path):
        raise NotGitRepositoryError(
            "Not a git repository. Initialize git first with: git init"
        )
    
    git_root = get_git_root(repo_path)
    if not git_root:
        raise NotGitRepositoryError("Cannot determine git repository root")
    
    gitignore_path = git_root / ".gitignore"
    
    # Check if .gitignore exists
    if not gitignore_path.exists():
        return ExclusionResult(
            success=True,
            message="No .gitignore file found",
            gitignore_path=gitignore_path,
            patterns_affected=[],
            already_configured=False,
            tracked_files=[],
            git_root=git_root,
        )
    
    # Check if nexkit section exists
    if not has_nexkit_section(gitignore_path):
        return ExclusionResult(
            success=True,
            message="Nexkit exclusions not found in .gitignore",
            gitignore_path=gitignore_path,
            patterns_affected=[],
            already_configured=False,
            tracked_files=[],
            git_root=git_root,
        )
    
    # Read and process content
    try:
        content = gitignore_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise OSError(f".gitignore file encoding issue: {e}")
    
    # Remove nexkit section
    lines = content.split("\n")
    new_lines = []
    in_nexkit_section = False
    
    for line in lines:
        if NEXKIT_SECTION_MARKER in line:
            in_nexkit_section = True
            continue
        
        if in_nexkit_section:
            if NEXKIT_SECTION_END_MARKER in line:
                in_nexkit_section = False
                continue
            # Skip lines within nexkit section
            continue
        
        new_lines.append(line)
    
    # Remove trailing empty lines that might have been left
    while new_lines and not new_lines[-1].strip():
        new_lines.pop()
    
    new_content = "\n".join(new_lines)
    if new_content:
        new_content += "\n"  # Ensure file ends with newline
    
    # Atomic write using temporary file
    temp_file = gitignore_path.with_suffix(".gitignore.tmp")
    try:
        temp_file.write_text(new_content, encoding="utf-8")
        temp_file.replace(gitignore_path)  # Atomic on POSIX and Windows
    except PermissionError as e:
        if temp_file.exists():
            temp_file.unlink()
        raise PermissionError(
            f"Cannot write to .gitignore: {e}. Check file permissions."
        )
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        raise OSError(f"Failed to update .gitignore: {e}")
    
    return ExclusionResult(
        success=True,
        message="Successfully removed nexkit exclusions from .gitignore",
        gitignore_path=gitignore_path,
        patterns_affected=NEXKIT_PATTERNS.copy(),
        already_configured=False,
        tracked_files=[],
        git_root=git_root,
    )


def check_exclusion_status(repo_path: Path) -> ExclusionStatus:
    """
    Check current status of nexkit git exclusion.
    
    Args:
        repo_path: Path to repository
    
    Returns:
        ExclusionStatus with current state
    
    Raises:
        NotGitRepositoryError: If not in a git repository
    """
    if not is_git_repository(repo_path):
        raise NotGitRepositoryError("Not a git repository")
    
    git_root = get_git_root(repo_path)
    if not git_root:
        raise NotGitRepositoryError("Cannot determine git repository root")
    
    gitignore_path = git_root / ".gitignore"
    has_gitignore = gitignore_path.exists()
    is_excluded = has_nexkit_section(gitignore_path) if has_gitignore else False
    
    # Determine missing patterns
    missing_patterns = []
    if not is_excluded:
        missing_patterns = NEXKIT_PATTERNS.copy()
    
    # Check tracked files
    tracked_files = []
    try:
        tracked_files = get_tracked_nexkit_files(repo_path)
    except Exception:
        pass  # If we can't check, just leave empty
    
    return ExclusionStatus(
        is_excluded=is_excluded,
        has_gitignore=has_gitignore,
        missing_patterns=missing_patterns,
        tracked_files=tracked_files,
        requires_cleanup=len(tracked_files) > 0,
        git_root=git_root,
        gitignore_path=gitignore_path if has_gitignore else None,
    )


def format_cleanup_guidance(tracked_files: List[Path], git_root: Path) -> str:
    """
    Generate user-friendly instructions for removing tracked files.
    
    Args:
        tracked_files: List of tracked nexkit files
        git_root: Repository root path
    
    Returns:
        Formatted guidance text
    """
    if not tracked_files:
        return ""
    
    lines = [
        "",
        "[yellow]⚠️  Nexkit files are currently tracked in git[/yellow]",
        "",
        f"Found {len(tracked_files)} tracked file(s):",
        "",
    ]
    
    # Show first 10 files
    for file in tracked_files[:10]:
        lines.append(f"  • {file}")
    
    if len(tracked_files) > 10:
        lines.append(f"  ... and {len(tracked_files) - 10} more")
    
    lines.extend([
        "",
        "[cyan]To remove these files from git tracking:[/cyan]",
        "",
        "  1. Run this command to untrack files (keeps local copies):",
        f"     [white]git rm --cached {' '.join(str(f) for f in tracked_files)}[/white]",
        "",
        "  2. Commit the change:",
        "     [white]git commit -m \"Stop tracking nexkit files\"[/white]",
        "",
        "  3. The files will remain in your working directory but won't be tracked.",
        "",
    ])
    
    return "\n".join(lines)
