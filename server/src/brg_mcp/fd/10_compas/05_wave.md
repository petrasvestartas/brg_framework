Ridge and valley wave, fd_wave.py: alternating high and low anchors with integrated ridge and valley cables.

Adapted from the COMPAS FormFinder wave example, PDF pages 64 to 70: https://github.com/BlockResearchGroup/compas-FoFin/blob/main/gitbook/examples-basic/tensile-form-active/mechanically-prestressed/wave.md

Historical precedent: convertible membrane roofing at Metzgergasse, Buchs; see `04_references.md`.

Tested with `compas 2.15.1`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Ridge and valley wave: five cables with q = 10 span between alternating anchors."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

mesh = Mesh.from_meshgrid(dx=10, nx=20)
support_y = {0, 2.5, 5, 7.5, 10}
fixed = [
    vertex
    for vertex in mesh.vertices_on_boundary()
    if mesh.vertex_attribute(vertex, "x") in {0, 10} and mesh.vertex_attribute(vertex, "y") in support_y
]

for vertex in fixed:
    if mesh.vertex_attribute(vertex, "y") in {2.5, 7.5}:
        mesh.vertex_attribute(vertex, "z", 2.5)

vertices = mesh.vertices_attributes("xyz")
edges = list(mesh.edges())
cables = {
    (u, v)
    for u, v in edges
    if mesh.vertex_attribute(u, "y") == mesh.vertex_attribute(v, "y") and mesh.vertex_attribute(u, "y") in support_y
}
forcedensities = [10.0 if edge in cables else 1.0 for edge in edges]

result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities)

print("alternating anchors:", result.vertices[fixed])
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

for vertex, xyz in zip(mesh.vertices(), result.vertices.tolist()):
    mesh.vertex_attributes(vertex, "xyz", xyz)

viewer = Viewer()
viewer.scene.add(
    mesh,
    show_points=True,
    vertexcolor={vertex: Color.from_hex("#2a6fdb") for vertex in fixed},
    linecolor={edge: Color.from_hex("#d62828") for edge in cables},
    pointsize=8,
)
viewer.show()
```
