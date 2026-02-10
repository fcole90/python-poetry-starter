---
name: conventions
description: Conventions and workflows for this Python project template using Poetry, Black, Pyright (strict), and pytest, with a feature-first layout
version: 0.2.0
---

# Project Conventions

## Purpose

Help the agent work within this Python template in a way that respects my structure, typing rules, and tooling, so the template stays clean and reusable.

## Project context

- Language: Python (>=3.13,<4.0)
- Package name: `my_project` (should be renamed by the user after initial setup)
- Source layout: `src/my_project` (or according to what the user provides)
- Feature-first structure:
  - `src/my_project/feat1/`
  - `src/my_project/feat2/`
  - Each feature keeps its code and tests close together.
- Tooling:
  - Poetry for packaging and dependency management
  - Black for formatting
  - Pyright with strict type checking
  - pytest for testing
  - `poethepoet` tasks under `[tool.poe.tasks]`

## When to use this skill

- Creating or updating features under `src/my_project/<feature_name>/`.
- Adding or updating tests for a feature.
- Creating CLI entrypoints or tasks.
- Adjusting project configuration related to Poetry, Pyright, Black, pytest, or Poe tasks.

## Structure and file placement

- Use a **feature-first** approach:
  - Group related code under `src/my_project/<feature_name>/`.
  - If a feature is self-contained, put its unit tests in the same feature folder, e.g.:
    - `src/my_project/feature/feature.py`
    - `src/my_project/feature/feature_test.py`
- Example of a feature structure
  - `src/my_project/feature/`
    - `main.py`
    - `main_test.py`
    - `types.py` (optional, may contain additional types used in the feature)
    - `api/`
      - `entity_api.py` (e.g fetching an endpoint)
    - `models`/
      - `entity.py` (e.g. Pydantic models)
      - `entity_test.py` (may contain or import mocks to test the model)
    - `services/`
      - `entity_service.py`
      - `entity_service_test.py`

- Do not create a separate top-level `tests` folder for this template.
- Keep module and test names descriptive and consistent.

## Additional utilities

- Additional utilities that are meant to be shared project-wise, go in a special feature-folder called `utils`
- This has a different structure than other feature-folders, as it contains folders divided by purpose
- `utils`
  - `web/`
    - `parser.py`
    - `parser_test.py`
    - `webdriver.py`
    - `webdriver_test.py`

## Typing rules

- Use clear, explicit typing everywhere:
  - Avoid untyped containers like `dict`, `list`, `tuple`, `set`.
  - Prefer precise types such as `dict[str, str]`, `list[int]`, `tuple[str, int]`, etc.
- Treat Pyright strict mode seriously:
  - Fix type issues by improving annotations, adding type guards, or restructuring code.
  - Prefer explicit checks and type guards (e.g. `isinstance` checks) over `# type: ignore`.
  - Only use `# type: ignore` as a last resort, with a short comment explaining why.
- For third-party libraries without type annotations:
  - Prefer installing appropriate type stub packages (e.g. from `types-…` distributions) when available.
  - If no stubs exist, consider creating minimal stubs in `src/typings` for the used parts of the API.

## CLI and scripts

- When a file is meant to be run from the command line:
  - Do **not** use the `if __name__ == "__main__":` pattern.
  - Instead, expose a clear function (e.g. `main()`) inside a module.
  - Register this function in `[tool.poetry.scripts]` so it becomes a CLI entrypoint.
- If the script is not simple Python or better modeled as a task:
  - Add it under `[tool.poe.tasks]` with an appropriate name.
  - Prefer Poe tasks for orchestration or shell-like commands, and Poetry scripts for Python entrypoints.

## Testing conventions

- If a feature is self-contained, add a unit test module next to it:
  - `feature.py` → `feature_test.py` in the same feature directory.
  - Test functions should be named like `test_my_feature()` when testing `my_feature()` in `feature.py`.
- Follow the existing pytest configuration:
  - Tests live under `src`, matching `*_test.py`.
- When adding or changing behavior:
  - Add at least one unit test for non-trivial logic.
  - Prefer focused, readable tests over large, multi-purpose ones.

## Tools and commands

When proposing changes, the agent should keep these commands in mind:

- `poetry run poe test` → run pytest tests.
- `poetry run poe lint` → run Black in check mode.
- `poetry run poe lint-fix` → format code with Black.
- `poetry run poe typecheck` → run Pyright on `./src`.

## General guidance for the agent

- Prefer small, incremental changes aligned with the feature-first layout.
- Maintain readability and consistency over cleverness.
- When in doubt about structure or naming, favor clarity and alignment with these conventions.
