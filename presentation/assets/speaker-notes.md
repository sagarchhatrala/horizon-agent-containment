# HAC Speaker Notes

## Slide Notes

1. Hook
   - Say: "The action was allowed. The capability was not."
   - Explain that HAC is about composition, not one obviously malicious command.

2. Problem
   - Walk through the timeline.
   - The final risk can appear only after state, artifacts, authority, and destinations accumulate.

3. OpenAI / Hugging Face incident
   - Keep this factual and restrained.
   - Say: "This demonstrates the problem class; I am not claiming HAC would have stopped this exact incident."
   - Connect the incident to multi-step behavior, cross-system access, and containment boundaries.

4. Horizons
   - ACB and similar tools are valuable at action and trajectory layers.
   - HAC introduces a different security object: emergent capability in the resulting state.

5. Difference
   - Make this the technical anchor.
   - Action policy asks whether an upload is allowed.
   - HAC asks whether this upload carries secret-derived provenance to an external destination.

6. What HAC tracks
   - Emphasize deterministic state, provenance, authority, trust, and composition.
   - No LLM classifier is used for the security decision.

7. Architecture
   - HAC is a reference-monitor concept between agents and tools.
   - Today it is local and prototype-level; future work is production integration.

8. Model independence
   - Same observable state plus same action means same security decision.
   - Open-weight and closed-weight models use the same containment abstraction.

9. Multi-agent
   - Authority composition is a core risk in swarms.
   - A's access does not become B's access without explicit delegation.

10. Product / market
   - Do not attack competitors.
   - Position HAC as a state/capability layer that can complement gateways, guardrails, identity, observability, and policy engines.

11. Why now
   - More tools, more agents, more authority, and longer tasks create a larger security state.
   - That forces security to move beyond individual actions.

12. Future
   - Separate today from next.
   - This builds credibility with technical judges.

13. Final
   - End on the memorable phrase:
   - "Actions are the primitives. Capabilities are the attack surface."

## 30-Second Pitch

AI agents rarely fail because of one obviously malicious action. The hard failures happen over a long horizon: an agent reads data, creates artifacts, transforms them, gains authority, and eventually creates a capability no single step revealed. HAC is a deterministic containment layer that tracks state, provenance, authority, and trust relationships, then blocks transitions that create forbidden capabilities. Actions are the primitives. Capabilities are the attack surface.

## 60-Second Pitch

Most agent security asks: "Is this action allowed?" That is necessary, but it is not enough for long-horizon agents. A sequence of reasonable actions can compose into something unsafe: read a secret, create a report, transform it, encrypt it, split it, and upload a chunk externally. HAC asks a different question: "What security capability does this transition create?" It tracks artifacts, provenance, credentials, delegation, trust boundaries, graph relationships, and history. The engine is deterministic, model-independent, and fail-closed. It does not call an LLM to decide security. It evaluates the resulting state against invariants like `SECRET_TO_EXTERNAL` and blocks the final transition atomically.

## 2-Minute Pitch

Agents are becoming runtime actors. They read files, call tools, use credentials, write code, contact other agents, and interact with external systems. That means security risk is no longer only about one command or one tool call. It is about what the agent accumulates over time.

HAC, Horizon Agent Containment, is built around that idea. Traditional controls ask whether the current action is allowed. HAC asks what capability the action creates when combined with current security state, history, provenance, authority, and trust relationships.

The prototype demonstrates this with a long-horizon exfiltration chain. The first five steps are allowed: read secret, create artifact, transform, encrypt, and split. The final upload is blocked because the resulting state would move secret-derived data to an external destination. Encryption does not erase provenance.

This is complementary to action-level systems like Agent Circuit Breaker. ACB can inspect actions and trajectories. HAC elevates the security object to emergent capability in evolving state.

The system is deterministic, offline, model-independent, and fail-closed. The roadmap is to turn this into a production reference-monitor layer for agent runtimes, MCP ecosystems, credential brokers, cloud infrastructure, and multi-agent systems.

## 5-Minute Pitch

Start with the hook: the action was allowed, the capability was not.

Explain that modern agents are not chatbots anymore. They are runtime actors. They can read data, create files, execute tools, call services, and hold credentials. The issue is not just one dangerous action. The issue is that capabilities accumulate.

Give the core example. An agent reads a secret for internal analysis. That may be legitimate. It creates an artifact. It transforms it. It encrypts it. It splits it. Each step may be defensible in isolation. But when one chunk is uploaded externally, the resulting state contains a forbidden capability: secret-derived data crossing to an external destination.

Introduce HAC. HAC evaluates:

```text
current security state
+ agent effect
+ history and provenance
= resulting security state
```

Then it asks whether the resulting state violates deterministic security invariants.

Clarify the relationship to existing controls. ACB and other runtime tools remain useful for action-level and trajectory-level enforcement. HAC is not claiming those are useless. It introduces a different abstraction boundary: capability containment.

Mention the OpenAI / Hugging Face incident carefully. It demonstrates the importance of multi-step agent containment, cross-system effects, network isolation, workload isolation, and long-task alignment. Do not claim HAC would have prevented it.

Show what the prototype does today: typed state, graph edges, provenance-preserving transformations, capability detection, invariant checks, fail-closed decisions, atomic blocking, MCP normalization, optional ACB bridge, and 41 collected tests.

End with the product vision: as agents get more tools, longer memory, more credentials, and multi-agent coordination, the security state grows. HAC aims to become a deterministic reference-monitor layer for autonomous systems.

## Judge Q&A

Q: Is HAC just a policy engine?

A: No. A policy engine usually evaluates the current request. HAC evaluates the hypothetical resulting security state and asks whether a new capability has emerged from history, provenance, authority, and relationships.

Q: Doesn't Agent Circuit Breaker already do long-horizon checks?

A: ACB already provides deterministic action-level controls, MCP interception, trajectory checks, run contracts, approvals, and audit evidence. HAC is complementary. HAC elevates the protected object from action or run-contract compliance to the capability created by evolving state.

Q: Is the logic hardcoded?

A: The prototype has implemented invariants as Python code for clarity and testability. The production direction is declarative policy-as-code for invariants, generic effect normalization, and graph reachability checks so teams can configure the security model without writing a custom branch for every tool.

Q: Does HAC depend on GPT, Claude, or another model?

A: No. The model family is recorded for audit context, but the decision is based on observable actions, state, provenance, authority, and invariants.

Q: Does HAC solve prompt injection?

A: No. It can contain some consequences of prompt injection if the injected behavior tries to create forbidden capabilities, but it is not a prompt-injection detector.

Q: What is implemented today?

A: A deterministic local prototype with state, graph, provenance, capability detection, invariants, fail-closed evaluation, long-horizon scenarios, MCP normalization, optional ACB bridge, a Streamlit demo, and tests.

Q: What is future work?

A: Declarative invariants, production integrations, persistent signed state, cloud/IAM/Kubernetes integrations, distributed swarm state, richer MCP middleware, and stronger policy authoring.

## Technical Limitations

- HAC only reasons over actions normalized into its model.
- Resource classifications and trust levels must be supplied by the integrating system.
- The prototype does not perform implicit declassification.
- It does not sandbox execution.
- It does not inspect hidden model reasoning.
- It does not prove network events occurred.
- It does not replace IAM, least privilege, monitoring, isolation, or human approval.
- The current adapter implementations are conceptual, not full production middleware.
- The current invariants are implemented in Python rather than a declarative policy language.

## Demo Transition

After the final slide, switch to the local Streamlit demo:

```bash
python -m streamlit run demo/app.py
```

Show:

1. Normal workflow allows all steps.
2. Data exfiltration allows the first five steps and blocks the final upload.
3. Untrusted privileged execution blocks the final elevated execution.
