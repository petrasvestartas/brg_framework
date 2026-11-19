Arch constraint, fd_arch_constraint.py: the middle line of the net slides on an arch.

Source: https://github.com/BlockResearchGroup/compas_fd/blob/main/docs/examples/example_mesh_constrained_on-arch.py

The original uses `NurbsCurve`, which needs a NURBS plugin; here the arch is a `Bezier` curve with the same control points.

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Bezier
from compas.geometry import Polyline
from compas_fd.constraints import Constraint
from compas_fd.constraints import CurveConstraint
from compas_fd.solvers import fd_constrained_numpy
from compas_viewer import Viewer
from scipy.optimize import minimize_scalar


class Arch(Bezier):
    """A Bezier curve that compas_fd can use as a constraint, without a NURBS plugin."""

    def closest_point(self, point, return_parameter=False):
        t = minimize_scalar(lambda t: self.point_at(t).distance_to_point(point), bounds=(0, 1), method="bounded").x
        return (self.point_at(t), t) if return_parameter else self.point_at(t)


Constraint.register(Arch, CurveConstraint)

mesh = Mesh.from_meshgrid(dx=10, nx=10)

vertices = mesh.vertices_attributes("xyz")
edges = list(mesh.edges())
fixed = list(mesh.vertices_where(vertex_degree=2))  # the four corners
forcedensities = [10.0 if mesh.is_edge_on_boundary(edge) else 1.0 for edge in edges]

# the nodes on the line x = 5 may only move along an arch over that line
arch = Arch([[5, 0, 0], [5, 5, 5], [5, 10, 0]])
constraints = [None] * mesh.number_of_vertices()
for vertex in mesh.vertices_where(x=5):
    constraints[vertex] = Constraint(arch)
    fixed.append(vertex)

result = fd_constrained_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities, constraints=constraints)

for vertex in mesh.vertices():
    mesh.vertex_attributes(vertex, "xyz", result.vertices[vertex].tolist())

sliding = [vertex for vertex in fixed if constraints[vertex]]
print("nodes on the arch:", len(sliding))
print("top of the arch:", max(result.vertices[sliding, 2]))
print("height range:", result.vertices[:, 2].min(), result.vertices[:, 2].max())
print("force range:", result.forces.min(), result.forces.max())

viewer = Viewer()
viewer.scene.add(mesh, show_points=False)
viewer.scene.add(Polyline([arch.point_at(i / 50) for i in range(51)]), linecolor=Color.cyan(), linewidth=3)
for vertex in fixed:
    color = Color.cyan() if constraints[vertex] else Color.from_hex("#2a6fdb")
    viewer.scene.add(mesh.vertex_point(vertex), pointcolor=color, pointsize=12)
viewer.show()
```
