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

**Status: unfilled, deliberately.**

The overlay maps to this list, so the lens should too. The mapping is left as TODO rather than populated, for one reason: entry IDs and titles must come from the published OWASP document, not from recollection. A standards crosswalk with a plausible-looking wrong ID is worse than an empty one. It will be cited.

## How to fill

1. Open the published OWASP Top 10 for Agentic Applications 2026 and transcribe the ten entries, with their exact IDs and titles, into the table below.
2. Map each technique from [../MATRIX.md](../MATRIX.md) to the entries it exercises. Expect one-to-many in both directions.
3. Note that the lens and OWASP are oriented differently and the mapping will be uneven by design: OWASP enumerates **weaknesses in agentic applications**, the lens enumerates **failures of the controls wrapped around them**. Several OWASP entries will map to no technique because they are design-time concerns the overlay does not address. Record those as out-of-scope rather than stretching a technique to cover them.
4. Cross-check against [overlay-mapping.md](overlay-mapping.md): where the overlay already claims an OWASP mapping for a playbook, the technique that validates that playbook should inherit it.

| OWASP 2026 entry | ID | Techniques | Notes |
|---|---|---|---|
| TODO | TODO | | |

## Expected shape

Without asserting IDs, the thematic correspondences to verify when filling the table:

- Entries concerning **excessive agency or over-privileged tool access** → L1 (OL-T102, OL-T104) and L2 (OL-T206).
- Entries concerning **indirect prompt injection via retrieved content** → L3 (OL-T307) and L4 (OL-T402), plus OL-T105 on the inventory side.
- Entries concerning **memory or context poisoning** → OL-T204, OL-T304, OL-T401.
- Entries concerning **identity, delegation, or impersonation** → OL-T102, OL-T106, OL-T306, OL-T403.
- Entries concerning **multi-agent or orchestration risk** → OL-T203.
- Entries concerning **insufficient monitoring or traceability** → the whole of L3.

Verify each before writing it down.
