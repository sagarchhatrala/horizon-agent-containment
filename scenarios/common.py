from __future__ import annotations

from hac.models import Agent, Classification, Credential, Resource, TrustLevel
from hac.state import SecurityState


def base_state() -> SecurityState:
    state = SecurityState()
    state.agents["agent-a"] = Agent("agent-a", "open-weight-demo", TrustLevel.INTERNAL, "session-1")
    state.agents["agent-b"] = Agent("agent-b", "closed-weight-demo", TrustLevel.INTERNAL, "session-2")
    state.resources["secret-db"] = Resource("secret-db", "database", Classification.SECRET, TrustLevel.INTERNAL)
    state.resources["repo"] = Resource("repo", "git", Classification.INTERNAL, TrustLevel.INTERNAL)
    state.resources["internal-store"] = Resource("internal-store", "object_store", Classification.INTERNAL, TrustLevel.INTERNAL)
    state.resources["public-internet"] = Resource("public-internet", "network", Classification.PUBLIC, TrustLevel.EXTERNAL)
    state.resources["external-package"] = Resource("external-package", "download", Classification.UNTRUSTED, TrustLevel.EXTERNAL)
    state.credentials["cred-a"] = Credential("cred-a", "internal:repo", "agent-a")
    state.credentials["cred-b"] = Credential("cred-b", "external:upload", "agent-b")
    state.trust_boundaries.add(("internal", "external"))
    return state