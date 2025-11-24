from __future__ import annotations

import json
import logging
from pathlib import Path

from pydantic import BaseModel

from sndtk.parsers.types import Function
from sndtk.spec.function import FunctionSpec
from sndtk.spec.scenario import ScenarioSpec
from sndtk.spec.types import StrPath

logger = logging.getLogger(__name__)


class FileSpec(BaseModel):
    filepath: StrPath
    testpath: StrPath
    functions: list[FunctionSpec]

    @classmethod
    def create(cls, filepath: Path, function: Function) -> FileSpec:
        testpath = filepath.parent / (filepath.stem + "_test.py")
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
                        testname=f"test__{function.identifier.replace('::', '__')}__placeholder_scenario{i}",
                        description=f"Placeholder scenario {i} (These scenarios are just a placeholder. Replace them with actual scenarios with sensible names and description. You do not have to limit the number of scenarios: use as many as is necessary to cover the function.)",
                    )
                    for i in range(3)
                ],
            )
        )
        return self

    @classmethod
    def load(cls, filepath: Path) -> FileSpec:
        spec_path = filepath.parent / (filepath.stem + "_spec.json")
        logger.debug(f"Loading spec from {spec_path}")
        with open(spec_path, "rb") as f:
            content = json.load(f)
            spec = cls.model_validate(content)
            logger.debug(f"Loaded spec with {len(spec.functions)} functions")
            return spec

    def save(self) -> Path:
        filepath = Path(self.filepath)
        spec_path = filepath.parent / (filepath.stem + "_spec.json")
        logger.info(f"Saving spec to {spec_path}")
        logger.debug(f"Spec contains {len(self.functions)} functions")
        with open(spec_path, "w") as f:
            json.dump(self.model_dump(exclude_none=True), f, indent=2)
        return spec_path
