Selfweight, fd_selfweight.py: the load of every node from its tributary area, and the net hanging under it.

Source: https://github.com/BlockResearchGroup/compas_fd/blob/main/tests/test_selfweight.py

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Selfweight: the load of every node of a 10 x 10 grid from its tributary area, then the net hanging under it."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas_fd.loads import SelfweightCalculator
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=10)  # 10 by 10 faces of 1 by 1
mesh.update_default_vertex_attributes(t=1.0)  # thickness

calculator = SelfweightCalculator(mesh, density=1)
selfweight = calculator(mesh.vertices_attributes("xyz"))

# a corner node carries 1/4 of a face, an edge node 1/2, an inner node 1
for vertex in [0, 1, 12]:
    print("node", vertex, "degree", mesh.vertex_degree(vertex), "selfweight", selfweight[vertex, 0])
print("total:", selfweight.sum())  # 10 x 10 x thickness x density = 100

# hang the net from its boundary under this selfweight
vertices = mesh.vertices_attributes("xyz")
fixed = list(mesh.vertices_on_boundary())
edges = list(mesh.edges())
loads = [[0, 0, -weight] for weight in selfweight[:, 0]]
result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=[10.0] * len(edges), loads=loads)

for vertex in mesh.vertices():
    mesh.vertex_attributes(vertex, "xyz", result.vertices[vertex].tolist())

print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())

viewer = Viewer()
viewer.scene.add(mesh, show_points=False)
for vertex in fixed:
    viewer.scene.add(mesh.vertex_point(vertex), pointcolor=Color.from_hex("#2a6fdb"), pointsize=8)
viewer.show()
```
