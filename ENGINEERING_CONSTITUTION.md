# ThermalOps Engineering Constitution

This constitution defines the default engineering standard for ThermalOps. It applies to desktop, portable, enterprise, adapters, services, tests, build/release automation, documentation, and any future AI capability.

## 1. Priority order

When concerns conflict, decide in this order:

1. business/domain correctness;
2. safety and security;
3. privacy and authorization boundaries;
4. reliability and recoverability;
5. maintainability and testability;
6. user experience and accessibility;
7. performance/efficiency;
8. delivery speed.

Fast code that can affect the wrong queue, leak customer data, or leave a customer machine in a degraded state is not acceptable progress.

## 2. Business rules first

The domain owns what a printer, print job, diagnostic finding, repair plan, impact level, policy, and post-condition mean.

UI, CLI, adapters, Windows APIs, vendor SDKs, and AI are interfaces to the domain. They are not the source of domain truth.

## 3. Architecture

Default architecture is a **modular monolith**.

- Domain is the authority.
- Application orchestrates use cases.
- Infrastructure implements operating-system/device boundaries.
- Vendor integrations are adapters.
- UI is a delivery mechanism.
- Entry projects are composition roots.
- Privileged execution is a separate trust boundary.

Use ADRs for meaningful architecture/security decisions. Do not introduce microservices, brokers, distributed state, or cloud infrastructure without a problem that demonstrably requires them.

## 4. Least privilege and safe defaults

- Read-only is the default mode.
- Portable Lite is permanently read-only.
- Portable Pro elevates only when an approved write operation is executed.
- The desktop UI should remain a standard-user process.
- Privileged helper capabilities are enumerated and schema-validated.
- No arbitrary shell/PowerShell execution surface is permitted.
- Destructive actions require preview, impact, scope, confirmation, and verification.
- Targeted remediation is preferred over global reset.

## 5. Repair transaction discipline

Every repair is modeled as a plan with:

- preconditions;
- affected resources;
- risk/impact level;
- snapshot requirements;
- ordered actions;
- timeouts;
- expected post-conditions;
- verification method;
- recovery/rollback path;
- audit events.

Canonical sequence:

```text
Preflight -> Snapshot -> Execute -> Verify -> Recovery/Rollback -> Post-condition
```

If a repair cannot be made safely transactional, document the residual risk and require stronger confirmation.

## 6. Portable purity

A successful portable session must not intentionally leave:

- installed services;
- scheduled tasks;
- startup entries;
- persistent helpers;
- background daemons;
- customer logs created by ThermalOps;
- temporary IPC endpoints;
- temporary executable copies.

Cleanup failure is a reportable diagnostic outcome, not something to ignore silently.

## 7. Privacy

Collect only what is required for diagnosis.

- Default storage is local and session-scoped.
- Default export is sanitized.
- Full technical export is explicit.
- No automatic upload.
- No customer data in telemetry because telemetry is off by default and not required.
- Redaction covers usernames, hostnames, IPs, server names, non-target printer queues, and other environment identifiers where appropriate.
- Retention in installed/enterprise mode must be policy-controlled.

## 8. Security engineering

Use applicable guidance from NIST SSDF, Microsoft Windows security guidance, OWASP ASVS for future service/API surfaces, and vendor security documentation.

Expected controls include:

- explicit trust boundaries;
- strict IPC ACLs and caller validation;
- input schema validation;
- allowlists over denylists for privileged actions;
- timeouts and bounded retries;
- safe temporary-file handling;
- code signing;
- checksums;
- SBOM;
- dependency review;
- secret scanning;
- CodeQL/static analysis where applicable;
- secure update design before auto-update exists.

## 9. Reliability

Operations must define timeouts and failure behavior. For recoverable external operations, use bounded retry/backoff where appropriate. Never retry destructive operations blindly.

Preserve original state when changing services/configuration. For example, restarting a service must account for its initial status and startup policy rather than assuming it should always end in `Running`.

## 10. Observability

Use structured events rather than only human text.

Each important operation should be traceable by session/correlation ID and include:

- timestamp;
- component;
- action/finding type;
- target resource ID;
- outcome;
- duration where useful;
- sanitized error details;
- before/after references for repairs.

Enterprise services, if introduced, should provide health/readiness and metrics appropriate to their operational surface. Distributed tracing is required only when a distributed architecture actually exists.

## 11. Testing

Use a testing pyramid appropriate to a hardware/Windows tool:

- many domain unit tests;
- component/contract tests at adapter boundaries;
- real Windows integration tests;
- focused security/failure-path tests;
- a small number of E2E workflows;
- hardware-in-the-loop validation for claims about physical device behavior.

Mocks are acceptable for true external boundaries. Do not mock away the main behavior being validated.

Negative cases are mandatory for privileged/repair logic: access denied, UAC denied, service stop/start failure, locked jobs, disconnect mid-operation, malformed device replies, timeouts, helper crash, cleanup failure, and partial repair.

## 12. CI/CD and Git

Work incrementally:

```text
logical change -> commit -> push -> CI -> next logical change
```

Rules:

- keep WIP low;
- preserve last-known-green;
- CI must be green before a release tag;
- release tag points to the green SHA;
- no safety-sensitive auto-merge;
- keep local/main synchronized with origin/main when closing a milestone;
- security/static/dependency checks are release gates once configured;
- failed checks must not be hidden by marking them optional without an ADR/rationale.

## 13. Supply chain and releases

A production release should provide:

- semantic version;
- source commit SHA;
- build identity;
- Authenticode signature for Windows executables when release signing is available;
- SHA-256 checksums;
- SBOM;
- release notes;
- supported OS/architecture matrix;
- known limitations;
- provenance/attestation where feasible.

Do not make unsupported claims about reproducibility or signature trust.

## 14. Documentation and reproducibility

A new contributor/agent should be able to understand:

- product boundaries;
- architecture;
- threat model;
- how to build/test;
- how to run safely;
- what each milestone means;
- what is validated vs experimental.

Documentation is part of the change, not post-project cleanup.

## 15. UX and accessibility

Expose evidence and impact clearly. Avoid magic green/red states with no explanation.

Destructive controls must communicate scope. N1 workflows should be simple without hiding the existence of advanced evidence for N2/N3.

Keyboard navigation, readable contrast, scaling, screen-reader semantics, and localization readiness are part of desktop quality.

## 16. AI

AI is optional and downstream of deterministic evidence.

AI may:

- explain findings;
- summarize a support bundle;
- retrieve approved documentation;
- suggest a deterministic troubleshooting path already allowed by policy.

AI may not:

- create an unrestricted command;
- execute a repair autonomously;
- override policy;
- invent device state;
- hide uncertainty;
- upload customer data without explicit policy/consent.

## 17. Project management

Use lightweight Kanban/milestones. Every item should have a Definition of Ready and Definition of Done appropriate to risk.

At milestone boundaries, perform an audit for:

- gaps;
- duplicated functionality;
- unnecessary complexity;
- security/privacy regressions;
- missing tests;
- missing observability;
- outdated docs;
- release readiness.

## 18. Honest status

Use precise status terms:

- **fixed** — implemented and validated;
- **partial** — some acceptance criteria remain;
- **experimental** — works in limited/controlled conditions and is not generally supported;
- **deferred** — intentionally postponed with rationale;
- **not validated** — implementation exists but required validation has not happened.

Never call a feature production-ready because the UI exists or the happy path ran once.
