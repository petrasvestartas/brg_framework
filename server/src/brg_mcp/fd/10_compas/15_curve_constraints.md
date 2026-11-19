Curve constraints, fd_curve_constraints.py: the boundary slides on the four curves of the Buda, Texas shell.

Source: https://blockresearchgroup.gitbook.io/compas-fofin/examples-advanced/curve-constraints-geometry-generation

The curves are the control points and knots of `texas_boundary_r7.3dm`.

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Polyline
from compas.geometry import Vector
from compas_fd.constraints import Constraint
from compas_fd.constraints import CurveConstraint
from compas_fd.solvers import fd_constrained_numpy
from compas_viewer import Viewer
from scipy.interpolate import BSpline
from scipy.optimize import minimize_scalar


class Spline:
    """A cubic B spline from Rhino control points and knots, usable as a compas_fd curve constraint without a NURBS plugin."""

    def __init__(self, points, knots, degree=3):
        self.spline = BSpline(knots, points, degree)
        self.domain = knots[0], knots[-1]

    def point_at(self, t):
        return Point(*self.spline(t))

    def tangent_at(self, t):
        return Vector(*self.spline.derivative()(t)).unitized()

    def closest_point(self, point, return_parameter=False):
        start, end = self.domain
        samples = [start + (end - start) * i / 100 for i in range(101)]
        best = min(samples, key=lambda t: self.point_at(t).distance_to_point(point))
        step = (end - start) / 100
        t = minimize_scalar(lambda t: self.point_at(t).distance_to_point(point), bounds=(max(start, best - step), min(end, best + step)), method="bounded").x
        return (self.point_at(t), t) if return_parameter else self.point_at(t)


Constraint.register(Spline, CurveConstraint)

# 0. input: the four boundary curves of texas_boundary_r7.3dm (metres), two arches, a curve on the ground and one at the top
# fmt: off
ground = Spline(
    [
        [3.5871, -0.5896, 0.0], [3.5184, -0.52, 0.0], [3.3913, -0.3746, 0.0], [3.2283, -0.1404, 0.0],
        [3.1026, 0.1074, 0.0], [3.0183, 0.3661, 0.0], [2.9782, 0.6328, 0.0], [2.9827, 0.904, 0.0],
        [3.03, 1.1769, 0.0], [3.1178, 1.449, 0.0], [3.1976, 1.6258, 0.0], [3.2438, 1.713, 0.0],
    ],
    [
        0.0, 0.0, 0.0, 0.0, 0.2935, 0.5779, 0.854, 1.1239, 1.3908, 1.6591, 1.9342, 2.2186,
        2.5147, 2.5147, 2.5147, 2.5147,
    ],
)
back_arch = Spline(
    [
        [0.2271, -0.2186, 0.7], [0.2652, -0.1942, 0.7707], [0.3428, -0.1445, 0.9073], [0.4654, -0.066, 1.1037],
        [0.5951, 0.0171, 1.2886], [0.7354, 0.1069, 1.4626], [0.8885, 0.2049, 1.6214], [1.0562, 0.3123, 1.7582],
        [1.2408, 0.4305, 1.8641], [1.4444, 0.5609, 1.9267], [1.6647, 0.7019, 1.9296], [1.8896, 0.846, 1.8626],
        [2.1033, 0.9828, 1.7336], [2.2972, 1.107, 1.5623], [2.4711, 1.2183, 1.3657], [2.6285, 1.3191, 1.1529],
        [2.7721, 1.411, 0.9297], [2.9033, 1.495, 0.7015], [3.0244, 1.5726, 0.4706], [3.1375, 1.645, 0.2371],
        [3.2091, 1.6908, 0.0793], [3.2438, 1.713, 0.0],
    ],
    [
        0.0, 0.0, 0.0, 0.0, 0.2519, 0.4939, 0.7331, 0.9734, 1.2159, 1.456, 1.6962, 1.9425,
        2.1993, 2.4724, 2.7602, 3.0477, 3.3305, 3.614, 3.8968, 4.1725, 4.4425, 4.7125, 4.9805, 4.9805,
        4.9805, 4.9805,
    ],
)
front_arch = Spline(
    [
        [0.1726, -0.5896, 0.7], [0.2132, -0.5894, 0.7764], [0.2998, -0.5888, 0.932], [0.4395, -0.588, 1.1632],
        [0.594, -0.5872, 1.392], [0.7638, -0.5864, 1.6117], [0.9543, -0.5856, 1.8181], [1.1731, -0.5848, 2.0028],
        [1.4278, -0.5842, 2.1457], [1.7168, -0.5838, 2.2097], [2.0071, -0.5838, 2.1645], [2.2623, -0.584, 2.0344],
        [2.4812, -0.5845, 1.8573], [2.6717, -0.585, 1.6532], [2.84, -0.5856, 1.4334], [2.9903, -0.5862, 1.2056],
        [3.1269, -0.5868, 0.9727], [3.2535, -0.5875, 0.7345], [3.372, -0.5882, 0.4919], [3.4831, -0.5889, 0.2468],
        [3.5531, -0.5894, 0.0825], [3.5871, -0.5896, 0.0],
    ],
    [
        0.0, 0.0, 0.0, 0.0, 0.2596, 0.534, 0.8103, 1.0873, 1.3661, 1.6517, 1.9432, 2.2341,
        2.5219, 2.8056, 3.0839, 3.3629, 3.6413, 3.9134, 4.1812, 4.451, 4.7226, 4.9909, 5.2584, 5.2584,
        5.2584, 5.2584,
    ],
)
top = Spline(
    [
        [0.2271, -0.2186, 0.7], [0.2558, -0.2587, 0.7], [0.32, -0.3905, 0.7], [0.2351, -0.5302, 0.7],
        [0.1726, -0.5896, 0.7],
    ],
    [
        0.0, 0.0, 0.0, 0.0, 0.148, 0.4066, 0.4066, 0.4066, 0.4066,
    ],
)
# fmt: on

# 1. create a cable mesh from a surface between the end points of the curves: 19 faces along the arches, 9 across
a, b, c, d = Point(0.1726, -0.5896, 0.7), Point(3.5871, -0.5896, 0.0), Point(3.2438, 1.713, 0.0), Point(0.2271, -0.2186, 0.7)
mesh = Mesh.from_meshgrid(dx=1, nx=19, dy=1, ny=9)
grid = {vertex: mesh.vertex_attributes(vertex, "xy") for vertex in mesh.vertices()}
for vertex in mesh.vertices():
    u, v, _ = mesh.vertex_attributes(vertex, "xyz")  # the grid spans 0 to 1 in both directions
    mesh.vertex_attributes(vertex, "xyz", a * ((1 - u) * (1 - v)) + b * (u * (1 - v)) + c * (u * v) + d * ((1 - u) * v))
index = mesh.vertex_index()
edges = list(mesh.edges())

# 2. identify anchors: the whole boundary
anchors = [vertex for vertex in mesh.vertices() if mesh.is_vertex_on_boundary(vertex)]
corners = [vertex for vertex in anchors if mesh.vertex_degree(vertex) == 2]

# 3. set anchor constraints: every boundary anchor between two corners slides on the curve of its side
constraints = [None] * mesh.number_of_vertices()
for vertex in anchors:
    if vertex not in corners:
        u, v = grid[vertex]
        curve = front_arch if v == 0 else back_arch if v == 1 else ground if u == 1 else top
        constraints[index[vertex]] = Constraint(curve)

# 4. force density method: the anchors slide until their reactions are normal to the curves
result = fd_constrained_numpy(
    vertices=mesh.vertices_attributes("xyz"),
    fixed=[index[vertex] for vertex in anchors],
    edges=[(index[u], index[v]) for u, v in edges],
    forcedensities=[1.0] * len(edges),
    constraints=constraints,
    kmax=500,
)
print("sliding anchors:", sum(constraint is not None for constraint in constraints))
print(
    "largest distance of an anchor to its curve:",
    max(
        constraints[index[vertex]].geometry.closest_point(result.vertices[index[vertex]]).distance_to_point(result.vertices[index[vertex]])
        for vertex in anchors
        if constraints[index[vertex]]
    ),
)

print("anchors:", len(anchors))
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

# show the result: tension red, anchors black, the curves cyan
for vertex in mesh.vertices():
    mesh.vertex_attributes(vertex, "xyz", result.vertices[index[vertex]].tolist())

viewer = Viewer()
viewer.scene.add(mesh, show_points=False, edgecolor=Color.from_hex("#d62828"), facecolor=Color.from_hex("#eeeeee"), linewidth=2)
viewer.scene.add(Pointcloud([mesh.vertex_point(vertex) for vertex in anchors]), pointcolor=Color.black(), pointsize=10)
for curve in (ground, back_arch, front_arch, top):
    start, end = curve.domain
    viewer.scene.add(Polyline([curve.point_at(start + (end - start) * i / 100) for i in range(101)]), linecolor=Color.cyan(), linewidth=3)
viewer.show()
```
