from __future__ import annotations

from hac.exceptions import ValidationError
from hac.graph import Edge
from hac.models import Action, ActionType, Artifact, Classification, EdgeType
from hac.provenance import inherit_provenance, join_classification, provenance_from_resource
from hac.state import SecurityState


def validate_state(state: SecurityState) -> None:
    for agent in state.agents.values():
        _require(agent.agent_id, "agent_id")
        _require(agent.model_family, "model_family")
        _require(agent.session_id, "session_id")
    for resource in state.resources.values():
        _require(resource.resource_id, "resource_id")
        _require(resource.resource_type, "resource_type")
    for artifact in state.artifacts.values():
        _require(artifact.artifact_id, "artifact_id")
        _require(artifact.creator, "creator")
        if not artifact.provenance or not artifact.provenance.source_ids:
            raise ValidationError(f"artifact {artifact.artifact_id} has missing provenance")
    for credential in state.credentials.values():
        _require(credential.credential_id, "credential_id")
        _require(credential.owner, "credential owner")
        if credential.owner not in state.agents:
            raise ValidationError(f"credential {credential.credential_id} has unknown owner")
    for edge in state.graph.edges:
        if not isinstance(edge, Edge):
            raise ValidationError("invalid graph edge")


def validate_action(state: SecurityState, action: Action) -> None:
    _require(action.action_id, "action_id")
    if action.actor not in state.agents:
        raise ValidationError(f"unknown agent: {action.actor}")
    if not isinstance(action.action_type, ActionType):
        raise ValidationError("unknown action type")
    match action.action_type:
        case ActionType.READ_RESOURCE:
            _known_resource(state, action.resource)
        case ActionType.CREATE_ARTIFACT:
            _require_new_artifact_id(state, action)
            if action.resource is not None:
                _known_resource(state, action.resource)
        case ActionType.TRANSFORM_ARTIFACT | ActionType.ENCRYPT_ARTIFACT | ActionType.PROCESS_ARTIFACT:
            _known_artifact(state, action.source)
            _require_new_artifact_id(state, action)
        case ActionType.SPLIT_ARTIFACT:
            _known_artifact(state, action.source)
            children = action.metadata.get("children")
            if not isinstance(children, list) or not children or not all(isinstance(c, str) and c for c in children):
                raise ValidationError("SPLIT_ARTIFACT requires metadata.children")
            for child in children:
                if child in state.artifacts:
                    raise ValidationError(f"artifact already exists: {child}")
        case ActionType.UPLOAD_ARTIFACT | ActionType.STORE_ARTIFACT:
            _known_artifact(state, action.source)
            _known_resource(state, action.destination)
        case ActionType.DOWNLOAD_EXTERNAL:
            _known_resource(state, action.source)
            _require_new_artifact_id(state, action)
        case ActionType.EXECUTE_ARTIFACT:
            _known_artifact(state, action.source)
        case ActionType.USE_CREDENTIAL | ActionType.ACQUIRE_CREDENTIAL:
            _known_credential(state, action.credential)
        case ActionType.CONTACT_AGENT:
            if action.destination not in state.agents:
                raise ValidationError(f"unknown destination agent: {action.destination}")
        case ActionType.DELEGATE_CREDENTIAL:
            _known_credential(state, action.credential)
            if action.destination not in state.agents:
                raise ValidationError(f"unknown destination agent: {action.destination}")
            credential = state.credentials[action.credential or ""]
            if credential.owner != action.actor:
                raise ValidationError("only credential owner can delegate")
        case ActionType.MODIFY_CODE | ActionType.RUN_TESTS | ActionType.BUILD_ARTIFACT:
            if action.source is not None:
                _known_artifact(state, action.source)
            if action.resource is not None:
                _known_resource(state, action.resource)
            if action.action_type == ActionType.BUILD_ARTIFACT:
                _require_new_artifact_id(state, action)
        case _:
            raise ValidationError("unknown action type")


def apply_transition(state: SecurityState, action: Action) -> SecurityState:
    next_state = state.clone()
    event = {
        "action_id": action.action_id,
        "actor": action.actor,
        "action_type": action.action_type.value,
        "source": action.source,
        "destination": action.destination,
        "resource": action.resource,
        "credential": action.credential,
        "metadata": _sorted_metadata(action.metadata),
    }
    next_state.history.append(event)
    match action.action_type:
        case ActionType.READ_RESOURCE:
            next_state.graph.add_edge(action.actor, EdgeType.READS, action.resource or "")
        case ActionType.CREATE_ARTIFACT:
            artifact_id = action.metadata["artifact_id"]
            if action.resource:
                resource = next_state.resources[action.resource]
                provenance = provenance_from_resource(resource)
                classification = join_classification(provenance, resource.classification)
                parents = (resource.resource_id,)
                next_state.graph.add_edge(action.actor, EdgeType.READS, resource.resource_id)
                next_state.graph.add_edge(artifact_id, EdgeType.DERIVES, resource.resource_id)
            else:
                classification = _classification_from_metadata(action)
                provenance = action.metadata.get("provenance")
                if provenance is None:
                    raise ValidationError("CREATE_ARTIFACT requires provenance when resource is absent")
                parents = tuple(action.metadata.get("parents", ()))
            next_state.artifacts[artifact_id] = Artifact(artifact_id, classification, provenance, action.actor, parents)
            next_state.graph.add_edge(action.actor, EdgeType.WRITES, artifact_id)
        case ActionType.TRANSFORM_ARTIFACT | ActionType.ENCRYPT_ARTIFACT | ActionType.PROCESS_ARTIFACT:
            parent = next_state.artifacts[action.source or ""]
            artifact_id = action.metadata["artifact_id"]
            provenance = inherit_provenance([parent])
            next_state.artifacts[artifact_id] = Artifact(
                artifact_id,
                join_classification(provenance, parent.classification),
                provenance,
                action.actor,
                (parent.artifact_id,),
            )
            next_state.graph.add_edge(artifact_id, EdgeType.DERIVES, parent.artifact_id)
            next_state.graph.add_edge(action.actor, EdgeType.WRITES, artifact_id)
        case ActionType.SPLIT_ARTIFACT:
            parent = next_state.artifacts[action.source or ""]
            provenance = inherit_provenance([parent])
            for child_id in action.metadata["children"]:
                next_state.artifacts[child_id] = Artifact(
                    child_id,
                    join_classification(provenance, parent.classification),
                    provenance,
                    action.actor,
                    (parent.artifact_id,),
                )
                next_state.graph.add_edge(child_id, EdgeType.DERIVES, parent.artifact_id)
                next_state.graph.add_edge(parent.artifact_id, EdgeType.CONTAINS, child_id)
        case ActionType.UPLOAD_ARTIFACT | ActionType.STORE_ARTIFACT:
            next_state.graph.add_edge(action.actor, EdgeType.SENDS, action.destination or "")
            next_state.graph.add_edge(action.source or "", EdgeType.SENDS, action.destination or "")
        case ActionType.DOWNLOAD_EXTERNAL:
            source = next_state.resources[action.source or ""]
            artifact_id = action.metadata["artifact_id"]
            provenance = provenance_from_resource(source)
            next_state.artifacts[artifact_id] = Artifact(
                artifact_id,
                join_classification(provenance, Classification.UNTRUSTED),
                provenance,
                action.actor,
                (source.resource_id,),
            )
            next_state.graph.add_edge(action.actor, EdgeType.READS, source.resource_id)
            next_state.graph.add_edge(artifact_id, EdgeType.DERIVES, source.resource_id)
        case ActionType.EXECUTE_ARTIFACT:
            next_state.graph.add_edge(action.actor, EdgeType.EXECUTES, action.source or "")
        case ActionType.USE_CREDENTIAL:
            next_state.graph.add_edge(action.actor, EdgeType.AUTHENTICATES, action.credential or "")
        case ActionType.CONTACT_AGENT:
            next_state.graph.add_edge(action.actor, EdgeType.CONNECTS, action.destination or "")
        case ActionType.ACQUIRE_CREDENTIAL:
            next_state.graph.add_edge(action.actor, EdgeType.OWNS, action.credential or "")
        case ActionType.DELEGATE_CREDENTIAL:
            credential_id = action.credential or ""
            next_state.delegations.add((action.actor, action.destination or "", credential_id))
            next_state.graph.add_edge(action.actor, EdgeType.DELEGATES, action.destination or "")
        case ActionType.MODIFY_CODE:
            if action.source:
                next_state.graph.add_edge(action.actor, EdgeType.WRITES, action.source)
        case ActionType.RUN_TESTS:
            if action.source:
                next_state.graph.add_edge(action.actor, EdgeType.EXECUTES, action.source)
        case ActionType.BUILD_ARTIFACT:
            artifact_id = action.metadata["artifact_id"]
            if action.source:
                parent = next_state.artifacts[action.source]
                provenance = inherit_provenance([parent])
                parents = (parent.artifact_id,)
                classification = join_classification(provenance, Classification.INTERNAL)
            else:
                resource = next_state.resources[action.resource or ""]
                provenance = provenance_from_resource(resource)
                parents = (resource.resource_id,)
                classification = join_classification(provenance, Classification.INTERNAL)
            next_state.artifacts[artifact_id] = Artifact(artifact_id, classification, provenance, action.actor, parents)
            next_state.graph.add_edge(action.actor, EdgeType.WRITES, artifact_id)
    return next_state


def _require(value: object, field_name: str) -> None:
    if value is None or value == "":
        raise ValidationError(f"missing {field_name}")


def _known_resource(state: SecurityState, resource_id: str | None) -> None:
    _require(resource_id, "resource")
    if resource_id not in state.resources:
        raise ValidationError(f"unknown resource: {resource_id}")


def _known_artifact(state: SecurityState, artifact_id: str | None) -> None:
    _require(artifact_id, "artifact")
    if artifact_id not in state.artifacts:
        raise ValidationError(f"unknown artifact: {artifact_id}")


def _known_credential(state: SecurityState, credential_id: str | None) -> None:
    _require(credential_id, "credential")
    if credential_id not in state.credentials:
        raise ValidationError(f"unknown credential: {credential_id}")


def _require_new_artifact_id(state: SecurityState, action: Action) -> None:
    artifact_id = action.metadata.get("artifact_id")
    if not isinstance(artifact_id, str) or not artifact_id:
        raise ValidationError(f"{action.action_type.value} requires metadata.artifact_id")
    if artifact_id in state.artifacts:
        raise ValidationError(f"artifact already exists: {artifact_id}")


def _classification_from_metadata(action: Action) -> Classification:
    try:
        return Classification(action.metadata["classification"])
    except Exception as exc:
        raise ValidationError("unknown classification") from exc


def _sorted_metadata(metadata: dict) -> dict:
    return {key: metadata[key] for key in sorted(metadata)}