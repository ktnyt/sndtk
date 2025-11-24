# Retesting

## Tasks

- Run `git status` and `git diff` to find edited files.
- Identify areas of edited files where there are changes in logic.
- Read the changes to understand the outcome of the changes.
- Use `cclsp:find_references` to find potential impact on other code.
- Locate the test spec JSON files for all files that are impacted.
  - If a file does not have an accompanying test spec JSON file, skip handling the file.
  - If a function is not specified in the test spec JSON file (including new functions), skip handling the function.
- Devise of a plan to modify the tests.
- Assess the risks of degradation and notify user if there are any potentially hazardous changes.
- Update the test spec JSON to match the modification plan.
- Modify the tests if everything is clear.
- Run `uv run mypy`, `uv run ruff check --fix --unsafe-fixes` and `uv run ruff format` on the test file.
- Run the tests with `uv run pytest path/to/function.py::Function::indeitifier`
- Run `uv run python -m sndtk --target path/to/function.py::Function::identifier` to check that the spec coverage is met.
