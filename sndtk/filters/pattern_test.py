"""Tests for PatternFilter."""

from pathlib import Path

from .pattern import DEFAULT_PATTENRS, PatternFilter


def test__PatternFilter____init____initializes_with_default_patterns() -> None:
    """Initializes successfully with default patterns when no patterns argument is provided."""
    filter_instance = PatternFilter()
    assert filter_instance.patterns == DEFAULT_PATTENRS


def test__PatternFilter____init____initializes_with_custom_patterns() -> None:
    """Initializes successfully with custom patterns list."""
    custom_patterns = ["*.py", "*.txt"]
    filter_instance = PatternFilter(patterns=custom_patterns)
    assert filter_instance.patterns == custom_patterns


def test__PatternFilter____init____initializes_with_empty_patterns() -> None:
    """Initializes successfully with empty patterns list (boundary value)."""
    filter_instance = PatternFilter(patterns=[])
    assert filter_instance.patterns == []


def test__PatternFilter____init____initializes_with_single_pattern() -> None:
    """Initializes successfully with single pattern (boundary value)."""
    single_pattern = ["*.py"]
    filter_instance = PatternFilter(patterns=single_pattern)
    assert filter_instance.patterns == single_pattern


def test__PatternFilter__is_ignored__returns_false_when_patterns_is_empty() -> None:
    """Returns False when patterns is empty (boundary value)."""
    filter_instance = PatternFilter(patterns=[])
    test_path = Path("test.py")
    assert filter_instance.is_ignored(test_path) is False


def test__PatternFilter__is_ignored__returns_true_when_path_matches_single_pattern() -> None:
    """Returns True when path matches single pattern (boundary value)."""
    filter_instance = PatternFilter(patterns=["*.py"])
    test_path = Path("test.py")
    assert filter_instance.is_ignored(test_path) is True


def test__PatternFilter__is_ignored__returns_false_when_path_does_not_match_single_pattern() -> (
    None
):
    """Returns False when path does not match single pattern (boundary value)."""
    filter_instance = PatternFilter(patterns=["*.py"])
    test_path = Path("test.txt")
    assert filter_instance.is_ignored(test_path) is False


def test__PatternFilter__is_ignored__returns_true_when_path_matches_pattern() -> None:
    """Returns True when path matches pattern."""
    filter_instance = PatternFilter(patterns=["*_test.py", "conftest.py"])
    test_path = Path("file_test.py")
    assert filter_instance.is_ignored(test_path) is True


def test__PatternFilter__is_ignored__returns_false_when_path_does_not_match_any_pattern() -> None:
    """Returns False when path does not match any pattern."""
    filter_instance = PatternFilter(patterns=["*_test.py", "conftest.py"])
    test_path = Path("file.py")
    assert filter_instance.is_ignored(test_path) is False


def test__PatternFilter__is_ignored__returns_true_when_path_matches_first_pattern() -> None:
    """Returns True when path matches the first pattern in patterns."""
    filter_instance = PatternFilter(patterns=["*_test.py", "conftest.py", "*.txt"])
    test_path = Path("file_test.py")
    assert filter_instance.is_ignored(test_path) is True


def test__PatternFilter__is_ignored__returns_true_when_path_matches_last_pattern() -> None:
    """Returns True when path matches the last pattern in patterns."""
    filter_instance = PatternFilter(patterns=["*_test.py", "conftest.py", "*.txt"])
    test_path = Path("file.txt")
    assert filter_instance.is_ignored(test_path) is True


def test__PatternFilter__is_ignored__handles_wildcard_patterns() -> None:
    """Handles wildcard patterns correctly (* and ?)."""
    filter_instance = PatternFilter(patterns=["test_*.py", "file?.py"])

    # Test * wildcard
    test_path1 = Path("test_file.py")
    assert filter_instance.is_ignored(test_path1) is True

    # Test ? wildcard
    test_path2 = Path("file1.py")
    assert filter_instance.is_ignored(test_path2) is True

    # Test non-matching
    test_path3 = Path("other.py")
    assert filter_instance.is_ignored(test_path3) is False


def test__PatternFilter__is_ignored__works_with_relative_and_absolute_paths() -> None:
    """Works correctly with both relative and absolute paths."""
    filter_instance = PatternFilter(patterns=["*_test.py"])
    test_file = Path("file_test.py")

    # Test with relative path
    assert filter_instance.is_ignored(test_file) is True

    # Test with absolute path
    assert filter_instance.is_ignored(test_file.resolve()) is True
