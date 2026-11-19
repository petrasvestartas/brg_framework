Conical, fd_conical.py: a mast in the centre, a light eye, and edge cables between eight anchors.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-basic/tensile-form-active/mechanically-prestressed/conical

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
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


# 2. identify anchors: the boundary and the node in the centre
centre = next(mesh.vertices_where(x=5, y=5))
anchors = [vertex for vertex in mesh.vertices() if mesh.is_vertex_on_boundary(vertex)] + [centre]

# 3. move nodes: the centre up in Z
mesh.vertex_attribute(centre, "z", 6.0)

# 4. force density method: a cone with a sharp tip
result = solve()
print("step 4, highest free node:", max(result.vertices[vertex, 2] for vertex in mesh.vertices() if vertex not in anchors))

# 5. remove edges: the two edges from the centre in Y and the four faces around the centre
#    open the light eye; the two edges in X stay and carry the eye from the mast
eye = [(centre, next(mesh.vertices_where(x=5, y=y))) for y in (4, 6)]
for face in list(mesh.vertex_faces(centre)):
    mesh.delete_face(face)
bars = [(centre, next(mesh.vertices_where(x=x, y=5))) for x in (4, 6)]
edges = list(mesh.edges()) + bars
q = {edge: 1.0 for edge in edges}
print("removed edges:", eye)

# 6. force density method: the smooth light eye
result = solve()

# 7. scale force densities: all boundaries, the outer edge and the edge of the eye, q x 5
for edge in mesh.edges():
    if mesh.is_edge_on_boundary(edge):
        q[edge] *= 5

# 8. force density method: with q = 5 on the boundaries the eye becomes small
result = solve()

# 9. identify anchors: unselect the outer boundary except the corners and the middle of every side
anchors = [vertex for vertex in anchors if vertex == centre or mesh.vertex_attribute(vertex, "x") in (0, 5, 10) and mesh.vertex_attribute(vertex, "y") in (0, 5, 10)]

# 10. force density method: the edge cables curve in between the anchors
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
for u, v in bars:  # the two edges that hang the eye from the mast, not part of any face
    viewer.scene.add(Line(mesh.vertex_point(u), mesh.vertex_point(v)), linecolor=Color.from_hex("#d62828"), linewidth=4)
viewer.show()
```
