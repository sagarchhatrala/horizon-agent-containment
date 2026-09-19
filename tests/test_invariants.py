from hac.engine import HACEngine
from hac.models import Action, ActionType, DecisionValue, InvariantType
from scenarios.common import base_state


def test_secret_to_external_blocks():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("i1", "agent-a", ActionType.CREATE_ARTIFACT, resource="secret-db", metadata={"artifact_id": "a"})).allowed
    decision = engine.evaluate(Action("i2", "agent-a", ActionType.UPLOAD_ARTIFACT, source="a", destination="public-internet"))
    assert decision.decision == DecisionValue.BLOCK
    assert InvariantType.SECRET_TO_EXTERNAL in decision.violated_invariants


def test_untrusted_to_privileged_blocks():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("i1", "agent-a", ActionType.DOWNLOAD_EXTERNAL, source="external-package", metadata={"artifact_id": "pkg"})).allowed
    decision = engine.evaluate(Action("i2", "agent-a", ActionType.EXECUTE_ARTIFACT, source="pkg", metadata={"privilege": "admin"}))
    assert not decision.allowed
    assert InvariantType.UNTRUSTED_TO_PRIVILEGED in decision.violated_invariants


def test_explicit_delegation_blocks_credential_use():
    engine = HACEngine(base_state())
    decision = engine.evaluate(Action("i1", "agent-a", ActionType.USE_CREDENTIAL, credential="cred-b"))
    assert not decision.allowed
    assert InvariantType.EXPLICIT_DELEGATION in decision.violated_invariants


def test_explicit_delegation_allows_credential_use():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("i1", "agent-b", ActionType.DELEGATE_CREDENTIAL, destination="agent-a", credential="cred-b")).allowed
    assert engine.evaluate(Action("i2", "agent-a", ActionType.USE_CREDENTIAL, credential="cred-b")).allowed


def test_credential_escalation_blocks():
    engine = HACEngine(base_state())
    decision = engine.evaluate(Action("i1", "agent-a", ActionType.ACQUIRE_CREDENTIAL, credential="cred-b"))
    assert not decision.allowed
    assert InvariantType.CREDENTIAL_ESCALATION in decision.violated_invariants


def test_trust_boundary_blocks_external_public_upload():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("i1", "agent-a", ActionType.CREATE_ARTIFACT, resource="repo", metadata={"artifact_id": "a"})).allowed
    decision = engine.evaluate(Action("i2", "agent-a", ActionType.UPLOAD_ARTIFACT, source="a", destination="public-internet"))
    assert not decision.allowed
    assert InvariantType.TRUST_BOUNDARY in decision.violated_invariants