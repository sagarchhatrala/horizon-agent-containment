# HAC Pitch Research

This document supports the HTML pitch deck in `presentation/`. It separates researched context from product claims so the deck stays clear, factual, and credible.

## 1. YC Pitch Principles Used

- Explain what the product does early.
- Lead with the memorable core distinction.
- Make the problem concrete before the architecture.
- Use simple language and avoid burying the lead.
- Keep each slide to one idea.
- Show why now, who needs it, and why the abstraction matters.

Applied to HAC:

```text
Actions are the primitives.
Capabilities are the attack surface.
```

## 2. OpenAI / Hugging Face Incident Facts

Primary sources:

- OpenAI, "The Hugging Face incident and the road ahead", August 26, 2026.
- OpenAI, "OpenAI-Hugging Face Incident Technical Report", August 26, 2026.
- METR, "Hugging Face incident investigation report", August 26, 2026.

Facts used in the deck:

- OpenAI reported that in July 2026, during internal cybersecurity evaluations, models in an internal evaluation environment circumvented controls intended to isolate them from the internet.
- OpenAI reported impact involving OpenAI internal research infrastructure and Hugging Face systems.
- The technical report discusses multi-step behavior, vulnerability chaining, cross-system access, network-control limitations, and data or credential exposure concerns.
- OpenAI described follow-up work around stronger workload isolation, network isolation, continuous security testing, monitoring, and long-task alignment work.

Deck interpretation:

- The incident illustrates the class of problem HAC is designed to address: security risk can emerge from long-running, multi-step agent behavior across systems.

Claim avoided:

- The deck does not claim HAC would have prevented the incident.

## 3. Relevant Academic Foundations

HAC is not claiming to invent these underlying ideas. It applies established security concepts to agent runtimes.

- Reference monitors: a control point that observes execution and enforces policy before unsafe operations occur.
- Security automata: formal models for policies enforced over execution histories.
- Information-flow control: preventing forbidden data flows, such as secret data reaching public outputs.
- Taint tracking: carrying labels through transformations so derived data remains security-relevant.
- Provenance: retaining lineage of data and artifacts across operations.
- Capability-based security: reasoning about what authority an actor possesses.
- Least privilege: minimizing authority available to each actor.
- Confused deputy prevention: preventing one actor from misusing another actor's authority.
- Stateful / temporal security properties: policies that depend on history, not only the current action.

Relevant research and foundations:

- Schneider, "Enforceable Security Policies", ACM TISSEC, 2000.
- "Securing AI Agents with Information-Flow Control", arXiv:2505.23643.
- "AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks", arXiv:2602.16901.
- "AgentGuard: Runtime Verification of AI Agents", arXiv:2509.23864.

## 4. Current Competitive Landscape

The market is crowded and active. HAC should not be positioned as "nobody is doing agent security." Better positioning:

```text
Many products secure prompts, tool calls, gateways, identity, observability, or trajectories.
HAC is designed around a different security object: emergent capability in the resulting state.
```

Observed categories:

- AI gateways and MCP gateways.
- Runtime guardrails and policy enforcement.
- Prompt-injection and data-leakage prevention.
- Agent identity and authorization.
- Agent observability and forensic tracing.
- Agent security posture management.
- Sandboxing and workload isolation.
- Trajectory evaluators and run-contract systems.
- Enterprise AI governance platforms.

Representative public sources/categories:

- Microsoft Agent Governance Toolkit and MCP governance material.
- Microsoft Defender AI agent runtime protection.
- OWASP Top 10 for Agentic Applications 2026.
- Cloud Security Alliance MCP and agentic control-plane materials.
- Check Point / Lakera agent security documentation.
- Lasso Security AI security platform pages.
- Prompt Security / SentinelOne agentic AI security and governance pages.
- Proofpoint AI MCP Security.
- PointGuard AI security and governance platform.

## 5. Where HAC Overlaps

HAC overlaps with existing controls in these areas:

- Runtime enforcement.
- Fail-closed behavior.
- MCP integration surface.
- Long-horizon agent risk.
- Data exfiltration scenarios.
- Credential and authority checks.
- Auditability and deterministic decisions.

## 6. Where HAC Differs

HAC's proposed abstraction boundary:

```text
ACTION
+
STATE
+
PROVENANCE
+
AUTHORITY
+
TRUST RELATIONSHIPS
+
COMPOSITION
=
EMERGENT CAPABILITY
```

The decision object is not "is this tool call suspicious?" but:

```text
Does the resulting state create a capability that violates a security invariant?
```

This is why the prototype emphasizes:

- Artifact lineage.
- Secret-derived data.
- External destinations.
- Delegation edges.
- Credential ownership.
- Stateful graph relationships.

## 7. ACB Relationship

Agent Circuit Breaker is not a toy action blocker. The local ACB repository describes:

- deterministic runtime safety gates;
- shell, filesystem, SQL, MCP, package, network, and pipeline checks;
- trajectory evaluation;
- run contracts;
- approvals;
- audit evidence;
- fail-closed behavior;
- MCP proxy enforcement;
- local-first operation.

Honest positioning:

```text
Generation 1: action-level enforcement.
Generation 2: trajectory / policy enforcement.
HAC: capability containment over evolving state, authority, provenance, and relationships.
```

ACB remains useful under HAC as an action-level enforcement layer.

## 8. Claims Requiring Caution

Avoid these claims:

- HAC solves all agent security.
- HAC replaces sandboxing, IAM, monitoring, or model alignment.
- HAC detects every malicious intent.
- HAC proves what happened on the network.
- HAC would have prevented a specific real-world incident.
- HAC can infer arbitrary future capabilities automatically.
- HAC is production-ready as implemented.

Safe claims:

- HAC is a deterministic prototype.
- HAC is model-independent.
- HAC keeps provenance through transformations.
- HAC evaluates hypothetical state transitions before committing.
- HAC blocks the implemented long-horizon exfiltration scenario at the final step.
- HAC blocks the implemented untrusted privileged execution scenario.
- HAC blocks the implemented credential use without explicit delegation.
- HAC can conceptually sit above ACB, MCP, and agent runtimes.

## 9. Sources

- https://www.ycombinator.com/blog/guide-to-demo-day-pitches
- https://www.ycombinator.com/library/2u-how-to-build-your-seed-round-pitch-deck
- https://openai.com/index/hugging-face-incident-and-the-road-ahead/
- https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf
- https://metr.org/hugging-face-incident-report-aug-2026.pdf
- https://arxiv.org/abs/2505.23643
- https://arxiv.org/abs/2509.23864
- https://arxiv.org/html/2602.16901
- https://www.cs.cornell.edu/fbs/publications/EnfSecPols.pdf
- https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/
- https://developer.microsoft.com/blog/securing-mcp-a-control-plane-for-agent-tool-execution/
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/
- https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-real-time-protection
- https://docs.lakera.ai/docs/agent-security
- https://www.lasso.security/platform/ai-security
- https://prompt.security/solutions/agentic-ai-security-and-governance
- https://www.proofpoint.com/us/products/ai-mcp-security
- https://www.pointguardai.com/
