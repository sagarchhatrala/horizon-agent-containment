from __future__ import annotations

from hac.models import Credential
from hac.state import SecurityState


def has_delegation(state: SecurityState, credential: Credential, actor_id: str) -> bool:
    return credential.owner == actor_id or (credential.owner, actor_id, credential.credential_id) in state.delegations


def can_acquire_credential(state: SecurityState, actor_id: str, credential: Credential) -> bool:
    agent = state.agents[actor_id]
    if credential.owner == actor_id:
        return True
    if (credential.owner, actor_id, credential.credential_id) in state.delegations:
        return True
    return agent.trust_level.value == "TRUSTED" and credential.scope.startswith("internal:")