# HAC Threat Model

HAC targets long-horizon agent failures where safe-looking steps compose into a dangerous resulting capability.

## In Scope

- Secret-derived data leaving the trusted environment.
- Untrusted downloaded artifacts executed with elevated privilege.
- Credential use without explicit delegation.
- Credential acquisition outside declared authority.
- Trust-boundary crossings hidden across multiple steps.
- Provenance loss through transformation, encryption, compression, or chunking.

## Out of Scope

- LLM prompt injection detection.
- Malware classification.
- Network reputation.
- Embedding similarity.
- Probabilistic risk scoring.
- Full sandboxing or runtime isolation.
- Complete prevention of every possible agent attack.

## Assumptions

Actions are normalized into HAC's `Action` model before evaluation. Resource classifications and trust levels are supplied by the integrating system. HAC fails closed when it cannot verify an action or state.