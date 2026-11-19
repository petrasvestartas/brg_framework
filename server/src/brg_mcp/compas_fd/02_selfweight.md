Selfweight, fd_selfweight.py: the selfweight of every node of a grid, from its tributary area.

Source: https://github.com/BlockResearchGroup/compas_fd/blob/main/tests/test_selfweight.py

Tested with `compas 2.15.1`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Selfweight: the load of every node of a 10 x 10 grid, from its tributary area."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas_fd.loads import SelfweightCalculator
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=10)  # 10 by 10 faces of 1 by 1
mesh.update_default_vertex_attributes(t=1.0)  # thickness

density = 1
calculator = SelfweightCalculator(mesh, density=density)
selfweight = calculator(mesh.vertices_attributes("xyz"))

# a corner node carries 1/4 of a face, an edge node 1/2, an inner node 1
for vertex in [0, 1, 12]:
    print("node", vertex, "degree", mesh.vertex_degree(vertex), "selfweight", selfweight[vertex, 0])
print("total:", selfweight.sum())  # 10 x 10 x thickness x density = 100

viewer = Viewer()
viewer.scene.add(mesh, show_points=True, pointsize=8)
load_color = Color.from_hex("#2e9e4a")
for vertex in mesh.vertices():
    x, y, z = mesh.vertex_coordinates(vertex)
    viewer.scene.add(Line([x, y, z], [x, y, z - float(selfweight[vertex, 0])]), linecolor=load_color, linewidth=3)
viewer.show()
```
