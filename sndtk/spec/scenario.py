from pydantic import BaseModel

from sndtk.spec.types import StrPath


class ScenarioSpec(BaseModel):
    testpath: StrPath | None
    testname: str
    description: str
