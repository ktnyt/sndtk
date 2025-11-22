from dataclasses import dataclass
from pathlib import Path

from sndtk.parsers.python import PythonParser
from sndtk.spec import ScenarioSpec


@dataclass
class ScenarioReport:
    testname: str
    reason: str | None = None

    @classmethod
    def generate(cls, scenario: ScenarioSpec, function_testpath: Path) -> ScenarioReport:
        testpath = scenario.testpath or function_testpath
        if not testpath.exists():
            return cls(
                testname=scenario.testname,
                reason=f"Test file not found: {testpath}",
            )

        parser = PythonParser()
        for function in parser.parse(testpath):
            if function.identifier == scenario.testname:
                return cls(
                    testname=scenario.testname,
                    reason=None,
                )

        return cls(
            testname=scenario.testname,
            reason=f"Test function not found: {scenario.testname}",
        )

    def __str__(self) -> str:
        if self.reason is None:
            return f"✅ {self.testname}"
        return f"❌ {self.testname}: {self.reason}"
