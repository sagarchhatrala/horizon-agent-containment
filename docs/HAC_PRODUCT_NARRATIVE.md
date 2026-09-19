# HAC Product Narrative

## Core thesis

"Everyone secures agent actions. HAC secures the capabilities that emerge when those actions are composed over a long horizon."

## Product framing

HAC is a deterministic containment primitive for a class of long-horizon agent failures. It is narrower than a general AI safety solution or a universal policy engine, but it addresses a real and commonly missed problem: the same action sequence that seems safe in isolation can create an unauthorized capability when composed over time.

## Actual repository behavior

The prototype demonstrates this with a secret-exfiltration path:
- read a secret
- create a derived artifact
- transform and encrypt it
- split it into chunks
- attempt an external upload

The early steps are allowed. The `UPLOAD_ARTIFACT` action is blocked because the resulting state develops a `DATA_EXFILTRATION` capability and violates the `SECRET_TO_EXTERNAL` invariant.

## Supported narrative

HAC is designed to:
- evaluate state transitions rather than isolated actions
- preserve and inspect provenance across transformations
- derive capabilities from security state and graph relationships
- enforce deterministic fail-closed invariants
- work across multiple model families without using model-based security scoring

## Unsupported narrative

HAC does not claim to:
- solve all AI safety problems
- guarantee perfect security
- block every possible attack
- replace sandboxing or runtime isolation
- detect prompt injection or malware classification by itself
- be a general-purpose policy system for arbitrary enterprise controls

## Positioning

The product story should emphasize containment, determinism, and long-horizon capability emergence rather than general AI trust or probabilistic risk. The advantage is that the decision is explainable and reproducible: explicit state + explicit provenance + explicit invariants = explicit decision.

---

## Supported Claims

- HAC is a deterministic containment primitive for long-horizon agent capability emergence.
- The prototype evaluates hypothetical state transitions and blocks violations of configured invariants.
- Provenance and classification are preserved across transformations and encryption in the current model.
- The prototype demonstrates secret-derived data crossing a trust boundary as a blocked `DATA_EXFILTRATION` capability.
- The engine is model-independent and not dependent on LLM-based judging.
- The repository includes conceptual MCP and ACB adapters, but the core logic is independent of them.

## Claims We Must Not Make

- "100% secure"
- "solves AI safety"
- "prevents every attack"
- "unhackable"
- "first ever"
- "works against all prompt injection and malware scenarios"
- "performs general-purpose policy evaluation for every enterprise control"
- "is a substitute for sandboxing or runtime isolation"
- "detects all malicious behavior without context"

## Recommended wording

Use language like:
- "prototype"
- "deterministic containment primitive"
- "state-based capability enforcement"
- "long-horizon security invariant enforcement"
- "fail-closed guardrail"

Avoid language that implies universal security guarantees or an all-encompassing AI safety solution.
