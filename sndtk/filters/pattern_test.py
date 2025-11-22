"""Tests for PatternFilter."""

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
