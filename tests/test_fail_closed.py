from hac.engine import HACEngine
from hac.models import Action, ActionType, Artifact, Classification, Provenance
from scenarios.common import base_state


def test_unknown_agent_blocks():
    decision = HACEngine(base_state()).evaluate(Action("f1", "ghost", ActionType.READ_RESOURCE, resource="repo"))
    assert not decision.allowed


def test_unknown_resource_blocks():
    decision = HACEngine(base_state()).evaluate(Action("f1", "agent-a", ActionType.READ_RESOURCE, resource="missing"))
    assert not decision.allowed


def test_missing_artifact_provenance_blocks():
    state = base_state()
    state.artifacts["bad"] = Artifact("bad", Classification.INTERNAL, Provenance((), ()), "agent-a")
    decision = HACEngine(state).evaluate(Action("f1", "agent-a", ActionType.STORE_ARTIFACT, source="bad", destination="internal-store"))
    assert not decision.allowed


def test_unknown_action_type_blocks():
    decision = HACEngine(base_state()).evaluate(Action("f1", "agent-a", "UNKNOWN", resource="repo"))  # type: ignore[arg-type]
    assert not decision.allowed


def test_malformed_action_blocks():
    decision = HACEngine(base_state()).evaluate(Action("", "agent-a", ActionType.READ_RESOURCE, resource="repo"))
    assert not decision.allowed


def test_unknown_credential_blocks():
    decision = HACEngine(base_state()).evaluate(Action("f1", "agent-a", ActionType.USE_CREDENTIAL, credential="missing"))
    assert not decision.allowed


def test_block_reason_says_fail_closed():
    decision = HACEngine(base_state()).evaluate(Action("f1", "agent-a", ActionType.READ_RESOURCE, resource="missing"))
    assert decision.reason.startswith("Fail closed:")