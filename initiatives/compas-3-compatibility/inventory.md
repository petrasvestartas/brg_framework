# Inventory

Checked on 2026-11-20 against the packages installed from PyPI by `pip install brg_framework` 0.1.2, and against `compas_framework` branch `c3-upgrade`.

## What `brg_framework` asks for

`pyproject.toml` requires `compas_framework>=0.1.3` and `compas>=2.16`. Neither has an upper limit. `requires-python` is `>=3.10`.

## What the packages ask for

| Package | Version | Requirement on `compas` |
| --- | --- | --- |
| `compas_fd` | 0.5.4 | any |
| `compas_dr` | 0.3.1 | `>=2.1` |
| `compas_tna` | 0.9.0 | any |
| `compas_tno` | 0.4.0 | any |
| `compas_dem` | 0.6.0 | `>=2.4` |
| `compas_ags` | 1.3.3 | any |
| `compas_viewer` | 2.0.2 | `>=2.2.0` |
| `compas_framework` | 0.1.3 | `>=2.13` |

No package has an upper limit. Four accept any version of `compas`.

## What COMPAS 3 changes

- PyPI today: `compas` 2.16.0, `compas_framework` 0.1.3.
- `compas` branch `initiative/repository-modernisation` is version 3.0.0 and requires Python 3.12 or newer.
- `compas_framework` branch `c3-upgrade` requires `compas>=3.0.0` and Python `>=3.12,<3.15`. Its `__version__` is still 0.1.3, so its next release number is not known.

## Not known

Whether the six BRG packages run on COMPAS 3. Nothing in this repository tests it.
