Curve constrained net, fd_curve_constraints.py: four curved boundaries carry sliding supports while only the corners remain permanently fixed.

Adapted from the COMPAS FormFinder curve constraints example, PDF pages 127 to 133: https://github.com/BlockResearchGroup/compas-FoFin/blob/main/gitbook/examples-advanced/curve-constraints-geometry-generation.md

Historical precedent: cable net and fabric formed thin shell by BRG and Escobedo Construction, Buda, Texas, 2014; see `04_references.md`.

The small Bezier subclass adds closest point projection with SciPy, so this example needs only `compas_fd` and `compas_viewer`.

Tested with `compas 2.15.1`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
"""Curve constrained net: quadratic Bezier boundaries with sliding supports."""

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Bezier
from compas.geometry import Polyline
from compas_fd.constraints import Constraint
from compas_fd.constraints import CurveConstraint
from compas_fd.solvers import fd_constrained_numpy
from compas_viewer import Viewer
from scipy.optimize import minimize_scalar


class ProjectedBezier(Bezier):
    def closest_point(self, point, return_parameter=False):
        result = minimize_scalar(lambda t: self.point_at(t).distance_to_point(point), bounds=(0, 1), method="bounded")
        xyz = self.point_at(result.x)
        return (xyz, result.x) if return_parameter else xyz


Constraint.register(ProjectedBezier, CurveConstraint)

mesh = Mesh.from_meshgrid(dx=10, nx=9, dy=10, ny=19)
curves = [
    ProjectedBezier([[0, 0, 0], [5, 0, 6], [10, 0, 0]]),
    ProjectedBezier([[0, 10, 0], [5, 10, 4], [10, 10, 0]]),
    ProjectedBezier([[0, 0, 0], [0, 5, 2], [0, 10, 0]]),
    ProjectedBezier([[10, 0, 0], [10, 5, 8], [10, 10, 0]]),
]


def curve_for(vertex):
    x, y, _ = mesh.vertex_attributes(vertex, "xyz")
    if y == 0:
        return curves[0]
    if y == 10:
        return curves[1]
    if x == 0:
        return curves[2]
    if x == 10:
        return curves[3]


corners = set(mesh.vertices_where(vertex_degree=2))
fixed = list(mesh.vertices_on_boundary())
constraints = [None] * mesh.number_of_vertices()
for vertex in fixed:
    if vertex not in corners:
        curve = curve_for(vertex)
        xyz = curve.closest_point(mesh.vertex_attributes(vertex, "xyz"))
        mesh.vertex_attributes(vertex, "xyz", xyz)
        constraints[vertex] = Constraint(curve)

vertices = mesh.vertices_attributes("xyz")
edges = list(mesh.edges())
result = fd_constrained_numpy(
    vertices=vertices,
    fixed=fixed,
    edges=edges,
    forcedensities=[1.0] * len(edges),
    constraints=constraints,
    kmax=200,
)

print("curve constrained supports:", sum(constraint is not None for constraint in constraints))
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

for vertex, xyz in zip(mesh.vertices(), result.vertices.tolist()):
    mesh.vertex_attributes(vertex, "xyz", xyz)

vertexcolor = {vertex: Color.from_hex("#2a6fdb" if vertex in corners else "#d62828") for vertex in fixed}

viewer = Viewer()
viewer.scene.add(mesh, show_points=True, vertexcolor=vertexcolor, pointsize=8)
for curve in curves:
    viewer.scene.add(Polyline([curve.point_at(i / 32) for i in range(33)]), linecolor=Color.from_hex("#2a6fdb"), linewidth=3)
viewer.show()
```
