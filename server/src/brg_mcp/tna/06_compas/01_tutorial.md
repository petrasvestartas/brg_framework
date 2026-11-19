Tutorial vault, tna_tutorial.py: a 10 by 10 grid on four corner supports with open, curved boundaries, the quick start of RhinoVAULT.

Adapted from the RhinoVAULT tutorial: https://blockresearchgroup.gitbook.io/rhinovault/introduction/tutorial

The four boundaries get sags of 10, 40, 20 and 30 % as in the figure of step 2c; the manual does not give the values of the other three, only `Sag_40`.

With 300 iterations the largest angle deviation is 3.4 degrees, below the 5 degrees that RhinoVAULT accepts.

Tested with `compas 2.16.0`, `compas_tna 0.9.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Thrust network analysis: the RhinoVAULT tutorial, a vault on four corner supports with open boundaries."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Translation
from compas.itertools import pairwise
from compas_tna.diagrams import ForceDiagram
from compas_tna.diagrams import FormDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_tna.equilibrium import relax_boundary_openings
from compas_tna.equilibrium import vertical_from_zmax
from compas_viewer import Viewer

# 1. pattern: a 10 x 10 grid of quads
form = FormDiagram.from_mesh(Mesh.from_meshgrid(dx=10, nx=10))

# 2a. supports: the vertices with two edges, the four corners
supports = list(form.vertices_where(vertex_degree=2))
form.vertices_attribute("is_support", True, keys=supports)

# 2b, 2c. relax the pattern with force densities, then give every opening its own sag (rise over span)
targets = [0.1, 0.4, 0.2, 0.3]
boundary = form.vertices_on_boundary()
start = boundary.index(supports[0])
boundary = boundary[start:-1] + boundary[: start + 1]
ends = [i for i, vertex in enumerate(boundary) if vertex in supports]
openings = [boundary[i : j + 1] for i, j in pairwise(ends) if j - i > 1]


def sag(opening):
    span = Line(form.vertex_point(opening[0]), form.vertex_point(opening[-1]))
    return max(form.vertex_point(vertex).distance_to_line(span) for vertex in opening[1:-1]) / span.length


relax_boundary_openings(form, supports)
for _ in range(10):
    sags = [sag(opening) for opening in openings]
    if all(abs(value - target) < 0.01 for value, target in zip(sags, targets)):
        break
    for value, target, opening in zip(sags, targets, openings):
        for edge in pairwise(opening):
            form.edge_attribute(edge, "q", form.edge_attribute(edge, "q") * value / target)
    relax_boundary_openings(form, supports)

# 3. form diagram: the plan of the vault, with one unloaded face per opening
form.vertices_attribute("z", 0)
form.update_boundaries()

# 4. force diagram: the dual of the form diagram
force = ForceDiagram.from_formdiagram(form)

# 5. horizontal equilibrium: the force edges turn until they are perpendicular to the form edges
horizontal_nodal(form, force, kmax=300)

# 6. vertical equilibrium: the highest node is at a quarter of the diagonal of the plan
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
