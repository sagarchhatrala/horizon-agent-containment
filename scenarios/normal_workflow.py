from __future__ import annotations

from hac.models import Action, ActionType
from scenarios.common import base_state


def state():
    return base_state()


def actions() -> list[Action]:
    return [
        Action("normal-1", "agent-a", ActionType.READ_RESOURCE, resource="repo"),
        Action("normal-2", "agent-a", ActionType.CREATE_ARTIFACT, resource="repo", metadata={"artifact_id": "code-change"}),
        Action("normal-3", "agent-a", ActionType.MODIFY_CODE, source="code-change"),
        Action("normal-4", "agent-a", ActionType.RUN_TESTS, source="code-change"),
        Action("normal-5", "agent-a", ActionType.BUILD_ARTIFACT, source="code-change", metadata={"artifact_id": "build-1"}),
        Action("normal-6", "agent-a", ActionType.STORE_ARTIFACT, source="build-1", destination="internal-store"),
    ]