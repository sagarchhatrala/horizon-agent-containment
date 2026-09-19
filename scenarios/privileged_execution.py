from __future__ import annotations

from hac.models import Action, ActionType
from scenarios.common import base_state


def state():
    return base_state()


def actions() -> list[Action]:
    return [
        Action("priv-1", "agent-a", ActionType.DOWNLOAD_EXTERNAL, source="external-package", metadata={"artifact_id": "pkg"}),
        Action("priv-2", "agent-a", ActionType.STORE_ARTIFACT, source="pkg", destination="internal-store"),
        Action("priv-3", "agent-a", ActionType.PROCESS_ARTIFACT, source="pkg", metadata={"artifact_id": "processed-pkg"}),
        Action("priv-4", "agent-a", ActionType.EXECUTE_ARTIFACT, source="processed-pkg", metadata={"privilege": "elevated"}),
    ]