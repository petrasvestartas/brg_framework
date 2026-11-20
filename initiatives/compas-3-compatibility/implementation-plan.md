# Implementation plan

Status: not started. Waiting for decisions 001 and 002.

## Work packages

### WP1: Limit COMPAS

**Ownership:** `brg_framework`.

- Change the `compas` requirement in `pyproject.toml`.
- Add the test.
- Add a line to `CHANGELOG.md`.

**Depends on:** decision 001.

**Gate:** `uv run ruff check .`, `uv run pyright`, `uv run pytest -q` pass, and `pip install brg_framework` from a clean environment installs `compas` 2.x.

### WP2: Lift the limit

**Ownership:** `brg_framework` and the six BRG repositories.

- Each BRG package releases a version that requires `compas>=3`.
- Raise the minimum versions in `pyproject.toml` and remove `<3`.

**Depends on:** decision 002 and WP1.

**Gate:** the build passes on Python 3.12 and newer with COMPAS 3.
