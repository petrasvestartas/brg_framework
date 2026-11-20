# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Documentation site (MkDocs Material, deployed to GitHub Pages on push to `main`): Introduction, Installation (with the list of installed packages), License and Changelog.
* `tasks.py` with `invoke` tasks (`test`, `lint`, `format`, `typecheck`, `release`, `prepare-changelog`) from `compas_invocations2`, and the `bump-my-version` configuration.
* GitHub templates: code of conduct, bug report and feature request issues, pull request template, changelog check on pull requests.
* Docs: Contributing and Release pages. `pyright` type check in CI and `invoke typecheck`.
* `initiatives/` with the handoff and decision templates, in the `compas_framework` layout.
* Workflow section in `AGENTS.md` and the skill that points to the `compas_framework` workflow.
* Links to the COMPAS agent guides (`compas_framework` `AGENTS.md`, agents, skills and initiatives on `c3-upgrade`, and `compas` `AGENTS.md`) in `AGENTS.md`, the skill and the docs.

### Changed

* Releases are published to PyPI with trusted publishing (environment `pypi`), and create a GitHub release.
* `build` workflow tests Python 3.10 to 3.13 on Linux, macOS and Windows, and the `server`.
* `.gitignore`: caches, `.DS_Store` and `*.egg-info/`.
* Fixed the types in `brg_framework.cli`.
* CI: read-only permissions, concurrency, `fail-fast: false` and `ruff format --check`.

### Removed

## [0.1.2] 2026-11-20

### Added

### Changed

* The `brg-methods` skill tells agents to follow the COMPAS framework guidelines (`compas_framework`).

### Removed

## [0.1.1] 2026-11-20

### Added

* `brg_framework` package: installs `compas_framework`, then `compas_fd`, `compas_dr`, `compas_tna`, `compas_tno`, `compas_dem`, `compas_ags` and `compas_viewer`.
* `brg` command: `brg install`, `brg examples`, `brg copy <name>`, `brg version`.
* The `brg-methods` skill ships inside the package.

### Changed

### Removed
