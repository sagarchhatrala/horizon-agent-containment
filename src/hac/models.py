from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DecisionValue(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


class TrustLevel(str, Enum):
    TRUSTED = "TRUSTED"
    INTERNAL = "INTERNAL"
    UNTRUSTED = "UNTRUSTED"
    EXTERNAL = "EXTERNAL"


class Classification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    SECRET = "SECRET"
    HIGHLY_SENSITIVE = "HIGHLY_SENSITIVE"
    UNTRUSTED = "UNTRUSTED"
    EXTERNAL = "EXTERNAL"


class ActionType(str, Enum):
    READ_RESOURCE = "READ_RESOURCE"
    CREATE_ARTIFACT = "CREATE_ARTIFACT"
    TRANSFORM_ARTIFACT = "TRANSFORM_ARTIFACT"
    ENCRYPT_ARTIFACT = "ENCRYPT_ARTIFACT"
    SPLIT_ARTIFACT = "SPLIT_ARTIFACT"
    UPLOAD_ARTIFACT = "UPLOAD_ARTIFACT"
    DOWNLOAD_EXTERNAL = "DOWNLOAD_EXTERNAL"
    STORE_ARTIFACT = "STORE_ARTIFACT"
    PROCESS_ARTIFACT = "PROCESS_ARTIFACT"
    EXECUTE_ARTIFACT = "EXECUTE_ARTIFACT"
    USE_CREDENTIAL = "USE_CREDENTIAL"
    CONTACT_AGENT = "CONTACT_AGENT"
    ACQUIRE_CREDENTIAL = "ACQUIRE_CREDENTIAL"
    DELEGATE_CREDENTIAL = "DELEGATE_CREDENTIAL"
    MODIFY_CODE = "MODIFY_CODE"
    RUN_TESTS = "RUN_TESTS"
    BUILD_ARTIFACT = "BUILD_ARTIFACT"


class CapabilityType(str, Enum):
    DATA_EXFILTRATION = "DATA_EXFILTRATION"
    UNTRUSTED_EXECUTION = "UNTRUSTED_EXECUTION"
    PRIVILEGED_EXECUTION = "PRIVILEGED_EXECUTION"
    CREDENTIAL_DELEGATION = "CREDENTIAL_DELEGATION"
    UNAUTHORIZED_EXTERNAL_ACCESS = "UNAUTHORIZED_EXTERNAL_ACCESS"
    CREDENTIAL_ESCALATION = "CREDENTIAL_ESCALATION"
    TRUST_BOUNDARY_CROSSING = "TRUST_BOUNDARY_CROSSING"
    NON_TRANSITIVE_AUTHORITY = "NON_TRANSITIVE_AUTHORITY"


class InvariantType(str, Enum):
    SECRET_TO_EXTERNAL = "SECRET_TO_EXTERNAL"
    UNTRUSTED_TO_PRIVILEGED = "UNTRUSTED_TO_PRIVILEGED"
    NON_TRANSITIVE_AUTHORITY = "NON_TRANSITIVE_AUTHORITY"
    EXPLICIT_DELEGATION = "EXPLICIT_DELEGATION"
    CREDENTIAL_ESCALATION = "CREDENTIAL_ESCALATION"
    TRUST_BOUNDARY = "TRUST_BOUNDARY"


class EdgeType(str, Enum):
    READS = "READS"
    WRITES = "WRITES"
    DERIVES = "DERIVES"
    CONTAINS = "CONTAINS"
    SENDS = "SENDS"
    EXECUTES = "EXECUTES"
    DELEGATES = "DELEGATES"
    AUTHENTICATES = "AUTHENTICATES"
    CONNECTS = "CONNECTS"
    TRUSTS = "TRUSTS"
    OWNS = "OWNS"


@dataclass(frozen=True)
class Agent:
    agent_id: str
    model_family: str
    trust_level: TrustLevel
    session_id: str


@dataclass(frozen=True)
class Resource:
    resource_id: str
    resource_type: str
    classification: Classification
    trust_level: TrustLevel


@dataclass(frozen=True)
class Provenance:
    source_ids: tuple[str, ...]
    classifications: tuple[Classification, ...]
    derived_from_external: bool = False
    declassified: bool = False

    def is_secret_derived(self) -> bool:
        return (
            Classification.SECRET in self.classifications
            or Classification.HIGHLY_SENSITIVE in self.classifications
        ) and not self.declassified

    def is_untrusted_derived(self) -> bool:
        return self.derived_from_external or Classification.UNTRUSTED in self.classifications


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    classification: Classification
    provenance: Provenance
    creator: str
    parents: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Credential:
    credential_id: str
    scope: str
    owner: str


@dataclass(frozen=True)
class Action:
    action_id: str
    actor: str
    action_type: ActionType
    source: str | None = None
    destination: str | None = None
    resource: str | None = None
    credential: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Capability:
    capability_type: CapabilityType
    subject: str
    object: str
    reason: str
    invariant: InvariantType | None = None