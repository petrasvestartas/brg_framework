# Initiatives

The layout follows [`compas_framework` initiatives](https://github.com/compas-dev/compas_framework/tree/c3-upgrade/initiatives). Read its `AGENTS.md` for the workflow.

One folder per initiative:

```text
initiatives/<name>/
├── README.md               # one paragraph, current phase, links to the files below
├── objective.md
├── inventory.md            # what exists today (reconnaissance)
├── proposal.md             # the recommended design, for approval
├── implementation-plan.md
├── handoff.md              # copy of _template/handoff.md, kept current
└── decisions/
    ├── README.md           # index of the decisions
    └── 001-short-title.md  # one decision per file, copy of _template/decision.md
```

A decision is `Proposed` until the user accepts it. Only then change it to `Accepted`.
