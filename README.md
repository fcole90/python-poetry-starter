# Opinionated Python project starter with batteries included [![.github/workflows/ci.yaml](https://github.com/fcole90/python-poetry-starter/actions/workflows/ci.yaml/badge.svg)](https://github.com/fcole90/python-poetry-starter/actions/workflows/ci.yaml)

This project is designed to be a quick-start for Python projects, providing a set of tools and configurations that make development easier. It includes:

- Initial Poetry setup with local virtualenv and including poe task runner as plugin
- Test setup with pytest
- Linting setup with blake
- Typechecking setup with pyright
- Continuous integration with GitHub Actions

## Requirements

- Python 3.13, if using [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#macos): `pyenv install 3.13.0 && pyenv local 3.13.0`
- Poetry, if using [pipx](https://github.com/pypa/pipx?tab=readme-ov-file#on-macos) (recommended): `pipx install poetry`

## Installation

```sh
poetry install
```

After this step you may want to close and reopen your terminal or IDE to ensure that the Poetry-managed virtual environment is activated correctly.

## Tests

```sh
poetry poe test
```

## Linting

```sh
poetry poe lint
```

## Typechecking

```sh
poetry poe typecheck
```
