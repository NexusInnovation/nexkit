"""
Unit tests for nexkit.gitignore module.

Tests cover git detection, exclusion patterns, file operations,
error handling, and edge cases.
"""

import pytest
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from nexkit import gitignore


# Fixtures
@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary git repository."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    # Initialize git
    subprocess.run(
        ["git", "init"],
        cwd=repo_path,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_path,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_path,
        check=True,
        capture_output=True
    )
    
    return repo_path


@pytest.fixture
def temp_repo_with_gitignore(temp_repo):
    """Create a temporary git repository with existing .gitignore."""
    gitignore_path = temp_repo / ".gitignore"
    gitignore_path.write_text("# Existing content\n*.log\n__pycache__/\n", encoding="utf-8")
    return temp_repo


@pytest.fixture
def temp_repo_with_nexkit_files(temp_repo):
    """Create a temporary git repository with nexkit files."""
    # Create nexkit directories and files
    specify_dir = temp_repo / ".specify"
    specify_dir.mkdir()
    (specify_dir / "test.txt").write_text("test", encoding="utf-8")
    
    specs_dir = temp_repo / "specs"
    specs_dir.mkdir()
    (specs_dir / "spec.md").write_text("spec", encoding="utf-8")
    
    prompts_dir = temp_repo / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "nexkit.test.md").write_text("prompt", encoding="utf-8")
    
    # Track files in git
    subprocess.run(
        ["git", "add", "."],
        cwd=temp_repo,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=temp_repo,
        check=True,
        capture_output=True
    )
    
    return temp_repo


# Test: Git repository detection
def test_is_git_repository_valid(temp_repo):
    """Test git repository detection for valid repository."""
    assert gitignore.is_git_repository(temp_repo) is True


def test_is_git_repository_invalid(tmp_path):
    """Test git repository detection for non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    assert gitignore.is_git_repository(non_repo) is False


def test_is_git_repository_git_not_installed():
    """Test git repository detection when git is not installed."""
    with patch("subprocess.run", side_effect=FileNotFoundError):
        assert gitignore.is_git_repository(Path.cwd()) is False


# Test: Get git root
def test_get_git_root_valid(temp_repo):
    """Test getting git root for valid repository."""
    root = gitignore.get_git_root(temp_repo)
    assert root is not None
    assert root == temp_repo


def test_get_git_root_subdirectory(temp_repo):
    """Test getting git root from subdirectory."""
    subdir = temp_repo / "subdir"
    subdir.mkdir()
    root = gitignore.get_git_root(subdir)
    assert root == temp_repo


def test_get_git_root_invalid(tmp_path):
    """Test getting git root for non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    root = gitignore.get_git_root(non_repo)
    assert root is None


# Test: Get tracked nexkit files
def test_get_tracked_nexkit_files_none(temp_repo):
    """Test getting tracked files when none exist."""
    tracked = gitignore.get_tracked_nexkit_files(temp_repo)
    assert tracked == []


def test_get_tracked_nexkit_files_some(temp_repo_with_nexkit_files):
    """Test getting tracked nexkit files."""
    tracked = gitignore.get_tracked_nexkit_files(temp_repo_with_nexkit_files)
    assert len(tracked) > 0
    # Check that paths are relative
    assert all(isinstance(f, Path) for f in tracked)


def test_get_tracked_nexkit_files_not_git_repo(tmp_path):
    """Test getting tracked files raises error for non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    with pytest.raises(gitignore.NotGitRepositoryError):
        gitignore.get_tracked_nexkit_files(non_repo)


@patch("subprocess.run", side_effect=FileNotFoundError)
def test_get_tracked_nexkit_files_git_not_installed(mock_run, temp_repo):
    """Test getting tracked files raises error when git not installed."""
    with pytest.raises(gitignore.GitNotInstalledError):
        gitignore.get_tracked_nexkit_files(temp_repo)


# Test: Has nexkit section
def test_has_nexkit_section_false(temp_repo):
    """Test section detection when no .gitignore exists."""
    gitignore_path = temp_repo / ".gitignore"
    assert gitignore.has_nexkit_section(gitignore_path) is False


def test_has_nexkit_section_false_empty_gitignore(temp_repo_with_gitignore):
    """Test section detection when .gitignore has no nexkit section."""
    gitignore_path = temp_repo_with_gitignore / ".gitignore"
    assert gitignore.has_nexkit_section(gitignore_path) is False


def test_has_nexkit_section_true(temp_repo):
    """Test section detection when nexkit section exists."""
    gitignore_path = temp_repo / ".gitignore"
    content = f"{gitignore.NEXKIT_SECTION_MARKER}\n.specify/\n{gitignore.NEXKIT_SECTION_END_MARKER}\n"
    gitignore_path.write_text(content, encoding="utf-8")
    assert gitignore.has_nexkit_section(gitignore_path) is True


# Test: Get nexkit section content
def test_get_nexkit_section_content():
    """Test section content generation."""
    content = gitignore.get_nexkit_section_content()
    assert gitignore.NEXKIT_SECTION_MARKER in content
    assert gitignore.NEXKIT_SECTION_END_MARKER in content
    assert ".specify/" in content
    assert "specs/" in content
    assert ".github/prompts/nexkit.*" in content


# Test: Add nexkit exclusions
def test_add_nexkit_exclusions_new_gitignore(temp_repo):
    """Test adding exclusions to new .gitignore."""
    result = gitignore.add_nexkit_exclusions(temp_repo)
    
    assert result.success is True
    assert result.already_configured is False
    assert len(result.patterns_affected) == 3
    assert result.gitignore_path.exists()
    
    content = result.gitignore_path.read_text(encoding="utf-8")
    assert gitignore.NEXKIT_SECTION_MARKER in content
    assert ".specify/" in content


def test_add_nexkit_exclusions_existing_gitignore(temp_repo_with_gitignore):
    """Test adding exclusions to existing .gitignore."""
    original_content = (temp_repo_with_gitignore / ".gitignore").read_text()
    
    result = gitignore.add_nexkit_exclusions(temp_repo_with_gitignore)
    
    assert result.success is True
    assert result.already_configured is False
    
    new_content = result.gitignore_path.read_text(encoding="utf-8")
    assert original_content in new_content
    assert gitignore.NEXKIT_SECTION_MARKER in new_content


def test_add_nexkit_exclusions_already_configured(temp_repo):
    """Test adding exclusions when already configured."""
    # Add exclusions first time
    gitignore.add_nexkit_exclusions(temp_repo)
    
    # Try adding again
    result = gitignore.add_nexkit_exclusions(temp_repo)
    
    assert result.success is True
    assert result.already_configured is True
    assert len(result.patterns_affected) == 0


def test_add_nexkit_exclusions_not_git_repo(tmp_path):
    """Test adding exclusions raises error for non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    with pytest.raises(gitignore.NotGitRepositoryError):
        gitignore.add_nexkit_exclusions(non_repo)


def test_add_nexkit_exclusions_with_tracked_files(temp_repo_with_nexkit_files):
    """Test adding exclusions when files are tracked."""
    result = gitignore.add_nexkit_exclusions(temp_repo_with_nexkit_files)
    
    assert result.success is True
    assert len(result.tracked_files) > 0


# Test: Remove nexkit exclusions
def test_remove_nexkit_exclusions_success(temp_repo):
    """Test removing exclusions."""
    # Add exclusions first
    gitignore.add_nexkit_exclusions(temp_repo)
    
    # Remove them
    result = gitignore.remove_nexkit_exclusions(temp_repo)
    
    assert result.success is True
    assert len(result.patterns_affected) == 3
    
    content = result.gitignore_path.read_text(encoding="utf-8")
    assert gitignore.NEXKIT_SECTION_MARKER not in content


def test_remove_nexkit_exclusions_preserves_other_content(temp_repo_with_gitignore):
    """Test removing exclusions preserves other .gitignore content."""
    original_content = (temp_repo_with_gitignore / ".gitignore").read_text()
    
    # Add and remove nexkit exclusions
    gitignore.add_nexkit_exclusions(temp_repo_with_gitignore)
    gitignore.remove_nexkit_exclusions(temp_repo_with_gitignore)
    
    final_content = (temp_repo_with_gitignore / ".gitignore").read_text()
    # Original content should be preserved (minus trailing newlines)
    assert original_content.strip() == final_content.strip()


def test_remove_nexkit_exclusions_no_gitignore(temp_repo):
    """Test removing exclusions when no .gitignore exists."""
    result = gitignore.remove_nexkit_exclusions(temp_repo)
    
    assert result.success is True
    assert len(result.patterns_affected) == 0


def test_remove_nexkit_exclusions_no_section(temp_repo_with_gitignore):
    """Test removing exclusions when section doesn't exist."""
    result = gitignore.remove_nexkit_exclusions(temp_repo_with_gitignore)
    
    assert result.success is True
    assert len(result.patterns_affected) == 0


def test_remove_nexkit_exclusions_not_git_repo(tmp_path):
    """Test removing exclusions raises error for non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    with pytest.raises(gitignore.NotGitRepositoryError):
        gitignore.remove_nexkit_exclusions(non_repo)


# Test: Check exclusion status
def test_check_exclusion_status_not_excluded(temp_repo):
    """Test status check when not excluded."""
    status = gitignore.check_exclusion_status(temp_repo)
    
    assert status.is_excluded is False
    assert status.has_gitignore is False
    assert len(status.missing_patterns) == 3
    assert status.requires_cleanup is False


def test_check_exclusion_status_excluded(temp_repo):
    """Test status check when excluded."""
    gitignore.add_nexkit_exclusions(temp_repo)
    
    status = gitignore.check_exclusion_status(temp_repo)
    
    assert status.is_excluded is True
    assert status.has_gitignore is True
    assert len(status.missing_patterns) == 0


def test_check_exclusion_status_with_tracked_files(temp_repo_with_nexkit_files):
    """Test status check with tracked files."""
    gitignore.add_nexkit_exclusions(temp_repo_with_nexkit_files)
    
    status = gitignore.check_exclusion_status(temp_repo_with_nexkit_files)
    
    assert status.requires_cleanup is True
    assert len(status.tracked_files) > 0


def test_check_exclusion_status_not_git_repo(tmp_path):
    """Test status check raises error for non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    with pytest.raises(gitignore.NotGitRepositoryError):
        gitignore.check_exclusion_status(non_repo)


# Test: Format cleanup guidance
def test_format_cleanup_guidance_empty():
    """Test cleanup guidance with no files."""
    guidance = gitignore.format_cleanup_guidance([], Path("/test"))
    assert guidance == ""


def test_format_cleanup_guidance_with_files(temp_repo):
    """Test cleanup guidance with files."""
    tracked_files = [Path("specs/test.md"), Path(".specify/config.json")]
    guidance = gitignore.format_cleanup_guidance(tracked_files, temp_repo)
    
    assert "git rm --cached" in guidance
    assert "specs/test.md" in guidance
    assert ".specify/config.json" in guidance


def test_format_cleanup_guidance_many_files(temp_repo):
    """Test cleanup guidance with many files (truncation)."""
    tracked_files = [Path(f"specs/file{i}.md") for i in range(15)]
    guidance = gitignore.format_cleanup_guidance(tracked_files, temp_repo)
    
    assert "git rm --cached" in guidance
    assert "and 5 more" in guidance


# Test: Error handling - permission errors
def test_add_nexkit_exclusions_permission_error(temp_repo):
    """Test permission error handling when writing .gitignore."""
    gitignore_path = temp_repo / ".gitignore"
    gitignore_path.write_text("", encoding="utf-8")
    gitignore_path.chmod(0o444)  # Read-only
    
    try:
        with pytest.raises(PermissionError):
            gitignore.add_nexkit_exclusions(temp_repo)
    finally:
        gitignore_path.chmod(0o644)  # Restore permissions


# Test: Atomic file operations
def test_add_nexkit_exclusions_atomic(temp_repo_with_gitignore):
    """Test that file operations are atomic (temp file cleanup)."""
    temp_file = temp_repo_with_gitignore / ".gitignore.tmp"
    
    # Ensure temp file doesn't exist before
    assert not temp_file.exists()
    
    gitignore.add_nexkit_exclusions(temp_repo_with_gitignore)
    
    # Ensure temp file doesn't exist after (cleaned up)
    assert not temp_file.exists()
