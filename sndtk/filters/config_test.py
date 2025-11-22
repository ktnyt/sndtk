"""Tests for ConfigFilter."""

import tempfile
from pathlib import Path

import pytest

from .config import ConfigFilter


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
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*_test.py", "conftest.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)
        assert filter_instance.exclude_patterns == ["*_test.py", "conftest.py"]


def test__ConfigFilter____init____handles_empty_exclude_patterns() -> None:
    """Handles empty exclude patterns list correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text("[tool.sndtk]\nexclude = []\n")

        filter_instance = ConfigFilter(root_path=root_path)
        assert filter_instance.exclude_patterns == []


def test__ConfigFilter____init____handles_missing_tool_sndtk_section() -> None:
    """Handles missing [tool.sndtk] section correctly (exclude defaults to empty list)."""
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


def test__ConfigFilter__is_ignored__returns_false_when_exclude_patterns_is_empty() -> None:
    """Returns False when exclude_patterns is empty."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text("[tool.sndtk]\nexclude = []\n")

        filter_instance = ConfigFilter(root_path=root_path)
        test_path = root_path / "test.py"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is False


def test__ConfigFilter__is_ignored__returns_true_when_path_matches_pattern() -> None:
    """Returns True when path matches exclude pattern."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*_test.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)
        test_path = root_path / "file_test.py"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is True


def test__ConfigFilter__is_ignored__returns_false_when_path_does_not_match_pattern() -> None:
    """Returns False when path does not match any exclude pattern."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*_test.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)
        test_path = root_path / "file.py"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is False


def test__ConfigFilter__is_ignored__returns_true_when_path_matches_first_pattern() -> None:
    """Returns True when path matches the first pattern in exclude_patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*_test.py", "conftest.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)
        test_path = root_path / "file_test.py"
        test_path.touch()

        assert filter_instance.is_ignored(test_path) is True


def test__ConfigFilter__is_ignored__returns_false_when_path_is_outside_root_path() -> None:
    """Returns False when path is outside root_path (ValueError case)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*_test.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)

        # Create a path outside root_path
        with tempfile.TemporaryDirectory() as outside_dir:
            outside_path = Path(outside_dir) / "file_test.py"
            outside_path.touch()

            assert filter_instance.is_ignored(outside_path) is False


def test__ConfigFilter__is_ignored__handles_wildcard_patterns() -> None:
    """Handles wildcard patterns correctly (* and ?)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["test_*.py", "file?.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)

        # Test * wildcard
        test_path1 = root_path / "test_file.py"
        test_path1.touch()
        assert filter_instance.is_ignored(test_path1) is True

        # Test ? wildcard
        test_path2 = root_path / "file1.py"
        test_path2.touch()
        assert filter_instance.is_ignored(test_path2) is True

        # Test non-matching
        test_path3 = root_path / "other.py"
        test_path3.touch()
        assert filter_instance.is_ignored(test_path3) is False


def test__ConfigFilter__is_ignored__works_with_relative_and_absolute_paths() -> None:
    """Works correctly with both relative and absolute paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_path = Path(tmpdir)
        pyproject_path = root_path / "pyproject.toml"
        pyproject_path.write_text('[tool.sndtk]\nexclude = ["*_test.py"]\n')

        filter_instance = ConfigFilter(root_path=root_path)
        test_file = root_path / "file_test.py"
        test_file.touch()

        # Test with absolute path
        assert filter_instance.is_ignored(test_file.resolve()) is True

        # Test with relative path
        assert filter_instance.is_ignored(test_file) is True
