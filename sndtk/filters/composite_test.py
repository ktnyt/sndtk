"""Tests for CompositeFileFilter."""

from pathlib import Path

from .composite import CompositeFileFilter
from .exact import ExactFilter
from .pattern import PatternFilter


def test__CompositeFileFilter____init____initializes_successfully_with_no_filters() -> None:
    """Initializes successfully with no filters (boundary value)."""
    filter_instance = CompositeFileFilter()
    assert filter_instance.filters == []


def test__CompositeFileFilter____init____initializes_successfully_with_single_filter() -> None:
    """Initializes successfully with single filter (boundary value)."""
    exact_filter = ExactFilter(Path("test.py"))
    filter_instance = CompositeFileFilter(exact_filter)
    assert len(filter_instance.filters) == 1
    assert filter_instance.filters[0] == exact_filter


def test__CompositeFileFilter____init____initializes_successfully_with_multiple_filters() -> None:
    """Initializes successfully with multiple filters."""
    exact_filter = ExactFilter(Path("test.py"))
    pattern_filter = PatternFilter()
    filter_instance = CompositeFileFilter(exact_filter, pattern_filter)
    assert len(filter_instance.filters) == 2
    assert filter_instance.filters[0] == exact_filter
    assert filter_instance.filters[1] == pattern_filter


def test__CompositeFileFilter__add__adds_filter_to_empty_list() -> None:
    """Adds filter to empty list (boundary value)."""
    filter_instance = CompositeFileFilter()
    exact_filter = ExactFilter(Path("test.py"))
    filter_instance.add(exact_filter)
    assert len(filter_instance.filters) == 1
    assert filter_instance.filters[0] == exact_filter


def test__CompositeFileFilter__add__adds_filter_to_existing_list() -> None:
    """Adds filter to existing list."""
    exact_filter1 = ExactFilter(Path("test1.py"))
    filter_instance = CompositeFileFilter(exact_filter1)
    exact_filter2 = ExactFilter(Path("test2.py"))
    filter_instance.add(exact_filter2)
    assert len(filter_instance.filters) == 2
    assert filter_instance.filters[0] == exact_filter1
    assert filter_instance.filters[1] == exact_filter2


def test__CompositeFileFilter__add__adds_multiple_filters_sequentially() -> None:
    """Adds multiple filters sequentially."""
    filter_instance = CompositeFileFilter()
    exact_filter = ExactFilter(Path("test.py"))
    pattern_filter = PatternFilter()
    filter_instance.add(exact_filter)
    filter_instance.add(pattern_filter)
    assert len(filter_instance.filters) == 2
    assert filter_instance.filters[0] == exact_filter
    assert filter_instance.filters[1] == pattern_filter


def test__CompositeFileFilter__is_ignored__returns_false_when_no_filters() -> None:
    """Returns False when no filters (boundary value)."""
    filter_instance = CompositeFileFilter()
    assert filter_instance.is_ignored(Path("test.py")) is False


def test__CompositeFileFilter__is_ignored__returns_false_when_all_filters_return_false() -> None:
    """Returns False when all filters return False."""
    exact_filter = ExactFilter(Path("test.py"))
    filter_instance = CompositeFileFilter(exact_filter)
    assert filter_instance.is_ignored(Path("test.py")) is False


def test__CompositeFileFilter__is_ignored__returns_true_when_single_filter_returns_true() -> None:
    """Returns True when single filter returns True."""
    exact_filter = ExactFilter(Path("test.py"))
    filter_instance = CompositeFileFilter(exact_filter)
    assert filter_instance.is_ignored(Path("other.py")) is True


def test__CompositeFileFilter__is_ignored__returns_true_when_any_filter_returns_true() -> None:
    """Returns True when any filter returns True."""
    exact_filter = ExactFilter(Path("test.py"))
    pattern_filter = PatternFilter()
    filter_instance = CompositeFileFilter(exact_filter, pattern_filter)
    assert filter_instance.is_ignored(Path("test_test.py")) is True
