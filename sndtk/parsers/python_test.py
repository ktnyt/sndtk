"""Tests for Python parser."""

import ast
import tempfile
from pathlib import Path

from sndtk.parsers.python import PythonParser, handle_function, search


def test__handle_function__yields_function_with_empty_context() -> None:
    """Yields function correctly with empty context (boundary value)."""
    filepath = Path("test.py")
    context: list[str] = []
    node = ast.FunctionDef(
        name="test_function",
        args=ast.arguments(),
        body=[],
        decorator_list=[],
        lineno=1,
        col_offset=0,
    )
    results = list(handle_function(node, filepath, context))
    assert len(results) == 1
    assert results[0].filepath == filepath
    assert results[0].name == "test_function"
    assert results[0].line == 1
    assert results[0].column == 0
    assert results[0].identifier == "test_function"


def test__handle_function__yields_function_with_context() -> None:
    """Yields function correctly with context."""
    filepath = Path("test.py")
    context = ["MyClass"]
    node = ast.FunctionDef(
        name="test_method",
        args=ast.arguments(),
        body=[],
        decorator_list=[],
        lineno=5,
        col_offset=4,
    )
    results = list(handle_function(node, filepath, context))
    assert len(results) == 1
    assert results[0].filepath == filepath
    assert results[0].name == "test_method"
    assert results[0].line == 5
    assert results[0].column == 4
    assert results[0].identifier == "MyClass::test_method"


def test__handle_function__processes_nested_functions() -> None:
    """Processes nested functions correctly."""
    filepath = Path("test.py")
    context: list[str] = []
    inner_node = ast.FunctionDef(
        name="inner_function",
        args=ast.arguments(),
        body=[],
        decorator_list=[],
        lineno=3,
        col_offset=4,
    )
    outer_node = ast.FunctionDef(
        name="outer_function",
        args=ast.arguments(),
        body=[inner_node],
        decorator_list=[],
        lineno=1,
        col_offset=0,
    )
    results = list(handle_function(outer_node, filepath, context))
    assert len(results) == 2
    assert results[0].name == "outer_function"
    assert results[0].identifier == "outer_function"
    assert results[1].name == "inner_function"
    assert results[1].identifier == "outer_function::inner_function"


def test__search__processes_function_def_node() -> None:
    """Processes FunctionDef node correctly."""
    filepath = Path("test.py")
    node = ast.FunctionDef(
        name="test_function",
        args=ast.arguments(),
        body=[],
        decorator_list=[],
        lineno=1,
        col_offset=0,
    )
    results = list(search(node, filepath))
    assert len(results) == 1
    assert results[0].name == "test_function"
    assert results[0].identifier == "test_function"


def test__search__processes_class_def_node() -> None:
    """Processes ClassDef node correctly."""
    filepath = Path("test.py")
    function_node = ast.FunctionDef(
        name="test_method",
        args=ast.arguments(),
        body=[],
        decorator_list=[],
        lineno=2,
        col_offset=4,
    )
    class_node = ast.ClassDef(
        name="MyClass",
        bases=[],
        keywords=[],
        body=[function_node],
        decorator_list=[],
        lineno=1,
        col_offset=0,
    )
    results = list(search(class_node, filepath))
    assert len(results) == 1
    assert results[0].name == "test_method"
    assert results[0].identifier == "MyClass::test_method"


def test__search__processes_other_node_types() -> None:
    """Processes other node types correctly (boundary value)."""
    filepath = Path("test.py")
    node = ast.Constant(value=42, lineno=1, col_offset=0)
    results = list(search(node, filepath))
    assert len(results) == 0


def test__search__processes_with_empty_context() -> None:
    """Processes correctly with empty context (boundary value)."""
    filepath = Path("test.py")
    context: list[str] = []
    node = ast.FunctionDef(
        name="test_function",
        args=ast.arguments(),
        body=[],
        decorator_list=[],
        lineno=1,
        col_offset=0,
    )
    results = list(search(node, filepath, context))
    assert len(results) == 1
    assert results[0].name == "test_function"
    assert results[0].identifier == "test_function"


def test__PythonParser__parse__parses_empty_file() -> None:
    """Parses empty file correctly (boundary value)."""
    parser = PythonParser()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        filepath = Path(f.name)
        f.write("")
    try:
        results = list(parser.parse(filepath))
        assert len(results) == 0
    finally:
        filepath.unlink()


def test__PythonParser__parse__parses_file_with_single_function() -> None:
    """Parses file with single function correctly (boundary value)."""
    parser = PythonParser()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        filepath = Path(f.name)
        f.write("def test_function():\n    pass\n")
    try:
        results = list(parser.parse(filepath))
        assert len(results) == 1
        assert results[0].name == "test_function"
        assert results[0].identifier == "test_function"
        assert results[0].filepath == filepath
    finally:
        filepath.unlink()


def test__PythonParser__parse__parses_file_with_multiple_functions() -> None:
    """Parses file with multiple functions correctly."""
    parser = PythonParser()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        filepath = Path(f.name)
        f.write("def function1():\n    pass\n\ndef function2():\n    pass\n")
    try:
        results = list(parser.parse(filepath))
        assert len(results) == 2
        assert results[0].name == "function1"
        assert results[0].identifier == "function1"
        assert results[1].name == "function2"
        assert results[1].identifier == "function2"
    finally:
        filepath.unlink()


def test__PythonParser__parse__parses_file_with_class_methods() -> None:
    """Parses file with class methods correctly."""
    parser = PythonParser()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        filepath = Path(f.name)
        f.write(
            "class MyClass:\n    def method1(self):\n        pass\n    def method2(self):\n        pass\n"
        )
    try:
        results = list(parser.parse(filepath))
        assert len(results) == 2
        assert results[0].name == "method1"
        assert results[0].identifier == "MyClass::method1"
        assert results[1].name == "method2"
        assert results[1].identifier == "MyClass::method2"
    finally:
        filepath.unlink()
