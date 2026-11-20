# AGENTS.md

Guidance for people and agents editing this repository.

## What this repository is

Mostly content. No BRG package imports it.
The package `brg_framework` (`src/`) installs the BRG packages and the command `brg`. It holds no theory and no examples: the skill comes from `skills/`, the examples from `server/`.

| Folder | Content | Edited by hand |
| --- | --- | --- |
| `src/brg_framework/` | The package: version, list of BRG packages, the `brg` command | yes |
| `theory/` | Method theory, one folder per method | yes |
| `skills/` | `brg-methods`: which package, and links to it. No package skills | yes |
| `server/` | The MCP server | yes |
| `evals/` | Tasks to measure tokens, time and correctness | yes |
| `initiatives/` | Plans and decisions for larger changes, in the `compas_framework` layout | yes |

## COMPAS framework and the COMPAS agent guides

`compas_framework` is installed with this package. When you write code, follow these, in this order. They are on the branch `c3-upgrade` (the move to COMPAS 3) and move to `main` when it is merged.

1. [`compas_framework` AGENTS.md](https://github.com/compas-dev/compas_framework/blob/c3-upgrade/AGENTS.md): the coordinator instructions and engineering principles for cross-package work.
2. [`compas_framework` agents](https://github.com/compas-dev/compas_framework/tree/c3-upgrade/.codex/agents): `architect`, `explorer`, `implementer`, `reviewer`, `documenter`. Use them the way that file says: architect for design, implementer for approved changes, reviewer to check.
3. [`compas_framework` skills](https://github.com/compas-dev/compas_framework/tree/c3-upgrade/.agents/skills): `update-docs`, `update-docstrings`, `update-type-hints`.
4. [`compas_framework` initiatives](https://github.com/compas-dev/compas_framework/tree/c3-upgrade/initiatives): objectives and accepted decisions. Read them before you change a shared contract.
5. [`compas` AGENTS.md](https://github.com/compas-dev/compas/blob/initiative/repository-modernisation/AGENTS.md): Python 3.12+ style, typing and runtime rules.

Some paths in those files are local to their author (for example the conda environment). Ignore them.
Where they differ from this file, this file wins for this repository only.

## Workflow

For any change that is more than a small fix, follow the workflow in [`compas_framework` AGENTS.md](https://github.com/compas-dev/compas_framework/blob/c3-upgrade/AGENTS.md) (sections "Workflow", "Verification Responsibilities", "Rules" and "Architecture Decision Records"). Do not copy it here. In short:

1. Investigate first (the `explorer` agent). Do not assume an API exists. Read the installed package.
2. Design (the `architect` agent) and **stop for approval** before you change code.
3. Implement only what was approved (the `implementer` agent). Run the checks below.
4. Review independently (the `reviewer` agent). Do not claim a check passed unless you ran it.
5. Record each significant decision as one file in `initiatives/<name>/decisions/NNN-title.md`, copied from `initiatives/_template/decision.md`. Mark it `Proposed` until the user accepts it. Keep the handoff in `initiatives/<name>/handoff.md`, copied from `initiatives/_template/handoff.md`. The layout is in [`initiatives/README.md`](initiatives/README.md) and follows [theirs](https://github.com/compas-dev/compas_framework/tree/c3-upgrade/initiatives).
6. Do not merge, tag or publish without explicit approval.

## Start or resume an initiative

An initiative is a larger change with a plan and decisions. It lives in `initiatives/<name>/`. See [`initiatives/README.md`](initiatives/README.md).

- **Start.** Create the branch `initiative/<name>`. Copy the templates from `initiatives/_template/`. The user writes `objective.md`. Then investigate (`inventory.md`), design (`proposal.md` and the decisions, all `Proposed`) and stop for approval.
- **Resume.** If the user says `Continue <name> from initiatives/<name>/handoff.md`, or the task names an initiative, read its `handoff.md` first, then only the files it links.
- **Work.** Do the approved work on the branch `initiative/<name>` and open a pull request. Do not merge or release without the user's approval.
- **Checkpoint.** Update `handoff.md` before you stop: the phase, the exact branch and commit, what is approved, the next tasks and what was verified.
- **Start a new conversation** for each initiative, or for each phase of a large one.

## Rules

1. Write each thing once. Theory lives only in `theory/`.
2. Link to packages, never copy their docs or API. The agent reads the installed package.
3. Skill names are lowercase with hyphens and equal the folder name: `brg-methods`.
4. Every code example is a file that runs. Say which package version it was run with.
5. Do not rename a heading in `theory/*/formulation.md` once something links to it.
6. Short sentences, plain words.

## Adding a package

1. Add it to `dependencies` in `pyproject.toml` and to `PACKAGES` in `src/brg_framework/__init__.py`.
2. Add a row to the table in `skills/brg-methods/SKILL.md`, with the repository and docs links.
3. Add `theory/<method>/` with the four pages and `teaching/`.

What the package itself ships is up to its developers.

## Checks

```bash
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest -q

cd server
uv sync --extra dev
uv run ruff check .
uv run pytest -q
```
