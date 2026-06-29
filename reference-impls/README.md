<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Reference Implementations                                         -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

# Reference Implementations

This directory contains **minimal, working reference implementations** of the framework's two operational contracts:

1. [`evidence_exporter/`](evidence_exporter/): a Python CLI implementing the [Evidence Export Script Contract](../schemas/evidence-export.spec.md) for Types A through F
2. [`kill_switch_demo/`](kill_switch_demo/): a Python tool-toggle demo showing Modes M0, M1, M3 against a synthetic agent

These are **not production code.** They are skeletons that demonstrate the contracts' shape, manifest discipline, and key behaviors. Adopters fork these and replace the stub adapters with their own vendor-specific integrations.

## Why these exist

The v0.24.0 holistic critique surfaced that the [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md) and [`schemas/kill-switch-api.md`](../schemas/kill-switch-api.md) contracts were exceptionally detailed but lacked working reference code. Every adopter re-invented the implementation independently, losing the convergence benefit the specs were designed to achieve. v0.26.0 ships these references to close the gap.

## Scope

| Implementation | What it does | What it does NOT do |
|---|---|---|
| `evidence_exporter` | Reads a synthetic-or-real evidence source layout; produces a manifest with integrity hashes; emits telemetry events; demonstrates parallel-export discipline; shows the per-type capture order | Connect to specific vendors (OpenAI, Anthropic, Salesforce, Okta); store evidence in production durable storage; handle PII redaction |
| `kill_switch_demo` | Demonstrates an in-memory tool registry that can be toggled to M0/M1/M3; shows the Activate/Status/Deactivate/Probe API shape; logs activation events | Integrate with LangGraph, Bedrock Agents, or specific vendor copilot platforms; persist state across restarts |

## Usage

Each subdirectory has its own README with run instructions.

### Adapting for production

The reference code is structured so that adopters can:

1. Fork the directory into their own repository
2. Replace the stub adapters (`adapters/*_stub.py`) with vendor-specific implementations
3. Wire up the manifest and telemetry producers to the customer's actual evidence-storage and SIEM systems
4. Run the reference test suite to confirm the contract conformance is preserved

## Conformance

The references conform to the contracts' **shape and discipline**, not to a specific vendor implementation. The framework's position is that contract conformance (correct manifest structure, correct exit codes, correct telemetry event format, correct probe behavior) matters more than vendor-specific adapters, which are necessarily site-specific.

## Dependencies

Python 3.10+ standard library only. No external dependencies; you can run these examples in any modern Python environment without pip-installing anything.

## Related

- [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md): the contract that `evidence_exporter` implements
- [`schemas/kill-switch-api.md`](../schemas/kill-switch-api.md): the contract that `kill_switch_demo` implements
- [`scripts/validate.py`](../scripts/validate.py): the AI-BOM and Privilege Matrix validator (a related but distinct contract: validates AI-BOM YAML and Privilege Matrix CSV against the JSON schemas)

---

*Source: AI IR Overlay framework, by Jacob Ideji.*

<https://www.linkedin.com/in/jacobideji/>
