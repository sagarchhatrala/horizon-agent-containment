# HAC Judge Questions and Factual Answers

## Why isn't this just a policy engine?
Because HAC evaluates the resulting security state after a hypothetical action, not just whether an individual action matches a static allowlist or blocklist. Its key primitive is capability emergence over a stateful action sequence, with provenance and invariant checks.

## How do you define a capability?
In this prototype, a capability is a state-derived security property that emerges when an artifact, credential, or trust relationship crosses a boundary or violates an invariant. Examples include `DATA_EXFILTRATION`, `UNTRUSTED_EXECUTION`, and `CREDENTIAL_ESCALATION`.

## How is capability detection deterministic?
Capabilities are recomputed from the current `SecurityState`, the action history, artifact provenance, and resource trust classifications. The logic is explicit and rule-based in `src/hac/capabilities.py`; there is no ML or probability-based scoring.

## What happens if a rule is missing?
The current implementation is fail-closed: if validation fails, state is malformed, or a reference cannot be verified, the action is blocked. A missing rule is not an excuse to continue; the engine rejects the transition rather than assume safety.

## How does provenance survive transformations?
The prototype preserves source IDs and classification sets through `inherit_provenance()` in `src/hac/provenance.py`. Transformations, encryption, compression, and chunking keep the secret lineage and classification attached to the derived artifact unless a process explicitly marks declassification (which the prototype does not implement).

## What happens with encryption?
Encryption is allowed in the prototype as long as it does not create a disallowed resulting state. The security model explicitly states that encryption, compression, chunking, and transformation preserve provenance and classification. This means encryption alone does not neutralize the invariant check.

## Does this work with GPT?
Yes, in the sense that the system is model-independent. The repository records the model family on the agent, but the security decision is based on state transition logic, not on the model. The prototype is not GPT-specific.

## Does this work with Claude?
The same answer applies: the design is model-independent. The architecture is not restricted to a single model provider.

## Does this work with Llama?
Yes, the prototype is not tied to a specific model family. The logic is backend-agnostic.

## Does this work with open-weight models?
Yes, this is compatible with open-weight models, because the decision logic runs on the environment state rather than evaluating the model for trust or risk.

## Does this require MCP?
No. The repository includes an `adapters/mcp.py` conceptual adapter, but the core HAC logic does not require MCP. It can be used with normalized actions and state transitions independent of the transport mechanism.

## What happens if the agent is compromised?
HAC is not a guarantee against all malicious behavior or prompt injection. Its scope is a deterministic containment layer for security-state capability violations. If the compromised agent can still generate actions that are accepted and validated by the environment, the engine will still evaluate those actions using the same state transition logic. In other words, HAC is a containment primitive, not a full endpoint defense or sandbox.

## How does ACB fit?
ACB is an optional action-level enforcement bridge described in `docs/ARCHITECTURE.md`. HAC is the stateful containment layer; ACB is the concept of integrating that logic with an action-level control plane or runtime boundary. It is not the same thing as the core HAC engine.

## What does HAC NOT protect against?
It does not claim to detect prompt injection, malware classification, network reputation, embedding similarity, or all possible attacks. It also does not provide full sandboxing or runtime isolation. Those are explicitly out of scope in `docs/THREAT_MODEL.md`.

## What is production missing?
The current prototype is a minimal deterministic engine. Production would need operational integration with resource classification feeds, trust propagation across systems, runtime enforcement boundaries, secrets management, credential and authorization plumbing, and broader policy orchestration across containers, Kubernetes, cloud, and cross-agent communication.

## Why can't the agent simply bypass HAC?
HAC is designed as a fail-closed enforcement layer around the state transition. If the action cannot be normalized or validated, or if the resulting state violates invariants, the transition is rejected. The current implementation does not rely on an LLM judge or a side channel; it forces the action to pass through the deterministic state evaluation before commit.
