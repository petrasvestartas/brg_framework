Catenary arch with corrugations, fd_corrugated_arch.py: the hanging cables inverted into a barrel vault, every second cable q x 2.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/compressive-form-active/catenary-arch-with-corrugations

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Pointcloud
from compas_fd.loads import SelfweightCalculator
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

# the Catenary Cables example, steps 1 to 7

# 1. create a mesh grid: 10 x 10 faces over 10 x 10
mesh = Mesh.from_meshgrid(dx=10, nx=10)
index = mesh.vertex_index()
edges = list(mesh.edges())
q = {edge: 1.0 for edge in edges}


def solve(xyz=None, kmax=100):
    """Force density method under selfweight.

    The selfweight of a node is its tributary area times the thickness, so it changes with the shape:
    solve, update the loads on the new shape, and solve again until the nodes stop moving.
    With ``kmax=1`` the loads are computed once, on the shape ``xyz``.
    """
    selfweight = SelfweightCalculator(mesh, density=1.0)
    xyz = xyz or mesh.vertices_attributes("xyz")
    for _ in range(kmax):
        result = fd_numpy(
            vertices=xyz,
            fixed=anchors,
            edges=edges,
            forcedensities=[q[edge] for edge in edges],
            loads=[[0, 0, -weight] for weight in selfweight(xyz)[:, 0]],
        )
        step = abs(result.vertices - xyz).max()
        xyz = result.vertices.tolist()
        if step < 1e-6:
            break
    return result


# 2. identify anchors: the two opposite boundaries x = 0 and x = 10
anchors = [vertex for vertex in mesh.vertices() if mesh.vertex_attribute(vertex, "x") in (0, 10)]

# 3. edge attributes: q = 0.0001 in the edges across the cables (along Y), it cannot be 0
cables = [(u, v) for u, v in edges if mesh.vertex_attribute(u, "y") == mesh.vertex_attribute(v, "y")]
for edge in edges:
    if edge not in cables:
        q[edge] = 0.0001

# 4. force density method: no load yet, the cables stay straight

# 5. vertex attributes: thickness 0.1 on all nodes, the selfweight follows from the tributary area
mesh.update_default_vertex_attributes(t=0.1)

# 6. scale force densities: the two boundary cables carry half a strip, q x 0.5
for u, v in cables:
    if mesh.vertex_attribute(u, "y") in (0, 10):
        q[(u, v)] *= 0.5

# 7. scale force densities: all cables between the supports x 0.35, until the target sag
for edge in cables:
    q[edge] *= 0.35

result = solve()
print("hanging cables, lowest node:", result.vertices[:, 2].min())

# Catenary Arch, 2. scale force densities: the cables x -1, from tension into compression
for edge in cables:
    q[edge] *= -1
result = solve()
print("barrel vault, highest node:", result.vertices[:, 2].max())

# 3. scale force densities: every second cable x 2; cables with more force rise less, the others more.
#    The selfweight is computed once, on the barrel vault: recomputed on the corrugated shape it grows
#    with the steep faces between the cables and the solution runs away
for u, v in cables:
    if mesh.vertex_attribute(u, "y") in (1, 3, 5, 7, 9):
        q[(u, v)] *= 2

result = solve(result.vertices.tolist(), kmax=1)
print("crowns of the cables, y = 0 to 10:", [float(round(result.vertices[vertex, 2], 2)) for vertex in mesh.vertices_where(x=5)])

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
