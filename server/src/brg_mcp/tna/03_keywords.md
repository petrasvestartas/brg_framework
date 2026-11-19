Keywords

- **Name** thrust network analysis, TNA.
- **Thrust network** a network of bars in compression that carries the loads to the supports. It is the three dimensional version of the thrust line of an arch.
- **Pattern** the lines in plan that the forces follow. It fixes the topology of the form diagram.
- **Form diagram** Γ, the projection of the thrust network on the horizontal plane. Its vertices are the nodes, its edges the bars, its faces the spaces between the bars.
- **Force diagram** Γ*, the dual of the form diagram: one vertex per space, one closed polygon per node. The length of an edge is the horizontal force in the corresponding bar.
- **Reciprocal diagrams** two dual diagrams whose corresponding edges are parallel, or all perpendicular after a turn of 90 degrees (Maxwell 1864). Then every node of the form diagram is in horizontal equilibrium.
- **Horizontal equilibrium** the step that makes the two diagrams reciprocal. `alpha` chooses which diagram moves: 100 keeps the form diagram, 0 keeps the force diagram.
- **Angle deviation** the angle between a form edge and its force edge after the turn of 90 degrees. It is zero in horizontal equilibrium; RhinoVAULT accepts up to 5 degrees.
- **Scale** the factor between lengths in the force diagram and horizontal forces. A larger scale means more thrust and a shallower vault.
- **Force density** q = scale · l* / l, the horizontal force of a bar over its length in plan. With q known, the heights follow from the same linear system as in the force density method.
- **Vertical equilibrium** the step that computes the heights z of the free nodes from the loads, the force densities and the heights of the supports.
- **zmax** the wanted height of the highest node. The scale is searched so that the thrust network reaches it.
- **Unloaded face** a face of the form diagram that closes an opening or a free edge. It carries no load and becomes one vertex of the force diagram.
- **hmin, hmax** bounds on the horizontal force of a form edge. **lmin, lmax** bounds on the length of a form or force edge.
- **Indeterminacy** a pattern with nodes of valency higher than three has many possible force diagrams. Each one is a different distribution of the forces and gives a different vault.
