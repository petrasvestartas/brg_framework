# COMPAS Python Examples

`compas_tna` is the thrust network analysis package of COMPAS, and `compas_viewer` displays the thrust network with its form and force diagram. Install them with `pip install compas_tna compas_viewer`, or `uv add compas_tna compas_viewer`.

Every example of the RhinoVAULT manual (https://blockresearchgroup.gitbook.io/rhinovault) is collected here as a standalone Python script that runs without Rhino. Each script follows the commands of the manual step by step. Type any command below to view its Python script (with `compas_viewer`) and run it locally.

## Tutorial

- `mcp_brg_tna_compas_tutorial`: [Tutorial vault on four corner supports](06_compas/01_tutorial.md) (`tna_tutorial.py`)

## Basic design

- `mcp_brg_tna_compas_creases`: [Creases](06_compas/02_creases.md) (`tna_creases.py`)
- `mcp_brg_tna_compas_holes`: [Holes](06_compas/03_holes.md) (`tna_holes.py`)
- `mcp_brg_tna_compas_drop_downs`: [Drop downs](06_compas/04_drop_downs.md) (`tna_drop_downs.py`)
- `mcp_brg_tna_compas_funnel_shell`: [Funnel shell](06_compas/05_funnel_shell.md) (`tna_funnel_shell.py`)
- `mcp_brg_tna_compas_lips`: [Lips](06_compas/06_lips.md) (`tna_lips.py`)

## Historical typologies

- `mcp_brg_tna_compas_fan_vault`: [Fan vault](06_compas/07_fan_vault.md) (`tna_fan_vault.py`)
- `mcp_brg_tna_compas_pillow_vault`: [Pillow vault](06_compas/08_pillow_vault.md) (`tna_pillow_vault.py`)
- `mcp_brg_tna_compas_barrel_vault`: [Barrel vault](06_compas/09_barrel_vault.md) (`tna_barrel_vault.py`)
- `mcp_brg_tna_compas_cross_vault`: [Cross vault](06_compas/10_cross_vault.md) (`tna_cross_vault.py`)

## Case studies

The manual lists three case studies, British Museum, Armadillo Vault and Free form Tile Vault. Their pages are still empty: no steps, no geometry. They have no Python example yet.

## Every script

1. Pattern, supports and boundaries build the `FormDiagram`; `form.update_boundaries()` closes every opening with an unloaded face.
2. `ForceDiagram.from_formdiagram(form)` makes the dual.
3. `horizontal_nodal(form, force, kmax)` makes the diagrams perpendicular and prints the largest angle deviation.
4. `vertical_from_zmax(form, zmax)` computes the heights and returns the scale of the force diagram.
5. The viewer shows the thrust network, the form diagram in plan (green) and the force diagram next to it (blue), supports in red.

## Related commands

- `compas_tna` package links: `mcp_brg_compas_tna`
- Algorithm and the matching RhinoVAULT commands: `mcp_brg_tna_algorithm`
- Presentations: `mcp_brg_tna_presentations`
