# Roadmap

Roadmap order is risk-driven. Do not skip read-only foundations to reach flashy repair/AI features.

## M0 — Constitution, threat model, and foundations

Deliver:

- engineering constitution;
- product specification;
- architecture and ADRs;
- portable contract;
- security/privacy model;
- diagnostic/repair model;
- testing/release plans;
- repository CI/document checks;
- license decision;
- initial issue/backlog structure.

Exit criteria:

- no contradictory safety requirements;
- privileged contract principles approved;
- read-only scope clearly separated from writes;
- license selected before accepting copied/third-party code;
- CI green.

## M1 — Read-only Windows diagnosis

Deliver:

- solution/projects;
- printer/job enumeration through Windows APIs;
- spooler read status/config evidence;
- structured Windows status flags;
- port/connection evidence;
- PnP/USB evidence;
- print-related Event Log collection;
- Quick Diagnosis rule engine v1;
- session timeline;
- read-only UI;
- sanitized report v1.

Exit criteria:

- no admin needed for supported read-only workflows;
- no write code reachable in Portable Lite;
- Windows integration tests green;
- evidence source visible in UI;
- no false `ONLINE` shortcut based on a single status integer.

## M2 — Safe repair

Deliver:

- privileged helper v1;
- authenticated/ACL-restricted IPC;
- typed capabilities;
- selected-job cancellation;
- controlled spooler restart;
- before/after snapshots;
- repair-plan preview/impact;
- explicit confirmation;
- verification/recovery;
- negative/security tests.

Exit criteria:

- no arbitrary command surface;
- targeted cancellation does not affect unrelated queues;
- failure injection demonstrates recovery behavior;
- helper terminates/cleans up in portable mode;
- all write paths policy-gated.

## M3 — Zebra native adapter

Deliver:

- adapter capability discovery;
- supported USB/network device discovery under policy;
- native status normalization;
- firmware/counter read where supported;
- selected read-only configuration;
- correlation with Windows queue evidence;
- real hardware validation matrix.

Exit criteria:

- distinguish Windows queue status from device physical status;
- malformed/timeouts handled safely;
- unsupported models/capabilities reported honestly;
- no firmware/configuration write yet unless separately approved.

## M4 — Support suite

Deliver:

- support bundle schemas;
- sanitized/full export UX;
- hash manifest;
- snapshot compare/diff;
- configuration export/diff;
- safe diagnostic label under policy;
- N1 handoff to N2/N3 workflow.

Exit criteria:

- redaction tests cover identifiers;
- bundle contents documented/versioned;
- diagnostic print is impossible in read-only mode;
- session cleanup validated.

## M5 — Enterprise hardening

Deliver:

- production signing pipeline;
- SBOM/checksums/provenance;
- policy profiles;
- WDAC/AppLocker deployment guidance;
- packaging decision for installed edition;
- security review of helper;
- CodeQL/dependency/license gates;
- stable release process.

Exit criteria:

- artifacts verifiably signed;
- security review findings addressed or explicitly accepted;
- install/uninstall and portable no-persistence tests green;
- release docs suitable for enterprise application-control review.

## M6 — Fleet

Deliver only after an ADR for persistence/service/central architecture.

Candidate capabilities:

- inventory;
- historical health;
- alerts;
- configuration drift;
- fleet policy;
- dashboard;
- RBAC/audit if central control exists.

Do not force Portable to depend on Fleet.

## M7 — Multi-vendor

Add adapters based on real demand/available hardware, initially considering Honeywell/TSC.

Adapter acceptance requires:

- capability matrix;
- official protocol/SDK review;
- contract tests;
- real hardware validation;
- no vendor-specific leakage into Domain.

## M8 — Knowledge/AI

Deliver optional assistance:

- local approved manual/runbook retrieval;
- evidence-cited explanations;
- support-note summarization;
- optional cloud provider integration under explicit privacy policy.

Exit criteria:

- core product works with AI completely disabled;
- AI cannot create/execute privileged actions;
- privacy/redaction policy tested;
- answers cite evidence/source material;
- uncertainty is visible.

## Cross-milestone audits

At the end of every milestone review:

- business-rule drift;
- gaps;
- deduplication opportunities;
- unnecessary complexity;
- security/privacy;
- QA/test debt;
- observability;
- docs;
- performance where relevant;
- release readiness;
- `fixed/partial/experimental/deferred/not validated` status.
