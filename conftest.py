"""Pytest configuration for sndtk project."""

import sys
from pathlib import Path

# Configure pytest to use importlib mode for _test.py files
# This allows pytest to properly import files with dots in their names
import pytest

# Ensure Python path includes the project root before any imports
project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest to use importlib import mode and ensure Python path."""
    # Set import mode to importlib to handle _test.py files correctly
    config.option.importmode = "importlib"
    # Ensure Python path is set
    project_root = Path(config.rootdir).resolve()  # type: ignore[attr-defined]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
