from pathlib import Path
from typing import Annotated

from pydantic import PlainSerializer

StrPath = Annotated[Path, PlainSerializer(lambda path: str(path))]
