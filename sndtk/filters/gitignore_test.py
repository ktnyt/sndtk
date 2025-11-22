"""Tests for GitignoreFilter."""

import tempfile
from pathlib import Path

import pytest

from .gitignore import GitignoreFilter


def test__GitignoreFilter____init____initializes_with_default_root_path() -> None:
    """Initializes successfully with default root_path (current directory)."""
    # Use the project root which has .gitignore
    filter_instance = GitignoreFilter()
    assert filter_instance.root_path.exists()
    assert filter_instance.gitignore_path.exists()
    assert filter_instance.gitignore_path.name == ".gitignore"


def test__GitignoreFilter____init____initializes_with_custom_root_path() -> None:
    """Initializes successfully with custom root_path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("*.pyc\n__pycache__/\n")

        filter_instance = GitignoreFilter(root_path=root_path)
        assert filter_instance.root_path == root_path.resolve()
        assert filter_instance.gitignore_path == root_path.resolve() / ".gitignore"


def test__GitignoreFilter____init____initializes_with_empty_gitignore() -> None:
    """Initializes successfully with empty .gitignore file (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("")

        filter_instance = GitignoreFilter(root_path=root_path)
        assert filter_instance.root_path == root_path.resolve()
        assert filter_instance.gitignore_path.exists()


def test__GitignoreFilter____init____raises_file_not_found_error_when_gitignore_not_exists() -> (
    None
):
    """Raises FileNotFoundError when .gitignore does not exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        # Do not create .gitignore

        with pytest.raises(FileNotFoundError) as exc_info:
            GitignoreFilter(root_path=root_path)
        assert ".gitignore not found" in str(exc_info.value)


def test__GitignoreFilter__is_ignored__returns_true_when_path_matches_pattern() -> None:
    """Returns True when path matches .gitignore pattern."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("*.pyc\n__pycache__/\n")

        filter_instance = GitignoreFilter(root_path=root_path)
        test_path = root_path / "file.pyc"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is True


def test__GitignoreFilter__is_ignored__returns_false_when_path_does_not_match_pattern() -> None:
    """Returns False when path does not match any .gitignore pattern."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("*.pyc\n__pycache__/\n")

        filter_instance = GitignoreFilter(root_path=root_path)
        test_path = root_path / "file.py"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is False


def test__GitignoreFilter__is_ignored__returns_false_when_gitignore_is_empty() -> None:
    """Returns False when .gitignore is empty (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("")

        filter_instance = GitignoreFilter(root_path=root_path)
        test_path = root_path / "file.py"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is False


def test__GitignoreFilter__is_ignored__returns_false_when_path_is_outside_root_path() -> None:
    """Returns False when path is outside root_path (ValueError case)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("*.pyc\n")

        filter_instance = GitignoreFilter(root_path=root_path)

        # Create a path outside root_path
        with tempfile.TemporaryDirectory() as outside_dir:
            outside_path = Path(outside_dir) / "file.pyc"
            outside_path.touch()

            assert filter_instance.is_ignored(outside_path) is False


def test__GitignoreFilter__is_ignored__works_with_relative_and_absolute_paths() -> None:
    """Works correctly with both relative and absolute paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("*.pyc\n")

        filter_instance = GitignoreFilter(root_path=root_path)
        test_file = root_path / "file.pyc"
        test_file.touch()

        # Test with absolute path
        assert filter_instance.is_ignored(test_file.resolve()) is True

        # Test with relative path
        assert filter_instance.is_ignored(test_file) is True


def test__GitignoreFilter__is_ignored__handles_multiple_patterns() -> None:
    """Handles multiple patterns correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        gitignore_path = root_path / ".gitignore"
        gitignore_path.write_text("*.pyc\n__pycache__/\n*.log\n")

        filter_instance = GitignoreFilter(root_path=root_path)

        # Test first pattern
        test_path1 = root_path / "file.pyc"
        test_path1.touch()
        assert filter_instance.is_ignored(test_path1) is True

        # Test second pattern
        test_path2 = root_path / "__pycache__" / "module.pyc"
        test_path2.parent.mkdir()
        test_path2.touch()
        assert filter_instance.is_ignored(test_path2) is True

        # Test third pattern
        test_path3 = root_path / "app.log"
        test_path3.touch()
        assert filter_instance.is_ignored(test_path3) is True

        # Test non-matching
        test_path4 = root_path / "file.py"
        test_path4.touch()
        assert filter_instance.is_ignored(test_path4) is False
