from pathlib import Path

import yaml
from pydantic import BaseModel

from sndtk.parsers.types import Function
from sndtk.spec.function import FunctionSpec
from sndtk.spec.scenario import ScenarioSpec
from sndtk.spec.types import StrPath


class FileSpec(BaseModel):
    filepath: StrPath
    functions: list[FunctionSpec]

    @classmethod
    def create(cls, filepath: Path, function: Function) -> FileSpec:
        spec = cls(filepath=filepath, functions=[])
        spec.add(filepath, function)
        return spec

    def add(self, filepath: Path, function: Function) -> FileSpec:
        self.functions.append(
            FunctionSpec(
                testpath=filepath.with_suffix(".test.py"),
                identifier=function.identifier,
                scenarios=[
                    ScenarioSpec(
                        testpath=None,
                        testname=f"{function.identifier.replace('::', '__')}__scenario{i}",
                        description=f"Scenario {i}",
                    )
                    for i in range(3)
                ],
            )
        )
        return self

    @classmethod
    def load(cls, filepath: Path) -> FileSpec:
        with open(filepath.with_suffix(".spec.yml")) as f:
            content = yaml.load(f, Loader=yaml.SafeLoader)
            spec = cls.model_validate(content)
            return spec

    def save(self) -> None:
        with open(self.filepath.with_suffix(".spec.yml"), "w") as f:
            yaml.dump(self.model_dump(), f)
