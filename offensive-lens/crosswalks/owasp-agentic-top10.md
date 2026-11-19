<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens Crosswalk: OWASP Agentic Top 10  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Unfilled by design. Standard IDs are transcribed, never recalled.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../../CONTENT_MAP.md) for the full repository map.*

---

# Crosswalk — Offensive Lens → OWASP Top 10 for Agentic Applications 2026

**Status: transcribed from the published document.** *OWASP Top 10 For Agentic Applications 2026*, Version 2026, December 2025, OWASP Gen AI Security Project — Agentic Security Initiative, CC BY-SA 4.0. Entry IDs and titles are transcribed from that document's section headings, never from recollection. Re-check them against the current edition before citing them.

## Why this crosswalk exists

The overlay maps to this list, so the lens should too. OWASP enumerates **weaknesses in agentic applications**; the lens enumerates **failures of the controls wrapped around them**. The mapping is therefore uneven by design and runs one-to-many in both directions: one entry exercises several techniques, and one technique answers to several entries.

## Table

| OWASP 2026 entry | ID | Techniques | Notes |
|---|---|---|---|
| Agent Goal Hijack | ASI01 | OL-T105, OL-T307, OL-T402 | Hijack arrives as injected content. OL-T105 tests whether the corpus that carries it is even declared, OL-T307 whether the responder can tell injected text from system-generated evidence, OL-T402 whether re-enable leaves the carrier in place. |
| Tool Misuse and Exploitation | ASI02 | OL-T101, OL-T102, OL-T104, OL-T206 | Misuse presupposes reach. OL-T101 and OL-T102 establish what the agent can actually call and at what effective scope, OL-T104 finds write paths through tools classified read-only, OL-T206 tests whether stripping one tool simply reroutes the capability. |
| Identity and Privilege Abuse | ASI03 | OL-T102, OL-T106, OL-T306, OL-T403 | OL-T102 and OL-T106 cover inflated scope and identity aliasing, OL-T306 whether downstream systems can attribute an action to the agent at all, OL-T403 whether the credential survives recovery. |
| Agentic Supply Chain Vulnerabilities | ASI04 | OL-T105, OL-T107, OL-T305, OL-T406 | Upstream compromise is only detectable against a recorded baseline. OL-T107 tests whether the AI-BOM is current, OL-T105 whether corpus drift is visible, OL-T305 whether configuration state is versioned, OL-T406 whether rollback returns to a vulnerable configuration. |
| Unexpected Code Execution | ASI05 | OL-T101, OL-T104, OL-T206 | Generic-capability tools are the vector. OL-T101 finds the ones that are reachable but undeclared, OL-T104 the ones that reach a write through a read-only label, OL-T206 whether containment strips shell, code interpreter and raw HTTP rather than only the named write tools. |
| Memory & Context Poisoning | ASI06 | OL-T204, OL-T304, OL-T401 | The three-stage question: OL-T304 whether memory survives containment as evidence, OL-T204 whether an entry written before containment executes after it, OL-T401 whether re-enable severs memory from the agent at all. |
| Insecure Inter-Agent Communication | ASI07 | OL-T203, OL-T306 | OL-T203 tests whether containing one agent contains what it delegates to, OL-T306 whether the receiving system records which agent acted. |
| Cascading Failures | ASI08 | OL-T202, OL-T203, OL-T205 | Propagation outruns containment. OL-T202 tests in-flight actions that complete after the switch, OL-T203 the relay to downstream agents, OL-T205 whether the kill switch depends on the control plane the incident is degrading. |
| Human-Agent Trust Exploitation | ASI09 | OL-T208, OL-T209, OL-T307, OL-T405 | The human in the loop is the target. OL-T208 and OL-T209 test whether approval is a real gate or a rubber stamp under load, OL-T405 whether the operator can approve their own re-enable, OL-T307 whether the evidence the human reads was authored by the adversary. |
| Rogue Agents | ASI10 | OL-T103, OL-T106, OL-T201, OL-T404 | OL-T103 finds agents outside the inventory, OL-T106 those running as something else, OL-T201 whether a contained agent still holds a write path, OL-T404 whether re-enable happens without a gate that would catch the drift. |

Twenty-five of the thirty-one techniques map to at least one entry. Nine are cited by two.

## What the transcription revealed: six techniques with no OWASP counterpart

| Technique | Name | Lens |
|---|---|---|
| OL-T207 | Containment application race | L2 |
| OL-T210 | Output-channel containment residue | L2 |
| OL-T301 | Prompt / response truncation | L3 |
| OL-T302 | Tool-call record gap on failure | L3 |
| OL-T303 | Retrieval trace absence | L3 |
| OL-T308 | Retention shorter than detection latency | L3 |

Four of the six are L3. The 2026 list carries no entry for insufficient logging, monitoring or traceability, so the lens's entire evidence-starvation axis has no weakness class to map to. This file's earlier *Expected shape* note predicted that "entries concerning insufficient monitoring or traceability" would map to the whole of L3; the transcription shows no such entry exists, and the prediction is corrected here rather than quietly dropped.

That asymmetry is the point of keeping the two catalogs side by side. An organization that satisfies all ten OWASP entries has said nothing about whether it could reconstruct the incident afterwards, and L3 is the part of the lens that asks.

Record the OWASP document version used, alongside the overlay version, in the assessment record's `scope_note`. For the mapping above that is `OWASP Top 10 for Agentic Applications 2026, Version 2026 (December 2025)`.
