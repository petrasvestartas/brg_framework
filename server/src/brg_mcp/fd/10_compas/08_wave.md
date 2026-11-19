Wave, fd_wave.py: ridge and valley cables between ten anchors.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/tensile-form-active/mechanically-prestressed/wave

Same nodes as the session file `Wave.json` of the manual, to 1e-14.

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Pointcloud
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

# 1. create a mesh grid: 20 x 20 faces over 10 x 10, for more design freedom
mesh = Mesh.from_meshgrid(dx=10, nx=20)
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


# 2. identify anchors: five nodes with equal spacing on the two sides x = 0 and x = 10
anchors = [
    vertex
    for vertex in mesh.vertices()
    if mesh.is_vertex_on_boundary(vertex) and mesh.vertex_attribute(vertex, "x") in (0, 10) and mesh.vertex_attribute(vertex, "y") in (0, 2.5, 5, 7.5, 10)
]

# 3. move nodes: every second anchor up in Z, the height of the FormFinder session file
for vertex in anchors:
    if mesh.vertex_attribute(vertex, "y") in (2.5, 7.5):
        mesh.vertex_attribute(vertex, "z", 2.644)

# 4. force density method: no clear ridges and valleys yet
result = solve()

# 5. scale force densities: the five edge loops between opposite anchors become ridge and valley cables, q x 10
for u, v in edges:
    y = mesh.vertex_attribute(u, "y")
    if y == mesh.vertex_attribute(v, "y") and y in (0, 2.5, 5, 7.5, 10):
        q[(u, v)] *= 10

# 6. force density method: the ridge and valley wave
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
