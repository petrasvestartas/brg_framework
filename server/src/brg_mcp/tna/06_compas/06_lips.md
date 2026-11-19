Lips, tna_lips.py: bounds on the force edge lengths move the largest forces from the open edges to the next line of edges, the open edges fold up into lips.

Adapted from the RhinoVAULT example Lips: https://blockresearchgroup.gitbook.io/rhinovault/examples/basic-design/lips

Precedent: the shells of Heinz Isler, whose free edges are stiffened by lips.

The pattern of the Rhino file is rebuilt from six patches; its vertices are within 0.06 of the original. Largest angle deviation 0.77 degrees and scale 0.861, in the session file of the manual 0.86 degrees and 0.898.

The three middle edges that leave every support arch also get the bounds 1 to 3, as in the session file; without them these force edges flip.

Tested with `compas 2.16.0`, `compas_tna 0.9.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Thrust network analysis: lips, a three legged vault whose open edges fold up into stiffening lips."""

from math import cos
from math import radians
from math import sin

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Translation
from compas.itertools import pairwise
from compas_tna.diagrams import ForceDiagram
from compas_tna.diagrams import FormDiagram
from compas_tna.equilibrium import horizontal_nodal
from compas_tna.equilibrium import relax_boundary_openings
from compas_tna.equilibrium import vertical_from_zmax
from compas_viewer import Viewer


def polar(radius, angle):
    return Point(radius * cos(radians(angle)), radius * sin(radians(angle)), 0)


def patch(a, b, c, d, nu, nv):
    """Quads of a nu x nv grid between four corners."""

    def point(u, v):
        return a * ((1 - u) * (1 - v)) + b * (u * (1 - v)) + c * (u * v) + d * ((1 - u) * v)

    return [[point(i / nu, j / nv), point((i + 1) / nu, j / nv), point((i + 1) / nu, (j + 1) / nv), point(i / nu, (j + 1) / nv)] for i in range(nu) for j in range(nv)]


# 1. pattern: three legs at 90, 210 and 330 degrees, each leg two patches of 4 x 3 quads around the centre
legs = [90, 210, 330]
polygons = []
for leg in legs:
    for side in (1, -1):
        quads = patch(polar(0, 0), polar(4.242, leg), polar(5.22, leg + side * 16.7), polar(2.765, leg + side * 60), 4, 3)
        polygons += quads if side == 1 else [quad[::-1] for quad in quads]
form = FormDiagram.from_mesh(Mesh.from_polygons(polygons, precision=6))

# 2. supports: the seven vertices at the end of every leg, moved onto an arch of radius 1.863
supports = []
for leg in legs:
    centre = polar(4.242 + 1.863, leg)
    for vertex in form.vertices_on_boundary():
        point = form.vertex_point(vertex)
        if vertex not in supports and point.distance_to_point(polar(5, leg)) < 1.6:
            form.vertex_attributes(vertex, "xyz", centre + (point - centre).unitized() * 1.863)
            supports.append(vertex)
form.vertices_attribute("is_support", True, keys=supports)

# the open edges between the legs curve inwards with a sag of 14.5 % of their span
targets = [0.145] * 3
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

# 5. horizontal equilibrium: the largest forces flow along the open edges
horizontal_nodal(form, force, kmax=1000)

# 6. modify the force diagram: bound the length of force edges, which is the horizontal force in the form edge
for u, v in form.edges_where(_is_edge=True):
    inside, outside = form.halfedge[u][v], form.halfedge[v][u]
    if form.face_attribute(inside, "_is_loaded"):
        inside, outside = outside, inside
        u, v = v, u
    if form.face_attribute(inside, "_is_loaded"):
        continue  # not an edge of an opening
    # small forces in the open edge
    force.edge_attributes((inside, outside), ["lmin", "lmax"], [1, 3])
    # large forces in the edge on the other side of the quad: the lip
    vertices = form.face_vertices(outside)
    i = vertices.index(u)
    a, b = vertices[i - 2], vertices[i - 3]
    force.edge_attributes((form.halfedge[a][b], form.halfedge[b][a]), ["lmin", "lmax"], [10, 15])
# small forces also in the other edges that leave the supports, so they do not collapse
for u, v in form.edges_where(_is_edge=True):
    edge = form.halfedge[u][v], form.halfedge[v][u]
    if (u in supports or v in supports) and force.edge_attribute(edge, "lmin") == 0:
        force.edge_attributes(edge, ["lmin", "lmax"], [1, 3])

# 7. horizontal equilibrium again: the forces move from the open edges to the lips
horizontal_nodal(form, force, kmax=1000)

# 8. vertical equilibrium: ask for a quarter of the diagonal of the plan; with the steep lips the solver ends lower
x, y = form.vertices_attribute("x"), form.vertices_attribute("y")
form, scale = vertical_from_zmax(form, zmax=0.25 * ((max(x) - min(x)) ** 2 + (max(y) - min(y)) ** 2) ** 0.5)
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
