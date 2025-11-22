"""Tests for Identifier."""

from pathlib import Path

import pytest

from sndtk.spec.types import Identifier


def test__Identifier__from_string__returns_none_when_string_is_empty() -> None:
    """Returns None when string is empty (boundary value)."""
    result = Identifier.from_string("")
    assert result is None


def test__Identifier__from_string__returns_identifier_with_filepath_only_when_ends_with_py() -> (
    None
):
    """Returns identifier with filepath only when string ends with .py."""
    result = Identifier.from_string("test.py")
    assert result is not None
    assert result.filepath == Path("test.py")
    assert result.function_identifier == ""


def test__Identifier__from_string__raises_value_error_when_no_separator() -> None:
    """Raises ValueError when string contains no separator."""
    with pytest.raises(ValueError, match="Invalid identifier: invalid"):
        Identifier.from_string("invalid")


def test__Identifier__from_string__returns_identifier_with_filepath_and_function_when_contains_separator() -> (
    None
):
    """Returns identifier with filepath and function when string contains separator."""
    result = Identifier.from_string("test.py::function_name")
    assert result is not None
    assert result.filepath == Path("test.py")
    assert result.function_identifier == "function_name"
