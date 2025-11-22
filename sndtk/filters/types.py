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


class CompositeFileFilter(FileFilter):
    """
    複数のFileFilterを組み合わせて統一的なフィルタリングを提供するクラス
    """

    def __init__(self, *filters: FileFilter) -> None:
        """
        複数のFileFilterを組み合わせて統一的なフィルタリングを提供するクラス

        Args:
            filters: 適用するFileFilterのリスト
        """
        self.filters = list(filters)

    def is_ignored(self, path: Path) -> bool:
        """
        いずれかのフィルターがTrueを返した場合にフィルタリング対象とする

        Args:
            path: 判定対象のパス

        Returns:
            bool: フィルタリング対象の場合True、対象外の場合False
        """
        return any(filter.is_ignored(path) for filter in self.filters)
