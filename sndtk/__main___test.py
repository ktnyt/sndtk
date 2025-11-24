"""Tests for __main__ module."""

import logging
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from sndtk.__main__ import cli, generate_reports, main, setup_logging, walk
from sndtk.spec.types import Identifier


def test__setup_logging__sets_warning_level_when_verbose_is_zero() -> None:
    """Sets WARNING level when verbose is zero (boundary value)."""
    logging.root.handlers.clear()
    setup_logging(0)
    assert logging.getLogger().level == logging.WARNING


def test__setup_logging__sets_info_level_when_verbose_is_one() -> None:
    """Sets INFO level when verbose is one (boundary value)."""
    logging.root.handlers.clear()
    setup_logging(1)
    assert logging.getLogger().level == logging.INFO


def test__setup_logging__sets_debug_level_when_verbose_is_two() -> None:
    """Sets DEBUG level when verbose is two (boundary value)."""
    logging.root.handlers.clear()
    setup_logging(2)
    assert logging.getLogger().level == logging.DEBUG


def test__setup_logging__sets_debug_level_when_verbose_is_greater_than_two() -> None:
    """Sets DEBUG level when verbose is greater than two."""
    logging.root.handlers.clear()
    setup_logging(3)
    assert logging.getLogger().level == logging.DEBUG


def test__walk__yields_no_paths_when_directory_is_empty() -> None:
    """Yields no paths when directory is empty (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        results = list(walk(path))
        assert len(results) == 0


def test__walk__yields_files_when_directory_contains_only_files() -> None:
    """Yields files correctly when directory contains only files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        file1 = path / "file1.txt"
        file2 = path / "file2.txt"
        file1.touch()
        file2.touch()
        results = list(walk(path))
        assert len(results) == 2
        assert file1 in results
        assert file2 in results


def test__walk__yields_files_from_nested_directories() -> None:
    """Yields files correctly from nested directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        subdir = path / "subdir"
        subdir.mkdir()
        file1 = path / "file1.txt"
        file2 = subdir / "file2.txt"
        file1.touch()
        file2.touch()
        results = list(walk(path))
        assert len(results) == 2
        assert file1 in results
        assert file2 in results


def test__walk__yields_files_from_mixed_structure() -> None:
    """Yields files correctly from mixed file and directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        file1 = path / "file1.txt"
        subdir1 = path / "subdir1"
        subdir1.mkdir()
        file2 = subdir1 / "file2.txt"
        subdir2 = subdir1 / "subdir2"
        subdir2.mkdir()
        file3 = subdir2 / "file3.txt"
        file1.touch()
        file2.touch()
        file3.touch()
        results = list(walk(path))
        assert len(results) == 3
        assert file1 in results
        assert file2 in results
        assert file3 in results


def test__generate_reports__generates_reports_with_no_identifier() -> None:
    """Generates reports correctly with no identifier."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        results = list(generate_reports(path, None))
        assert len(results) >= 1
        assert any(r.filepath == test_file for r in results)


def test__generate_reports__generates_reports_with_identifier() -> None:
    """Generates reports correctly with identifier."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        identifier = Identifier(filepath=test_file, function_identifier="")
        results = list(generate_reports(path, identifier))
        assert len(results) >= 1
        assert any(r.filepath == test_file for r in results)


def test__generate_reports__filters_non_python_files() -> None:
    """Filters non-Python files correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        txt_file = path / "test.txt"
        txt_file.write_text("text content\n")
        results = list(generate_reports(path, None))
        assert all(r.filepath.suffix == ".py" for r in results)
        assert not any(r.filepath == txt_file for r in results)


def test__generate_reports__generates_no_reports_when_directory_is_empty() -> None:
    """Generates no reports when directory is empty (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        results = list(generate_reports(path, None))
        assert len(results) == 0


def test__main__processes_reports_when_first_is_false() -> None:
    """Processes all reports correctly when first is False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            main(path, first=False, create=False, identifier=None)
            output = mock_stdout.getvalue()
            assert len(output) > 0


def test__main__returns_exit_code_zero_when_first_is_false_and_no_uncovered_functions() -> None:
    """Returns exit code 0 when first is False and no uncovered functions found (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        test_test_file = path / "test_test.py"
        test_test_file.write_text("def test__test_function__scenario0():\n    pass\n")
        spec_file = path / "test_spec.json"
        import json

        spec_data = {
            "filepath": str(test_file),
            "testpath": str(test_test_file),
            "functions": [
                {
                    "testpath": None,
                    "identifier": "test_function",
                    "scenarios": [
                        {
                            "testpath": None,
                            "testname": "test__test_function__scenario0",
                            "description": "Test scenario",
                        }
                    ],
                }
            ],
        }
        with open(spec_file, "w") as f:
            json.dump(spec_data, f)
        with patch("sys.stdout", new=StringIO()):
            result = main(path, first=False, create=False, identifier=None)
            assert result == 0


def test__main__returns_exit_code_one_when_first_is_false_and_uncovered_functions_exist() -> None:
    """Returns exit code 1 when first is False and uncovered functions exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        with patch("sys.stdout", new=StringIO()):
            result = main(path, first=False, create=False, identifier=None)
            assert result == 1


def test__main__returns_first_uncovered_when_first_is_true_and_create_is_false() -> None:
    """Returns first uncovered function correctly when first is True and create is False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            result = main(path, first=True, create=False, identifier=None)
            output = mock_stdout.getvalue()
            assert len(output) > 0
            assert result == 1


def test__main__returns_exit_code_one_when_first_is_true_and_create_is_false_and_uncovered_found() -> (
    None
):
    """Returns exit code 1 when first is True, create is False, and uncovered function found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        with patch("sys.stdout", new=StringIO()):
            result = main(path, first=True, create=False, identifier=None)
            assert result == 1


def test__main__creates_spec_when_first_is_true_and_create_is_true_and_filespec_is_none() -> None:
    """Creates spec correctly when first is True, create is True, and filespec is None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            main(path, first=True, create=True, identifier=None)
            output = mock_stdout.getvalue()
            assert "Created spec" in output
            spec_file = path / "test_spec.json"
            assert spec_file.exists()


def test__main__returns_exit_code_zero_when_first_is_true_and_create_is_true_and_uncovered_found() -> (
    None
):
    """Returns exit code 0 when first is True, create is True, and uncovered function found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        with patch("sys.stdout", new=StringIO()):
            result = main(path, first=True, create=True, identifier=None)
            assert result == 0


def test__main__adds_to_existing_spec_when_first_is_true_and_create_is_true_and_filespec_exists() -> (
    None
):
    """Adds to existing spec correctly when first is True, create is True, and filespec exists."""
    import json

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text(
            "def test_function():\n    pass\n\ndef another_function():\n    pass\n"
        )
        spec_file = path / "test_spec.json"
        spec_data = {
            "filepath": str(test_file),
            "testpath": str(path / "test_test.py"),
            "functions": [
                {
                    "testpath": None,
                    "identifier": "test_function",
                    "scenarios": [
                        {
                            "testpath": None,
                            "testname": "test__test_function__scenario0",
                            "description": "Test scenario",
                        }
                    ],
                }
            ],
        }
        with open(spec_file, "w") as f:
            json.dump(spec_data, f)
        test_test_file = path / "test_test.py"
        test_test_file.write_text("def test__test_function__scenario0():\n    pass\n")
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            main(path, first=True, create=True, identifier=None)
            output = mock_stdout.getvalue()
            assert "Created spec" in output
            with open(spec_file) as f:
                updated_spec = json.load(f)
            assert len(updated_spec["functions"]) == 2


def test__main__logs_message_when_first_is_true_and_no_uncovered_functions() -> None:
    """Logs message correctly when first is True and no uncovered functions found (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        test_test_file = path / "test_test.py"
        test_test_file.write_text("def test__test_function__scenario0():\n    pass\n")
        spec_file = path / "test_spec.json"
        import json

        spec_data = {
            "filepath": str(test_file),
            "testpath": str(test_test_file),
            "functions": [
                {
                    "testpath": None,
                    "identifier": "test_function",
                    "scenarios": [
                        {
                            "testpath": None,
                            "testname": "test__test_function__scenario0",
                            "description": "Test scenario",
                        }
                    ],
                }
            ],
        }
        with open(spec_file, "w") as f:
            json.dump(spec_data, f)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            main(path, first=True, create=False, identifier=None)
            output = mock_stdout.getvalue()
            assert len(output) == 0


def test__main__returns_exit_code_zero_when_first_is_true_and_no_uncovered_functions() -> None:
    """Returns exit code 0 when first is True and no uncovered functions found (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text("def test_function():\n    pass\n")
        test_test_file = path / "test_test.py"
        test_test_file.write_text("def test__test_function__scenario0():\n    pass\n")
        spec_file = path / "test_spec.json"
        import json

        spec_data = {
            "filepath": str(test_file),
            "testpath": str(test_test_file),
            "functions": [
                {
                    "testpath": None,
                    "identifier": "test_function",
                    "scenarios": [
                        {
                            "testpath": None,
                            "testname": "test__test_function__scenario0",
                            "description": "Test scenario",
                        }
                    ],
                }
            ],
        }
        with open(spec_file, "w") as f:
            json.dump(spec_data, f)
        with patch("sys.stdout", new=StringIO()):
            result = main(path, first=True, create=False, identifier=None)
            assert result == 0


def test__main__processes_reports_with_identifier_when_first_is_false() -> None:
    """Processes reports correctly with identifier when first is False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text(
            "def test_function():\n    pass\n\ndef another_function():\n    pass\n"
        )
        identifier = Identifier(filepath=test_file, function_identifier="test_function")
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            main(path, first=False, create=False, identifier=identifier)
            output = mock_stdout.getvalue()
            assert len(output) > 0
            assert "test_function" in output or "test.py" in output


def test__main__returns_first_uncovered_with_identifier_when_first_is_true_and_create_is_false() -> (
    None
):
    """Returns first uncovered function correctly with identifier when first is True and create is False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        pyproject_toml = path / "pyproject.toml"
        pyproject_toml.write_text("[tool.sndtk]\nexclude = []\n")
        test_file = path / "test.py"
        test_file.write_text(
            "def test_function():\n    pass\n\ndef another_function():\n    pass\n"
        )
        identifier = Identifier(filepath=test_file, function_identifier="test_function")
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            result = main(path, first=True, create=False, identifier=identifier)
            output = mock_stdout.getvalue()
            assert len(output) > 0
            assert result == 1


def test__cli__calls_main_successfully_with_default_arguments() -> None:
    """Calls main successfully with default arguments."""
    with (
        patch("sys.argv", ["sndtk"]),
        patch("sndtk.__main__.main") as mock_main,
        patch("sndtk.__main__.setup_logging") as mock_setup_logging,
    ):
        mock_main.return_value = 0
        result = cli()
        mock_setup_logging.assert_called_once_with(0)
        mock_main.assert_called_once_with(
            root=Path("."), create=False, first=False, identifier=None
        )
        assert result == 0


def test__cli__calls_main_correctly_with_custom_root_path() -> None:
    """Calls main correctly with custom root path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with (
            patch("sys.argv", ["sndtk", "--root", tmpdir]),
            patch("sndtk.__main__.main") as mock_main,
            patch("sndtk.__main__.setup_logging") as mock_setup_logging,
        ):
            mock_main.return_value = 0
            result = cli()
            mock_setup_logging.assert_called_once_with(0)
            mock_main.assert_called_once_with(
                root=Path(tmpdir), create=False, first=False, identifier=None
            )
            assert result == 0


def test__cli__calls_main_correctly_with_create_and_first_flags() -> None:
    """Calls main correctly with create and first flags."""
    with (
        patch("sys.argv", ["sndtk", "--create", "--first"]),
        patch("sndtk.__main__.main") as mock_main,
        patch("sndtk.__main__.setup_logging") as mock_setup_logging,
    ):
        mock_main.return_value = 0
        result = cli()
        mock_setup_logging.assert_called_once_with(0)
        mock_main.assert_called_once_with(root=Path("."), create=True, first=True, identifier=None)
        assert result == 0


def test__cli__calls_main_correctly_with_target_identifier() -> None:
    """Calls main correctly with target identifier."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.touch()
        with (
            patch("sys.argv", ["sndtk", "--target", f"{test_file}::test_function"]),
            patch("sndtk.__main__.main") as mock_main,
            patch("sndtk.__main__.setup_logging") as mock_setup_logging,
        ):
            mock_main.return_value = 0
            result = cli()
            mock_setup_logging.assert_called_once_with(0)
            mock_main.assert_called_once()
            call_args = mock_main.call_args
            assert call_args.kwargs["root"] == Path(".")
            assert call_args.kwargs["create"] is False
            assert call_args.kwargs["first"] is False
            assert call_args.kwargs["identifier"] is not None
            assert call_args.kwargs["identifier"].filepath == test_file
            assert call_args.kwargs["identifier"].function_identifier == "test_function"
            assert result == 0


def test__cli__calls_setup_logging_correctly_with_verbose_count() -> None:
    """Calls setup_logging correctly with verbose count."""
    with (
        patch("sys.argv", ["sndtk", "-vv"]),
        patch("sndtk.__main__.main") as mock_main,
        patch("sndtk.__main__.setup_logging") as mock_setup_logging,
    ):
        mock_main.return_value = 0
        result = cli()
        mock_setup_logging.assert_called_once_with(2)
        mock_main.assert_called_once()
        assert result == 0
