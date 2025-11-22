import logging
from pathlib import Path

import yaml
from pydantic import BaseModel

from sndtk.parsers.types import Function
from sndtk.spec.function import FunctionSpec
from sndtk.spec.scenario import ScenarioSpec
from sndtk.spec.types import StrPath

logger = logging.getLogger(__name__)


class FileSpec(BaseModel):
    filepath: StrPath
    testpath: StrPath | None = None
    functions: list[FunctionSpec]

    @classmethod
    def create(cls, filepath: Path, function: Function) -> FileSpec:
        testpath = filepath.with_suffix(".test.py")
        spec = cls(filepath=filepath, testpath=testpath, functions=[])
        spec.add(function)
        return spec

    def add(self, function: Function) -> FileSpec:
        self.functions.append(
            FunctionSpec(
                testpath=None,
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
        spec_path = filepath.with_suffix(".spec.yml")
        logger.debug(f"Loading spec from {spec_path}")
        with open(spec_path) as f:
            content = yaml.load(f, Loader=yaml.SafeLoader)
            spec = cls.model_validate(content)
            logger.debug(f"Loaded spec with {len(spec.functions)} functions")
            return spec

    def save(self) -> Path:
        spec_path = self.filepath.with_suffix(".spec.yml")
        logger.info(f"Saving spec to {spec_path}")
        logger.debug(f"Spec contains {len(self.functions)} functions")
        with open(spec_path, "w") as f:
            yaml.dump(self.model_dump(exclude_none=True), f)
        return spec_path
