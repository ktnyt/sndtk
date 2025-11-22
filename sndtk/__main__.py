import argparse
from collections.abc import Generator
from os import listdir
from pathlib import Path

from sndtk.filters import DEFAULT_FILTER
from sndtk.report import FileReport
from sndtk.spec import FileSpec


def walk(path: Path) -> Generator[Path]:
    for item in listdir(path):
        item_path = path / item
        if item_path.is_dir():
            yield from walk(item_path)
        else:
            yield item_path


def generate_reports(root: Path) -> Generator[FileReport]:
    for path in walk(root):
        if path.suffix == ".py" and not DEFAULT_FILTER.is_ignored(path):
            yield FileReport.generate(path)


def main(root: Path, *, create: bool = False, first: bool = False) -> None:
    if create:
        assert first, "Create one function spec at a time to avoid task explosion"

    reports = generate_reports(root)
    for report in reports:
        if first:
            function_report = report.get_first_uncovered_function()
            if function_report is not None:
                if not create:
                    print(
                        FileReport(
                            filepath=report.filepath,
                            filespec=report.filespec,
                            functions=[function_report],
                        )
                    )
                    return

                if report.filespec is None:
                    filespec = FileSpec.create(report.filepath, function_report.function)
                else:
                    filespec = report.filespec.add(report.filepath, function_report.function)

                filespec.save()
                print(
                    f"Created spec for {function_report.function.identifier} in {report.filepath}"
                )
                return

        print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--first", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)

    args = parser.parse_args()

    main(root=args.root, create=args.create, first=args.first)
