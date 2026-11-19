Pillow vault, tna_pillow_vault.py: a circular plan with all boundary vertices supported, the simplest case: no openings and no constraints.

Adapted from the RhinoVAULT example Pillow Vault: https://blockresearchgroup.gitbook.io/rhinovault/examples/historical-typologies/pillow-vault

The pattern of the Rhino file is rebuilt with the same topology: a 6 by 6 grid with two rings of 24 quads. With the default height of 3.536 the scale is 2.153, in the session file of the manual 2.166.

Tested with `compas 2.16.0`, `compas_tna 0.9.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Thrust network analysis: a pillow vault, a circular plan with every boundary vertex supported."""

from math import cos
from math import radians
from math import sin

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_tna.diagrams import ForceDiagram
from compas_tna.diagrams import FormDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_tna.equilibrium import relax_boundary_openings
from compas_tna.equilibrium import vertical_from_zmax
from compas_viewer import Viewer

# 1. pattern: a 6 x 6 grid in the middle, with two rings of 24 quads around it, on a circle of radius 5
mesh = Mesh.from_meshgrid(dx=6, nx=6)
loop = mesh.vertices_on_boundary()[:-1]  # 24 vertices, clockwise from the corner at 225 degrees
for radius in (4, 5):
    ring = [mesh.add_vertex(x=3 + radius * cos(radians(225 - 15 * i)), y=3 + radius * sin(radians(225 - 15 * i)), z=0) for i in range(24)]
    for i in range(24):
        mesh.add_face([loop[i - 1], loop[i], ring[i], ring[i - 1]])
    loop = ring
form = FormDiagram.from_mesh(mesh)

# 2. supports: all vertices of the boundary circle
supports = loop
form.vertices_attribute("is_support", True, keys=supports)
relax_boundary_openings(form, supports)  # smooth the pattern inside the circle with force densities

# 3. form diagram: no openings, so no unloaded faces
form.update_boundaries()

# 4. force diagram: the dual of the form diagram
force = ForceDiagram.from_formdiagram(form)

# 5. horizontal equilibrium: the force edges turn until they are perpendicular to the form edges
horizontal_nodal(form, force, kmax=100)

# 6. vertical equilibrium: the highest node is at 2
form, scale = vertical_from_zmax(form, zmax=2)
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
