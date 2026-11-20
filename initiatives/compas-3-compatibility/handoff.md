# Initiative Handoff

Last updated: 2026-11-20

## Resume here

Current phase: `architecture`

Status: The inventory, the proposal and two decisions are written. Work stops here until the user accepts or changes the decisions.

Read next:

1. `objective.md`
2. `proposal.md`
3. `decisions/README.md`

Do not reread the entire initiative unless the next task requires it.

## Decisions and approvals

- Accepted: none.
- Proposed: [001](decisions/001-limit-compas.md) and [002](decisions/002-lift-the-limit.md). The user must accept or change them.
- Scope boundary: no dependency, test or release change is authorized.

## Working state

| Repository | Branch | Exact head | Pull request | Status |
|---|---|---|---|---|
| `BlockResearchGroup/brg_framework` | `main` | `b59aa3225642a783c90ff80e687f4dd61b042240` | none | clean, pushed (this initiative's files are added after this head) |

Preserve any unrelated dirty paths explicitly. Never infer a branch head from
an earlier conversation.

## Completed at this checkpoint

- Inventory of the `compas` requirements of the six BRG packages, `compas_viewer` and `compas_framework`, from the installed metadata.

## Next tasks

1. The user accepts, changes or rejects decisions 001 and 002.
2. WP1 in `implementation-plan.md`.

## Blockers and approval gates

- Decisions 001 and 002 are not accepted.
- Whether the BRG packages work on COMPAS 3 is not known.

## Verification

Last verified:

- Metadata of the installed packages read with `importlib.metadata` — done, see the inventory.
- Nothing else is verified. No code changed.

Evidence by layer:

| Layer | Status | Evidence |
|---|---|---|
| Local focused checks | not applicable | No code changed in this checkpoint. |
| Package CI | not applicable | No code changed in this checkpoint. |
| Framework integration CI | not run | Nothing tests the BRG packages on COMPAS 3. This is the open question in the objective. |
| Candidate-artifact CI | not applicable | No release is proposed. |

Run next:

```text
uv run pytest -q
```
