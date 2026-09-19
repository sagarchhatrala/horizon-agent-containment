from __future__ import annotations

from hac.models import Capability, CapabilityType, Classification, InvariantType, TrustLevel
from hac.state import SecurityState


def recompute_capabilities(state: SecurityState) -> list[Capability]:
    capabilities: dict[tuple[str, str, str], Capability] = {}
    for event in state.history:
        action = event.get("action_type")
        actor = event.get("actor", "")
        if action in {"UPLOAD_ARTIFACT", "STORE_ARTIFACT"}:
            artifact_id = event.get("source")
            dest_id = event.get("destination")
            artifact = state.artifacts.get(artifact_id)
            dest = state.resources.get(dest_id)
            if artifact and dest and artifact.provenance.is_secret_derived() and _is_external_destination(dest.classification, dest.trust_level):
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.DATA_EXFILTRATION,
                        artifact_id,
                        dest_id,
                        "SECRET-DERIVED artifact is crossing into an external destination.",
                        InvariantType.SECRET_TO_EXTERNAL,
                    ),
                )
            if dest and _is_external_destination(dest.classification, dest.trust_level) and not event.get("metadata", {}).get("authorized_boundary"):
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.TRUST_BOUNDARY_CROSSING,
                        actor,
                        dest_id,
                        "Action crosses a trust boundary without explicit authorization.",
                        InvariantType.TRUST_BOUNDARY,
                    ),
                )
        if action == "EXECUTE_ARTIFACT":
            artifact_id = event.get("source")
            artifact = state.artifacts.get(artifact_id)
            privileged = event.get("metadata", {}).get("privilege") in {"elevated", "privileged", "admin", "root"}
            authorized = event.get("metadata", {}).get("authorized") is True
            if artifact and privileged:
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.PRIVILEGED_EXECUTION,
                        actor,
                        artifact_id,
                        "Artifact is executable with elevated privilege.",
                        None,
                    ),
                )
            if artifact and artifact.provenance.is_untrusted_derived() and privileged and not authorized:
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.UNTRUSTED_EXECUTION,
                        actor,
                        artifact_id,
                        "UNTRUSTED artifact is executable with elevated privilege.",
                        InvariantType.UNTRUSTED_TO_PRIVILEGED,
                    ),
                )
        if action == "USE_CREDENTIAL":
            credential_id = event.get("credential")
            credential = state.credentials.get(credential_id)
            if credential and credential.owner != actor and (credential.owner, actor, credential.credential_id) not in state.delegations:
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.CREDENTIAL_DELEGATION,
                        actor,
                        credential_id,
                        "Agent is using another agent's credential without explicit delegation.",
                        InvariantType.EXPLICIT_DELEGATION,
                    ),
                )
            if credential and event.get("metadata", {}).get("assume_authority") and credential.owner != actor:
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.NON_TRANSITIVE_AUTHORITY,
                        actor,
                        credential.owner,
                        "Using a service credential does not grant the service owner's authority.",
                        InvariantType.NON_TRANSITIVE_AUTHORITY,
                    ),
                )
        if action == "ACQUIRE_CREDENTIAL":
            credential_id = event.get("credential")
            credential = state.credentials.get(credential_id)
            if credential and credential.owner != actor and not event.get("metadata", {}).get("authorized"):
                _add(
                    capabilities,
                    Capability(
                        CapabilityType.CREDENTIAL_ESCALATION,
                        actor,
                        credential_id,
                        "Agent is acquiring a credential outside declared authority.",
                        InvariantType.CREDENTIAL_ESCALATION,
                    ),
                )
    return [capabilities[k] for k in sorted(capabilities)]


def _is_external_destination(classification: Classification, trust_level: TrustLevel) -> bool:
    return classification in {Classification.PUBLIC, Classification.EXTERNAL} or trust_level == TrustLevel.EXTERNAL


def _add(items: dict[tuple[str, str, str], Capability], capability: Capability) -> None:
    items[(capability.capability_type.value, capability.subject, capability.object)] = capability