Arch supported, fd_arch_supported.py: half a cylinder between two anchored arches, with edge cables along the free edges.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/tensile-form-active/mechanically-prestressed/arch-supported

The manual scales the edges interactively; here the edges along the length get q x 0.5 and the free edges q x 5.

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""FormFinder Arch Supported: half a cylinder between two anchored arches, with edge cables along the free edges."""

from math import cos
from math import pi
from math import sin

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Pointcloud
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

# 1. create a cable mesh from a cylinder: radius 5, length 10, 16 faces along the perimeter and 4 along the length;
#    the cylinder lies along Y, so that its two boundary circles stand up as arches
perimeter, length = 16, 4
vertices = [[5 * cos(2 * pi * j / perimeter), 10 * i / length, 5 * sin(2 * pi * j / perimeter)] for i in range(length + 1) for j in range(perimeter)]
faces = [
    [i * perimeter + j, i * perimeter + (j + 1) % perimeter, (i + 1) * perimeter + (j + 1) % perimeter, (i + 1) * perimeter + j] for i in range(length) for j in range(perimeter)
]
mesh = Mesh.from_vertices_and_faces(vertices, faces)
mesh.update_default_vertex_attributes(px=0.0, py=0.0, pz=0.0)
index = mesh.vertex_index()
edges = list(mesh.edges())
q = {edge: 1.0 for edge in edges}


def solve():
    """Force density method: the equilibrium of the current anchors, force densities and loads."""
    return fd_numpy(
        vertices=mesh.vertices_attributes("xyz"),
        fixed=[index[vertex] for vertex in anchors],
        edges=[(index[u], index[v]) for u, v in edges],
        forcedensities=[q[edge] for edge in edges],
        loads=[mesh.vertex_attributes(vertex, ["px", "py", "pz"]) for vertex in mesh.vertices()],
    )


# 2. identify anchors: the two boundary circles
anchors = [vertex for vertex in mesh.vertices() if mesh.is_vertex_on_boundary(vertex)]

# 3. force density method: a closed, narrow waisted cylinder
result = solve()
print("step 3, waist radius:", (result.vertices[index[2 * perimeter], 0] ** 2 + result.vertices[index[2 * perimeter], 2] ** 2) ** 0.5)

# 4. scale force densities: the edges along the length x 0.5, the cylinder becomes more narrow waisted
along = [(u, v) for u, v in edges if mesh.vertex_attribute(u, "y") != mesh.vertex_attribute(v, "y")]
for edge in along:
    q[edge] *= 0.5
result = solve()
print("step 4, waist radius:", (result.vertices[index[2 * perimeter], 0] ** 2 + result.vertices[index[2 * perimeter], 2] ** 2) ** 0.5)

# 5. delete edges: the lower half of the cylinder, with its faces and nodes
for face in list(mesh.faces()):
    if mesh.face_centroid(face)[2] < 0:
        mesh.delete_face(face)
mesh.remove_unused_vertices()
index = mesh.vertex_index()
edges = list(mesh.edges())
q = {edge: 0.5 if edge in along or edge[::-1] in along else 1.0 for edge in edges}
anchors = [vertex for vertex in mesh.vertices() if mesh.vertex_attribute(vertex, "y") in (0, 10)]

# 6. scale force densities: the two free edges along the length become edge cables, q x 5
for u, v in edges:
    if mesh.is_edge_on_boundary((u, v)) and mesh.vertex_attribute(u, "y") != mesh.vertex_attribute(v, "y"):
        q[(u, v)] *= 5

result = solve()

print("anchors:", len(anchors))
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

# show the result: tension red, compression blue, anchors black
for vertex in mesh.vertices():
    mesh.vertex_attributes(vertex, "xyz", result.vertices[index[vertex]].tolist())
edgecolor = {edge: Color.from_hex("#d62828" if force > 0 else "#2a6fdb") for edge, force in zip(edges, result.forces.ravel())}

viewer = Viewer()
viewer.scene.add(mesh, show_points=False, edgecolor=edgecolor, facecolor=Color.from_hex("#eeeeee"), linewidth=2)
viewer.scene.add(Pointcloud([mesh.vertex_point(vertex) for vertex in anchors]), pointcolor=Color.black(), pointsize=10)
viewer.show()
```
