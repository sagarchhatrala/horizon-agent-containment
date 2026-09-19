from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from adapters.simulator import run_actions
from hac.engine import HACEngine
from scenarios import data_exfiltration, normal_workflow, privileged_execution


SCENARIOS = {
    "NORMAL WORKFLOW": normal_workflow,
    "DATA EXFILTRATION": data_exfiltration,
    "UNTRUSTED PRIVILEGED EXECUTION": privileged_execution,
}


st.set_page_config(page_title="HAC", layout="wide")
st.title("HAC - Horizon Agent Containment")

scenario_name = st.sidebar.radio("Scenario", list(SCENARIOS))
scenario = SCENARIOS[scenario_name]
engine = HACEngine(scenario.state())
decisions = run_actions(engine, scenario.actions())

agent = engine.state.agents.get("agent-a")
st.subheader("Agent")
st.write({"Agent": agent.agent_id, "Model": agent.model_family, "Trust": agent.trust_level.value})

st.subheader("Action History")
rows = []
for action, decision in zip(scenario.actions(), decisions):
    rows.append(
        {
            "Action": action.action_type.value,
            "Source": action.source or action.resource or "",
            "Destination": action.destination or "",
            "Decision": decision.decision.value,
            "Detected capability": ", ".join(c.capability_type.value for c in decision.capabilities_detected if c.invariant) or "-",
            "Invariant": ", ".join(i.value for i in decision.violated_invariants) or "-",
        }
    )
st.dataframe(rows, use_container_width=True)

latest = decisions[-1]
left, right = st.columns(2)
with left:
    st.subheader("Current Security State")
    st.json(engine.state.to_dict(), expanded=False)
with right:
    st.subheader("Current Transition")
    st.write(
        {
            "Decision": latest.decision.value,
            "Reason": latest.reason,
            "Transition": latest.transition_id,
            "Capabilities": [c.capability_type.value for c in latest.capabilities_detected],
            "Invariant": [i.value for i in latest.violated_invariants],
        }
    )

st.subheader("Capability Graph")
st.dataframe(engine.state.graph.to_dict()["edges"], use_container_width=True)