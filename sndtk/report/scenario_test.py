"""Tests for ScenarioReport."""

import tempfile
from pathlib import Path

from sndtk.report.scenario import ScenarioReport
from sndtk.spec.scenario import ScenarioSpec


def test__ScenarioReport__generate__returns_report_with_reason_when_test_file_not_found() -> None:
    """Returns report with reason when test file not found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        function_testpath = Path(tmpdir) / "nonexistent_test.py"
        scenario = ScenarioSpec(testpath=None, testname="test_function", description="Test")
        report = ScenarioReport.generate(scenario, function_testpath)
        assert report.testname == "test_function"
        assert report.reason is not None
        assert "Test file not found" in report.reason


def test__ScenarioReport__generate__returns_report_with_no_reason_when_function_found() -> None:
    """Returns report with no reason when function found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write("def test_function():\n    pass\n")
        scenario = ScenarioSpec(testpath=None, testname="test_function", description="Test")
        report = ScenarioReport.generate(scenario, test_file)
        assert report.testname == "test_function"
        assert report.reason is None


def test__ScenarioReport__generate__returns_report_with_reason_when_function_not_found() -> None:
    """Returns report with reason when function not found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write("def other_function():\n    pass\n")
        scenario = ScenarioSpec(testpath=None, testname="test_function", description="Test")
        report = ScenarioReport.generate(scenario, test_file)
        assert report.testname == "test_function"
        assert report.reason is not None
        assert "Test function not found" in report.reason


def test__ScenarioReport__generate__uses_scenario_testpath_when_provided() -> None:
    """Uses scenario testpath when provided."""
    with tempfile.TemporaryDirectory() as tmpdir:
        scenario_testpath = Path(tmpdir) / "scenario_test.py"
        function_testpath = Path(tmpdir) / "function_test.py"
        with open(scenario_testpath, "w") as f:
            f.write("def test_function():\n    pass\n")
        scenario = ScenarioSpec(
            testpath=scenario_testpath, testname="test_function", description="Test"
        )
        report = ScenarioReport.generate(scenario, function_testpath)
        assert report.testname == "test_function"
        assert report.reason is None


def test__ScenarioReport____str____returns_checkmark_when_reason_is_none() -> None:
    """Returns checkmark string when reason is None (boundary value)."""
    report = ScenarioReport(testname="test_function", reason=None)
    result = str(report)
    assert result == "✅ test_function"


def test__ScenarioReport____str____returns_cross_with_reason_when_reason_exists() -> None:
    """Returns cross string with reason when reason exists."""
    report = ScenarioReport(
        testname="test_function", reason="Test function not found: test_function"
    )
    result = str(report)
    assert result == "❌ test_function: Test function not found: test_function"
