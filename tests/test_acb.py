from adapters.acb import ACBAdapter
from hac.engine import HACEngine
from hac.models import Action, ActionType
from scenarios.common import base_state


def test_acb_adapter_allows_when_hac_and_enforcer_allow():
    adapter = ACBAdapter(HACEngine(base_state()), action_enforcer=lambda action: True)
    decision = adapter.authorize(Action("a1", "agent-a", ActionType.READ_RESOURCE, resource="repo"))
    assert decision.allowed


def test_acb_adapter_blocks_when_hac_blocks():
    adapter = ACBAdapter(HACEngine(base_state()), action_enforcer=lambda action: True)
    decision = adapter.authorize(Action("a1", "agent-a", ActionType.READ_RESOURCE, resource="missing"))
    assert not decision.allowed


def test_acb_adapter_blocks_when_enforcer_blocks():
    adapter = ACBAdapter(HACEngine(base_state()), action_enforcer=lambda action: False)
    decision = adapter.authorize(Action("a1", "agent-a", ActionType.READ_RESOURCE, resource="repo"))
    assert not decision.allowed
    assert "ACB" in decision.reason