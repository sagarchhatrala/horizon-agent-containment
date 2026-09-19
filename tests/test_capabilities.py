from hac.capabilities import recompute_capabilities
from hac.engine import HACEngine
from hac.models import Action, ActionType, CapabilityType
from hac.transitions import apply_transition
from scenarios.common import base_state


def test_data_exfiltration_capability_is_derived_from_state():
    state = base_state()
    state = apply_transition(state, Action("c1", "agent-a", ActionType.CREATE_ARTIFACT, resource="secret-db", metadata={"artifact_id": "a"}))
    state = apply_transition(state, Action("c2", "agent-a", ActionType.UPLOAD_ARTIFACT, source="a", destination="public-internet"))
    capabilities = recompute_capabilities(state)
    assert CapabilityType.DATA_EXFILTRATION in {c.capability_type for c in capabilities}


def test_untrusted_execution_capability_is_derived_from_state():
    state = base_state()
    state = apply_transition(state, Action("c1", "agent-a", ActionType.DOWNLOAD_EXTERNAL, source="external-package", metadata={"artifact_id": "pkg"}))
    state = apply_transition(state, Action("c2", "agent-a", ActionType.EXECUTE_ARTIFACT, source="pkg", metadata={"privilege": "root"}))
    capabilities = recompute_capabilities(state)
    assert CapabilityType.UNTRUSTED_EXECUTION in {c.capability_type for c in capabilities}


def test_model_family_does_not_affect_decision():
    s1 = base_state()
    s2 = base_state()
    s1.agents["agent-a"] = s1.agents["agent-a"].__class__("agent-a", "model-one", s1.agents["agent-a"].trust_level, "session-1")
    s2.agents["agent-a"] = s2.agents["agent-a"].__class__("agent-a", "model-two", s2.agents["agent-a"].trust_level, "session-1")
    a = Action("c1", "agent-a", ActionType.CREATE_ARTIFACT, resource="repo", metadata={"artifact_id": "a"})
    assert HACEngine(s1).evaluate(a).decision == HACEngine(s2).evaluate(a).decision