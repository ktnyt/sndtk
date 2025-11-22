# Coverage Check

## Tasks

- Run `uv run python -m sndtk --first` command; if no uncovered functions are found, report and finish.
- If a function is missing test scenarios (indicated by ❌), implement those scenarios in the test file specified in the specfile.
- If a function does not have any specs (indicated by ⚠️), run `uv run python -m sndtk --first --create` command.
- Use cclsp:find_definition MCP tool on the target function implementation to understand the target function logic.
- Use cclsp:find_references MCP tool to find and understand the context of the target function usage.
- Identify essential test scenarios with boundary value analysis. DO NOT INCLUDE SCENARIOS THAT ASSUME INCORRECT ARGUMENT/RETURN TYPES.
- Overwrite the scenario defaults.
- Implement the test scenarios.
- Run `uv run mypy`, `uv run ruff check --fix --unsafe-fixes` and `uv run ruff format` on the test file.
- Run `uv run python -m sndtk --target path/to/function.py::Function::identifier` to check that the target function is no longer uncovered.
- Report and finish. DO NOT PROCEED TO DO ANY MORE WORK UNLESS EXPLICITY SPECIFIED FROM THE USRE.

## Conventions

### Test description

- Describe tests in English.
- Use table testing where applicable to reduce the number of scenarios.
