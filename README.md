# HAC - Horizon Agent Containment

**Deterministic containment for long-horizon AI agents.**

AI agents rarely fail because of one obviously malicious action. Long-horizon failures emerge when individually legitimate actions compose into an unauthorized capability.

HAC is a prototype security primitive for that class of failure. It tracks the security state created by an agent over time, derives capabilities from that state, and blocks transitions that violate deterministic security invariants.

```text
Traditional control:
Action -> Policy -> Allow / Block

HAC:
Action -> State Transition -> Capability Graph -> Security Invariant -> Allow / Block
```

Core idea:

```text
CURRENT SECURITY STATE
+
AGENT EFFECT
+
HISTORY / PROVENANCE
=
RESULTING SECURITY STATE
```

The decision is based on the resulting state, not on an LLM, embedding score, model reputation, or external threat feed.

## Status

HAC is a hackathon-stage prototype with a working deterministic engine, tests, scenarios, Streamlit demo, MCP conceptual adapter, and optional Agent Circuit Breaker bridge.

It is intended to demonstrate a security architecture idea:

> Actions are the primitives. Capabilities are the attack surface.

HAC does not claim to solve all agent security, replace sandboxing, replace IAM, replace monitoring, or prevent every real-world incident. It provides deterministic containment around explicitly modeled state, provenance, authority, and capability invariants.

## Live Materials

- Pitch deck: https://sagarchhatrala.github.io/horizon-agent-containment/presentation/
- Personal-site deck mirror: https://sagarchhatrala.github.io/hac/

The authoritative executable demo remains the local Streamlit app:

```bash
python -m streamlit run demo/app.py
```

## What HAC Demonstrates

The primary long-horizon scenario:

```text
READ SECRET        ALLOW
CREATE ARTIFACT    ALLOW
TRANSFORM          ALLOW
ENCRYPT            ALLOW
CHUNK              ALLOW
EXTERNAL UPLOAD    BLOCK
```

The final step is blocked because the resulting state would create:

```text
SECRET-DERIVED DATA -> EXTERNAL DESTINATION
```

That is a `DATA_EXFILTRATION` capability violating the `SECRET_TO_EXTERNAL` invariant.

Encryption, compression, chunking, and transformation do not erase provenance.

## Implemented Capabilities

HAC deterministically derives capabilities from state, graph relationships, action history, provenance, trust, and authority.

Implemented capability types include:

- `DATA_EXFILTRATION`
- `UNTRUSTED_EXECUTION`
- `PRIVILEGED_EXECUTION`
- `CREDENTIAL_DELEGATION`
- `UNAUTHORIZED_EXTERNAL_ACCESS`
- `CREDENTIAL_ESCALATION`
- `TRUST_BOUNDARY_CROSSING`
- `NON_TRANSITIVE_AUTHORITY`

## Implemented Invariants

- `SECRET_TO_EXTERNAL`: secret or highly sensitive derived data must not reach an external/public destination.
- `UNTRUSTED_TO_PRIVILEGED`: untrusted or external artifacts must not execute with elevated privilege without authorization.
- `NON_TRANSITIVE_AUTHORITY`: using a service does not automatically grant that service owner's authority.
- `EXPLICIT_DELEGATION`: another agent's credential requires explicit delegation.
- `CREDENTIAL_ESCALATION`: agents cannot acquire credentials outside declared authority.
- `TRUST_BOUNDARY`: crossing a trust boundary must be explicitly represented and authorized.

## Design Properties

- **Deterministic**: same state plus same action produces the same decision.
- **Model-independent**: model family is recorded but does not drive authorization.
- **Fail-closed**: unknown agents, resources, actions, malformed inputs, invalid state, or missing provenance block.
- **Stateful**: graph, artifacts, credentials, delegations, capabilities, and history survive across actions.
- **Provenance-aware**: derived artifacts retain lineage from source data.
- **Capability-aware**: decisions are based on what the resulting state enables.
- **Offline core**: no network calls, LLM calls, ML models, embeddings, or external threat intelligence are required.

## Architecture

```text
Agent Action
    |
    v
Validate action, actor, resources, credentials
    |
    v
Clone committed security state
    |
    v
Apply hypothetical transition
    |
    v
Update provenance + graph + history
    |
    v
Recompute capabilities
    |
    v
Evaluate invariants
    |
    +--> ALLOW: commit resulting state
    |
    +--> BLOCK: discard hypothetical state
```

Blocked actions are atomic: the committed state is not mutated.

## Relationship To Agent Circuit Breaker

HAC is independent, but optionally integrable with Agent Circuit Breaker.

The intended layering is:

```text
Generation 1: Action-level enforcement
"What is this tool call about to do?"

Generation 2: Trajectory / policy enforcement
"Is this run still inside the declared boundary?"

HAC: Capability containment
"What capability has emerged from accumulated state, authority, provenance, and relationships?"
```

Agent Circuit Breaker remains useful underneath HAC as an action-level and trajectory-level enforcement layer. HAC introduces a different abstraction boundary: evaluating emergent capability in the resulting security state.

## Install

Requirements:

- Python 3.10+
- No runtime dependencies for the core engine
- Optional: `pytest` for tests
- Optional: `streamlit` for the demo

Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev,demo]"
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,demo]"
```

## Run Tests

```bash
python -m pytest
```

Current local validation: `41 passed`.

## Run Local Demo

```bash
python -m streamlit run demo/app.py
```

Open:

```text
http://localhost:8501
```

The Streamlit demo shows:

- agent identity and model family;
- action history;
- current security state;
- current transition;
- detected capability;
- violated invariant;
- capability graph.

## Run Static Pitch Deck

Open directly:

```text
presentation/index.html
```

Or serve locally:

```bash
python -m http.server 8766
```

Then open:

```text
http://127.0.0.1:8766/presentation/
```

The deck is static HTML/CSS/JavaScript with no external runtime dependencies. It supports keyboard navigation, fullscreen mode, and print/PDF export.

## Project Layout

```text
src/hac/        core deterministic engine
adapters/       simulator, MCP, and ACB adapters
scenarios/      normal workflow and attack scenarios
tests/          deterministic, fail-closed, provenance, capability, adapter tests
demo/           local Streamlit visualization
docs/           architecture, security model, threat model, pitch research
presentation/   GitHub Pages-ready pitch deck
```

## Security Boundaries

HAC is not:

- an LLM alignment system;
- a prompt-injection detector;
- a sandbox;
- an antivirus engine;
- an IAM provider;
- a network firewall;
- a complete data-loss-prevention platform;
- a replacement for monitoring, isolation, approvals, or least privilege.

HAC is:

- a deterministic state-transition evaluator;
- a provenance-preserving containment primitive;
- a capability graph and invariant checker;
- a prototype for long-horizon agent security research and product exploration.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Security Model](docs/SECURITY_MODEL.md)
- [Threat Model](docs/THREAT_MODEL.md)
- [Pitch Research](docs/PITCH_RESEARCH.md)

## License

Prototype repository for hackathon and research demonstration purposes. Add an explicit open-source license before production reuse or external contribution intake.
