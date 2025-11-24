"""Tests for FileReport."""

import tempfile
from pathlib import Path

from sndtk.parsers.types import Function
from sndtk.report.file import FileReport
from sndtk.report.function import FunctionReport
from sndtk.report.scenario import ScenarioReport
from sndtk.spec.types import Identifier


def test__FileReport__generate__generates_report_with_no_identifier() -> None:
    """Generates report correctly with no identifier."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        with open(filepath, "w") as f:
            f.write("def function1():\n    pass\n\ndef function2():\n    pass\n")
        report = FileReport.generate(filepath, None)
        assert report.filepath == filepath
        assert len(report.functions) == 2
        assert report.functions[0].function.name == "function1"
        assert report.functions[1].function.name == "function2"


def test__FileReport__generate__generates_report_with_file_identifier() -> None:
    """Generates report correctly with file identifier."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        with open(filepath, "w") as f:
            f.write("def function1():\n    pass\n\ndef function2():\n    pass\n")
        identifier = Identifier(filepath=filepath, function_identifier="")
        report = FileReport.generate(filepath, identifier)
        assert report.filepath == filepath
        assert len(report.functions) == 2


def test__FileReport__generate__generates_report_with_function_identifier() -> None:
    """Generates report correctly with function identifier."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        with open(filepath, "w") as f:
            f.write("def function1():\n    pass\n\ndef function2():\n    pass\n")
        identifier = Identifier(filepath=filepath, function_identifier="function1")
        report = FileReport.generate(filepath, identifier)
        assert report.filepath == filepath
        assert len(report.functions) == 1
        assert report.functions[0].function.name == "function1"


def test__FileReport__generate__generates_report_without_spec_file() -> None:
    """Generates report correctly without spec file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        with open(filepath, "w") as f:
            f.write("def test_function():\n    pass\n")
        report = FileReport.generate(filepath, None)
        assert report.filepath == filepath
        assert report.filespec is None
        assert len(report.functions) == 1
        assert len(report.functions[0].scenarios) == 0


def test__FileReport__generate__generates_report_with_empty_file() -> None:
    """Generates report correctly with empty file (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.py"
        with open(filepath, "w") as f:
            f.write("")
        report = FileReport.generate(filepath, None)
        assert report.filepath == filepath
        assert len(report.functions) == 0


def test__FileReport__get_first_uncovered_function__returns_none_when_empty() -> None:
    """Returns None when functions list is empty (boundary value)."""
    filepath = Path("test.py")
    report = FileReport(filepath=filepath, filespec=None, functions=[])
    result = report.get_first_uncovered_function()
    assert result is None


def test__FileReport__get_first_uncovered_function__returns_first_uncovered_function() -> None:
    """Returns first uncovered function correctly."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    uncovered_report = FunctionReport(function=function2, scenarios=[])
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report, uncovered_report]
    )
    result = report.get_first_uncovered_function()
    assert result is not None
    assert result.function.name == "function2"


def test__FileReport__get_first_uncovered_function__returns_none_when_all_covered() -> None:
    """Returns None when all functions are covered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report1 = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    covered_report2 = FunctionReport(
        function=function2, scenarios=[ScenarioReport(testname="test2", reason=None)]
    )
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report1, covered_report2]
    )
    result = report.get_first_uncovered_function()
    assert result is None


def test__FileReport__covered__returns_true_when_empty() -> None:
    """Returns True when functions list is empty (boundary value)."""
    filepath = Path("test.py")
    report = FileReport(filepath=filepath, filespec=None, functions=[])
    assert report.covered is True


def test__FileReport__covered__returns_true_when_all_covered() -> None:
    """Returns True when all functions are covered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report1 = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    covered_report2 = FunctionReport(
        function=function2, scenarios=[ScenarioReport(testname="test2", reason=None)]
    )
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report1, covered_report2]
    )
    assert report.covered is True


def test__FileReport__covered__returns_false_when_some_uncovered() -> None:
    """Returns False when some functions are uncovered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    uncovered_report = FunctionReport(function=function2, scenarios=[])
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report, uncovered_report]
    )
    assert report.covered is False


def test__FileReport__uncovered_count__returns_zero_when_empty() -> None:
    """Returns zero when functions list is empty (boundary value)."""
    filepath = Path("test.py")
    report = FileReport(filepath=filepath, filespec=None, functions=[])
    assert report.uncovered_count == 0


def test__FileReport__uncovered_count__returns_zero_when_all_covered() -> None:
    """Returns zero when all functions are covered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report1 = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    covered_report2 = FunctionReport(
        function=function2, scenarios=[ScenarioReport(testname="test2", reason=None)]
    )
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report1, covered_report2]
    )
    assert report.uncovered_count == 0


def test__FileReport__uncovered_count__returns_count_when_some_uncovered() -> None:
    """Returns correct count when some functions are uncovered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    function3 = Function(
        filepath=filepath,
        name="function3",
        line=10,
        column=0,
        identifier="function3",
    )
    covered_report = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    uncovered_report1 = FunctionReport(function=function2, scenarios=[])
    uncovered_report2 = FunctionReport(function=function3, scenarios=[])
    report = FileReport(
        filepath=filepath,
        filespec=None,
        functions=[covered_report, uncovered_report1, uncovered_report2],
    )
    assert report.uncovered_count == 2


def test__FileReport__uncovered_count__returns_count_when_all_uncovered() -> None:
    """Returns correct count when all functions are uncovered (boundary value)."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    uncovered_report1 = FunctionReport(function=function1, scenarios=[])
    uncovered_report2 = FunctionReport(function=function2, scenarios=[])
    report = FileReport(
        filepath=filepath,
        filespec=None,
        functions=[uncovered_report1, uncovered_report2],
    )
    assert report.uncovered_count == 2


def test__FileReport____str____returns_emoji_when_empty() -> None:
    """Returns emoji string when functions list is empty (boundary value)."""
    filepath = Path("test.py")
    report = FileReport(filepath=filepath, filespec=None, functions=[])
    result = str(report)
    assert result == f"🪽 {filepath}"


def test__FileReport____str____returns_checkmark_when_covered() -> None:
    """Returns checkmark string when all functions are covered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report1 = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    covered_report2 = FunctionReport(
        function=function2, scenarios=[ScenarioReport(testname="test2", reason=None)]
    )
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report1, covered_report2]
    )
    result = str(report)
    assert result == f"✅ {filepath}"


def test__FileReport____str____returns_cross_with_reports_when_uncovered() -> None:
    """Returns cross string with function reports when uncovered."""
    filepath = Path("test.py")
    function1 = Function(
        filepath=filepath,
        name="function1",
        line=1,
        column=0,
        identifier="function1",
    )
    function2 = Function(
        filepath=filepath,
        name="function2",
        line=5,
        column=0,
        identifier="function2",
    )
    covered_report = FunctionReport(
        function=function1, scenarios=[ScenarioReport(testname="test1", reason=None)]
    )
    uncovered_report = FunctionReport(function=function2, scenarios=[])
    report = FileReport(
        filepath=filepath, filespec=None, functions=[covered_report, uncovered_report]
    )
    result = str(report)
    assert result.startswith(f"❌ {filepath}:")
    assert "function1" in result or "function2" in result
