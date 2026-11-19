Cross vault, tna_cross_vault.py: four barrel vaults meet on two diagonal ribs that carry the thrust to four corner supports.

Adapted from the RhinoVAULT example Cross Vault: https://blockresearchgroup.gitbook.io/rhinovault/examples/historical-typologies/cross-vault

Checked against the session file of the manual (`examples_cross_vault_6.json`): the same force diagram scale, 2.0612111187002.

Tested with `compas 2.16.0`, `compas_tna 0.9.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Thrust network analysis: a cross vault, four barrel vaults that meet on two diagonal ribs."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_tna.diagrams import ForceDiagram
from compas_tna.diagrams import FormDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_tna.equilibrium import vertical_from_zmax
from compas_viewer import Viewer

# 1. pattern: a 10 x 10 grid, the cells on the two diagonals are split into triangles
form = FormDiagram.create_cross(x_span=(0, 10), y_span=(0, 10), n=10, supports="corners")

# 2. supports: the four corners
supports = list(form.supports())

# 3. form diagram: the four free edges become four unloaded faces
form.update_boundaries()

# 4. modify the form diagram: fix the horizontal force of the edges with hmin = hmax
for edge in form.edges_where(_is_edge=True):
    (x0, y0, _), (x1, y1, _) = form.edge_coordinates(edge)
    x, y = (x0 + x1) / 2 - 5, (y0 + y1) / 2 - 5  # midpoint, seen from the centre
    if x0 != x1 and y0 != y1:
        if max(abs(x), abs(y)) > 1:
            continue  # the diagonal ribs are free, they collect the thrust of the arches
        force = 1  # the four diagonals at the centre
    elif max(abs(x), abs(y)) == 5:
        force = 1  # the four boundary arches carry half a strip
    elif (y0 == y1) == (abs(y) > abs(x)):
        force = 2  # the arches, parallel to the nearest boundary
    else:
        force = 1e-5  # across the arches: almost no force
    form.edge_attributes(edge, ["hmin", "hmax"], [force, force])

# 5. force diagram: the dual of the form diagram
force = ForceDiagram.from_formdiagram(form)

# 6. horizontal equilibrium: the edges across the arches collapse, the diagonals and arches remain
horizontal_nodal(form, force, kmax=3000)

# 7. vertical equilibrium: the highest node is at a quarter of the diagonal of the plan
form, scale = vertical_from_zmax(form, zmax=0.25 * 200**0.5)
force.attributes["scale"] = scale

edges = list(form.edges_where(_is_edge=True))
print("supports:", len(supports))
print("largest angle deviation:", max(form.edges_attribute("_a", keys=edges)))
print("force diagram scale:", scale)
print("height range:", min(form.vertices_attribute("z")), max(form.vertices_attribute("z")))
print("force range:", min(form.edges_attribute("_f", keys=edges)), max(form.edges_attribute("_f", keys=edges)))

# thrust network in 3D, form diagram in plan (green), force diagram next to it (blue)
thrust = form.copy(cls=Mesh)
for face in list(form.faces_where(_is_loaded=False)):
    thrust.delete_face(face)
plan = thrust.copy()
plan.vertices_attribute("z", 0)
x, y = form.vertices_attribute("x"), form.vertices_attribute("y")
fx, fy = force.vertices_attribute("x"), force.vertices_attribute("y")
force.transform(Translation.from_vector([min(x) + 1.3 * (max(x) - min(x)) - min(fx), (min(y) + max(y) - min(fy) - max(fy)) / 2, 0]))
vertexcolor = {vertex: Color.from_hex("#d62828") for vertex in supports}

viewer = Viewer()
viewer.scene.add(thrust, show_points=True, vertexcolor=vertexcolor, pointsize=8)
viewer.scene.add(plan, show_faces=False, linecolor=Color.from_hex("#2e9e4a"))
viewer.scene.add(force, show_faces=False, linecolor=Color.from_hex("#2a6fdb"))
viewer.show()
```
