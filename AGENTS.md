# AGENTS.md

This file is the operating contract for coding agents and automation working in ThermalOps.

## Required reading

Before changing code or architecture, read in this order:

1. `ENGINEERING_CONSTITUTION.md`
2. `docs/PRODUCT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/SECURITY_AND_PRIVACY.md`
5. `docs/DIAGNOSTICS_AND_REPAIR.md`
6. the relevant ADRs and milestone section in `docs/ROADMAP.md`

If a requested change conflicts with the constitution or safety model, stop and describe the conflict instead of silently weakening a guardrail.

## Non-negotiable constraints

- Domain rules are authoritative; UI convenience must not redefine them.
- Default behavior is read-only.
- The desktop UI must not require permanent elevation.
- Privileged operations must be explicit, allowlisted, structured, auditable, and narrowly scoped.
- Never add a generic `ExecuteCommand`, arbitrary PowerShell, arbitrary cmd, dynamic shell string, or equivalent privileged escape hatch.
- Never use broad spool-directory deletion as the normal method to clear one printer/job.
- Never label a device healthy solely because one Windows status integer is zero. Status must preserve evidence and bit/field semantics.
- Never let AI decide or execute repair actions.
- Never add required cloud, login, telemetry, or internet dependencies to core diagnosis/repair.
- Never collect or export customer-identifying data without a clear purpose and sanitization path.
- Never perform automatic network scanning. Discovery beyond local evidence requires explicit policy/operator permission.
- Portable mode must leave no intentional persistence after a clean session exit.
- Do not add firmware update or driver-install behavior without a dedicated ADR, threat analysis, rollback design, and milestone approval.
- Do not add microservices to solve an in-process modularity problem.

## Architecture expectations

Start with a modular monolith and explicit boundaries:

- `ThermalOps.Domain` — entities, value objects, invariants, findings, repair-plan model.
- `ThermalOps.Application` — use cases and orchestration.
- `ThermalOps.Infrastructure.Windows` — WinSpool, SCM, PnP, Event Log, filesystem/OS implementations.
- `ThermalOps.Adapters.Zebra` — Zebra-specific discovery/status/configuration implementation.
- `ThermalOps.Desktop` — WPF composition/UI only.
- `ThermalOps.PrivilegedHelper` — minimal elevated process with strict IPC.
- test projects mirroring the boundaries.

The entry point is the composition root. Infrastructure depends inward; domain must not depend on UI, Windows APIs, Zebra SDK, filesystem, networking, or AI.

## Repair workflow

Every state-changing operation must fit this lifecycle:

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

A command returning exit code 0 is not sufficient verification.

## Evidence model

Diagnostic findings must preserve:

- source (`WindowsSpooler`, `PnP`, `EventLog`, `ZebraNative`, etc.);
- observation timestamp;
- raw/normalized value where safe;
- confidence or certainty semantics if inference is involved;
- reason/evidence;
- recommended action separated from observed fact.

Do not merge observations and conclusions into one opaque string.

## Privacy

Use session-local storage under a temporary OS directory. Do not write customer logs to removable media automatically. Sanitized report is the default export. Full technical bundles require explicit choice.

Never commit real customer hostnames, usernames, IPs, serial numbers, tickets, printer configurations, logs, credentials, or screenshots.

## Testing rules

Changes are not done until relevant tests exist.

At minimum consider:

- unit tests for domain/diagnostic rules;
- contract tests for adapters;
- Windows integration tests where possible;
- negative/failure-path tests;
- security tests for privileged IPC;
- a small number of real E2E scenarios;
- hardware-in-the-loop checks for vendor-native behavior before claiming support.

Mocks are for true external boundaries, not for hiding broken internal integration.

## Git/CI

- Keep commits logically scoped.
- Push after logical checkpoints and let CI run asynchronously.
- Preserve a known-green commit.
- Do not tag/release red CI.
- Do not auto-merge safety-sensitive changes.
- Release tags must point to a green commit.
- Status reports must say `fixed`, `partial`, `experimental`, `deferred`, or `not validated` accurately.

## Documentation

For user-visible behavior, update the relevant docs in the same change. For architecture/security decisions, add or update an ADR rather than burying the decision in code comments.

## External code and licenses

Do not copy implementation code from projects without a compatible license and attribution review. Prefer official API documentation and independent implementation. Dependency additions require purpose, maintenance, security, and license review.
