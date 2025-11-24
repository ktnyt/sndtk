from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from sndtk.parsers.python import PythonParser
from sndtk.spec import FileSpec
from sndtk.spec.types import Identifier

from .function import FunctionReport

logger = logging.getLogger(__name__)


@dataclass
class FileReport:
    filepath: Path
    filespec: FileSpec | None
    functions: list[FunctionReport]

    @classmethod
    def generate(cls, filepath: Path, identifier: Identifier | None) -> FileReport:
        logger.debug(f"Generating report for {filepath}")
        parser = PythonParser()
        functions = list(parser.parse(filepath))
        logger.debug(f"Parsed {len(functions)} functions from {filepath}")

        try:
            filespec = FileSpec.load(filepath)
            logger.debug(f"Loaded spec file for {filepath}")
        except FileNotFoundError:
            logger.debug(f"No spec file found for {filepath}")
            filespec = None

        spec_dict = {f.identifier: f for f in filespec.functions} if filespec else {}
        file_testpath = filespec.testpath if filespec and filespec.testpath else None
        function_reports = [
            FunctionReport.generate(function, spec_dict, file_testpath)
            for function in functions
            if identifier is None
            or identifier.function_identifier == ""
            or function.identifier == identifier.function_identifier
        ]
        logger.debug(f"Generated {len(function_reports)} function reports")
        return FileReport(filepath=filepath, filespec=filespec, functions=function_reports)

    def get_first_uncovered_function(self) -> FunctionReport | None:
        if len(self.functions) == 0:
            return None
        return next((function for function in self.functions if not function.covered), None)

    @property
    def covered(self) -> bool:
        if len(self.functions) == 0:
            return True
        return all(function.covered for function in self.functions)

    def __str__(self) -> str:
        if len(self.functions) == 0:
            return f"🪽 {self.filepath}"

        if self.covered:
            return f"✅ {self.filepath}"

        function_reports = "\n".join([f"  {function}" for function in self.functions])
        return f"❌ {self.filepath}:\n{function_reports}"
