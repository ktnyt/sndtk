"""Tests for FileSpec."""

import json
import tempfile
from pathlib import Path

from sndtk.parsers.types import Function
from sndtk.spec.file import FileSpec


def test__FileSpec__create__creates_spec_with_correct_testpath() -> None:
    """Creates spec correctly with correct testpath."""
    filepath = Path("test.py")
    function = Function(
        filepath=filepath,
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    spec = FileSpec.create(filepath, function)
    assert spec.filepath == filepath
    assert spec.testpath == Path("test_test.py")
    assert len(spec.functions) == 1


def test__FileSpec__create__creates_spec_with_function_added() -> None:
    """Creates spec correctly with function added."""
    filepath = Path("module.py")
    function = Function(
        filepath=filepath,
        name="my_function",
        line=5,
        column=4,
        identifier="my_function",
    )
    spec = FileSpec.create(filepath, function)
    assert len(spec.functions) == 1
    assert spec.functions[0].identifier == "my_function"
    assert len(spec.functions[0].scenarios) == 3


def test__FileSpec__create__creates_spec_with_nested_path() -> None:
    """Creates spec correctly with nested path."""
    filepath = Path("subdir/module.py")
    function = Function(
        filepath=filepath,
        name="nested_function",
        line=10,
        column=0,
        identifier="nested_function",
    )
    spec = FileSpec.create(filepath, function)
    assert spec.filepath == filepath
    assert spec.testpath == Path("subdir/module_test.py")
    assert len(spec.functions) == 1


def test__FileSpec__add__adds_function_to_empty_list() -> None:
    """Adds function to empty list (boundary value)."""
    filepath = Path("test.py")
    spec = FileSpec(filepath=filepath, testpath=Path("test_test.py"), functions=[])
    function = Function(
        filepath=filepath,
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    result = spec.add(function)
    assert len(spec.functions) == 1
    assert spec.functions[0].identifier == "test_function"
    assert len(spec.functions[0].scenarios) == 3
    assert result is spec


def test__FileSpec__add__adds_function_to_existing_list() -> None:
    """Adds function to existing list."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    spec = FileSpec.create(filepath, function1)
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    spec.add(function2)
    assert len(spec.functions) == 2
    assert spec.functions[0].identifier == "function1"
    assert spec.functions[1].identifier == "function2"


def test__FileSpec__add__handles_function_identifier_with_separator() -> None:
    """Handles function identifier with separator correctly."""
    filepath = Path("test.py")
    spec = FileSpec(filepath=filepath, testpath=Path("test_test.py"), functions=[])
    function = Function(
        filepath=filepath,
        name="method",
        line=1,
        column=0,
        identifier="MyClass::method",
    )
    spec.add(function)
    assert len(spec.functions) == 1
    assert spec.functions[0].identifier == "MyClass::method"
    assert spec.functions[0].scenarios[0].testname == "test__MyClass__method__placeholder_scenario0"


def test__FileSpec__add__returns_self() -> None:
    """Returns self correctly."""
    filepath = Path("test.py")
    spec = FileSpec(filepath=filepath, testpath=Path("test_test.py"), functions=[])
    function = Function(
        filepath=filepath,
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    result = spec.add(function)
    assert result is spec


def test__FileSpec__load__loads_spec_from_valid_json_file() -> None:
    """Loads spec correctly from valid JSON file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        spec_path = Path(tmpdir) / "test_spec.json"
        spec_data = {
            "filepath": str(filepath),
            "testpath": str(Path(tmpdir) / "test_test.py"),
            "functions": [
                {
                    "testpath": None,
                    "identifier": "test_function",
                    "scenarios": [
                        {
                            "testpath": None,
                            "testname": "test__test_function__scenario0",
                            "description": "Test scenario 0",
                        }
                    ],
                }
            ],
        }
        with open(spec_path, "w") as f:
            json.dump(spec_data, f)
        spec = FileSpec.load(filepath)
        assert spec.filepath == filepath
        assert len(spec.functions) == 1
        assert spec.functions[0].identifier == "test_function"


def test__FileSpec__load__loads_spec_with_empty_functions() -> None:
    """Loads spec correctly with empty functions list (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        spec_path = Path(tmpdir) / "test_spec.json"
        spec_data = {
            "filepath": str(filepath),
            "testpath": str(Path(tmpdir) / "test_test.py"),
            "functions": [],
        }
        with open(spec_path, "w") as f:
            json.dump(spec_data, f)
        spec = FileSpec.load(filepath)
        assert spec.filepath == filepath
        assert len(spec.functions) == 0


def test__FileSpec__load__loads_spec_with_multiple_functions() -> None:
    """Loads spec correctly with multiple functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        spec_path = Path(tmpdir) / "test_spec.json"
        spec_data = {
            "filepath": str(filepath),
            "testpath": str(Path(tmpdir) / "test_test.py"),
            "functions": [
                {
                    "testpath": None,
                    "identifier": "function1",
                    "scenarios": [],
                },
                {
                    "testpath": None,
                    "identifier": "function2",
                    "scenarios": [],
                },
            ],
        }
        with open(spec_path, "w") as f:
            json.dump(spec_data, f)
        spec = FileSpec.load(filepath)
        assert spec.filepath == filepath
        assert len(spec.functions) == 2
        assert spec.functions[0].identifier == "function1"
        assert spec.functions[1].identifier == "function2"


def test__FileSpec__save__saves_spec_to_json_file() -> None:
    """Saves spec correctly to JSON file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        spec = FileSpec(
            filepath=filepath,
            testpath=Path(tmpdir) / "test_test.py",
            functions=[],
        )
        spec_path = spec.save()
        assert spec_path.exists()
        with open(spec_path) as f:
            saved_data = json.load(f)
        assert saved_data["filepath"] == str(filepath)
        assert saved_data["testpath"] == str(Path(tmpdir) / "test_test.py")
        assert saved_data["functions"] == []


def test__FileSpec__save__saves_spec_with_empty_functions() -> None:
    """Saves spec correctly with empty functions list (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "module.py"
        spec = FileSpec(
            filepath=filepath,
            testpath=Path(tmpdir) / "module_test.py",
            functions=[],
        )
        spec_path = spec.save()
        assert spec_path == Path(tmpdir) / "module_spec.json"
        assert spec_path.exists()
        loaded_spec = FileSpec.load(filepath)
        assert len(loaded_spec.functions) == 0


def test__FileSpec__save__returns_correct_path() -> None:
    """Returns correct path after saving."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        spec = FileSpec(
            filepath=filepath,
            testpath=Path(tmpdir) / "test_test.py",
            functions=[],
        )
        spec_path = spec.save()
        expected_path = Path(tmpdir) / "test_spec.json"
        assert spec_path == expected_path
        assert spec_path.exists()
