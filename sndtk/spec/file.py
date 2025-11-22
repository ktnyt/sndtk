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


def to_specpath(filepath: Path) -> Path:
    return filepath.with_suffix(".spec.yml")


def load_filespec(filepath: Path) -> FileSpec:
    with open(to_specpath(filepath)) as f:
        content = yaml.load(f, Loader=yaml.SafeLoader)
        spec = FileSpec.model_validate(content)
        return spec


def create_empty_filespec(filepath: Path, functions: list[Function]) -> FileSpec:
    specpath = to_specpath(filepath)
    testpath = filepath.with_suffix(".test.py")
    spec = FileSpec(
        filepath=specpath,
        functions=[
            FunctionSpec(
                testpath=testpath,
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
            for function in functions
        ],
    )

    with open(specpath, "w") as f:
        yaml.dump(spec.model_dump(), f)

    return spec
