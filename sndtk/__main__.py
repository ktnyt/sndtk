import argparse
import logging
from collections.abc import Generator
from os import listdir
from pathlib import Path

from sndtk.filters import (
    CompositeFileFilter,
    ConfigFilter,
    ExactFilter,
    GitignoreFilter,
    PatternFilter,
)
from sndtk.report import FileReport
from sndtk.spec import FileSpec
from sndtk.spec.types import Identifier


def setup_logging(verbose: int) -> None:
    """Set up logging configuration based on verbose level.

    Args:
        verbose: Number of -v flags (0=WARNING, 1=INFO, 2+=DEBUG)
    """
    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(levelname)s:%(name)s:%(message)s",
        datefmt=None,
    )


def walk(path: Path) -> Generator[Path]:
    logger = logging.getLogger(__name__)
    for item in listdir(path):
        item_path = path / item
        if item_path.is_dir():
            logger.debug(f"Entering directory: {item_path}")
            yield from walk(item_path)
        else:
            logger.debug(f"Found file: {item_path}")
            yield item_path


def generate_reports(root: Path, identifier: Identifier | None = None) -> Generator[FileReport]:
    logger = logging.getLogger(__name__)
    logger.info(f"Generating reports for root: {root}")

    filter = CompositeFileFilter(
        GitignoreFilter(),
        PatternFilter(),
        ConfigFilter(),
    )

    if identifier is not None:
        filter.add(ExactFilter(identifier.filepath))

    for path in walk(root):
        if path.suffix == ".py":
            if filter.is_ignored(path):
                logger.debug(f"Ignoring file (filtered): {path}")
                continue
            logger.debug(f"Processing file: {path}")
            yield FileReport.generate(path, identifier)


def main(
    root: Path,
    *,
    create: bool = False,
    first: bool = False,
    identifier: Identifier | None = None,
) -> None:
    logger = logging.getLogger(__name__)
    if create:
        assert first, "Create one function spec at a time to avoid task explosion"
        logger.info("Create mode enabled")

    reports = generate_reports(root, identifier)
    for report in reports:
        if first:
            function_report = report.get_first_uncovered_function()
            if function_report is not None:
                if not create:
                    logger.debug(
                        f"Found first uncovered function: {function_report.function.identifier}"
                    )
                    print(
                        FileReport(
                            filepath=report.filepath,
                            filespec=report.filespec,
                            functions=[function_report],
                        )
                    )
                    return

                logger.info(f"Creating spec for {function_report.function.identifier}")
                if report.filespec is None:
                    filespec = FileSpec.create(report.filepath, function_report.function)
                else:
                    filespec = report.filespec.add(function_report.function)

                specpath = filespec.save()
                print(f"Created spec for {function_report.function.identifier} in {specpath}")
                return
        else:
            logger.info(f"Report for {report.filepath}: {report}")
            print(report)

    if first:
        logger.info("No uncovered functions found")
        return


def cli() -> None:
    """Command-line interface entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--first", action="store_true")
    parser.add_argument("--target", type=str, default="")
    parser.add_argument("-v", "--verbose", action="count", default=0)

    args = parser.parse_args()

    setup_logging(args.verbose)

    main(
        root=args.root,
        create=args.create,
        first=args.first,
        identifier=Identifier.from_string(args.target) if args.target else None,
    )


if __name__ == "__main__":
    cli()
