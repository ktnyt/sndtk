from dataclasses import dataclass
from pathlib import Path

from sndtk.parsers.python import PythonParser
from sndtk.spec import FileSpec

from .function import FunctionReport


@dataclass
class FileReport:
    filepath: Path
    filespec: FileSpec | None
    functions: list[FunctionReport]

    @classmethod
    def generate(cls, filepath: Path) -> FileReport:
        parser = PythonParser()
        functions = list(parser.parse(filepath))

        try:
            filespec = FileSpec.load(filepath)
        except FileNotFoundError:
            filespec = None

        spec_dict = {f.identifier: f for f in filespec.functions} if filespec else {}
        function_reports = [FunctionReport.generate(function, spec_dict) for function in functions]
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
