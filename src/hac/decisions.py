from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hac.models import Capability, DecisionValue, InvariantType


@dataclass(frozen=True)
class Decision:
    decision: DecisionValue
    reason: str
    violated_invariants: tuple[InvariantType, ...]
    capabilities_detected: tuple[Capability, ...]
    transition_id: str
    state_before: dict[str, Any]
    state_after: dict[str, Any]

    @property
    def allowed(self) -> bool:
        return self.decision == DecisionValue.ALLOW