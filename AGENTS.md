# AGENTS.md

Operating contract for coding agents/automation working in ThermalOps.

## Required reading

Before architecture/behavior changes read:

1. `ENGINEERING_CONSTITUTION.md`
2. `docs/PRODUCT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/SECURITY_AND_PRIVACY.md`
5. `docs/PREVENTIVE_MAINTENANCE.md`
6. `docs/FIELD_SERVICE_AND_ESCALATION.md`
7. `docs/DIAGNOSTICS_AND_REPAIR.md`
8. relevant ADRs / `docs/ROADMAP.md`

For packaging/enterprise changes also read `docs/DEPLOYMENT_AND_LIFECYCLE.md`. For fleet work read `docs/FLEET_AND_CONDITION_MONITORING.md`.

If a request conflicts with the constitution/safety model, stop and surface the conflict instead of weakening a guardrail.

## Non-negotiable constraints

- Domain rules are authoritative.
- Default is read-only.
- Portable Lite is structurally read-only.
- Main UI does not stay elevated.
- Privileged actions are typed, allowlisted, narrow, auditable and policy-gated.
- No generic shell/PowerShell/cmd/execute endpoint.
- No broad spool-directory deletion for a selected job/queue.
- Never declare physical health from one Windows status value.
- Windows/vendor/technician evidence remain distinguishable.
- AI never decides/executes repair, maintenance due, disposition, firmware/config changes or policy.
- Core field functionality cannot require cloud/login/internet/telemetry.
- No automatic broad network scan.
- No automatic customer-data upload or USB logging.
- Portable leaves no intentional persistence.
- Maintenance intervals/lifetimes require a source/applicability record; never invent them.
- Do not assume a field technician is authorized to disassemble/repair hardware.
- Organization/customer/vendor-specific escalation rules are policy/configuration, not hard-coded public core.
- Imported policy/baseline can only constrain/inform; it cannot unlock absent executable capability.
- Firmware update/driver install requires dedicated ADR/threat/rollback design.
- Do not add microservices to solve in-process modularity.

## Architecture expectations

Start modular monolith:

- `ThermalOps.Domain` — evidence, printer/job, maintenance, disposition, service-case, repair-plan invariants;
- `ThermalOps.Application` — use cases/orchestration;
- `ThermalOps.Infrastructure.Windows` — WinSpool/SCM/PnP/Event Log/OS;
- `ThermalOps.Adapters.Zebra` — Zebra capability/evidence adapter;
- `ThermalOps.Desktop` — WPF composition/UI;
- `ThermalOps.PrivilegedHelper` — minimal elevated process;
- tests mirror boundaries.

Domain must not depend on WPF, Windows interop implementation, filesystem/network implementation, vendor SDK, database, installer or AI.

## Evidence discipline

Every important observation preserves source, timestamp, target, normalized value, collection outcome and safe raw representation when needed.

Keep distinct:

```text
Observed fact
Derived finding
Maintenance recommendation
Service disposition
Operator request
Executed action
Verified result
Technician observation
```

## Preventive maintenance discipline

Maintenance tasks preserve task ID/version, source, applicability, trigger/interval, safety notes and result.

Unknown data stays unknown. Baseline drift is not proof of failure. Health scoring, if added, must be deterministic/explainable/versioned.

## Local remediation workflow

```text
Preflight
 -> Snapshot
 -> Present plan/impact
 -> Explicit confirmation
 -> Execute
 -> Verify
 -> Recovery/Rollback if required
 -> Post-condition
 -> Audit event
```

Exit code 0 is not verification.

## Field/escalation discipline

Do not hard-code assumptions about RMA, equipment removal, support levels, or who contacts a vendor. Use generic `ServiceDisposition` / `EscalationPolicy` and leave proprietary policy outside public core.

## Privacy

Session-local temp storage. Sanitized report default. Full/support/vendor case explicit. Never commit real customer logs, hostnames, usernames, IPs, serials, tickets, configs, credentials or screenshots.

## Testing

Relevant changes require tests: domain, contract, Windows integration, failure paths, helper security, preventive schedule/baseline, redaction/service-case, portable E2E, hardware-in-the-loop for vendor claims, and lifecycle tests for Enterprise packaging.

Mocks are for true external boundaries, not for hiding broken internal integration.

## Git/CI

- logical commits;
- push logical checkpoints;
- preserve last-known-green;
- no release tag on red CI;
- no safety-sensitive auto-merge;
- release tag identifies validated green source;
- report `fixed`, `partial`, `experimental`, `deferred`, `not validated` accurately.

## Documentation/ADRs

Behavior and docs change together. Architecture/security/lifecycle decisions use ADRs.

## External code/licenses

Public source is not automatically reusable. Confirm license/attribution/security/maintenance before dependency/code reuse. Prefer official API docs and independent implementation.
