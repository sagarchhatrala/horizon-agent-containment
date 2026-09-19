from __future__ import annotations

from hac.capabilities import recompute_capabilities
from hac.invariants import evaluate_invariants
from hac.models import Capability, InvariantType
from hac.state import SecurityState


def evaluate_state(state: SecurityState) -> tuple[list[Capability], list[InvariantType]]:
    state.capabilities = recompute_capabilities(state)
    return state.capabilities, evaluate_invariants(state)