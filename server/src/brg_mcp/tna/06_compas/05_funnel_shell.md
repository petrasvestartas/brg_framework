Funnel shell, tna_funnel_shell.py: inner and outer ring are supported, then the outer supports are lifted to a height of 3 and vertical equilibrium is solved again.

Adapted from the RhinoVAULT example Funnel Shell: https://blockresearchgroup.gitbook.io/rhinovault/examples/basic-design/barrel-vault-3

The manual page is marked as in progress: it lists the commands, its Rhino file and figures are missing. The pattern here is the ring of the Holes example.

Tested with `compas 2.16.0`, `compas_tna 0.9.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from math import cos
from math import radians
from math import sin

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_tna.diagrams import ForceDiagram
from compas_tna.diagrams import FormDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_tna.equilibrium import vertical_from_zmax
from compas_viewer import Viewer

# 1. pattern: 5 rings of 22 quads between an inner circle and an outer circle
n, rings = 22, 5
vertices = []
for j in range(rings + 1):
    radius = 1.32 + j * (4.735 - 1.32) / rings
    for i in range(n):
        angle = radians(-90 + i * 360 / n)
        vertices.append([radius * cos(angle), radius * sin(angle), 0])
faces = [[j * n + i, (j + 1) * n + i, (j + 1) * n + (i + 1) % n, j * n + (i + 1) % n] for j in range(rings) for i in range(n)]
form = FormDiagram.from_mesh(Mesh.from_vertices_and_faces(vertices, faces))

# 2. supports: all vertices of the inner and of the outer boundary
inner = list(range(n))
outer = list(range(rings * n, (rings + 1) * n))
supports = inner + outer
form.vertices_attribute("is_support", True, keys=supports)

# 3. form diagram
form.update_boundaries()

# 4. force diagram: the dual of the form diagram
force = ForceDiagram.from_formdiagram(form)

# 5. horizontal equilibrium: the force edges turn until they are perpendicular to the form edges
horizontal_nodal(form, force, kmax=1000)

# 6. vertical equilibrium: with all supports on the ground the result is a ring shaped vault
form, scale = vertical_from_zmax(form, zmax=1.5)
print("height range with all supports on the ground:", min(form.vertices_attribute("z")), max(form.vertices_attribute("z")))

# 7. modify the thrust diagram: lift the supports of the outer boundary to a height of 3
form.vertices_attribute("z", 3, keys=outer)

# 8. vertical equilibrium again: the vault now rises from the inner ring to the outer ring
form, scale = vertical_from_zmax(form, zmax=3.5)
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
