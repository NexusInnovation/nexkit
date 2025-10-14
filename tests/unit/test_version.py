"""Unit tests for version display functionality."""
import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from nexkit import get_version, get_git_tag


class TestVersionFunctions(unittest.TestCase):
    """Test version-related functions."""

    def test_get_version_returns_string(self):
        """Test that get_version returns a string."""
        version = get_version()
        self.assertIsInstance(version, str)
        self.assertNotEqual(version, "")

    def test_get_version_format(self):
        """Test that version follows expected format or is 'unknown'."""
        version = get_version()
        # Should be either version number like "1.0.1" or "unknown"
        self.assertTrue(
            version == "unknown" or 
            version.replace(".", "").replace("-", "").replace("dev", "").replace("a", "").replace("b", "").replace("rc", "").isdigit() or
            "." in version
        )

    def test_get_git_tag_returns_string(self):
        """Test that get_git_tag returns a string."""
        git_tag = get_git_tag()
        self.assertIsInstance(git_tag, str)
        self.assertNotEqual(git_tag, "")

    def test_get_git_tag_handles_git_unavailable(self):
        """Test that get_git_tag handles when git is not available."""
        with patch('subprocess.run', side_effect=FileNotFoundError):
            git_tag = get_git_tag()
            self.assertEqual(git_tag, "unknown")

    def test_get_git_tag_handles_git_error(self):
        """Test that get_git_tag handles git command errors."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        
        with patch('subprocess.run', return_value=mock_result):
            git_tag = get_git_tag()
            self.assertEqual(git_tag, "unknown")

    def test_get_git_tag_handles_timeout(self):
        """Test that get_git_tag handles timeout gracefully."""
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd="git", timeout=2)):
            git_tag = get_git_tag()
            self.assertEqual(git_tag, "unknown")

    def test_get_git_tag_success(self):
        """Test that get_git_tag returns tag when git succeeds."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "v1.2.3-4-gabcdef\n"
        
        with patch('subprocess.run', return_value=mock_result):
            git_tag = get_git_tag()
            self.assertEqual(git_tag, "v1.2.3-4-gabcdef")


if __name__ == '__main__':
    unittest.main()
