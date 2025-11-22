from dataclasses import dataclass

from sndtk.parsers.types import Function
from sndtk.spec import FunctionSpec

from .scenario import ScenarioReport


@dataclass
class FunctionReport:
    function: Function
    scenarios: list[ScenarioReport]

    @classmethod
    def generate(
        cls,
        function: Function,
        spec_dict: dict[str, FunctionSpec],
    ) -> FunctionReport:
        function_spec = spec_dict.get(function.identifier)
        if function_spec is None:
            return FunctionReport(function=function, scenarios=[])
        scenarios = [
            ScenarioReport.generate(scenario, function_spec.testpath)
            for scenario in function_spec.scenarios
        ]
        return FunctionReport(function=function, scenarios=scenarios)

    @property
    def covered(self) -> bool:
        if len(self.scenarios) == 0:
            return False
        return all(scenario.reason is None for scenario in self.scenarios)

    def __str__(self) -> str:
        total = len(self.scenarios)
        if total == 0:
            return f"⚠️ {self.function.name}: No scenarios defined"

        covered = len([scenario for scenario in self.scenarios if scenario.reason is None])
        if covered == total:
            return f"✅ {self.function.name}"

        scenario_report = "\n".join([f"    {scenario}" for scenario in self.scenarios])
        return f"❌ {self.function.name} ({covered / total:.2%}):\n{scenario_report}"
