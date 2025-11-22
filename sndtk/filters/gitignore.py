from __future__ import annotations

from pathlib import Path

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern


class GitignoreFilter:
    def __init__(self, root_path: Path = Path(".")) -> None:
        self.root_path = root_path.resolve()
        self.gitignore_path = self.root_path / ".gitignore"

        if not self.gitignore_path.exists():
            raise FileNotFoundError(f".gitignore not found at {self.gitignore_path}")

        with self.gitignore_path.open() as f:
            self.spec = PathSpec.from_lines(GitWildMatchPattern, f)

    def is_ignored(self, path: Path) -> bool:
        try:
            abs_path = path.resolve()
            rel_path = abs_path.relative_to(self.root_path)
            return self.spec.match_file(str(rel_path))

        except ValueError:
            return False
