# HAC Security Model

The central primitive is:

```text
CURRENT SECURITY STATE
+
AGENT EFFECT
+
HISTORY / PROVENANCE
=
RESULTING SECURITY STATE
```

The security decision is based on the resulting state. This allows HAC to block long-horizon failures where each individual action may look legitimate.

## Properties

- Deterministic: identical state plus identical action yields the same decision.
- Model-independent: model family is recorded but not used for authorization.
- Fail-closed: unverifiable state, malformed actions, unknown references, and unknown action types block.
- Stateful: graph, artifacts, delegations, credentials, and history survive across actions.
- Provenance-aware: derived artifacts inherit source provenance.
- Capability-aware: capabilities are derived from state relationships.

## Implemented Invariants

- `SECRET_TO_EXTERNAL`: secret or highly sensitive derived data cannot reach an external or public destination.
- `UNTRUSTED_TO_PRIVILEGED`: untrusted/external artifacts cannot execute with elevated privilege without explicit authorization.
- `NON_TRANSITIVE_AUTHORITY`: using a service does not grant that service owner's authority.
- `EXPLICIT_DELEGATION`: another agent's credential requires explicit delegation.
- `CREDENTIAL_ESCALATION`: agents cannot acquire credentials outside declared authority.
- `TRUST_BOUNDARY`: trust-boundary crossings must be explicitly authorized.

## Declassification

The prototype implements no implicit declassification. Encryption, compression, chunking, and transformation preserve provenance and classification.