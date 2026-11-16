<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens L1: Inventory Drift  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The AI-BOM is a declaration. The runtime is the truth.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../../CONTENT_MAP.md) for the full repository map.*

---

# L1 · Inventory Drift

**Validates:** Overlay Control 1 (Inventory, the AI-BOM)
**CSF 2.0:** Identify
**Premise:** The AI-BOM records "the deployed identity, granted scopes, tools, write-enabled targets, memory, and data sources" of each production agent. That record is a declaration written by a human at a point in time. The runtime is the truth. L1 measures the delta.

Why this lens runs first: every other overlay control is scoped by the inventory. Containment strips the tools the inventory names. Evidence collects the classes the inventory implies. Recovery restores the configuration the inventory describes. A wrong inventory does not make the other controls fail loudly. It makes them succeed against the wrong target set.

---

### OL-T101 — Undeclared tool reachability

**Premise:** The AI-BOM's tool list is maintained by hand; tool registration is maintained by deployment.

**Procedure**
1. Enumerate the agent's tool set *from the runtime*: the registry, manifest, or MCP server list it resolves at execution time.
2. Independently, ask the agent to enumerate its own available tools. Record the answer; do not treat it as authoritative.
3. Diff both against the AI-BOM entry.
4. For each tool present in the runtime but absent from the AI-BOM, determine whether it can write, and to what.

**PASS**. Runtime set and AI-BOM agree in both directions.
**PARTIAL**. The runtime set cannot be enumerated independently of the AI-BOM. The inventory is unfalsifiable, which is a governance finding in its own right.
**FAIL**. Any tool is reachable at runtime and undeclared, or declared and absent.

**Expected defensive signal:** tool-registration change produces an AI-BOM drift alert, or CI fails on the AI-BOM's schema freshness check.
**Remediation theme:** generate the AI-BOM's tool list from the runtime registry rather than maintaining it alongside.

### OL-T102 — Effective-scope inflation

**Premise:** Declared scope is what was requested. Effective scope is what the token actually carries, after group membership, role inheritance, and consent-screen defaults.

**Procedure**
1. For each identity in the AI-BOM, retrieve the live grant from the identity provider or the token's own introspection endpoint.
2. Expand transitively: group memberships, inherited roles, resource-level ACLs that name the identity indirectly.
3. Diff effective against declared.
4. Classify each excess permission by whether it is write-capable.

**PASS**. Effective equals declared.
**PARTIAL**. Effective scope cannot be computed from available tooling.
**FAIL**. Effective scope exceeds declared, in any write-capable dimension.

**Expected defensive signal:** periodic entitlement review covering non-human identities, not only staff.
**Remediation theme:** dedicated agent identities with no group membership; scope grants pinned and reviewed as code.

### OL-T103 — Shadow agent deployment

**Premise:** The inventory covers agents someone remembered to register.

**Procedure**
1. From the model-provider or gateway billing/usage records, enumerate every distinct API key, service account, or client ID with inference traffic in the last 30 days.
2. Diff against the set of agents in the AI-BOM.
3. For each unaccounted caller, identify owner, purpose, and whether it holds tool access.

**PASS**. Every inference-producing identity maps to an AI-BOM entry.
**PARTIAL**. Usage records are not attributable to identities at the needed granularity.
**FAIL**. Any production inference traffic is unattributable to a registered agent.

**Expected defensive signal:** inference egress is gated through a broker that rejects unregistered callers.
**Remediation theme:** make registration the path of least resistance: no AI-BOM entry, no key.

### OL-T104 — Transitive write path via read-only tool

**Premise:** "Read-only" is a property of a tool's interface, not of its consequences. The overlay's M1 preserves read-only tools for forensic continuity; that is only safe if read-only tools are inert.

**Write risk: yes.** Requires per-exercise sign-off.

**Procedure**
1. List every tool the AI-BOM classifies as read-only.
2. For each, trace what the *downstream system* does on read: webhooks on access, read-triggered workflow automations, search queries that create index entries, ticket views that notify, "preview" endpoints that render and send.
3. Exercise each candidate with a benign canary and observe whether any state outside the agent changed.

**PASS**. No read-only tool produces observable external state change.
**PARTIAL**. Downstream behavior is undocumented and could not be traced for one or more tools.
**FAIL**. Any read-only-classified tool produced a write, notification, or external side effect.

**Expected defensive signal:** none expected. This is a classification defect, and the absence of a signal is the point.
**Remediation theme:** classify tools by effect, not by HTTP verb. Re-derive the M1 tool set from the corrected classification.

### OL-T105 — Retrieval-corpus drift

**Premise:** The AI-BOM names data sources. It rarely pins their contents, and retrieval corpora are frequently writable by a wider population than the agent's operators.

**Procedure**
1. For each declared data source, establish who can add or modify documents in it.
2. Compare that population against the agent's privilege level. A corpus writable by any employee, feeding an agent with finance write scope, is a privilege inversion.
3. Record last-modified distribution for the corpus and compare against the AI-BOM's freshness date.

**PASS**. Corpus write population is equal to or narrower than the agent's operator set, and freshness is current.
**PARTIAL**. Write population cannot be determined.
**FAIL**. The corpus is writable by a population broader than the agent's privilege justifies.

**Expected defensive signal:** corpus writes are logged with author attribution and retained at least as long as agent evidence.
**Remediation theme:** treat retrieval corpora as privileged configuration; gate writes to them at the agent's own privilege level.

### OL-T106 — Agent identity aliasing

**Premise:** Attribution during an incident requires that one acting identity map to one agent. Shared service accounts collapse that mapping, and the collapse is invisible until it is needed.

**Procedure**
1. Group AI-BOM entries by deployed identity.
2. Any identity serving more than one agent, or any agent presenting more than one identity, is an aliasing case.
3. For each case, attempt the question an incident will ask: *given this downstream audit entry, which agent made it?* Answer it using only logs.

**PASS**. One identity, one agent, and downstream entries are attributable from logs alone.
**PARTIAL**. Attribution is possible but requires correlation across systems with no shared identifier.
**FAIL**. A downstream action cannot be attributed to a specific agent.

**Expected defensive signal:** a request/trace ID propagated from agent invocation to downstream audit entry.
**Remediation theme:** one identity per agent per environment; propagate a correlation ID into every tool call.

### OL-T107 — Stale AI-BOM freshness

**Premise:** The overlay ships `scripts/verify.py` to check schema conformity and data freshness in CI. A freshness check is only a control if failing it blocks something.

**Procedure**
1. Record each AI-BOM entry's freshness date and the deployment date of its agent's most recent change.
2. Determine what happens when the freshness check fails: does CI block the deploy, open a ticket, or emit a warning nobody reads?
3. Test it. Deploy a trivial, in-scope agent configuration change without updating the AI-BOM.

**PASS**. The change was blocked, or shipped with an auto-updated AI-BOM.
**PARTIAL**. The check fired and was advisory only.
**FAIL**. No check fired, or the last freshness date predates the agent's current configuration by more than one release cycle.

**Expected defensive signal:** the CI failure itself.
**Remediation theme:** make the AI-BOM a deploy gate. An inventory that cannot block is documentation.

---

## Lens verdict

L1 is validated when OL-T101 through OL-T107 are all PASS. In practice the first run of L1 produces FAILs on T101 and T102 in most deployments, because both are maintained by hand and drift silently.

Record the write-capable delta separately from the total delta. The write-capable delta is the number that changes the blast radius of every subsequent lens.
