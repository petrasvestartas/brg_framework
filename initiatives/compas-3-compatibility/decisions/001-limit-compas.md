# Title: How do we keep COMPAS 3 out of `pip install brg_framework`?

## Status

Proposed

## Context

Nothing limits the `compas` version. When COMPAS 3 is released, `pip` can install it for new users. Four BRG packages accept any `compas`, and nobody has tested them on COMPAS 3. See the inventory.

## Options

1. Do nothing. Simple, but new users may get a broken install on the day COMPAS 3 is released.
2. Limit `compas_framework` (for example `<0.2`). The next version number of `compas_framework` is not known, so the limit may not exclude COMPAS 3.
3. Limit `compas` itself: `compas>=2.16,<3`. Certain, and one line.

## Recommendation

Choose option 3. Keep `compas_framework>=0.1.3`.

## Consequences

- New installs get COMPAS 2 until the limit is lifted.
- Users who want COMPAS 3 cannot use `brg_framework` yet.
- A test keeps the limit honest.

## Affected packages

`brg_framework`.

## Dependencies

None.
