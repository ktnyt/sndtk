from __future__ import annotations

import ast
import logging
from collections.abc import Generator
from pathlib import Path

from sndtk.parsers.types import Function

logger = logging.getLogger(__name__)


def handle_function(
    node: ast.FunctionDef, filepath: Path, context: list[str]
) -> Generator[Function]:
    identifier = "::".join([*context, node.name])
    yield Function(
        filepath=filepath,
        name=node.name,
        line=node.lineno,
        column=node.col_offset,
        identifier=identifier,
    )

    for child in ast.iter_child_nodes(node):
        yield from search(child, filepath, [*context, node.name])


def search(node: ast.AST, filepath: Path, context: list[str] = []) -> Generator[Function]:
    if isinstance(node, ast.FunctionDef):
        yield from handle_function(node, filepath, context)
        return

    if isinstance(node, ast.ClassDef):
        context = [*context, node.name]

    for child in ast.iter_child_nodes(node):
        yield from search(child, filepath, context)


class PythonParser:
    """
    Pythonコードを解析するクラス
    """

    def parse(self, filepath: Path) -> Generator[Function]:
        """
        Pythonコードを解析する

        Args:
            file_path: 解析対象のPythonファイルのパス

        Returns:
            ast.Module: 解析結果のASTモジュール
        """
        logger.debug(f"Parsing Python file: {filepath}")
        with open(filepath) as f:
            source_code = f.read()

        tree = ast.parse(source_code, filename=str(filepath))
        function_count = 0
        for function in search(tree, filepath):
            function_count += 1
            yield function
        logger.debug(f"Parsed {function_count} functions from {filepath}")
