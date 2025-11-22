"""Tests for FileFilter protocol."""

from pathlib import Path

from .pattern import PatternFilter
from .types import FileFilter


def test__FileFilter__is_ignored__returns_true_when_implementing_class_returns_true() -> None:
    """Returns True when implementing class returns True."""
    filter_instance: FileFilter = PatternFilter(patterns=["*.py"])
    test_path = Path("test.py")
    assert filter_instance.is_ignored(test_path) is True


def test__FileFilter__is_ignored__returns_false_when_implementing_class_returns_false() -> None:
    """Returns False when implementing class returns False."""
    filter_instance: FileFilter = PatternFilter(patterns=["*.py"])
    test_path = Path("test.txt")
    assert filter_instance.is_ignored(test_path) is False


def test__FileFilter__is_ignored__works_with_relative_and_absolute_paths() -> None:
    """Works correctly with both relative and absolute paths."""
    filter_instance: FileFilter = PatternFilter(patterns=["*_test.py"])
    test_file = Path("file_test.py")

    # Test with relative path
    assert filter_instance.is_ignored(test_file) is True

    # Test with absolute path
    assert filter_instance.is_ignored(test_file.resolve()) is True
