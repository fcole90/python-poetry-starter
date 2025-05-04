# Opinionated Python project starter with batteries included

This project is designed to be a quick-start for Python projects, providing a set of tools and configurations that make development easier. It includes:

- Initial Poetry setup with local virtualenv and including poe task runner as plugin
- Test setup with pytest
- Linting setup with blake
- Typechecking setup with pyright
- Continuous integration with GitHub Actions

## Installation

```sh
poetry install
```

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
