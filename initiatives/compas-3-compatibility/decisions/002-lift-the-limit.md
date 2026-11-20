# Title: When do we lift the `compas<3` limit?

## Status

Proposed

## Context

The limit from decision 001 should not stay forever. COMPAS 3 needs Python 3.12 or newer, while `brg_framework` supports Python 3.10 and 3.11.

## Options

1. Lift it when COMPAS 3 is released. Fast, but the BRG packages may not work.
2. Lift it when all six BRG packages release a version that requires `compas>=3` and the build passes.
3. Lift it per package. Not possible: one `compas` version is installed for all of them.

## Recommendation

Choose option 2. When it is lifted, change `requires-python` to `>=3.12`, or publish a separate release line for COMPAS 3.

## Consequences

- Users on Python 3.10 and 3.11 stay on the COMPAS 2 line.
- The release that lifts the limit is a minor version, with a note in the changelog.

## Affected packages

`brg_framework` and the six BRG packages.

## Dependencies

001.
