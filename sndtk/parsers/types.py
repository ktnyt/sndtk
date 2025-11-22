from dataclasses import dataclass
from pathlib import Path


@dataclass
class Function:
    filepath: Path
    name: str
    line: int
    column: int
    identifier: str
