from __future__ import annotations

from typing import Any

from hac.engine import HACEngine
from hac.models import Action, ActionType


TOOL_ACTIONS = {
    "read_resource": ActionType.READ_RESOURCE,
    "create_artifact": ActionType.CREATE_ARTIFACT,
    "transform_artifact": ActionType.TRANSFORM_ARTIFACT,
    "encrypt_artifact": ActionType.ENCRYPT_ARTIFACT,
    "split_artifact": ActionType.SPLIT_ARTIFACT,
    "upload_artifact": ActionType.UPLOAD_ARTIFACT,
    "download_external": ActionType.DOWNLOAD_EXTERNAL,
    "store_artifact": ActionType.STORE_ARTIFACT,
    "process_artifact": ActionType.PROCESS_ARTIFACT,
    "execute_artifact": ActionType.EXECUTE_ARTIFACT,
    "use_credential": ActionType.USE_CREDENTIAL,
}


class MCPAdapter:
    def __init__(self, engine: HACEngine):
        self.engine = engine

    def normalize(self, request: dict[str, Any]) -> Action:
        try:
            tool_name = request["tool"]
            args = request.get("arguments", {})
            return Action(
                action_id=request["id"],
                actor=request["agent_id"],
                action_type=TOOL_ACTIONS[tool_name],
                source=args.get("source"),
                destination=args.get("destination"),
                resource=args.get("resource"),
                credential=args.get("credential"),
                metadata=args.get("metadata", {}),
            )
        except Exception as exc:
            raise ValueError(f"malformed MCP request: {exc}") from exc

    def authorize_tool_request(self, request: dict[str, Any]):
        try:
            action = self.normalize(request)
        except Exception as exc:
            return self.engine.evaluate(
                Action(
                    action_id=str(request.get("id", "malformed")),
                    actor=str(request.get("agent_id", "")),
                    action_type="UNKNOWN",  # type: ignore[arg-type]
                    metadata={"error": str(exc)},
                )
            )
        return self.engine.evaluate(action)