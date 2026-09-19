from __future__ import annotations

from hac.decisions import Decision
from hac.engine import HACEngine
from hac.models import Action


def run_actions(engine: HACEngine, actions: list[Action]) -> list[Decision]:
    return [engine.evaluate(action) for action in actions]