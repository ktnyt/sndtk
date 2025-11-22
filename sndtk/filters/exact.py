from pathlib import Path


class ExactFilter:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def is_ignored(self, path: Path) -> bool:
        return path != self.filepath
