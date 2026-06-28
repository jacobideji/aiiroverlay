<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Crosswalk — AI IR Overlay vs OWASP Top 10 for Agentic Applications 2026                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Mappings to all 10 ASI risks: ASI01–ASI10.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Crosswalk: AI IR Overlay ↔ OWASP Top 10 for Agentic Applications 2026

OWASP's Agentic Top 10 (released December 2025 by the OWASP GenAI Security Project) is the most current ranking of risks specific to autonomous and agentic AI. The 10 risks (ASI01–ASI10) cover goal hijacking, tool misuse, identity abuse, supply chain, code execution, memory poisoning, inter-agent communication, cascading failures, human-agent trust, and rogue behavior.

The AI IR Overlay provides the **operational machinery** (inventory, staged containment, evidence preservation, controlled recovery) for **responding to incidents** in each ASI category. OWASP categorizes what can go wrong. The AI IR Overlay specifies how to detect, contain, prove, and recover when it does.

## At a Glance

| ASI Risk | Primary AI IR Overlay Controls | Most Relevant Artifacts |
|---|---|---|
| **ASI01** Agent Goal Hijack | MVO-3 Evidence + Triage Q1 | Prompt/response logs (A) · config snapshot (E) |
| **ASI02** Tool Misuse & Exploitation | MVO-1 Inventory + MVO-2 Safe Modes (M3) + Triage Q1, Q5 | Agent Privilege Matrix · tool-call ledger (B) |
| **ASI03** Identity & Privilege Abuse | MVO-1 Inventory + Triage Q3 | AI-BOM `identity` section · SaaS audit logs (F) |
| **ASI04** Agentic Supply Chain Compromise | MVO-1 Inventory + MVO-3 Evidence | AI-BOM `model` + `retrieval` sections · config snapshot (E) |
| **ASI05** Unexpected Code Execution | MVO-2 Safe Modes (M4) + Triage Q1, Q5 | Tool-call ledger (B) · Kill-Switch M4 |
| **ASI06** Memory & Context Poisoning | MVO-1 Inventory + MVO-3 Evidence + Mental Model | Memory snapshot (D) · retrieval traces (C) |
| **ASI07** Insecure Inter-Agent Communication | MVO-1 Inventory + MVO-3 Evidence | AI-BOM `tools` section · tool-call ledger (B) |
| **ASI08** Cascading Agent Failures | MVO-2 Safe Modes (M3 + M4) + MVO-4 Controlled Re-Enable | Kill-Switch ladder · staged recovery sequence |
| **ASI09** Human-Agent Trust Exploitation | Mental Model + Maturity Roadmap | Operating cadence · drill design |
| **ASI10** Rogue Agents | MVO-2 Safe Modes (M4) + MVO-3 Evidence | Full A–F evidence set · Kill-Switch M4 |

## Detailed Mappings

### ASI01: Agent Goal Hijack

**Threat:** Prompt injection, indirect prompt injection, or context manipulation that causes the agent to pursue an attacker's goal instead of the user's.

**AI IR Overlay response:**

- **MVO-3 Minimum Evidence Set, type A (Prompt/Response Record)** is the primary forensic artifact. It captures the injected payload, the resulting plan, and the deviation from intended behavior.
- **MVO-3, type E (Configuration Snapshot)** captures the system prompt and guardrails in effect at the time of hijack. Essential to prove the agent's intended scope.
- **Six Triage Questions Q1** ("What tools can the agent call?") scopes the blast radius of the hijacked plan before containment.

**Operational priority:** Preserve A and E **before** rotating the system prompt or retraining. The rush-to-fix often destroys the evidence needed to prove what the agent was instructed to do.

### ASI02: Tool Misuse & Exploitation

**Threat:** The agent invokes legitimate tools in unintended ways (e.g., sending mass emails, deleting records, triggering financial actions) due to malicious instruction or buggy planning.

**AI IR Overlay response:**

- **MVO-1 Inventory.** The **Agent Privilege Matrix** (T0/T1/T2 tiering) is the pre-incident control. Every tool is pre-classified by risk so containment can be surgical, not binary.
- **MVO-2 Safe Modes, Mode M3 (Tool Tiering).** The operational mechanism. Disable T2 tools, keep T0/T1, business continues.
- **MVO-3, type B (Tool-Call Ledger).** Captures both attempted and successful calls. Denied calls are evidence of intent.
- **Triage Q1 + Q5.** First-hour discipline matches threat to least-disruptive safe mode.

**Operational priority:** Pre-tier tools (see the [Agent Privilege Matrix](../templates/agent-privilege-matrix.csv) and its [README](../templates/README-privilege-matrix.md)). Without this, M3 can't execute under pressure. The pre-incident discipline is operationalized in [Playbook 04: Tool Design Is Containment](../playbooks/04-tool-design-is-containment.md).

### ASI03: Identity & Privilege Abuse

**Threat:** The agent's service account, delegated OAuth grant, or impersonation token has more privilege than its task requires, and that excess is exploited.

**AI IR Overlay response:**

- **MVO-1 Inventory.** AI-BOM's `identity` section is the authoritative record: principal, scopes, rotation cadence. Reviewed in PAM cadence per the Mental Model clause *"if it can act, govern it as a privileged identity."*
- **Triage Q3** ("What identity does it run as?") immediately scopes downstream audit trails and accountability.
- **MVO-3, type F (Identity and SaaS Audit-Log Correlation).** The downstream evidence proving what the identity touched, with which target systems.

**Operational priority:** AI-BOM `identity` section **must** include scopes and rotation cadence. Otherwise audit becomes guesswork.

### ASI04: Agentic Supply Chain Compromise

**Threat:** Compromised models, retrieval corpora, tool definitions, or middleware libraries inject malicious behavior upstream of any individual agent.

**AI IR Overlay response:**

- **MVO-1 Inventory.** AI-BOM's `model` (provider, model ID, version pinning, fallback) and `retrieval` (corpora, URIs, sensitivities, refresh cadences) sections are the supply-chain manifest.
- **MVO-3, type E (Configuration Snapshot).** Captures tool definitions and retriever settings at incident time, enabling supply-chain forensics.
- **Mental Model clause 3** ("if it can retrieve, protect it as a production system"): corpora updates are change-control events, tracked in CMDB.

**Operational priority:** Pin model versions in AI-BOM and treat corpus refreshes as production deployments.

### ASI05: Unexpected Code Execution

**Threat:** The agent triggers execution of arbitrary code via tools like code interpreters, shell tools, or sandboxes, beyond what the user or operator intended.

**AI IR Overlay response:**

- **MVO-2 Safe Modes, Mode M4 (Full Disable).** When code execution is the harm vector, M4 is appropriate. The cost of staged containment exceeds the cost of stopping execution.
- **MVO-3, type B (Tool-Call Ledger).** Must capture every code-execution invocation with parameters and results, with retention long enough for forensics.
- **Triage Q1 + Q5.** Q1 lists the code-execution tools, Q5 confirms M4 is the right response.

**Operational priority:** Code-execution tools are Tier-T2 by default in the Privilege Matrix. Require approvals (M2) at minimum, disable on suspicion.

### ASI06: Memory & Context Poisoning

**Threat:** Adversarial content persisted in agent memory (per-user or shared) or injected into retrieved context causes downstream actions to be poisoned across sessions.

**AI IR Overlay response:**

- **MVO-1 Inventory.** AI-BOM's `memory` section (scope: off / per-user / shared, retention, classification) and `retrieval` section are the inventory artifacts.
- **Mental Model clause 2** ("if it can remember, treat it as a data store"): memory falls under SOC 2, HIPAA, GDPR, and PCI assessments.
- **MVO-3, type D (Memory Snapshot).** Captures persistent context at incident time. Without it, you can't prove cross-session bleed.
- **MVO-3, type C (Retrieval Traces).** Captures what the agent retrieved, from which corpus, at which version, with what scores. Without this, the input vector is unprovable.

**Operational priority:** If memory is `scope: shared`, treat memory bleed across users as its own incident class. Capture D **before** cleaning or rotating memory.

### ASI07: Insecure Inter-Agent Communication

**Threat:** Agents communicating via standardized protocols (e.g., MCP) trust each other's outputs without verification, propagating attacks across an agent mesh.

**AI IR Overlay response:**

- **MVO-1 Inventory.** AI-BOM's `tools` section must capture inter-agent connectors and the agents on the other end (treat them as external systems). The agent-dependency graph specified in [Playbook 08](../playbooks/08-multi-agent-blast-radius.md) lives here.
- **MVO-3, type B (Tool-Call Ledger).** Captures messages exchanged across agents, with parameters and results. Each cross-agent message carries a trace ID per [Playbook 08](../playbooks/08-multi-agent-blast-radius.md).
- **Mental Model clause 4** ("if it can change, manage it as software"): inter-agent protocols are infrastructure, so deployment requires review.

**Operational priority:** Each inter-agent connector counts as a distinct tool in the Privilege Matrix and must be tier-classified. The full operational response (structured handoff contracts, bounded delegation at 2 hops, orchestrator-first containment, cascade-isolation gates) is specified in [Playbook 08: Multi-Agent Systems Multiply Blast Radius](../playbooks/08-multi-agent-blast-radius.md).

### ASI08: Cascading Agent Failures

**Threat:** One failing or compromised agent triggers a cascade of failures across other agents that depend on its outputs, magnifying the blast radius.

**AI IR Overlay response:**

- **MVO-2 Safe Modes, Modes M3 + M4 plus orchestrator-first containment.** [Playbook 08](../playbooks/08-multi-agent-blast-radius.md) specifies the orchestrator-first sequence: stop the orchestrator before the originating agent to halt further delegation system-wide. Cascade propagation typically runs 5 to 30 seconds, so the framework's containment latency requirement is sub-60-second automation per [Playbook 11](../playbooks/11-monitoring-detection.md).
- **MVO-4 Controlled Re-Enable.** Staged recovery is **mandatory** to prevent re-triggering the cascade during restoration. The dependency-graph re-enablement order specified in [Playbook 08](../playbooks/08-multi-agent-blast-radius.md) re-enables agents from the leaves of the dependency graph inward; the orchestrator is the last component re-enabled.
- **Maturity Roadmap Level 4 (Resilient).** Quarterly tabletops should include a cross-agent failure scenario.

**Operational priority:** Inventory must capture inter-agent dependencies (which agents depend on which). [Playbook 08](../playbooks/08-multi-agent-blast-radius.md) specifies the dependency graph as a load-bearing artifact in the AI-BOM.

### ASI09: Human-Agent Trust Exploitation

**Threat:** Humans develop excessive trust in agent outputs and act on bad recommendations (e.g., a finance copilot recommends an urgent payment based on a poisoned invoice).

**AI IR Overlay response:**

- **Mental Model.** The four-clause discipline is the operator-level countermeasure. Every agent output is a *recommendation*, not an *order*. Human review remains the control of last resort for high-impact actions.
- **MVO-2 Safe Modes, Mode M2 (Approvals Required).** Pre-positioned two-person rule for high-impact actions (financial, external-facing).
- **Maturity Roadmap Level 4 (Resilient).** Quarterly tabletops should include a trust-exploitation scenario where the agent's recommendation is subtly wrong.

**Operational priority:** Drills should include both *agent is wrong* and *user trusts incorrect output* scenarios. Without operator training, the technical controls have a human-shaped hole.

### ASI10: Rogue Agents

**Threat:** An agent's behavior drifts from its intended function due to reward hacking, goal drift, or collusion with other agents. The drift goes undetected until material harm occurs.

**AI IR Overlay response:**

- **MVO-2 Safe Modes, Mode M4 (Full Disable).** Once rogue behavior is confirmed, full disable preserves the state for forensics.
- **MVO-3 Minimum Evidence Set (full A–F).** Rogue-agent investigations are often complex and benefit from the **entire** evidence set, not just one type.
- **Maturity Roadmap Level 3 (Provable).** The ability to export the full A–F set within 60 minutes is the precondition for proving what a rogue agent did.

**Operational priority:** Define drift detection criteria pre-incident. A "rogue" determination is a category jump that requires CISO/IC approval, not a Tier-1 SOC call.

## How to Use This Crosswalk

When responding to a threat report, security researcher disclosure, or auditor question framed in OWASP ASI terms, this crosswalk provides direct evidence of AI IR Overlay readiness.

**Example:** *"Walk us through how your organization would detect, contain, and recover from an ASI06 Memory & Context Poisoning incident."*

**Answer:** *"Our [AI-BOM](../templates/ai-bom.yaml) documents memory scope (per-user vs shared), retention, and sensitivity classification for every agent. Detection sources include Type-A prompt logs and Type-C retrieval traces. Containment uses M3 (Tool Tiering) if a single tool is the carrier, M4 (Full Disable) if memory bleed is confirmed. Pre-containment, we capture Type-D (Memory Snapshot) and Type-C (Retrieval Traces) to preserve the input vector. Recovery follows M5 with corpus version verification before re-enabling memory. Our quarterly tabletops include a memory-poisoning scenario per Level 4 (Resilient) maturity. For the full ASI06 response procedure, see [Playbook 03: RAG / Knowledge-Base Forensics](../playbooks/03-rag-knowledge-base-forensics.md)."*

## Relationship to OWASP Top 10 for LLM Applications

OWASP's earlier **Top 10 for LLM Applications** (current version 2025.1) covers single-model risks: prompt injection, training data poisoning, model denial of service, and so on. The Agentic Top 10 is **additive**. It covers risks that emerge only when LLMs are wired into multi-step plans with tools, memory, and inter-agent protocols.

The AI IR Overlay focuses on agent-class incidents (the Agentic Top 10 territory). For LLM-only incidents in non-agentic systems, traditional application IR plus 800-61 r3 is usually sufficient.

## Status

- **Mapping completeness:** all 10 ASI categories have substantive playbook coverage.
  - **ASI01 Agent Goal Hijack:** [Playbook 01](../playbooks/01-agent-as-privileged-identity.md) (general response) and [Playbook 06](../playbooks/06-prompt-injection-workflow.md) (workflow-injection variant, the dominant 2026 manifestation).
  - **ASI02 Tool Misuse & Exploitation** and **ASI05 Unexpected Code Execution:** [Playbook 04](../playbooks/04-tool-design-is-containment.md).
  - **ASI03 Identity & Privilege Abuse:** [Playbook 07](../playbooks/07-secrets-and-tokens.md).
  - **ASI04 Agentic Supply Chain Compromise:** [Playbook 07](../playbooks/07-secrets-and-tokens.md) (vendor credential discipline) and [Playbook 10](../playbooks/10-vendor-copilots.md) (the framework's dedicated vendor-copilot response playbook).
  - **ASI06 Memory & Context Poisoning:** [Playbook 03](../playbooks/03-rag-knowledge-base-forensics.md) (RAG forensics), [Playbook 06](../playbooks/06-prompt-injection-workflow.md) (workflow-injection vector), and [Playbook 11](../playbooks/11-monitoring-detection.md) (detection).
  - **ASI07 Insecure Inter-Agent Communication** and **ASI08 Cascading Agent Failures:** [Playbook 08](../playbooks/08-multi-agent-blast-radius.md).
  - **ASI09 Human-Agent Trust Exploitation:** [Playbook 24](../playbooks/24-board-ready-scorecard.md).
  - **ASI10 Rogue Agents:** [Playbook 11](../playbooks/11-monitoring-detection.md) (detection signals) and [Playbook 12](../playbooks/12-insider-threat-3.md) (response and investigation; the matched detection-response pair completing the rogue-agent coverage arc).
- **Coverage status:** complete through `v0.14.x`. The two largest gaps from the v0.10.x baseline are now closed: ASI04 supply-chain response by [Playbook 10](../playbooks/10-vendor-copilots.md) in `v0.13.0`, and ASI10 rogue-agent response by [Playbook 12](../playbooks/12-insider-threat-3.md) in `v0.11.0`. Future playbooks will add ASI-cross-cutting controls and deepen coverage on emerging variants.
- **Validation:** unreviewed by OWASP. This is the maintainer's interpretation, offered in good faith.

## Source

- OWASP Top 10 for Agentic Applications 2026 (Agentic Security Initiative), OWASP GenAI Security Project, December 2025. Available at [genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).
- OWASP Top 10 for LLM Applications (2025.1), OWASP Foundation. Available at [owasp.org/www-project-top-10-for-large-language-model-applications/](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

---

*Last revised: 2026-06-28 · Maintainer interpretation, not an OWASP publication.*

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
