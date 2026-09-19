from __future__ import annotations

from collections.abc import Callable

from hac.decisions import Decision
from hac.engine import HACEngine
from hac.models import Action, DecisionValue


ActionEnforcer = Callable[[Action], bool]


class ACBAdapter:
    """Optional bridge: HAC evaluates state first, then ACB can enforce the action."""

    def __init__(self, engine: HACEngine, action_enforcer: ActionEnforcer | None = None):
        self.engine = engine
        self.action_enforcer = action_enforcer

    def authorize(self, action: Action) -> Decision:
        decision = self.engine.evaluate(action)
        if not decision.allowed:
            return decision
        if self.action_enforcer is not None and not self.action_enforcer(action):
            return Decision(
                decision=DecisionValue.BLOCK,
                reason="Blocked by downstream ACB action enforcement.",
                violated_invariants=decision.violated_invariants,
                capabilities_detected=decision.capabilities_detected,
                transition_id=decision.transition_id,
                state_before=decision.state_before,
                state_after=decision.state_after,
            )
        return decision