"""
Integration tests for git exclusion CLI commands.

Tests cover full CLI workflows including command execution,
error handling, and user interactions.
"""

import pytest
import subprocess
from pathlib import Path
from typer.testing import CliRunner
from nexkit import app, gitignore


runner = CliRunner()


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


# Test: add-exclusion command
def test_add_exclusion_command_success(temp_repo, monkeypatch):
    """Test add-exclusion command success."""
    monkeypatch.chdir(temp_repo)
    
    result = runner.invoke(app, ["add-exclusion"])
    
    assert result.exit_code == 0
    assert "Successfully added nexkit exclusions" in result.stdout
    
    # Verify .gitignore was created
    gitignore_path = temp_repo / ".gitignore"
    assert gitignore_path.exists()
    content = gitignore_path.read_text()
    assert gitignore.NEXKIT_SECTION_MARKER in content


def test_add_exclusion_command_with_path(temp_repo):
    """Test add-exclusion command with explicit path."""
    result = runner.invoke(app, ["add-exclusion", str(temp_repo)])
    
    assert result.exit_code == 0
    assert "Successfully added nexkit exclusions" in result.stdout


def test_add_exclusion_command_already_configured(temp_repo, monkeypatch):
    """Test add-exclusion command when already configured."""
    monkeypatch.chdir(temp_repo)
    
    # Add exclusions first time
    runner.invoke(app, ["add-exclusion"])
    
    # Try adding again
    result = runner.invoke(app, ["add-exclusion"])
    
    assert result.exit_code == 0
    assert "already configured" in result.stdout


def test_add_exclusion_command_not_git_repo(tmp_path, monkeypatch):
    """Test add-exclusion command in non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    monkeypatch.chdir(non_repo)
    
    result = runner.invoke(app, ["add-exclusion"])
    
    assert result.exit_code == 1
    assert "Not a git repository" in result.stdout


# Test: remove-exclusion command
def test_remove_exclusion_command_success(temp_repo, monkeypatch):
    """Test remove-exclusion command success."""
    monkeypatch.chdir(temp_repo)
    
    # Add exclusions first
    runner.invoke(app, ["add-exclusion"])
    
    # Remove them
    result = runner.invoke(app, ["remove-exclusion"])
    
    assert result.exit_code == 0
    assert "Successfully removed nexkit exclusions" in result.stdout
    
    # Verify section was removed
    gitignore_path = temp_repo / ".gitignore"
    content = gitignore_path.read_text()
    assert gitignore.NEXKIT_SECTION_MARKER not in content


def test_remove_exclusion_command_with_path(temp_repo):
    """Test remove-exclusion command with explicit path."""
    # Add exclusions first
    runner.invoke(app, ["add-exclusion", str(temp_repo)])
    
    result = runner.invoke(app, ["remove-exclusion", str(temp_repo)])
    
    assert result.exit_code == 0
    assert "Successfully removed nexkit exclusions" in result.stdout


def test_remove_exclusion_command_no_gitignore(temp_repo, monkeypatch):
    """Test remove-exclusion command when no .gitignore exists."""
    monkeypatch.chdir(temp_repo)
    
    result = runner.invoke(app, ["remove-exclusion"])
    
    assert result.exit_code == 0
    assert "No .gitignore file found" in result.stdout


def test_remove_exclusion_command_no_section(temp_repo, monkeypatch):
    """Test remove-exclusion command when section doesn't exist."""
    monkeypatch.chdir(temp_repo)
    
    # Create .gitignore without nexkit section
    gitignore_path = temp_repo / ".gitignore"
    gitignore_path.write_text("*.log\n", encoding="utf-8")
    
    result = runner.invoke(app, ["remove-exclusion"])
    
    assert result.exit_code == 0
    assert "not found" in result.stdout


def test_remove_exclusion_command_not_git_repo(tmp_path, monkeypatch):
    """Test remove-exclusion command in non-repository."""
    non_repo = tmp_path / "not_a_repo"
    non_repo.mkdir()
    monkeypatch.chdir(non_repo)
    
    result = runner.invoke(app, ["remove-exclusion"])
    
    assert result.exit_code == 1
    assert "Not a git repository" in result.stdout


# Test: Round-trip operations
def test_add_remove_add_exclusion(temp_repo, monkeypatch):
    """Test adding, removing, and re-adding exclusions."""
    monkeypatch.chdir(temp_repo)
    
    # Add
    result1 = runner.invoke(app, ["add-exclusion"])
    assert result1.exit_code == 0
    assert "Successfully added" in result1.stdout
    
    # Remove
    result2 = runner.invoke(app, ["remove-exclusion"])
    assert result2.exit_code == 0
    assert "Successfully removed" in result2.stdout
    
    # Add again
    result3 = runner.invoke(app, ["add-exclusion"])
    assert result3.exit_code == 0
    assert "Successfully added" in result3.stdout


# Test: Preservation of existing content
def test_add_exclusion_preserves_existing_content(temp_repo, monkeypatch):
    """Test that adding exclusions preserves existing .gitignore content."""
    monkeypatch.chdir(temp_repo)
    
    # Create .gitignore with existing content
    gitignore_path = temp_repo / ".gitignore"
    original_content = "# My project\n*.log\n__pycache__/\n"
    gitignore_path.write_text(original_content, encoding="utf-8")
    
    # Add exclusions
    result = runner.invoke(app, ["add-exclusion"])
    assert result.exit_code == 0
    
    # Verify original content is preserved
    new_content = gitignore_path.read_text()
    assert original_content in new_content
    assert gitignore.NEXKIT_SECTION_MARKER in new_content


def test_remove_exclusion_preserves_existing_content(temp_repo, monkeypatch):
    """Test that removing exclusions preserves existing .gitignore content."""
    monkeypatch.chdir(temp_repo)
    
    # Create .gitignore with existing content
    gitignore_path = temp_repo / ".gitignore"
    original_content = "# My project\n*.log\n__pycache__/\n"
    gitignore_path.write_text(original_content, encoding="utf-8")
    
    # Add and remove exclusions
    runner.invoke(app, ["add-exclusion"])
    result = runner.invoke(app, ["remove-exclusion"])
    assert result.exit_code == 0
    
    # Verify original content is preserved (minus trailing whitespace)
    final_content = gitignore_path.read_text()
    assert original_content.strip() == final_content.strip()


# Test: Tracked files warning
def test_add_exclusion_shows_cleanup_guidance(temp_repo, monkeypatch):
    """Test that add-exclusion shows cleanup guidance for tracked files."""
    monkeypatch.chdir(temp_repo)
    
    # Create and track nexkit files
    specify_dir = temp_repo / ".specify"
    specify_dir.mkdir()
    (specify_dir / "test.txt").write_text("test", encoding="utf-8")
    
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
    
    # Add exclusions
    result = runner.invoke(app, ["add-exclusion"])
    
    assert result.exit_code == 0
    assert "tracked in git" in result.stdout
    assert "git rm --cached" in result.stdout


# Test: Command help text
def test_add_exclusion_help():
    """Test add-exclusion command help text."""
    result = runner.invoke(app, ["add-exclusion", "--help"])
    
    assert result.exit_code == 0
    assert "Add nexkit exclusion patterns" in result.stdout
    assert ".specify/" in result.stdout
    assert "specs/" in result.stdout


def test_remove_exclusion_help():
    """Test remove-exclusion command help text."""
    result = runner.invoke(app, ["remove-exclusion", "--help"])
    
    assert result.exit_code == 0
    assert "Remove nexkit exclusion patterns" in result.stdout


# Test: Banner display
def test_commands_show_banner(temp_repo, monkeypatch):
    """Test that commands show the nexkit banner."""
    monkeypatch.chdir(temp_repo)
    
    result = runner.invoke(app, ["add-exclusion"])
    
    # Banner should be displayed
    expected_banner = "=== NEXKIT CLI ==="
    assert expected_banner in result.stdout
