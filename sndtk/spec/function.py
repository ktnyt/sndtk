from pydantic import BaseModel

from sndtk.spec.scenario import ScenarioSpec
from sndtk.spec.types import StrPath


class FunctionSpec(BaseModel):
    testpath: StrPath
    identifier: str
    scenarios: list[ScenarioSpec]
