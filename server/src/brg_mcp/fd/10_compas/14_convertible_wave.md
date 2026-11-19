Convertible wave, fd_convertible_wave.py: the Wave with its middle anchors on rails, opened by pulling two corners to y = 13.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-advanced/line-constraints-convertible-wave

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Pointcloud
from compas_fd.constraints import Constraint
from compas_fd.solvers import fd_constrained_numpy
from compas_viewer import Viewer

# 1. open the example file: the Wave example, rebuilt here
mesh = Mesh.from_meshgrid(dx=10, nx=20)
index = mesh.vertex_index()
edges = list(mesh.edges())
anchors = [vertex for vertex in mesh.vertices() if mesh.vertex_attribute(vertex, "x") in (0, 10) and mesh.vertex_attribute(vertex, "y") in (0, 2.5, 5, 7.5, 10)]
for vertex in anchors:
    if mesh.vertex_attribute(vertex, "y") in (2.5, 7.5):
        mesh.vertex_attribute(vertex, "z", 2.644)
q = {(u, v): 10.0 if mesh.vertex_attribute(u, "y") == mesh.vertex_attribute(v, "y") and mesh.vertex_attribute(u, "y") in (0, 2.5, 5, 7.5, 10) else 1.0 for u, v in edges}

# 2. add line constraints: the anchors between the corners slide on a rail along Y,
#    so they only take reactions perpendicular to the rail
corners = [vertex for vertex in anchors if mesh.vertex_attribute(vertex, "y") in (0, 10)]
constraints = [None] * mesh.number_of_vertices()
for vertex in anchors:
    if vertex not in corners:
        x, y, z = mesh.vertex_attributes(vertex, "xyz")
        constraints[index[vertex]] = Constraint(Line([x, 0, z], [x, 10, z]))

# 3. open the convertible further: pull the two corners at y = 10 along the rails to y = 13
for vertex in corners:
    if mesh.vertex_attribute(vertex, "y") == 10:
        mesh.vertex_attribute(vertex, "y", 13)

result = fd_constrained_numpy(
    vertices=mesh.vertices_attributes("xyz"),
    fixed=[index[vertex] for vertex in anchors],
    edges=[(index[u], index[v]) for u, v in edges],
    forcedensities=[q[edge] for edge in edges],
    constraints=constraints,
    kmax=500,
)
print("sliding anchors, y:", [float(round(result.vertices[index[vertex], 1], 3)) for vertex in anchors if constraints[index[vertex]]])

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
for vertex in anchors:
    if constraints[index[vertex]]:
        viewer.scene.add(constraints[index[vertex]].geometry, linecolor=Color.cyan(), linewidth=3)
viewer.show()
```
