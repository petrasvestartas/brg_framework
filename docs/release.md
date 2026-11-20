# Release

1. Add the changes to the `Unreleased` section of `CHANGELOG.md`.
2. Commit everything and push to `main`. Wait for the `build` workflow to pass.
3. Run, in a terminal:

   ```bash
   uv run invoke release patch
   ```

   Use `minor` or `major` when the version needs it. The task formats, tests, bumps the version, tags it, builds the package and prepares the next `Unreleased` section.
4. Push the commits and the tag:

   ```bash
   git push --tags && git push
   ```

The `v*` tag starts the `release` workflow. It tests the package, publishes it to PyPI with trusted publishing (environment `pypi`) and creates the GitHub release.
