"""Tests for ConfigFilter."""

import tempfile
from pathlib import Path

import pytest

from sndtk.filters.config import ConfigFilter


def test__ConfigFilter____init____initializes_with_default_root_path() -> None:
    """Initializes successfully with default root_path (current directory)."""
    # Use the project root which has pyproject.toml
    filter_instance = ConfigFilter()
    assert filter_instance.root_path.exists()
    assert filter_instance.pyproject_path.exists()
    assert filter_instance.pyproject_path.name == "pyproject.toml"


def test__ConfigFilter____init____initializes_with_custom_root_path() -> None:
    """Initializes successfully with custom root_path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text("[tool.sndtk]\nexclude = []\n")

        filter_instance = ConfigFilter(root_path=root_path)
        assert filter_instance.root_path == root_path.resolve()
        assert filter_instance.pyproject_path == root_path.resolve() / "pyproject.toml"


def test__ConfigFilter____init____loads_exclude_patterns_from_pyproject_toml() -> None:
    """Loads exclude patterns correctly from pyproject.toml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*.test.py", "conftest.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)
        assert filter_instance.exclude_patterns == ["*.test.py", "conftest.py"]


def test__ConfigFilter____init____handles_empty_exclude_patterns() -> None:
    """Handles empty exclude patterns list."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text("[tool.sndtk]\nexclude = []\n")

        filter_instance = ConfigFilter(root_path=root_path)
        assert filter_instance.exclude_patterns == []


def test__ConfigFilter____init____handles_missing_tool_sndtk_section() -> None:
    """Handles missing [tool.sndtk] section (exclude defaults to empty list)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[project]\nname = "test"\n')

        filter_instance = ConfigFilter(root_path=root_path)
        assert filter_instance.exclude_patterns == []


def test__ConfigFilter____init____raises_file_not_found_error_when_pyproject_toml_not_exists() -> (
    None
):
    """Raises FileNotFoundError when pyproject.toml does not exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        # Do not create pyproject.toml

        with pytest.raises(FileNotFoundError) as exc_info:
            ConfigFilter(root_path=root_path)
        assert "pyproject.toml not found" in str(exc_info.value)


def test__ConfigFilter____init____raises_value_error_when_exclude_patterns_not_list() -> None:
    """Raises ValueError when exclude patterns is not a list."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = "not a list"\n')

        with pytest.raises(ValueError) as exc_info:
            ConfigFilter(root_path=root_path)
        assert "exclude_patterns must be a list" in str(exc_info.value)


def test__ConfigFilter____init____raises_value_error_when_invalid_toml() -> None:
    """Raises ValueError when TOML format is invalid."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text("invalid toml content [\n")

        with pytest.raises(ValueError) as exc_info:
            ConfigFilter(root_path=root_path)
        assert "Failed to load exclude patterns" in str(exc_info.value)
