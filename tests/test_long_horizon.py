from adapters.simulator import run_actions
from hac.engine import HACEngine
from hac.models import CapabilityType, DecisionValue
from scenarios import capability_delegation, data_exfiltration, normal_workflow, privileged_execution


def test_data_exfiltration_blocks_only_final_step():
    decisions = run_actions(HACEngine(data_exfiltration.state()), data_exfiltration.actions())
    assert [d.decision for d in decisions[:5]] == [DecisionValue.ALLOW] * 5
    assert decisions[5].decision == DecisionValue.BLOCK
    assert CapabilityType.DATA_EXFILTRATION in {c.capability_type for c in decisions[5].capabilities_detected}


def test_legitimate_long_horizon_workflow_succeeds():
    decisions = run_actions(HACEngine(normal_workflow.state()), normal_workflow.actions())
    assert all(d.allowed for d in decisions)


def test_external_privileged_execution_blocks_final_step():
    decisions = run_actions(HACEngine(privileged_execution.state()), privileged_execution.actions())
    assert [d.decision for d in decisions[:3]] == [DecisionValue.ALLOW] * 3
    assert decisions[3].decision == DecisionValue.BLOCK
    assert CapabilityType.UNTRUSTED_EXECUTION in {c.capability_type for c in decisions[3].capabilities_detected}


def test_delegation_attack_blocks_without_delegation():
    decisions = run_actions(HACEngine(capability_delegation.state()), capability_delegation.blocked_actions())
    assert decisions[0].allowed
    assert not decisions[1].allowed


def test_repeat_same_state_and_action_is_deterministic():
    action = data_exfiltration.actions()[0]
    d1 = HACEngine(data_exfiltration.state()).evaluate(action)
    d2 = HACEngine(data_exfiltration.state()).evaluate(action)
    assert d1 == d2