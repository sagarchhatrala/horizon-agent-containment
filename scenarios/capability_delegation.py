from __future__ import annotations

from hac.models import Action, ActionType
from scenarios.common import base_state


def state():
    return base_state()


def blocked_actions() -> list[Action]:
    return [
        Action("deleg-1", "agent-a", ActionType.CONTACT_AGENT, destination="agent-b"),
        Action("deleg-2", "agent-a", ActionType.USE_CREDENTIAL, credential="cred-b", metadata={"assume_authority": True}),
    ]


def allowed_actions() -> list[Action]:
    return [
        Action("deleg-ok-1", "agent-b", ActionType.DELEGATE_CREDENTIAL, destination="agent-a", credential="cred-b"),
        Action("deleg-ok-2", "agent-a", ActionType.USE_CREDENTIAL, credential="cred-b"),
    ]