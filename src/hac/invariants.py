from __future__ import annotations

from hac.models import InvariantType
from hac.state import SecurityState


def evaluate_invariants(state: SecurityState) -> list[InvariantType]:
    violations: set[InvariantType] = set()
    for capability in state.capabilities:
        if capability.invariant is not None:
            violations.add(capability.invariant)
    return sorted(violations, key=lambda invariant: invariant.value)