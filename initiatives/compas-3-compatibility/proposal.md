# Proposal

## Summary

Limit `brg_framework` to COMPAS 2 until every BRG package is shown to work on COMPAS 3. Test the limit so a change cannot slip in.

> `pip install brg_framework` must never install a COMPAS major version that the BRG packages were not tested with.

## Why not limit `compas_framework` instead

Its next version number is not known (the branch still says 0.1.3), so a range such as `<0.2` may or may not exclude the COMPAS 3 release. The limit on `compas` itself is certain.

## Recommended change

1. In `pyproject.toml`, change `compas>=2.16` to `compas>=2.16,<3`.
2. Keep `compas_framework>=0.1.3`. With `compas<3`, `pip` picks the newest `compas_framework` that allows COMPAS 2.
3. Add a test that fails when the installed `compas` major version is not 2.
4. Lift the limit only after the six BRG packages release versions that require `compas>=3` and the build passes with them.

See the decisions for the options and trade-offs.

## Affected packages

`brg_framework`. No other repository changes.

## Proposed tests

- `tests/test_package.py`: the installed `compas` major version equals 2.
- CI: the existing matrix, unchanged.
