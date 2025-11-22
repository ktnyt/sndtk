import argparse
from collections.abc import Generator
from os import listdir
from pathlib import Path

from sndtk.filters import DEFAULT_FILTER
from sndtk.report import FileReport


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


def main(root: Path, *, first: bool = False) -> None:
    reports = generate_reports(root)
    for report in reports:
        if first:
            if report.first_uncovered is not None:
                print(report.first_uncovered)
                return
        print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--first", action="store_true")
    args = parser.parse_args()
    main(root=args.root, first=args.first)
