from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

from pydantic import PlainSerializer

StrPath = Annotated[Path, PlainSerializer(lambda path: str(path))]


@dataclass
class Identifier:
    filepath: Path
    function_identifier: str

    @classmethod
    def from_string(cls, string: str) -> Identifier | None:
        if string == "":
            return None
        if string.endswith(".py"):
            return cls(filepath=Path(string), function_identifier="")
        if "::" not in string:
            raise ValueError(f"Invalid identifier: {string}")
        filepath_str, function_identifier = string.split("::", 1)
        return cls(filepath=Path(filepath_str), function_identifier=function_identifier)
