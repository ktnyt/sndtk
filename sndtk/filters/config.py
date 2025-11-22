from __future__ import annotations

import fnmatch
import logging
import tomllib
from pathlib import Path

from sndtk.filters.types import FileFilter

logger = logging.getLogger(__name__)


class ConfigFilter(FileFilter):
    def __init__(self, root_path: Path = Path(".")) -> None:
        self.root_path = root_path.resolve()
        self.pyproject_path = self.root_path / "pyproject.toml"

        if not self.pyproject_path.exists():
            logger.error(f"pyproject.toml not found at {self.pyproject_path}")
            raise FileNotFoundError(f"pyproject.toml not found at {self.pyproject_path}")

        try:
            logger.debug(f"Loading config from {self.pyproject_path}")
            with open(self.pyproject_path, "rb") as f:
                data = tomllib.load(f)

            # [tool.coverage-checker.exclude] を取得
            tool_config = data.get("tool", {})
            coverage_config = tool_config.get("coverage-checker", {})
            self.exclude_patterns = coverage_config.get("exclude", [])
            if not isinstance(self.exclude_patterns, list):
                raise ValueError("exclude_patterns must be a list")

            logger.debug(f"Loaded {len(self.exclude_patterns)} exclude patterns")

        except (tomllib.TOMLDecodeError, OSError, TypeError) as e:
            logger.error(f"Failed to load exclude patterns: {e}", exc_info=True)
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
                    logger.debug(f"Path {path_str} matched exclude pattern: {pattern}")
                    return True

            return False

        except ValueError:
            logger.debug(f"Could not determine relative path for {path}")
            return False
