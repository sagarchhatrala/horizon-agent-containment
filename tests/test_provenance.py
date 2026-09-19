from hac.engine import HACEngine
from hac.models import Action, ActionType, Classification
from scenarios.common import base_state


def test_secret_provenance_survives_transform_encrypt_split():
    engine = HACEngine(base_state())
    for action in [
        Action("p1", "agent-a", ActionType.CREATE_ARTIFACT, resource="secret-db", metadata={"artifact_id": "a"}),
        Action("p2", "agent-a", ActionType.TRANSFORM_ARTIFACT, source="a", metadata={"artifact_id": "b"}),
        Action("p3", "agent-a", ActionType.ENCRYPT_ARTIFACT, source="b", metadata={"artifact_id": "c"}),
        Action("p4", "agent-a", ActionType.SPLIT_ARTIFACT, source="c", metadata={"children": ["d"]}),
    ]:
        assert engine.evaluate(action).allowed
    assert engine.state.artifacts["d"].provenance.is_secret_derived()


def test_encryption_does_not_declassify():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("p1", "agent-a", ActionType.CREATE_ARTIFACT, resource="secret-db", metadata={"artifact_id": "a"})).allowed
    assert engine.evaluate(Action("p2", "agent-a", ActionType.ENCRYPT_ARTIFACT, source="a", metadata={"artifact_id": "enc"})).allowed
    assert engine.state.artifacts["enc"].classification == Classification.SECRET


def test_external_download_is_untrusted_derived():
    engine = HACEngine(base_state())
    assert engine.evaluate(Action("p1", "agent-a", ActionType.DOWNLOAD_EXTERNAL, source="external-package", metadata={"artifact_id": "pkg"})).allowed
    assert engine.state.artifacts["pkg"].provenance.is_untrusted_derived()