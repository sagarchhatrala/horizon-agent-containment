# HAC Architecture

HAC evaluates agent activity as deterministic security state transitions.

Flow:

1. Normalize an action.
2. Validate the current state and all references.
3. Clone the committed state.
4. Apply the action to the clone.
5. Preserve and update provenance.
6. Update the security graph.
7. Recompute capabilities from graph and history.
8. Evaluate invariants.
9. Commit only if no invariant fails.

The core package does not call a model, network service, embedding index, or external reputation feed.

## Modules

- `models.py`: typed agents, resources, artifacts, credentials, actions, capabilities, and enums.
- `state.py`: committed security state and deterministic snapshots.
- `graph.py`: explicit security relationship graph.
- `provenance.py`: provenance inheritance and classification joins.
- `transitions.py`: deterministic state transition logic.
- `capabilities.py`: state-derived capability detection.
- `invariants.py`: invariant checks over detected capabilities.
- `engine.py`: fail-closed transition orchestration.
- `adapters/mcp.py`: conceptual MCP request normalization.
- `adapters/acb.py`: optional action-level enforcement bridge.

## Design Boundary

HAC is a containment primitive. It is not a general policy engine and does not try to decide whether an isolated action looks malicious. It evaluates whether an action causes the resulting state to contain an unauthorized capability.