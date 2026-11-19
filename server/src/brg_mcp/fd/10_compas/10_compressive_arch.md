Compressive arch supported net, fd_compressive_arch.py: a negative middle loop supports a net otherwise in tension.

Adapted from the COMPAS FormFinder mixed form active example, PDF pages 114 to 121: https://github.com/BlockResearchGroup/compas-FoFin/blob/main/gitbook/examples-basic/mixed-form-active/compressive-arch-supported.md

Historical precedent: Munich Ice Ring Roof by Ackermann und Partner and Schlaich Bergermann Partner, 1967; see `04_references.md`.

Tested with `compas 2.15.1`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Mixed form active net: an internal compressive arch between eight anchors."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=10)
corners = list(mesh.vertices_where(vertex_degree=2))
midpoints = [
    vertex
    for vertex in mesh.vertices_on_boundary()
    if (mesh.vertex_attribute(vertex, "x") == 5) != (mesh.vertex_attribute(vertex, "y") == 5)
]
fixed = corners + midpoints

for vertex in corners:
    mesh.vertex_attribute(vertex, "z", -1.0)

vertices = mesh.vertices_attributes("xyz")
edges = list(mesh.edges())
arch_edges = {(u, v) for u, v in edges if mesh.vertex_attribute(u, "y") == mesh.vertex_attribute(v, "y") == 5}
forcedensities = [-0.75 if edge in arch_edges else 1.0 for edge in edges]

result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities)

print("arch crown:", result.vertices[60])
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range: compression to tension:", result.forces.min(), result.forces.max())

for vertex, xyz in zip(mesh.vertices(), result.vertices.tolist()):
    mesh.vertex_attributes(vertex, "xyz", xyz)

viewer = Viewer()
viewer.scene.add(
    mesh,
    show_points=True,
    vertexcolor={vertex: Color.from_hex("#2a6fdb") for vertex in fixed},
    linecolor={edge: Color.from_hex("#2a6fdb") for edge in arch_edges},
    pointsize=10,
)
viewer.show()
```
