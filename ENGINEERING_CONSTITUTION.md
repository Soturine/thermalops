# ThermalOps Engineering Constitution

This constitution governs desktop, portable, enterprise, adapters, preventive maintenance, field service, fleet, tests, releases, documentation and future AI.

## 1. Priority order

1. business/domain correctness;
2. safety/security;
3. authorization/privacy;
4. reliability/recoverability;
5. maintainability/testability;
6. UX/accessibility;
7. efficiency;
8. delivery speed.

Fast behavior that affects the wrong queue, invents maintenance advice, leaks customer data, exceeds technician authority or leaves a machine degraded is not progress.

## 2. Domain authority

Domain owns printer/job/evidence/finding, maintenance task/inspection/baseline/due, service disposition/case, policy, RepairPlan and post-condition semantics.

UI, Windows APIs, vendor SDKs, files, AI and fleet infrastructure are interfaces, not sources of business truth.

## 3. Architecture

Default modular monolith. Domain inward; Application orchestrates; infrastructure/vendor adapters implement boundaries; UI delivers; entry point composes; privileged execution is separate trust boundary.

No microservices/broker/cloud merely for appearance.

## 4. Evidence integrity

Never collapse distinct sources into an opaque status. Preserve source/timestamp/target/outcome and distinguish observed facts, technician observations, derived findings, recommendations, disposition, actions and validation.

Unknown is not healthy.

## 5. Preventive-maintenance integrity

- maintenance is read-only-first;
- intervals/thresholds/lifetimes require approved source/applicability;
- no invented replacement schedule;
- baseline drift is a finding, not automatic fault proof;
- technician physical checks are human evidence;
- software does not assume disassembly authorization;
- health scoring, if present, is deterministic, explainable and versioned;
- predictive claims require separate validated data program.

## 6. Field-service scope

ThermalOps supports diagnosis, preventive inspection, local authorized remediation, evidence, disposition and escalation assistance.

`Repair` does not imply bench/internal hardware repair.

Company/customer/vendor-specific RMA/support workflow is policy/configuration, not hard-coded public core.

## 7. Least privilege / safe defaults

- read-only default;
- Portable Lite permanently read-only;
- Pro elevates only approved action;
- UI remains standard user;
- helper capabilities typed/schema-validated/allowlisted;
- no arbitrary shell/script;
- destructive action requires preview/scope/confirmation/verification;
- targeted remediation before global reset.

## 8. Repair transaction discipline

Every state-changing action has preconditions, affected resources, impact, snapshot, ordered actions, timeout, post-condition, verification, recovery and audit.

```text
Preflight -> Snapshot -> Execute -> Verify -> Recovery/Rollback -> Post-condition
```

## 9. Portable purity

A successful session leaves no intentional service, task, startup entry, persistent helper/daemon, customer log, IPC endpoint or temporary executable copy.

Cleanup failure is a reported outcome.

## 10. Privacy

Collect only required data. Session-local storage; sanitized export default; full/service-case explicit; no automatic upload; no required telemetry; policy-controlled Enterprise retention.

## 11. Security engineering

Apply NIST SSDF, Microsoft Windows security guidance, OWASP guidance for future APIs and vendor security docs as relevant.

Expected controls include trust boundaries, IPC ACLs, caller validation, schema validation, allowlists, bounded input/timeouts, safe temp files, code signing, SHA-256, SBOM, dependency/license review, secret/static analysis and secure-update design before auto-update.

Imported policy/baseline is untrusted data and cannot create executable capability.

## 12. Reliability

Define timeout/failure behavior. Bounded retry/backoff for safe recoverable external reads; never blindly retry destructive actions. Preserve original service/config state.

## 13. Observability

Structured events with session/correlation ID, timestamp, component, type, target, outcome, duration when useful, sanitized error and before/after references.

Fleet adds health/readiness/metrics appropriate to actual distributed components only.

## 14. Testing

Many domain tests; adapter contracts; real Windows integration; preventive schedule/baseline tests; security/failure tests; few meaningful E2E; hardware-in-the-loop for physical device claims; lifecycle tests for installed Enterprise.

Negative paths are mandatory for privileged/repair behavior.

## 15. CI/CD and Git

```text
logical change -> commit -> push -> CI -> next logical change
```

Preserve last-known-green; no release tag on red CI; no safety-sensitive auto-merge; security/dependency/license gates become release requirements once configured.

## 16. Supply chain / release

Production distribution should expose semantic version, source SHA, build identity, Authenticode when available, checksums, SBOM, notes, OS/arch support, known limits and provenance where feasible.

## 17. Deployment lifecycle

Portable has no installer/persistence. Enterprise packaging must support predictable install, silent deployment, offline deployment, upgrade/migration/recovery, uninstall and normal-path no-reboot where technically possible. No early silent self-update.

## 18. UX/accessibility

Show evidence, impact and scope. N1 is guided; N2/N3 can inspect detail. Destructive actions are secondary. Support keyboard navigation, readable contrast, scaling, screen-reader semantics and localization readiness.

## 19. AI

AI may explain/summarize/retrieve approved docs. AI may not execute/authorize repair, define maintenance due, assign disposition, invent state, override policy or upload customer data without explicit policy/consent.

## 20. Project management

Lightweight Kanban/milestones; Definition of Ready/Done by risk. Milestone audit covers gaps, duplicate complexity, security/privacy, tests, observability, docs, licensing and release readiness.

## 21. Honest status

- **fixed** — implemented and validated;
- **partial** — criteria remain;
- **experimental** — limited/controlled support;
- **deferred** — intentionally postponed;
- **not validated** — implementation exists without required validation.

Never call a feature production-ready because UI/happy-path exists.
