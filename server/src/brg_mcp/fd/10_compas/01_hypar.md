Hypar, fd_hypar.py: one free node between four supports.

Source: https://github.com/BlockResearchGroup/compas_fd/blob/main/tests/test_hypar.py

Tested with `compas 2.16.0`, `compas_fd 0.5.4`, `compas_viewer 2.0.2`.

```python
from compas.colors import Color
from compas.datastructures import Graph
from compas_fd.solvers import fd_numpy
from compas_viewer import Viewer

vertices = [
    [0, 0, 0],  # 0: free node, the start position does not matter
    [0, 0, 1],  # 1: support
    [1, 0, 0],  # 2: support
    [1, 1, 1],  # 3: support
    [0, 1, 0],  # 4: support
]
fixed = [1, 2, 3, 4]
edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
forcedensities = [1, 1, 1, 1]  # q = force / length of each cable

result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities)

print("free node:", result.vertices[0])  # equal q: the average of the supports, [0.5 0.5 0.5]
print("forces:", result.forces.ravel())
print("lengths:", result.lengths.ravel())

graph = Graph.from_nodes_and_edges(result.vertices.tolist(), edges)
vertexcolor = {0: Color.from_hex("#d62828"), **{node: Color.from_hex("#2a6fdb") for node in fixed}}

viewer = Viewer()
viewer.scene.add(graph, show_points=True, vertexcolor=vertexcolor, pointsize=14, linewidth=3)
viewer.show()
```
