# Opinionated Python project starter with batteries included [![.github/workflows/ci.yaml](https://github.com/fcole90/python-poetry-starter/actions/workflows/ci.yaml/badge.svg)](https://github.com/fcole90/python-poetry-starter/actions/workflows/ci.yaml)

This project is designed to be a quick-start for Python projects, providing a set of tools and configurations that make development easier. It includes:

- Initial uv setup with local virtualenv and including poe task runner
- Test setup with pytest
- Linting setup with blake
- Typechecking setup with pyright
- Continuous integration with GitHub Actions

## Requirements

- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
or
- Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

uv can manage Python versions directly. To install Python 3.13 via uv: `uv python install 3.13`

## Installation

```sh
uv sync
```

After this step you may want to close and reopen your terminal or IDE to ensure that the uv-managed virtual environment is activated correctly.

## Tests

```sh
uv run poe test
```

## Linting

```sh
uv run poe lint
```

## Typechecking

```sh
uv run poe typecheck
```
