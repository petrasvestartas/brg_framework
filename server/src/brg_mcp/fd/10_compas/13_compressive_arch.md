Compressive arch supported, fd_compressive_arch.py: a cable net in tension hanging from an arch in compression.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/mixed-form-active/compressive-arch-supported

The arch is smooth only for q below about -5.1; here q = -5.5 gives an arch of 2.9 over a span of 10.

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""FormFinder Compressive Arch Supported: a cable net in tension carried by an internal arch in compression."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Pointcloud
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

# 1. create a mesh grid: 10 x 10 faces over 10 x 10
mesh = Mesh.from_meshgrid(dx=10, nx=10)
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


# 2. identify anchors: the corners and the middle of every side
anchors = [
    vertex
    for vertex in mesh.vertices()
    if mesh.is_vertex_on_boundary(vertex) and mesh.vertex_attribute(vertex, "x") in (0, 5, 10) and mesh.vertex_attribute(vertex, "y") in (0, 5, 10)
]

# 3. force density method: a flat net
result = solve()

# 4. move nodes: the corners slightly down in Z
for vertex in anchors:
    if mesh.vertex_degree(vertex) == 2:
        mesh.vertex_attribute(vertex, "z", -1.0)
result = solve()

# 5. scale force densities: the middle edge loop from (5, 0) to (5, 10) into compression.
#    Compressive elements are very sensitive to q: between about -0.4 and -5.1 the arch buckles into waves,
#    below -5.1 it is a smooth arch, and the closer q is to -5.1, the higher the arch
arch = [(u, v) for u, v in edges if mesh.vertex_attribute(u, "x") == mesh.vertex_attribute(v, "x") == 5]
for edge in arch:
    q[edge] = -5.5

# the net shapes over a compressive arch
result = solve()
print("top of the arch:", max(result.vertices[index[u], 2] for u, _ in arch))

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
