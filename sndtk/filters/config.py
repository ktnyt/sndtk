from __future__ import annotations

import fnmatch
import tomllib
from pathlib import Path

from sndtk.filters.types import FileFilter


class ConfigFilter(FileFilter):
    def __init__(self, root_path: Path = Path(".")) -> None:
        self.root_path = root_path.resolve()
        self.pyproject_path = self.root_path / "pyproject.toml"

        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at {self.pyproject_path}")

        try:
            with open(self.pyproject_path, "rb") as f:
                data = tomllib.load(f)

            # [tool.coverage-checker.exclude] を取得
            tool_config = data.get("tool", {})
            coverage_config = tool_config.get("coverage-checker", {})
            self.exclude_patterns = coverage_config.get("exclude", [])
            if not isinstance(self.exclude_patterns, list):
                raise ValueError("exclude_patterns must be a list")

        except (tomllib.TOMLDecodeError, OSError, TypeError) as e:
            raise ValueError("Failed to load exclude patterns") from e

    def is_ignored(self, path: Path) -> bool:
        if not self.exclude_patterns:
            return False

        try:
            abs_path = path.resolve()
            rel_path = abs_path.relative_to(self.root_path)
            path_str = str(rel_path)

            for pattern in self.exclude_patterns:
                if fnmatch.fnmatch(path_str, pattern):
                    return True

            return False

        except ValueError:
            return False
