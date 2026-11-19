Algorithm

```
1. Draw the pattern: the plan of the forces ◄────────┐
        ▼                                            │
2. Choose the supports ◄─────────────────────────────┐
        ▼                                            │
3. Curve the open boundaries (force density) ◄───────┐
        ▼                                            │
4. Form diagram Γ: pattern + one face per opening    │
        ▼                                            │
5. Force diagram Γ*: the dual of the form diagram    │
        ▼                                            │
6. Horizontal equilibrium: make all edge pairs       │
   of Γ and Γ* perpendicular ◄───────────────────────┐
        ▼                                            │
7. Force densities q = scale · l* / l                │
        ▼                                            │
8. Vertical equilibrium: solve for the heights z,    │
   find the scale for the wanted height zmax         │
        ▼                                            │
9. Design satisfactory? ──── no ? ───────────────────┘
        ▼
10. Materialize: thickness, stereotomy, fabrication
```

Steps 1 to 8 are the commands of RhinoVAULT and the functions of `compas_tna`:

| Step | RhinoVAULT | `compas_tna` |
|------|------------|--------------|
| 1 | `RV_pattern` | `FormDiagram.from_mesh`, `FormDiagram.from_lines`, `FormDiagram.create_cross`, `FormDiagram.create_fan` |
| 2 | `RV_pattern_supports` | vertex attribute `is_support` |
| 3 | `RV_pattern_relax`, `RV_pattern_boundaries` | `relax_boundary_openings` |
| 4 | `RV_form` | `form.update_boundaries()` |
| 5 | `RV_force` | `ForceDiagram.from_formdiagram` |
| 6 | `RV_tna_horizontal` | `horizontal_nodal` |
| 6 | `RV_form_modify`, `RV_force_modify` | edge attributes `hmin`, `hmax` (form) and `lmin`, `lmax` (force) |
| 8 | `RV_tna_vertical` | `vertical_from_zmax` |
| 8 | `RV_thrust_modify` | vertex attribute `z` of the supports |
