Hypar membrane, fd_hypar_membrane.py: a four point sail with two raised corners and stronger edge cables.

Adapted from the COMPAS FormFinder hypar example, PDF pages 38 to 46: https://github.com/BlockResearchGroup/compas-FoFin/blob/main/gitbook/examples-basic/tensile-form-active/mechanically-prestressed/hypar.md

Historical precedent: Frei Otto's mechanically prestressed membrane at Bundesgartenschau Kassel, 1955; see `04_references.md`.

Tested with `compas 2.15.1`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Hypar membrane: opposite high supports and boundary cables with q = 5."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=10)
fixed = list(mesh.vertices_where(vertex_degree=2))

for vertex in fixed:
    x, y, _ = mesh.vertex_attributes(vertex, "xyz")
    if x == y:
        mesh.vertex_attribute(vertex, "z", 2.0)

vertices = mesh.vertices_attributes("xyz")
edges = list(mesh.edges())
forcedensities = [5.0 if mesh.is_edge_on_boundary(edge) else 1.0 for edge in edges]

result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities)

print("supports:", [(vertex, vertices[vertex]) for vertex in fixed])
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

for vertex, xyz in zip(mesh.vertices(), result.vertices.tolist()):
    mesh.vertex_attributes(vertex, "xyz", xyz)

viewer = Viewer()
viewer.scene.add(
    mesh,
    show_points=True,
    vertexcolor={vertex: Color.from_hex("#2a6fdb") for vertex in fixed},
    linecolor={edge: Color.from_hex("#d62828") for edge in edges if mesh.is_edge_on_boundary(edge)},
    pointsize=10,
)
viewer.show()
```
