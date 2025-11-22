from pydantic import BaseModel, Field

from sndtk.spec.types import StrPath


class ScenarioSpec(BaseModel):
    testpath: StrPath | None = Field(default=None)
    testname: str
    description: str
