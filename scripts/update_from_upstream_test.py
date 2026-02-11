"""Unit tests for update_from_upstream."""

import subprocess
import sys
import pytest
from unittest.mock import patch
from pathlib import Path

# Add scripts to path for testing
sys.path.insert(0, str(Path(__file__).parent))

# Relative import for same-directory module
from update_from_upstream import run_git, get_recent_upstream_changes


def test_run_git_success() -> None:
    """Test successful git command."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess([], 0, "output", "")
        result = run_git(["status"])
        assert result == "output"


def test_run_git_failure() -> None:
    """Test git command failure."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess([], 1, "", "error")
        with pytest.raises(subprocess.CalledProcessError):
            run_git(["invalid"], check=True, raise_on_error=True)


def test_get_recent_upstream_changes() -> None:
    """Test changelog extraction."""
    with patch("update_from_upstream.run_git") as mock_run:
        mock_run.return_value = "abc123 fix bug\ndef456 add feature"
        changes = get_recent_upstream_changes("upstream/main")
        assert len(changes) == 2
