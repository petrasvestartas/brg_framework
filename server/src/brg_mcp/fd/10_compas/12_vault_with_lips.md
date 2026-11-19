Vault with lips, fd_vault_with_lips.py: a compression vault on four corners, q = -3 on the lips and the edges.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/compressive-form-active/vault-with-lips

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
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

# 3. force density method: all edges in tension, the net stays flat
result = solve()

# 4. scale force densities: all edges x -1, now in compression
for edge in edges:
    q[edge] *= -1

# 5. force density method: still flat, there is no load
result = solve()

# 6. load: pz = -0.1 on every node
mesh.vertices_attribute("pz", -0.1)

# 7. force density method: a compression vault
result = solve()
print("step 7, height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())

# 8. scale force densities: q = -3 on the edge loops of the lips, one row in from each side,
#    and on the boundary edges between the anchors
for u, v in edges:
    (xu, yu, _), (xv, yv, _) = mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)
    if (xu == xv and xu in (0, 1, 9, 10)) or (yu == yv and yu in (0, 1, 9, 10)):
        q[(u, v)] = -3.0

# 9. force density method: the vault with lips
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
