# Coverage Check

## Tasks

- Run `uv run python -m sndtk --first` command; if no uncovered functions are found, report and finish.
- If a function is missing test scenarios (indicated by ❌), implement those scenarios in the test file specified in the specfile.
- If a function does not have any specs (indicated by ⚠️), run `uv run python -m sndtk --first --create` command.
- Use cclsp:find_definition MCP tool on the target function implementation to understand the target function logic.
- Use cclsp:find_references MCP tool to find and understand the context of the target function usage.
- Identify essential test scenarios with boundary value analysis. DO NOT INCLUDE SCENARIOS THAT ASSUME INCORRECT ARGUMENT/RETURN TYPES.
- Double check to be absolutely certain that all edge cases are considered in the test.
- Overwrite the scenario defaults.
- Implement the test scenarios.
- Run `uv run mypy`, `uv run ruff check --fix --unsafe-fixes` and `uv run ruff format` on the test file.
- Run the tests with `uv run pytest path/to/function.py::Function::indeitifier`
- Run `uv run python -m sndtk --target path/to/function.py::Function::identifier` to check that the target function is no longer uncovered.
- Report and finish. DO NOT PROCEED TO DO ANY MORE WORK UNLESS EXPLICITY SPECIFIED FROM THE USER.

## Conventions

### Test description

- Describe tests in English.
- Use table testing where applicable to reduce the number of scenarios.

#### Template patterns

Follow these patterns based on the test scenario type:

**Success cases (normal behavior):**

- `"[Action] successfully when [condition]"`
  - Example: `"Initializes successfully with default root_path (current directory)"`
  - Example: `"Returns True when path matches exclude pattern"`
- `"[Action] correctly with [input/context]"`
  - Example: `"Loads exclude patterns correctly from pyproject.toml"`
  - Example: `"Handles wildcard patterns correctly (* and ?)"`

**Return value assertions:**

- `"Returns [value] when [condition]"`
  - Example: `"Returns False when exclude_patterns is empty"`
  - Example: `"Returns True when path matches the first pattern in exclude_patterns"`

**Error/exception cases:**

- `"Raises [ExceptionType] when [condition]"`
  - Example: `"Raises FileNotFoundError when pyproject.toml does not exist"`
  - Example: `"Raises ValueError when exclude patterns is not a list"`

**Edge cases and boundary values:**

- Add `(boundary value)` annotation when testing edge cases
  - Example: `"Initializes successfully with empty patterns list (boundary value)"`
  - Example: `"Initializes successfully with single pattern (boundary value)"`

**Complex scenarios:**

- For scenarios testing multiple aspects, use: `"[Action] [aspect1] and [aspect2]"`
  - Example: `"Works correctly with both relative and absolute paths"`

#### Guidelines

- Start with a verb (Initializes, Returns, Raises, Handles, Works, etc.)
- Be specific about conditions and expected outcomes
- Use present tense
- Keep descriptions concise but informative
- For boundary value tests, explicitly mark with `(boundary value)`
