# Roadmap

O roadmap do ThermalOps é **risk-driven**. Read-only evidence, Domain correctness e policy boundaries vêm antes de broad remediation, fleet automation ou AI/predictive features.

A ordem existe para reduzir retrabalho e evitar que uma capability chamativa dependa de fundações frágeis.

## Regras do Roadmap

- milestone não é “concluído” por quantidade de files/UI;
- exit criteria precisam ser verificáveis;
- status deve ser honesto;
- hardware claims exigem HIL;
- write/privileged milestones exigem failure/security tests;
- architecture decisions significativas recebem ADR;
- docs/test/release impact fazem parte da mesma entrega;
- não pular foundations para chegar em AI/Fleet.

## M0 — Product, Safety, Maintenance e Field-Service Foundations

### Objetivo

Definir o que o ThermalOps é, o que não é, como protege customer endpoints e quais boundaries guiarão implementação.

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
- Portable contract;
- Preventive Maintenance model;
- Field Service/Escalation model;
- diagnostics/local-remediation model;
- Deployment/Lifecycle contract;
- Security/Privacy threat model;
- Support Bundle/ServiceCase direction;
- Fleet/Condition Monitoring direction;
- Testing Strategy;
- Release Engineering plan;
- public research notes;
- CI documentation checks;
- license decision;
- initial issue/backlog.

### Exit Criteria

- no contradictory safety requirements;
- read-only, Local Remediation, hardware service e escalation scopes distintos;
- maintenance rules exigem source/applicability;
- `Unknown` semantics explícitas;
- privileged-helper principles accepted;
- Portable no-persistence contract explícito;
- localization boundary definida;
- documentation structure coerente;
- license selecionada antes de aceitar copied third-party implementation code;
- CI green.

### Status

`partial` enquanto license decision e demais M0 governance items permanecerem abertos.

## M1 — Read-only Windows Diagnosis Foundation

### Objetivo

Criar o primeiro executable útil e seguro: diagnosis Windows read-only com evidence estruturada.

### Deliverables

- .NET solution/projects necessários;
- Domain primitives para PrinterIdentity, Evidence, Finding, Policy e Snapshot;
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
- localization resource foundation (`pt-BR` reference);
- sanitized diagnostic report v1;
- Portable Lite build skeleton;
- Windows integration test foundation.

### Non-goals

- privileged helper;
- repair;
- firmware write;
- driver install;
- broad network scan;
- Fleet backend;
- AI dependency.

### Exit Criteria

- supported read-only workflows sem admin;
- no write code reachable em Lite/`--readonly`;
- Windows integration tests green;
- evidence source/timestamp visible;
- `status == 0 => healthy` shortcut inexistente;
- no hidden persistence;
- no hard-coded business decisions based on localized strings;
- sanitized report funciona offline.

## M2 — Safe Local Remediation

### Objetivo

Adicionar um conjunto mínimo de actions que realmente ajudem em field support sem criar generic privileged control plane.

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
- `--readonly` continua impossível de burlar;
- `Repair` continua significando Local Remediation, não hardware service.

## M3 — Zebra Native Adapter

### Objetivo

Adicionar evidence direta da impressora Zebra para diferenciar Windows/transport de physical/vendor-native state.

### Deliverables

- Zebra adapter project/contract implementation;
- capability discovery;
- local/known-endpoint discovery sob policy;
- supported Link-OS/SGD/ZPL reads;
- native status normalization;
- firmware read;
- counter/odometer read where supported;
- selected read-only configuration;
- device warnings/errors;
- correlation com Windows PrinterIdentity/evidence;
- parser safety limits;
- contract tests;
- real hardware validation matrix.

### Exit Criteria

- Windows queue e physical-device status separados;
- unsupported capability apresentada honestamente;
- malformed/truncated/oversized/timeout paths seguros;
- claimed model/capability combinations validados em hardware real;
- no generic arbitrary vendor command interface;
- no firmware/config write salvo novo ADR/milestone approval.

## M4 — Support + Preventive Suite

### Objetivo

Transformar diagnosis pontual em workflow completo de preventiva, report e escalation handoff.

### Deliverables

- `MaintenanceInspection` v1;
- versioned/source-backed MaintenanceTaskCatalog;
- Technician checklist;
- `MaintenanceDue` states;
- MaintenanceBaseline import/export;
- baseline compatibility validation;
- configuration diff/drift;
- HealthAssessment components;
- optional explainable numeric score somente se justified;
- Preventive Report;
- versioned support schemas;
- sanitized/full Support Bundle;
- `ServiceDisposition`;
- `ServiceCase`/escalation package;
- privacy preview;
- attachment safety foundation, se attachments entrarem no milestone;
- diagnostic label sob policy;
- N1 -> N2/N3 handoff workflow;
- localization dos human-readable reports.

### Exit Criteria

- nenhum invented maintenance interval;
- task source/version/applicability preservadas;
- automatic vs TechnicianObservation distinguíveis;
- incompatible baseline tratado corretamente;
- `Unknown` não vira healthy/not-due;
- redaction tests cobrem identifiers;
- diagnostic print impossível em read-only;
- ServiceDisposition é policy-aware;
- `RemoveFromService` exige explicit authority;
- schemas versionados;
- bundle manifest/hash validado;
- archive/path handling seguro;
- session cleanup/no persistence validado.

## M5 — Enterprise Hardening e Deployment Lifecycle

### Objetivo

Transformar artifacts de desenvolvimento em distribuição corporativa previsível e governável.

### Deliverables

- production signing pipeline;
- SHA-256 checksums;
- SBOM;
- provenance/attestation where feasible;
- CodeQL/static analysis;
- dependency/vulnerability gates;
- license inventory/gates;
- policy profiles hardening;
- WDAC/AppLocker/EDR deployment guidance;
- installed-edition packaging ADR;
- interactive install;
- silent install/uninstall;
- offline deployment;
- deterministic exit codes/logs;
- upgrade/migration;
- rollback/recovery;
- data retention choices;
- clean uninstall;
- no-reboot normal-path validation;
- helper security review;
- stable release procedure.

### Exit Criteria

- artifacts verifiably signed quando signing infrastructure disponível;
- package final smoke-tested;
- clean/silent install/uninstall tests green;
- N-1 -> N upgrade green;
- migration failure/recovery testado;
- Portable no-persistence tests green;
- endpoint application-control review docs completas;
- security findings resolved ou explicitamente accepted com residual risk;
- project/dependency licensing adequado à distribuição.

## M6 — Fleet + Condition Monitoring

### Prerequisite

Dedicated ADR para persistence, identity, agent/service, Central API, auth/RBAC, TLS/certificates e retention.

### Objetivo

Adicionar visão contínua e maintenance by exception sem tornar Portable dependente de backend.

### Candidate Deliverables

- managed inventory;
- device identity lifecycle;
- maintenance schedule/history;
- MaintenanceBaseline assignment;
- configuration drift history;
- HealthAssessment history;
- ConditionTrend;
- recurring ServiceCase/failure views;
- explainable AlertRule engine;
- debounce/dedup/cooldown;
- maintenance-window suppression;
- maintenance-by-exception dashboard;
- RBAC;
- audit;
- retention/deletion;
- backup/restore;
- managed collector/agent se necessário;
- health/readiness/metrics;
- offline backlog/degraded behavior.

### Exit Criteria

- Portable totalmente funcional sem Fleet;
- identity collisions tratadas;
- security/RBAC model reviewed;
- TLS/certificate lifecycle definido;
- retention policy validada;
- backup/restore testados;
- alert storm controls testados;
- every alert drills down to evidence/rule version;
- trend não é apresentada como proven cause;
- central agent/service usa least privilege;
- upgrade/migration operacional testado.

## M7 — Multi-vendor Adapters

### Objetivo

Adicionar vendor support de acordo com demanda real, hardware disponível e official interface quality.

Candidates iniciais podem incluir:

- Honeywell;
- TSC;
- SATO;
- outros somente quando justificados.

### Adapter Acceptance Requirements

- business/use-case demand;
- official protocol/SDK review;
- license/redistribution review;
- capability matrix;
- contract tests;
- parser/security review;
- HIL hardware;
- no vendor-specific leakage into Domain;
- known limitations;
- model/firmware/transport applicability.

“Multi-vendor” não significa que todos os vendors precisam oferecer as mesmas capabilities.

## M8 — Knowledge / AI Assistance

### Objetivo

Adicionar optional assistance sem tornar AI source of truth/control plane.

### Candidate Deliverables

- local approved manual/runbook retrieval;
- source/evidence citations;
- Finding explanation;
- Preventive Report summary;
- ServiceCase summary;
- configuration diff explanation;
- support-note draft;
- multilingual explanation;
- optional cloud provider integration sob explicit privacy policy;
- RAG prompt-injection defenses;
- AI evaluation harness.

### Exit Criteria

- core funciona totalmente com AI disabled;
- AI não executa/habilita privileged action;
- AI não define maintenance due/ServiceDisposition;
- no customer-data upload by default;
- redaction/privacy tests;
- source/evidence citations visíveis;
- unsupported claims/uncertainty avaliados;
- deterministic fallback funcional.

## M9 — Predictive-Maintenance Research

### Status

`deferred` e **não é promised product feature**.

### Entry Criteria

Só iniciar com:

- volume suficiente de historical data;
- representative populations;
- useful business target;
- clear labels/ground truth;
- privacy/legal basis para dados;
- baseline deterministic metrics.

### Validation Requirements

- defined prediction target;
- representative dataset;
- train/validation/test separation;
- time leakage prevention;
- false-positive/false-negative cost analysis;
- calibration;
- confidence/reliability analysis;
- device/model applicability matrix;
- concept/data drift monitoring;
- comparison to deterministic baseline;
- human review;
- policy boundary;
- rollback/disable criteria;
- prospective validation antes de high-stakes claim.

### Forbidden Early Claim

Não publicar:

```text
“Printer will fail in N days.”
“Printhead has X days remaining.”
```

sem validation suficiente para aquele target/population.

## Cross-Milestone Audit

Ao fim de cada milestone revisar:

### Business / Domain

- business-rule drift;
- contradictory semantics;
- missing Domain concepts;
- UI redefinindo Domain;
- policy bypass.

### Architecture

- boundary leakage;
- duplicated modules;
- unnecessary complexity;
- premature distributed architecture;
- vendor leakage.

### Safety / Security / Privacy

- new trust boundaries;
- privileged surface;
- imported data handling;
- customer-data collection;
- network behavior;
- persistence;
- threat-model updates.

### Quality

- test debt;
- flaky tests;
- failure-path coverage;
- HIL coverage;
- observability;
- performance budgets.

### UX / Localization

- accessibility;
- progressive disclosure;
- technical terminology consistency;
- missing localization resources;
- safety-warning clarity.

### Release / Supply Chain

- dependency/license status;
- SBOM;
- static/security gates;
- packaging;
- docs;
- known limitations;
- release readiness.

## Honest Status Vocabulary

Use:

- **fixed** — implemented e required validation concluída;
- **partial** — acceptance criteria faltando;
- **experimental** — funciona em subset/controlled conditions;
- **deferred** — intentionally postponed com rationale;
- **not validated** — implementation existe sem required validation.

Não usar “done”, “stable” ou “supported” quando essas palavras escondem validation gaps.

## Próximo Passo Atual

Enquanto M0 governance não estiver completamente fechado, o implementation work pode avançar de forma incremental no M1 somente se não depender da decisão pendente de licensing/copying de terceiros.

O primeiro objetivo executable permanece: **read-only Windows diagnosis foundation**, com code e tests em inglês, UI localization-ready e pt-BR como locale de referência.
