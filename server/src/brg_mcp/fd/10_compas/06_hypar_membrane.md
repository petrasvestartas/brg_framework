Hypar membrane, fd_hypar_membrane.py: two raised corners and boundary cables, q x 5.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/tensile-form-active/mechanically-prestressed/hypar

The manual does not give the height of the raised corners; here it is 5.

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""FormFinder Hypar: a four point sail with two raised corners and boundary cables."""

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


# 2. identify anchors: the corners
anchors = list(mesh.vertices_where(vertex_degree=2))

# 3. move nodes: two opposite corners up in Z
for vertex in anchors:
    if mesh.vertex_attribute(vertex, "x") == mesh.vertex_attribute(vertex, "y"):
        mesh.vertex_attribute(vertex, "z", 5.0)

# 4. force density method: the shape is still too soft along the free edges
result = solve()
print("step 4, middle of a free edge:", result.vertices[5])

# 5. scale force densities: the boundary edges become edge cables, q x 5
for edge in edges:
    if mesh.is_edge_on_boundary(edge):
        q[edge] *= 5

# 6. force density method: the hypar
result = solve()
print("step 6, middle of a free edge:", result.vertices[5])

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
