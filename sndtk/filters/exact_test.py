"""Tests for ExactFilter."""

from pathlib import Path

from .exact import ExactFilter


def test__ExactFilter____init____initializes_successfully_with_relative_path() -> None:
    """Initializes successfully with relative path."""
    filepath = Path("test.py")
    filter_instance = ExactFilter(filepath)
    assert filter_instance.filepath == filepath


def test__ExactFilter____init____initializes_successfully_with_absolute_path() -> None:
    """Initializes successfully with absolute path."""
    filepath = Path("/tmp/test.py")
    filter_instance = ExactFilter(filepath)
    assert filter_instance.filepath == filepath


def test__ExactFilter____init____initializes_successfully_with_nonexistent_path() -> None:
    """Initializes successfully with nonexistent path (boundary value)."""
    filepath = Path("nonexistent_file.py")
    filter_instance = ExactFilter(filepath)
    assert filter_instance.filepath == filepath


def test__ExactFilter__is_ignored__returns_false_when_path_matches_filepath() -> None:
    """Returns False when path matches filepath."""
    filepath = Path("test.py")
    filter_instance = ExactFilter(filepath)
    assert filter_instance.is_ignored(filepath) is False


def test__ExactFilter__is_ignored__returns_true_when_path_does_not_match_filepath() -> None:
    """Returns True when path does not match filepath."""
    filepath = Path("test.py")
    filter_instance = ExactFilter(filepath)
    assert filter_instance.is_ignored(Path("other.py")) is True
