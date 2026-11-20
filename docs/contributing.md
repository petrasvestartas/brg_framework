# Contributing

Install [uv](https://docs.astral.sh/uv/), clone the repository and install the development tools:

```bash
uv sync --extra dev
```

Run the checks before you push:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest -q
```

The same checks run in CI. Each is also a task: `uv run invoke test`, `lint`, `format`, `typecheck`.

Rules for agents and people are in [`AGENTS.md`](https://github.com/BlockResearchGroup/brg_framework/blob/main/AGENTS.md).
They follow the [COMPAS framework guidelines](https://github.com/compas-dev/compas_framework/blob/c3-upgrade/AGENTS.md).

Add a line to the `Unreleased` section of `CHANGELOG.md` with every change.
