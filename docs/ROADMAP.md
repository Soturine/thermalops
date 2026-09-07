# Roadmap

Roadmap order is risk-driven. Read-only evidence and policy boundaries come before broad repair, fleet automation or predictive/AI features.

## M0 — Product, safety, maintenance, and field-service foundations

Deliver:

- engineering constitution;
- product specification;
- architecture/ADRs;
- portable contract;
- preventive-maintenance model;
- field-service/escalation model;
- deployment/lifecycle contract;
- security/privacy model;
- diagnostics/local-remediation model;
- support/service-case schemas direction;
- fleet/condition-monitoring direction;
- test/release plans;
- research notes;
- CI/document checks;
- license decision;
- issue/backlog structure.

Exit criteria:

- no contradictory safety requirements;
- read-only, local remediation, hardware-service and escalation scopes are distinct;
- preventive tasks require source/applicability;
- privileged-helper principles approved;
- Portable no-persistence contract explicit;
- license selected before accepting copied third-party implementation code;
- CI green.

## M1 — Read-only Windows diagnosis foundation

Deliver:

- .NET solution/projects;
- domain evidence/finding/policy primitives;
- WinSpool printer/job enumeration;
- Spooler read state/config evidence;
- structured Windows printer status flags;
- port/transport evidence;
- PnP/USB evidence;
- print Event Log evidence;
- session timeline;
- Quick Diagnosis rules v1;
- WPF read-only UI;
- sanitized diagnostic report v1;
- Portable Lite build skeleton.

Exit criteria:

- no admin for supported reads;
- no write code reachable in Lite/`--readonly`;
- Windows integration tests green;
- evidence source visible;
- no `status == 0 => healthy printer` shortcut;
- no hidden persistence.

## M2 — Safe local remediation

Deliver:

- privileged helper v1;
- restricted/authenticated local IPC;
- typed capabilities;
- selected-job cancellation;
- controlled Spooler restart;
- before/after snapshots;
- RepairPlan preview/impact/confirmation;
- verification/recovery;
- negative/security tests.

Exit criteria:

- no arbitrary command surface;
- unrelated queues not affected by targeted cancellation;
- service-state recovery tested;
- helper cleanup validated;
- all writes policy-gated;
- “repair” remains local remediation, not hardware service.

## M3 — Zebra native adapter

Deliver:

- capability discovery;
- local/known-endpoint discovery under policy;
- native status normalization;
- firmware/counter read where supported;
- selected read-only configuration;
- device warning/error evidence;
- correlation with Windows evidence;
- hardware validation matrix.

Exit criteria:

- Windows and physical-device status remain separate;
- malformed/timeouts safe;
- unsupported capabilities honest;
- real hardware validates claimed capability/model combinations;
- no firmware/config write unless separately approved.

## M4 — Support + preventive suite

Deliver:

- MaintenanceInspection v1;
- source-backed maintenance task catalog;
- technician checklist;
- baseline import/export/diff;
- maintenance due states;
- explainable health components;
- Preventive Report;
- support bundle schemas;
- service-case/escalation package;
- ServiceDisposition;
- safe diagnostic label under policy;
- N1 -> N2/N3 handoff.

Exit criteria:

- no invented maintenance interval;
- auto vs technician evidence distinguishable;
- redaction tests cover identifiers;
- diagnostic print impossible read-only;
- service disposition is policy-aware;
- report/bundle schemas versioned;
- session cleanup validated.

## M5 — Enterprise hardening and deployment lifecycle

Deliver:

- production signing pipeline;
- checksums/SBOM/provenance;
- policy profiles;
- WDAC/AppLocker/security deployment guidance;
- installed-edition packaging ADR;
- interactive/silent install/uninstall contract;
- offline deployment;
- upgrade/migration/rollback design;
- no-reboot normal-path goal validation;
- helper security review;
- CodeQL/dependency/license gates;
- stable release process.

Exit criteria:

- artifacts verifiably signed when signing available;
- install/uninstall/upgrade tests green;
- Portable no-persistence tests green;
- release docs suitable for enterprise review;
- security review findings resolved or explicitly accepted.

## M6 — Fleet + condition monitoring

Only after ADR for persistence/service/central architecture.

Deliver candidate capabilities:

- inventory;
- maintenance schedule/history;
- configuration baselines/drift;
- health component history;
- condition trends;
- recurring service-case/failure views;
- explainable deduplicated alerts;
- maintenance-by-exception dashboard;
- RBAC/audit/retention;
- backup/restore and operational health.

Exit criteria:

- Portable works independently;
- security/retention model validated;
- alerts drill down to evidence;
- trend is not presented as proven failure cause;
- central service/agent obeys least privilege.

## M7 — Multi-vendor

Add vendor adapters based on real support demand and available hardware, considering Honeywell/TSC/SATO or others only after protocol/SDK/license review.

Each adapter requires capability matrix, contract tests, real hardware validation and no vendor leakage into Domain.

## M8 — Knowledge / AI assistance

Optional:

- local approved manual/runbook retrieval;
- evidence-cited explanations;
- support/preventive/service-case summaries;
- optional cloud provider under explicit privacy policy.

Exit criteria:

- core works with AI disabled;
- AI cannot enable or execute privileged actions;
- AI cannot define maintenance due/disposition;
- privacy/redaction tested;
- uncertainty/evidence citations visible.

## M9 — Predictive-maintenance research

Not a promised product feature.

Start only with sufficient representative labeled history and a defined business target.

Requirements before any prediction claim:

- prediction target/ground truth;
- representative dataset;
- train/validation/test separation;
- false-positive/negative cost analysis;
- calibration;
- model/device applicability matrix;
- drift monitoring;
- human/policy review;
- benchmark against deterministic baselines.

No “failure in N days” claim without validation.

## Cross-milestone audit

At each milestone review business-rule drift, gaps, duplication, complexity, security/privacy, test debt, observability, accessibility/UX, performance, docs, licensing, supply chain and release readiness. Use honest status: `fixed`, `partial`, `experimental`, `deferred`, `not validated`.
