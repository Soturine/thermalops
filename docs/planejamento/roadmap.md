# Roadmap

O roadmap do ThermalOps é **risk-driven**. Read-only evidence, Domain correctness, policy boundaries, source/applicability e security vêm antes de broad remediation, managed fleet automation, AI ou predictive claims.

A expansão recente adiciona três áreas transversais sem alterar esse princípio:

- `Lifecycle & Health` — separar usage/condition/maintenance/current health de RUL;
- `Guided Operations` — troubleshooting e procedures source-backed sem script/AI control plane;
- `Self-Service` — standard-user ExperienceProfile, policy-driven e corporate-friendly.

## Regras do Roadmap

- milestone não é concluído por quantidade de files/UI;
- exit criteria precisam ser verificáveis;
- `Unknown`, `Unsupported`, `Blocked` e `NotValidated` são resultados legítimos;
- hardware/native claims exigem HIL;
- write/privileged/native-action milestones exigem failure/security tests;
- architecture/security decisions relevantes recebem ADR;
- docs/test/release impact fazem parte da mesma entrega;
- não pular foundations para chegar em AI/Fleet;
- uma capability presente no manual/vendor UI não é automaticamente programmatically supported;
- Self-Service não pode depender de security bypass;
- RUL não pode ser implementado como fórmula arbitrária ou LLM output.

## M0 — Product, Safety, Lifecycle, Guidance e Self-Service Foundations

### Objetivo

Definir o que o ThermalOps é, o que não é, como protege customer endpoints e quais Domain/security boundaries guiarão implementation.

### Deliverables

- Engineering Constitution;
- AGENTS operating contract;
- product specification;
- documentation governance/subfolders;
- localization/terminology strategy;
- C#/.NET/WPF ADR;
- privileged-helper ADR;
- field-service/preventive scope ADR;
- maintenance/health ADR;
- localization ADR;
- Guided Operations/Knowledge ADR;
- Self-Service/ExperienceProfile ADR;
- Lifecycle/Health/RUL semantics ADR;
- Portable contract;
- Preventive Maintenance model;
- Lifecycle & Health model;
- Guided Operations / Knowledge model;
- Self-Service model;
- Field Service/Escalation model;
- diagnostics/local-remediation model;
- Deployment/Lifecycle contract;
- Security/Privacy threat model;
- Self-Service/Guided Operations threat-model supplement;
- Support Bundle/ServiceCase direction;
- Fleet/Condition Monitoring direction;
- Testing Strategy;
- dedicated validation matrix para lifecycle/guidance/self-service;
- Release Engineering plan;
- public research notes;
- documentation CI checks;
- license decision;
- initial issue/backlog.

### Exit Criteria

- no contradictory safety requirements;
- read-only, GuidedManual, AssistedWrite, Local Remediation, hardware service e escalation scopes distinct;
- knowledge/runbooks cannot create code capability;
- ExperienceProfile cannot grant authorization;
- maintenance rules require source/applicability;
- `Unknown` semantics explicit;
- lifecycle/current-health/RUL semantics separate;
- privileged-helper principles accepted;
- Portable no-persistence contract explicit;
- localization boundary defined;
- documentation structure coherent;
- open research gaps explicitly listed rather than guessed;
- license selected before accepting copied third-party implementation code;
- CI green.

### Status

`partial` while license decision and other M0 governance items remain open.

## M1 — Read-only Windows Diagnosis + Guidance Primitives

### Objetivo

Criar o primeiro executable útil e seguro: Windows read-only diagnosis com structured evidence e foundations que futuros guided workflows reutilizam.

### Deliverables

- .NET solution/projects necessários;
- Domain primitives para `PrinterIdentity`, `DiagnosticEvidence`, `DiagnosticFinding`, `Policy`, `PrinterSnapshot`;
- minimal primitives para `CanonicalSymptom`, `GuidanceSession` e read-only `Runbook` resolution, sem vendor write actions;
- WinSpool printer enumeration;
- job enumeration;
- Print Spooler read state/config evidence;
- structured Windows printer status flags;
- port/transport evidence;
- PnP/USB evidence;
- print-related Event Log evidence;
- session timeline;
- Quick Diagnosis rule engine v1;
- WPF read-only UI;
- SelfService/Technician presentation proof using same Domain results, sem central auth dependency;
- localization resource foundation (`pt-BR` reference);
- sanitized diagnostic report v1;
- Portable Lite build skeleton;
- Windows integration test foundation.

### Non-goals

- privileged helper;
- device-side config writes;
- firmware/driver install;
- broad network scan;
- managed Self-Service identity/RBAC;
- Fleet backend;
- AI dependency;
- RUL.

### Exit Criteria

- supported read-only workflows sem admin;
- no write code reachable em Lite/`--readonly`;
- Windows integration tests green;
- evidence source/timestamp visible;
- `status == 0 => healthy` shortcut inexistente;
- no hidden persistence;
- no hard-coded business decisions based on localized strings;
- same Domain result across SelfService/Technician presentation test;
- runbook primitives cannot execute arbitrary content;
- sanitized report works offline.

## M2 — Safe Local Remediation Foundation

### Objetivo

Adicionar conjunto mínimo de actions úteis em field support sem criar generic privileged control plane. Essa foundation também será reutilizada por future Guided Operations state-changing actions.

### Deliverables

- Temporary Privileged Helper v1;
- restricted/authenticated local IPC;
- protocol version/session binding;
- typed capabilities;
- selected-job cancellation;
- controlled Print Spooler restart;
- RepairPlan model/use cases;
- before/after snapshots;
- impact preview;
- explicit confirmation;
- post-condition verification;
- recovery/rollback;
- audit events;
- ActionSafetyClass integration for Windows-side actions;
- negative/security tests;
- dedicated destructive test environment.

### Exit Criteria

- no arbitrary command surface;
- helper rejects unknown capability;
- targeted cancellation não afeta unrelated queue;
- stale target revalidation funciona;
- service-state recovery testada;
- UAC-denied/helper-crash paths seguros;
- helper cleanup/no persistence validado;
- all writes policy-gated;
- `--readonly` impossible to bypass;
- Runbook/AI cannot call helper except through typed registered action;
- `Repair` continues meaning Local Remediation, not hardware service.

## M3 — Zebra Native Evidence, Capabilities e Lifecycle Metrics

### Objetivo

Adicionar evidence direta da Zebra e capability discovery para diferenciar Windows/transport de physical/vendor-native state e alimentar preventive/lifecycle/guidance.

### Deliverables

- Zebra adapter implementation;
- capability discovery;
- local/known-endpoint discovery under policy;
- supported Link-OS/SGD/ZPL reads;
- native status normalization;
- firmware read;
- odometer/counter reads where supported;
- `UsageMetric` mapping with raw/normalized units;
- selected read-only configuration;
- SettingsProvider read capability mapping where supported;
- device warnings/errors;
- manufacturer warning mapping;
- correlation with Windows `PrinterIdentity`;
- parser safety limits;
- adapter contract tests;
- real HIL matrix.

### Native diagnostic research track

Mapear, model by model and interface by interface, whether programmatic support exists for candidates such as:

```text
ConfigurationReport
NetworkConfigurationReport
PrintQualityReport
CommunicationDiagnosticsTest
SensorProfileReport
MediaCalibration
```

A feature remains `planned/not validated` until exact invocation/applicability/HIL exist.

### Exit Criteria

- Windows queue and physical-device status separated;
- unsupported capability shown honestly;
- `OperatingHours` not populated unless source/interface proves support;
- usage unit/resettable semantics tested;
- malformed/truncated/oversized/timeout paths safe;
- claimed model/capability combinations HIL-validated;
- no generic arbitrary vendor command interface;
- no firmware/config write by default.

## M4 — Support + Preventive + Guided Operations Suite

### Objetivo

Transform point-in-time diagnosis into complete preventive, guided troubleshooting, report and escalation workflows.

### Deliverables

- `MaintenanceInspection` v1;
- source-backed `MaintenanceTaskCatalog`;
- Technician checklist;
- `MaintenanceDue` states;
- MaintenanceBaseline import/export;
- baseline compatibility validation;
- configuration diff/drift;
- `HealthAssessment` components;
- `ComponentCondition` v1 for supported evidence;
- optional explainable numeric score only if justified;
- Preventive Report;
- versioned Support Bundle schemas;
- `ServiceDisposition`;
- `ServiceCase`/escalation package;
- privacy preview;
- diagnostic label under policy;
- data-only Runbook schema and repository;
- guided troubleshooting read/manual workflows;
- local Knowledge Pack foundation with manifest/hash/source metadata;
- source/version/applicability UI;
- GuidanceSession timeline and ServiceCase linkage;
- approved Zebra native diagnostic actions only for validated capabilities;
- Commissioning/Return-to-Service design prototype, write phases possibly deferred;
- localization of human-readable guidance/reports.

### Exit Criteria

- no invented maintenance interval/lifetime;
- task source/version/applicability preserved;
- automatic vs TechnicianObservation distinct;
- incompatible baseline handled;
- `Unknown` not converted to healthy/not-due;
- Health is not RUL;
- invalid Runbook/Knowledge Pack cannot execute anything;
- diagnostic/write action impossible read-only;
- ServiceDisposition policy-aware;
- schemas versioned;
- archive/path handling safe;
- local Knowledge Pack works offline for supported scenario;
- GuidanceSession can end in resolution or escalation without AI;
- HIL validates each advertised native action;
- session cleanup/no persistence validated.

## M5 — Enterprise Hardening, Managed Self-Service e Deployment Integrations

### Objetivo

Transform development artifacts into predictable corporate distribution and make approved Self-Service usable in restrictive enterprise environments without bypassing endpoint controls.

### Deliverables

- production signing pipeline;
- SHA-256/SBOM/provenance;
- CodeQL/static/dependency/license gates;
- policy profiles hardening;
- WDAC/App Control/AppLocker/EDR deployment guidance;
- installed-edition packaging ADR;
- interactive and silent install/uninstall;
- offline deployment;
- deterministic exit codes/logs;
- upgrade/migration/rollback;
- data retention choices;
- clean uninstall;
- no-reboot normal path validation;
- managed `SelfService` ExperienceProfile;
- user/asset scope architecture;
- optional organization identity/SSO integration design;
- helpdesk connector interface + one optional reference connector only when justified;
- outbound-only ServiceCase submission semantics;
- proxy/firewall endpoint documentation;
- signed/trusted Knowledge Pack distribution design if needed;
- helper and integration security review.

### Exit Criteria

- standard-user Self-Service normal flow has no UAC;
- ExperienceProfile cannot grant capabilities;
- asset-scope tests pass for managed mode;
- endpoint-control blocked behavior is explicit and safe;
- no recommendation to bypass corporate controls;
- privacy preview matches helpdesk payload;
- connector failure falls back to export;
- packages/install lifecycle tests green;
- Portable independence/no-persistence remains green;
- license and redistribution requirements satisfied.

## M6 — Fleet + Condition Monitoring + Health History

### Prerequisite

Dedicated ADR for persistence, identity, agent/service, Central API, auth/RBAC, TLS/certificates and retention.

### Objective

Add continuous visibility and maintenance by exception without making Portable dependent on backend.

### Candidate Deliverables

- managed inventory;
- device identity lifecycle;
- maintenance schedule/history;
- usage history;
- component/HealthAssessment history;
- MaintenanceBaseline assignment;
- configuration drift history;
- ConditionTrend;
- recurring ServiceCase analysis;
- explainable AlertRule engine;
- debounce/dedup/cooldown;
- maintenance-window suppression;
- maintenance-by-exception dashboard;
- compatible peer-group comparisons;
- RBAC/audit/retention/deletion;
- backup/restore;
- managed collector/agent if necessary;
- health/readiness/metrics;
- offline backlog/degraded behavior.

### Exit Criteria

- Portable fully functional without Fleet;
- identity collisions/replacements handled;
- security/RBAC reviewed;
- retention validated;
- backup/restore tested;
- every alert drills down to evidence/rule version;
- trend not presented as causation;
- high usage not presented as fault;
- central agent/service least privilege;
- upgrade/migration operationally tested.

## M7 — Multi-vendor Adapters

### Objective

Add vendor support according to real demand, hardware availability and official interface quality.

Candidates may include Honeywell, TSC, SATO and others only when justified.

### Acceptance Requirements

- real business/use-case demand;
- official protocol/SDK review;
- license/redistribution review;
- capability matrix;
- contract tests;
- parser/security review;
- HIL hardware;
- Lifecycle/Usage metrics semantics mapped without assuming parity;
- Guided Operations source/runbook applicability;
- no vendor leakage into Domain;
- known limitations.

`Multi-vendor` does not mean every vendor exposes identical status, counters, self-tests or settings.

## M8 — Knowledge / AI Assistance

### Objective

Add optional AI/RAG assistance without making model output a source of truth/control plane.

### Candidate Deliverables

- approved manual/runbook retrieval;
- source/evidence citations;
- natural-language symptom -> candidate canonical symptom;
- Finding/Health explanation;
- Preventive/Guidance/ServiceCase summary;
- configuration diff explanation;
- support-note draft;
- multilingual explanation;
- optional cloud provider under explicit privacy policy;
- prompt-injection defenses;
- AI evaluation harness.

### Exit Criteria

- core Guided Operations fully works with AI disabled;
- AI cannot select/authorize typed action without deterministic re-resolution;
- AI cannot define maintenance due/ServiceDisposition/RUL;
- no customer-data upload by default;
- redaction/privacy tests;
- source/evidence citations visible;
- unsupported claims/uncertainty evaluated;
- deterministic fallback works.

## M9 — Predictive Maintenance / Remaining Useful Life Research

### Status

`deferred` and **not a promised product feature**.

### Entry Criteria

Only start with:

- sufficient historical data volume;
- representative populations;
- defined failure/component target;
- labels/ground truth;
- privacy/legal basis;
- deterministic baseline metrics;
- clear business value.

### Validation Requirements

- defined prediction target;
- treatment of maintenance/replacement/censoring;
- temporal train/validation/test separation;
- leakage prevention;
- false-positive/negative cost;
- calibration;
- applicability matrix;
- concept/data drift monitoring;
- benchmark against deterministic rules;
- human/policy review;
- rollback/disable criteria;
- prospective validation before high-stakes claim.

### Forbidden Early Claims

```text
Printer will fail in N days
Printhead has 62% life remaining
Component must be replaced next week
```

unless validated for the explicit applicability class.

## Cross-Milestone Audit

At every milestone boundary review:

### Business / Domain

- business-rule drift;
- health/lifecycle semantic collapse;
- ExperienceProfile mistaken for authorization;
- knowledge mistaken for executable authority;
- missing source/applicability;
- policy bypass.

### Architecture

- boundary leakage;
- duplicate diagnosis engines;
- unnecessary projects/services;
- premature distributed architecture;
- vendor leakage;
- general-purpose runbook scripting creeping in.

### Safety / Security / Privacy

- new trust boundaries;
- privileged/vendor write surface;
- knowledge/import handling;
- customer-data collection;
- helpdesk/network behavior;
- persistence;
- threat-model updates;
- endpoint-control compatibility.

### Quality

- test debt/flakiness;
- failure-path coverage;
- HIL coverage;
- units/conversion correctness;
- observability;
- performance budgets.

### UX / Accessibility / Localization

- progressive disclosure;
- same Domain result across profiles;
- plain-language Self-Service;
- technical detail availability;
- accessibility;
- safety translation quality;
- uncertainty visible.

### Release / Supply Chain

- dependency/license status;
- vendor SDK/manual redistribution status;
- SBOM/security gates;
- packaging/signing;
- known limitations;
- release readiness.

## Honest Status Vocabulary

Use only:

- `fixed` — implemented and required validation completed;
- `partial` — acceptance criteria missing;
- `experimental` — works in controlled subset;
- `deferred` — intentionally postponed with rationale;
- `not validated` — implementation exists without required validation.

Do not use `done`, `stable`, `supported`, `predictive` or `remaining life` when these terms hide validation gaps.

## Próximo passo atual

M0 remains `partial` primarily because governance/licensing remains open. Implementation can proceed incrementally in M1 without waiting for AI, Fleet or predictive work.

The first executable objective remains **read-only Windows diagnosis**, now with enough Domain/architecture planning to ensure it can later feed Guided Operations, Self-Service and Lifecycle/Health without redesigning the core.
