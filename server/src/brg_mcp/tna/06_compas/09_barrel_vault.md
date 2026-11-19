Barrel vault, tna_barrel_vault.py: parallel arches with equal thrust between two supported edges, the force diagram collapses to a line.

Adapted from the RhinoVAULT example Barrel Vault: https://blockresearchgroup.gitbook.io/rhinovault/examples/historical-typologies/barrel-vault

Checked against the session file of the manual (`examples_barrel_6.json`): the same force diagram scale, 2.0147687799773.

Tested with `compas 2.16.0`, `compas_tna 0.9.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_tna.diagrams import ForceDiagram
from compas_tna.diagrams import FormDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_tna.equilibrium import vertical_from_zmax
from compas_viewer import Viewer

# 1. pattern: a 10 x 10 grid of quads
form = FormDiagram.from_mesh(Mesh.from_meshgrid(dx=10, nx=10))

# 2. supports: all vertices of the bottom and top edges
supports = [vertex for vertex in form.vertices() if form.vertex_attribute(vertex, "y") in (0, 10)]
form.vertices_attribute("is_support", True, keys=supports)

# 3. form diagram: the two free edges become two unloaded faces
form.update_boundaries()

# 4. modify the form diagram: fix the horizontal force of every edge with hmin = hmax
for edge in form.edges_where(_is_edge=True):
    (x0, y0, _), (x1, y1, _) = form.edge_coordinates(edge)
    if y0 == y1:
        force = 1e-5  # across the arches: almost no force
    elif x0 in (0, 10):
        force = 1  # the two boundary arches carry half a strip
    else:
        force = 2  # the arches
    form.edge_attributes(edge, ["hmin", "hmax"], [force, force])

# 5. force diagram: the dual of the form diagram
force = ForceDiagram.from_formdiagram(form)

# 6. horizontal equilibrium: the force diagram collapses to one line, all arches have the same thrust
horizontal_nodal(form, force, kmax=1000)

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
