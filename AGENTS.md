# AGENTS.md

Guidance for people and agents editing this repository.

## What this repository is

Mostly content. No BRG package imports it.
The package `brg_framework` (`src/`) installs the BRG packages and the command `brg`. It holds no theory and no examples: the skill comes from `skills/`, the examples from `server/`.

| Folder | Content | Edited by hand |
| --- | --- | --- |
| `src/brg_framework/` | The package: version, list of BRG packages, the `brg` command | yes |
| `theory/` | Method theory, one folder per method | yes |
| `catalog/` | Packages and the method table | yes, for now |
| `skills/` | `brg-methods`: which package, and links to it. No package skills | yes |
| `server/` | The MCP server | yes |
| `evals/` | Tasks to measure tokens, time and correctness | yes |

## Rules

1. Write each thing once. Theory lives only in `theory/`.
2. Link to packages, never copy their docs or API. The agent reads the installed package.
3. Skill names are lowercase with hyphens and equal the folder name: `brg-methods`.
4. Every code example is a file that runs. Say which package version it was run with.
5. Do not rename a heading in `theory/*/formulation.md` once something links to it.
6. Short sentences, plain words.

## Adding a package

1. Add a row to `catalog/packages.toml` and to `catalog/methods.md`.
2. Add `theory/<method>/` with the four pages and `teaching/`.
3. Add a row to the table in `skills/brg-methods/SKILL.md`, with the repository and docs links.

What the package itself ships is up to its developers.

## Checks

```bash
uv sync --extra dev
uv run ruff check .
uv run pytest -q

cd server
uv sync --extra dev
uv run ruff check .
uv run pytest -q
```
