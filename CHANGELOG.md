# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Documentation site at https://blockresearchgroup.github.io/brg_framework/ (MkDocs Material): installation with the list of installed packages, contributing, release, changelog and license.
* Agent guidance that follows the [COMPAS framework](https://github.com/compas-dev/compas_framework/tree/c3-upgrade) (`c3-upgrade`): links to its `AGENTS.md`, agents, skills and initiatives, and a workflow section in `AGENTS.md` and the `brg-methods` skill (investigate, design and stop for approval, implement, review).
* `initiatives/` with the handoff and decision templates, in the `compas_framework` layout.
* Development tooling: `invoke` tasks (`test`, `lint`, `format`, `typecheck`, `release`, `prepare-changelog`), `pyright` type check, and the `bump-my-version` configuration.
* GitHub templates: code of conduct, issue and pull request templates, and a changelog check on pull requests.

### Changed

* CI follows the `compas_framework` workflows: actions pinned to commit SHAs, read-only permissions, concurrency, `ruff format --check` and `pyright`, and tests on Python 3.10 to 3.13 on Linux, macOS and Windows.
* Release: the package is built once, checked (`twine check`, clean wheel smoke test, tag equals version), then the same files are published to PyPI with trusted publishing and attached to the GitHub release.
* Docs are built in strict mode on pull requests and deployed from `main`.
* Fixed the types in `brg_framework.cli`.

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
