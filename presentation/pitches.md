# HAC Pitches

## 30-second pitch

Today, most agent security controls ask whether an individual action is safe. But long-horizon agents can compose individually legitimate actions into capabilities nobody explicitly authorized. HAC, Horizon Agent Containment, tracks security state and provenance across the agent's action horizon and deterministically blocks the transition when that composition creates an unauthorized capability. It does not matter whether the agent runs GPT, Claude, Llama, or a custom model. The model makes the decision about what to do; HAC deterministically decides what the environment will allow.

## 60-second pitch

Most agent security tools reason about single actions in isolation. That misses the real failure mode of long-horizon agents: a sequence of safe-looking steps can create a capability no one meant to grant. HAC focuses on the resulting state, not the isolated prompt or tool call.

The prototype maintains security state, provenance, graph relationships, and declared trust boundaries. Each action is evaluated as a hypothetical transition. HAC recomputes the capability graph and checks invariants before committing the change. If a transformation, encryption, or chunking step still preserves the secret lineage, and then an external upload crosses the trust boundary, the transition is blocked as a `DATA_EXFILTRATION` capability.

This is deterministic and model-independent. The model can be GPT, Claude, Llama, or something custom; the decision about whether the environment will allow the transition remains a fixed security rule.

## 2-minute pitch

The core idea behind HAC is simple: agent security fails when action sequences compose into unauthorized capabilities.

Most current controls focus on single actions, such as "is this tool call allowed," "does this prompt look malicious," or "is this action within policy." That helps with obvious misuse, but it misses a deeper class of failures. A long-horizon agent can read a secret, derive an artifact, transform it, encrypt it, split it into chunks, and upload a fragment externally. Each step may appear legitimate on its own. But the composition changes the security state and creates a new capability: data exfiltration.

HAC addresses that by tracking security state, provenance, and graph relationships across the agent's action history. Every action is treated as a hypothetical state transition. Before the transition is committed, HAC recomputes capabilities and evaluates invariants such as `SECRET_TO_EXTERNAL` and `TRUST_BOUNDARY`.

This prototype is deterministic, fail-closed, and model-independent. It does not depend on LLM-based judges, embeddings, or probabilistic scoring. It evaluates a fixed state transition and blocks if the resulting state violates an invariant.

The current prototype demonstrates the attack chain directly: read secret, create artifact, transform, encrypt, chunk, and then block the external upload. The interesting part is not that the final action is suspicious in isolation. It is that the sequence created a capability the environment never authorized.

## 5-minute technical explanation

HAC is a deterministic containment primitive for a class of long-horizon agent failures. The repository implements this as a state-transition system rather than a policy engine.

At a high level, the model is:

```text
CURRENT SECURITY STATE
+
AGENT EFFECT
+
HISTORY / PROVENANCE
=
RESULTING SECURITY STATE
```

The prototype tracks:
- agents and their trust level
- artifacts and their classification
- resources and trust boundaries
- credentials and authority
- provenance lineage across transformations
- graph edges showing reads, writes, derives, and trust relationships
- historical actions and capability recomputation

Each action is normalized into the `Action` dataclass and evaluated as a hypothetical transition in `HACEngine.evaluate()`. The engine validates the state and action, applies the transition to a clone, recomputes capabilities, and then checks invariants. If any invariant fails, the transition is blocked. Otherwise the state is committed.

The main detection path is:
- `transitions.py` applies transformations and preserves provenance
- `provenance.py` carries source IDs and classifications forward
- `capabilities.py` identifies capability creation like `DATA_EXFILTRATION` or `UNTRUSTED_EXECUTION`
- `invariants.py` maps capability violations to invariant names like `SECRET_TO_EXTERNAL`
- `engine.py` rejects the transition if any invariant is violated

The primary demonstration is the exfiltration scenario in `scenarios/data_exfiltration.py`. The flow is: read a secret, create a derived artifact, transform it, encrypt it, split it into chunks, and then attempt an external upload. The earlier actions are allowed, because they preserve lineage and do not yet cross an external boundary. The final upload is blocked because it would create a secret-derived artifact crossing to a public external destination.

This is not a claim that HAC solves every agent failure. The project explicitly states a narrower scope in the threat model: secret-derived data leaving the trusted environment, untrusted artifacts executing with elevated privilege, credential misuse, trust-boundary crossings, and provenance loss through transformation or encryption.

The strength of the approach is determinism. The decision is not made by a judge model or an ML classifier. It is derived from explicit state, provenance, and invariant logic. That makes the decision explainable, reproducible, and compatible across different agent backends such as GPT, Claude, Llama, or other open-weight models.
