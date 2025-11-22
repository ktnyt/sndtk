from __future__ import annotations

import fnmatch
from pathlib import Path

from .types import FileFilter

DEFAULT_PATTENRS = [
    "**/test_*.py",
    "**/tests.py",
    "**/test/*.py",
    "**/tests/*.py",
    "**/*_test.py",
    "**/*_test.py",
    "**/conftest.py",
    ".venv/**/*.py",
]


class PatternFilter(FileFilter):
    def __init__(self, patterns: list[str] = DEFAULT_PATTENRS) -> None:
        self.patterns = patterns

    def is_ignored(self, path: Path) -> bool:
        path_str = str(path)

        for pattern in self.patterns:
            if fnmatch.fnmatch(path_str, pattern):
                return True

        return False
