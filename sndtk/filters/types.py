from pathlib import Path
from typing import Protocol


class FileFilter(Protocol):
    """ファイルフィルタリングのためのプロトコル"""

    def is_ignored(self, path: Path) -> bool:
        """
        指定されたパスがフィルタリング対象かどうかを判定する

        Args:
            path: 判定対象のパス

        Returns:
            bool: フィルタリング対象の場合True、対象外の場合False
        """
        ...
