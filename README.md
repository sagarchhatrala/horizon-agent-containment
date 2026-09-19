# HAC - Horizon Agent Containment

AI agents rarely fail because of one obviously malicious action. Long-horizon failures emerge when individually legitimate actions compose into an unauthorized capability.

Traditional agent security:

```text
Action -> Policy
```

HAC:

```text
Action -> State Transition -> Capability -> Invariant
```

HAC is a deterministic containment primitive for a class of long-horizon security failures. It does not claim to solve every agent attack, and it does not depend on LLMs, ML models, embeddings, model reputation, or external threat intelligence.

## Prototype

The prototype tracks agents, resources, artifacts, credentials, provenance, delegations, graph edges, capabilities, and action history. Each action is evaluated as a hypothetical transition and committed only if the resulting state preserves all configured security invariants.

Primary demonstration:

```text
READ SECRET       ALLOW
CREATE ARTIFACT   ALLOW
TRANSFORM         ALLOW
ENCRYPT           ALLOW
CHUNK             ALLOW
EXTERNAL UPLOAD   BLOCK
```

The final step is blocked because the resulting state would create a `DATA_EXFILTRATION` capability: secret-derived data crossing to an external destination.

## Run Tests

```bash
python -m pytest
```

## Run Demo

```bash
python -m streamlit run demo/app.py
```

The repository includes `.streamlit/config.toml` so the demo runs locally on `localhost`, headless, with Streamlit usage telemetry disabled.

Quick local checks:

```bash
curl -I http://localhost:8501
curl http://localhost:8501/_stcore/health
```

## Pitch Deck

The GitHub Pages-ready pitch deck is in `presentation/`.

Open locally:

```bash
presentation/index.html
```

Serve locally:

```bash
python -m http.server 8766
```

Then open:

```text
http://127.0.0.1:8766/presentation/
```

Deploy with GitHub Pages:

1. Push the repository to GitHub.
2. In GitHub, open `Settings -> Pages`.
3. Set source to `Deploy from a branch`.
4. Select the branch and repository root.
5. Open `/presentation/` on the generated Pages URL.

The deck is static HTML/CSS/JavaScript, has no external runtime dependencies, supports keyboard navigation, and includes print/PDF styles.

## Layout

- `src/hac/`: core deterministic engine.
- `adapters/`: conceptual simulator, MCP, and ACB adapters.
- `scenarios/`: normal workflow and attack workflows.
- `tests/`: deterministic, fail-closed, provenance, capability, adapter, and long-horizon tests.
- `demo/`: Streamlit visualization.
- `docs/`: architecture, security model, and threat model.
