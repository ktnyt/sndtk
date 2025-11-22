from pydantic import BaseModel, Field

from sndtk.spec.scenario import ScenarioSpec
from sndtk.spec.types import StrPath


class FunctionSpec(BaseModel):
    testpath: StrPath | None = Field(default=None)
    identifier: str
    scenarios: list[ScenarioSpec]
