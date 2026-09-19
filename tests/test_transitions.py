from hac.engine import HACEngine
from hac.models import Action, ActionType, EdgeType
from scenarios.common import base_state


def test_read_resource_adds_read_edge():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("t1", "agent-a", ActionType.READ_RESOURCE, resource="repo")).allowed
    assert engine.state.graph.has_edge("agent-a", EdgeType.READS, "repo")


def test_create_artifact_from_resource_adds_artifact():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("t1", "agent-a", ActionType.CREATE_ARTIFACT, resource="repo", metadata={"artifact_id": "a"})).allowed
    assert "a" in engine.state.artifacts


def test_duplicate_artifact_blocks():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("t1", "agent-a", ActionType.CREATE_ARTIFACT, resource="repo", metadata={"artifact_id": "a"})).allowed
    assert not engine.evaluate(Action("t2", "agent-a", ActionType.CREATE_ARTIFACT, resource="repo", metadata={"artifact_id": "a"})).allowed


def test_delegation_action_records_delegation():
    engine = HACEngine(base_state())
    decision = engine.evaluate(Action("t1", "agent-b", ActionType.DELEGATE_CREDENTIAL, destination="agent-a", credential="cred-b"))
    assert decision.allowed
    assert ("agent-b", "agent-a", "cred-b") in engine.state.delegations