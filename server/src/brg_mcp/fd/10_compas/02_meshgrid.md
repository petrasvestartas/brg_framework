Mesh grid, fd_meshgrid.py: a flat net on four corners with stronger boundary cables, and the support reactions.

Source: https://github.com/BlockResearchGroup/compas_fd/blob/main/docs/examples/example_mesh_basic.py

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Force density: a flat 10 x 10 net on four corner supports, with ten times stronger boundary cables."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=10)

vertices = mesh.vertices_attributes("xyz")
fixed = list(mesh.vertices_where(vertex_degree=2))  # the four corners
edges = list(mesh.edges())
forcedensities = [10.0 if mesh.is_edge_on_boundary(edge) else 1.0 for edge in edges]

result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities)

for vertex in mesh.vertices():
    mesh.vertex_attributes(vertex, "xyz", result.vertices[vertex].tolist())

# no loads: the net stays flat, the boundary cables pull in between the corners
print("supports:", fixed)
print("middle of the bottom edge:", result.vertices[5])
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

viewer = Viewer()
viewer.scene.add(mesh, show_points=False)
for vertex in fixed:
    point = mesh.vertex_point(vertex)
    reaction = -result.residuals[vertex] * 0.1  # the support reaction, scaled
    viewer.scene.add(point, pointcolor=Color.from_hex("#2a6fdb"), pointsize=14)
    viewer.scene.add(Line(point, point + reaction), linecolor=Color.from_hex("#2e9e4a"), linewidth=3)
viewer.show()
```
