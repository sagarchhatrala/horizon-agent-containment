from hac.engine import HACEngine
from hac.models import Action, ActionType
from scenarios.common import base_state


def test_state_clone_preserves_original_on_allow():
    engine = HACEngine(base_state())
    decision = engine.evaluate(Action("a1", "agent-a", ActionType.READ_RESOURCE, resource="repo"))
    assert decision.allowed
    assert decision.state_before["history"] == []
    assert len(engine.state.history) == 1


def test_state_snapshot_is_deterministically_sorted():
    snapshot = base_state().to_dict()
    assert list(snapshot["agents"]) == ["agent-a", "agent-b"]
    assert snapshot["delegations"] == []


def test_blocked_action_does_not_mutate_state():
    engine = HACEngine(base_state())
    before = engine.state.to_dict()
    decision = engine.evaluate(Action("bad", "missing", ActionType.READ_RESOURCE, resource="repo"))
    assert not decision.allowed
    assert engine.state.to_dict() == before