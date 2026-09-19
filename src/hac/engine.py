from __future__ import annotations

import hashlib
import json

from hac.decisions import Decision
from hac.evaluator import evaluate_state
from hac.models import Action, Capability, DecisionValue
from hac.state import SecurityState
from hac.transitions import apply_transition, validate_action, validate_state


class HACEngine:
    def __init__(self, state: SecurityState | None = None):
        self.state = state or SecurityState()

    def evaluate(self, action: Action) -> Decision:
        before = self.state.to_dict()
        transition_id = _transition_id(before, action)
        try:
            validate_state(self.state)
            validate_action(self.state, action)
            hypothetical = apply_transition(self.state, action)
            capabilities, violations = evaluate_state(hypothetical)
            after = hypothetical.to_dict()
            if violations:
                return Decision(
                    decision=DecisionValue.BLOCK,
                    reason=_blocked_reason(capabilities),
                    violated_invariants=tuple(violations),
                    capabilities_detected=tuple(capabilities),
                    transition_id=transition_id,
                    state_before=before,
                    state_after=after,
                )
            self.state = hypothetical
            return Decision(
                decision=DecisionValue.ALLOW,
                reason="Transition preserves configured security invariants.",
                violated_invariants=(),
                capabilities_detected=tuple(capabilities),
                transition_id=transition_id,
                state_before=before,
                state_after=after,
            )
        except Exception as exc:
            return Decision(
                decision=DecisionValue.BLOCK,
                reason=f"Fail closed: {exc}",
                violated_invariants=(),
                capabilities_detected=(),
                transition_id=transition_id,
                state_before=before,
                state_after=before,
            )


def _transition_id(state_before: dict, action: Action) -> str:
    payload = {
        "state": state_before,
        "action": {
            "action_id": action.action_id,
            "actor": action.actor,
            "action_type": action.action_type.value if hasattr(action.action_type, "value") else str(action.action_type),
            "source": action.source,
            "destination": action.destination,
            "resource": action.resource,
            "credential": action.credential,
            "metadata": action.metadata,
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def _blocked_reason(capabilities: list[Capability]) -> str:
    violating = [c for c in capabilities if c.invariant is not None]
    if not violating:
        return "Security invariant violation."
    first = sorted(violating, key=lambda c: (c.invariant.value if c.invariant else "", c.capability_type.value))[0]
    return f"Capability: {first.capability_type.value}. Reason: {first.reason} Invariant: {first.invariant.value}."