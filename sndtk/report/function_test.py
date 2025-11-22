"""Tests for FunctionReport."""

import tempfile
from pathlib import Path

from sndtk.parsers.types import Function
from sndtk.report.function import FunctionReport
from sndtk.report.scenario import ScenarioReport
from sndtk.spec.function import FunctionSpec
from sndtk.spec.scenario import ScenarioSpec


def test__FunctionReport__generate__returns_empty_scenarios_when_spec_not_found() -> None:
    """Returns empty scenarios when spec not found (boundary value)."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    spec_dict: dict[str, FunctionSpec] = {}
    report = FunctionReport.generate(function, spec_dict, None)
    assert report.function == function
    assert len(report.scenarios) == 0


def test__FunctionReport__generate__returns_empty_scenarios_when_testpath_is_none() -> None:
    """Returns empty scenarios when testpath is None (boundary value)."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    function_spec = FunctionSpec(testpath=None, identifier="test_function", scenarios=[])
    spec_dict = {"test_function": function_spec}
    report = FunctionReport.generate(function, spec_dict, None)
    assert report.function == function
    assert len(report.scenarios) == 0


def test__FunctionReport__generate__uses_function_spec_testpath_when_provided() -> None:
    """Uses function spec testpath when provided."""
    with tempfile.TemporaryDirectory() as tmpdir:
        function_testpath = Path(tmpdir) / "function_test.py"
        file_testpath = Path(tmpdir) / "file_test.py"
        with open(function_testpath, "w") as f:
            f.write("def test_function():\n    pass\n")
        function = Function(
            filepath=Path("test.py"),
            name="test_function",
            line=1,
            column=0,
            identifier="test_function",
        )
        scenario = ScenarioSpec(testpath=None, testname="test_function", description="Test")
        function_spec = FunctionSpec(
            testpath=function_testpath, identifier="test_function", scenarios=[scenario]
        )
        spec_dict = {"test_function": function_spec}
        report = FunctionReport.generate(function, spec_dict, file_testpath)
        assert report.function == function
        assert len(report.scenarios) == 1
        assert report.scenarios[0].testname == "test_function"
        assert report.scenarios[0].reason is None


def test__FunctionReport__generate__uses_file_testpath_when_function_spec_testpath_is_none() -> (
    None
):
    """Uses file testpath when function spec testpath is None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_testpath = Path(tmpdir) / "file_test.py"
        with open(file_testpath, "w") as f:
            f.write("def test_function():\n    pass\n")
        function = Function(
            filepath=Path("test.py"),
            name="test_function",
            line=1,
            column=0,
            identifier="test_function",
        )
        scenario = ScenarioSpec(testpath=None, testname="test_function", description="Test")
        function_spec = FunctionSpec(
            testpath=None, identifier="test_function", scenarios=[scenario]
        )
        spec_dict = {"test_function": function_spec}
        report = FunctionReport.generate(function, spec_dict, file_testpath)
        assert report.function == function
        assert len(report.scenarios) == 1
        assert report.scenarios[0].testname == "test_function"
        assert report.scenarios[0].reason is None


def test__FunctionReport__generate__generates_scenario_reports_when_scenarios_exist() -> None:
    """Generates scenario reports correctly when scenarios exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write("def test_function():\n    pass\n")
        function = Function(
            filepath=Path("test.py"),
            name="test_function",
            line=1,
            column=0,
            identifier="test_function",
        )
        scenario1 = ScenarioSpec(testpath=None, testname="test_function", description="Test 1")
        scenario2 = ScenarioSpec(testpath=None, testname="test_function", description="Test 2")
        function_spec = FunctionSpec(
            testpath=test_file, identifier="test_function", scenarios=[scenario1, scenario2]
        )
        spec_dict = {"test_function": function_spec}
        report = FunctionReport.generate(function, spec_dict, None)
        assert report.function == function
        assert len(report.scenarios) == 2
        assert report.scenarios[0].testname == "test_function"
        assert report.scenarios[1].testname == "test_function"


def test__FunctionReport__generate__returns_empty_scenarios_when_scenarios_list_is_empty() -> None:
    """Returns empty scenarios when scenarios list is empty (boundary value)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write("def test_function():\n    pass\n")
        function = Function(
            filepath=Path("test.py"),
            name="test_function",
            line=1,
            column=0,
            identifier="test_function",
        )
        function_spec = FunctionSpec(testpath=test_file, identifier="test_function", scenarios=[])
        spec_dict = {"test_function": function_spec}
        report = FunctionReport.generate(function, spec_dict, None)
        assert report.function == function
        assert len(report.scenarios) == 0


def test__FunctionReport__covered__returns_false_when_scenarios_empty() -> None:
    """Returns False when scenarios list is empty (boundary value)."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    report = FunctionReport(function=function, scenarios=[])
    assert report.covered is False


def test__FunctionReport__covered__returns_true_when_all_scenarios_covered() -> None:
    """Returns True when all scenarios are covered."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    scenario1 = ScenarioReport(testname="test1", reason=None)
    scenario2 = ScenarioReport(testname="test2", reason=None)
    report = FunctionReport(function=function, scenarios=[scenario1, scenario2])
    assert report.covered is True


def test__FunctionReport__covered__returns_false_when_some_scenarios_uncovered() -> None:
    """Returns False when some scenarios are uncovered."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    scenario1 = ScenarioReport(testname="test1", reason=None)
    scenario2 = ScenarioReport(testname="test2", reason="Test function not found: test2")
    report = FunctionReport(function=function, scenarios=[scenario1, scenario2])
    assert report.covered is False


def test__FunctionReport____str____returns_warning_when_scenarios_empty() -> None:
    """Returns warning string when scenarios list is empty (boundary value)."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    report = FunctionReport(function=function, scenarios=[])
    result = str(report)
    assert result == "⚠️ test_function: No scenarios defined"


def test__FunctionReport____str____returns_checkmark_when_all_covered() -> None:
    """Returns checkmark string when all scenarios are covered."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    scenario1 = ScenarioReport(testname="test1", reason=None)
    scenario2 = ScenarioReport(testname="test2", reason=None)
    report = FunctionReport(function=function, scenarios=[scenario1, scenario2])
    result = str(report)
    assert result == "✅ test_function"


def test__FunctionReport____str____returns_cross_with_percentage_when_some_uncovered() -> None:
    """Returns cross string with percentage when some scenarios are uncovered."""
    function = Function(
        filepath=Path("test.py"),
        name="test_function",
        line=1,
        column=0,
        identifier="test_function",
    )
    scenario1 = ScenarioReport(testname="test1", reason=None)
    scenario2 = ScenarioReport(testname="test2", reason="Test function not found: test2")
    report = FunctionReport(function=function, scenarios=[scenario1, scenario2])
    result = str(report)
    assert result.startswith("❌ test_function (50.00%):")
    assert "test1" in result or "test2" in result
