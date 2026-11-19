Lifted corner, fd_lifted_corner.py: the same net with one corner lifted to 7.

Source: https://github.com/BlockResearchGroup/compas_fd/blob/main/notebooks/00_basic.ipynb

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=10)
for vertex in mesh.vertices_where(x=10, y=10):
    mesh.vertex_attribute(vertex, "z", 7)

vertices = mesh.vertices_attributes("xyz")
fixed = list(mesh.vertices_where(vertex_degree=2))  # the four corners
edges = list(mesh.edges())
forcedensities = [10.0 if mesh.is_edge_on_boundary(edge) else 1.0 for edge in edges]

result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities)

for vertex in mesh.vertices():
    mesh.vertex_attributes(vertex, "xyz", result.vertices[vertex].tolist())

print("supports:", [vertices[vertex] for vertex in fixed])
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

viewer = Viewer()
viewer.scene.add(mesh, facecolor=Color.from_hex("#cccccc"), show_points=False)
for vertex in fixed:
    viewer.scene.add(mesh.vertex_point(vertex), pointcolor=Color.from_hex("#2a6fdb"), pointsize=14)
viewer.show()
```
