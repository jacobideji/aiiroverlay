<!-- ────────────────────────────────────────────────────────────────── -->
<!--  The Six-Question Printable Card                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **One-page card designed to live on a SOC wall.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# AI IR Overlay — First-Hour Triage Card

> **An agent with tool access is a privileged identity. Respond like one.**

---

## Walk these six in order — do not skip ahead

### 1 · WHAT CAN IT DO?

Tools enabled. Read vs. write. Internal vs. external.

### 2 · WHERE CAN IT WRITE?

Email · CRM · Ticketing · Cloud · ERP · Code · Anything that changes records.

### 3 · WHO IS IT?

Service account · Delegated OAuth · User impersonation · Shared token.

### 4 · DOES IT REMEMBER?

Memory on/off · Per-user or shared · Retention · Sensitivity.

### 5 · WHAT IS THE LEAST DISRUPTIVE SAFE MODE?

**M1** Read-Only · **M2** Approvals · **M3** Tool Tiering · **M4** Full Disable

### 6 · WHAT IS THE EVIDENCE PLAN?

Prompts · Tool calls · Retrieval traces · Memory · Config · Identity logs.
**Capture before you rotate.**

---

## Kill-Switch Ladder

```
M0 Observe       →  Normal operations
M1 Read-Only     →  Suspicious, low/moderate impact         (preferred first move)
M2 Approvals     →  Must keep running, need two-person rule
M3 Tool Tiering  →  Disable high-risk tools only
M4 Full Disable  →  Active harm or confirmed compromise
M5 Re-Enable     →  Containment validated, staged recovery
```

---

## The Mental Model

> If it can **act** → govern as **privileged identity**
> If it can **remember** → treat as **data store**
> If it can **retrieve** → protect as **production system**
> If it can **change** → manage as **software** (rollback + audit)

---

*AI IR Overlay™ · Apache 2.0 · jacobideji.com*
*Founded by Jacob Ideji*
