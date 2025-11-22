Sandhittiko: self-evident and visible test case management tool.

## Overview

Sandhittiko (sndtk) is a Python test case management tool that helps you maintain test coverage by tracking test specifications in JSON files. It analyzes your Python code, identifies functions that need test coverage, and generates test specifications that can be used to guide test implementation.

## Features

- **Function Discovery**: Automatically parses Python files and extracts function definitions (including nested functions and class methods)
- **Test Specification Management**: Maintains test specifications in JSON files (`*_spec.json`) alongside your source code
- **Coverage Reporting**: Reports which functions have test coverage and which scenarios are missing
- **Spec Generation**: Automatically creates test specifications for uncovered functions
- **Smart Filtering**: Filters out test files, gitignored files, and configurable patterns

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Usage

### Basic Usage

Scan the project and report test coverage:

```bash
sndtk --root .
```

### Find First Uncovered Function

Find the first function that needs test coverage:

```bash
sndtk --root . --first
```

### Create Test Specification

Create a test specification for the first uncovered function:

```bash
sndtk --root . --create --first
```

### Target Specific Function

Analyze a specific function:

```bash
sndtk --root . --target path/to/file.py::function_name
sndtk --root . --target path/to/file.py::ClassName::method_name
```

### Verbose Output

Get more detailed logging:

```bash
sndtk --root . -v    # INFO level
sndtk --root . -vv   # DEBUG level
```

## Project Structure

```
sndtk/
├── filters/      # File filtering (gitignore, patterns, config)
├── parsers/      # Python code parsing (AST-based)
├── report/       # Test coverage reporting
└── spec/         # Test specification management
```

## Configuration

Configure file exclusions in `pyproject.toml`:

```toml
[tool.sndtk]
exclude = ["*_test.py", "conftest.py"]
```

## How It Works

1. **Parsing**: Uses Python's AST to extract all function definitions from `.py` files
2. **Specification**: Test specifications are stored in `*_spec.json` files containing:
   - Function identifiers
   - Test scenarios with descriptions
   - Test file paths
3. **Reporting**: Compares parsed functions against specifications and checks if test functions exist
4. **Filtering**: Applies multiple filters to exclude test files and other unwanted files

## Test Specification Format

Test specifications are stored in JSON files (e.g., `module_spec.json`):

```json
{
  "filepath": "path/to/module.py",
  "testpath": "path/to/module_test.py",
  "functions": [
    {
      "identifier": "function_name",
      "scenarios": [
        {
          "testname": "test__function_name__placeholder_scenario0",
          "description": "Placeholder scenario 0..."
        }
      ]
    }
  ]
}
```

## Requirements

- Python >= 3.14
- pathspec >= 0.12.1
- pydantic >= 2.12.4

## Development

Install development dependencies:

```bash
uv sync --dev
```

Run tests:

```bash
pytest
```

Run type checking:

```bash
mypy sndtk
pyright sndtk
```

Run linting:

```bash
ruff check sndtk
```
