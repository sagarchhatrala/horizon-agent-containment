from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any

from hac.graph import SecurityGraph
from hac.models import Agent, Artifact, Capability, Credential, Resource


@dataclass
class SecurityState:
    agents: dict[str, Agent] = field(default_factory=dict)
    resources: dict[str, Resource] = field(default_factory=dict)
    artifacts: dict[str, Artifact] = field(default_factory=dict)
    credentials: dict[str, Credential] = field(default_factory=dict)
    graph: SecurityGraph = field(default_factory=SecurityGraph)
    delegations: set[tuple[str, str, str]] = field(default_factory=set)
    trust_boundaries: set[tuple[str, str]] = field(default_factory=set)
    capabilities: list[Capability] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)

    def clone(self) -> "SecurityState":
        return deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agents": {k: _dataclass_to_plain(v) for k, v in sorted(self.agents.items())},
            "resources": {k: _dataclass_to_plain(v) for k, v in sorted(self.resources.items())},
            "artifacts": {k: _dataclass_to_plain(v) for k, v in sorted(self.artifacts.items())},
            "credentials": {k: _dataclass_to_plain(v) for k, v in sorted(self.credentials.items())},
            "graph": self.graph.to_dict(),
            "delegations": [list(x) for x in sorted(self.delegations)],
            "trust_boundaries": [list(x) for x in sorted(self.trust_boundaries)],
            "capabilities": [_dataclass_to_plain(c) for c in sorted(self.capabilities, key=lambda c: (c.capability_type.value, c.subject, c.object))],
            "history": self.history,
        }


def _dataclass_to_plain(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _dataclass_to_plain(getattr(value, k)) for k in value.__dataclass_fields__}
    if isinstance(value, tuple):
        return [_dataclass_to_plain(v) for v in value]
    if isinstance(value, list):
        return [_dataclass_to_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _dataclass_to_plain(v) for k, v in sorted(value.items())}
    if hasattr(value, "value"):
        return value.value
    return value