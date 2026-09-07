# Arquitetura

## Visão geral

ThermalOps começa como **modular monolith** com um Temporary Privileged Helper separado como security boundary.

A arquitetura deve suportar crescimento de scope sem transformar o projeto precocemente em microservices ou espalhar vendor-specific logic pelo Domain.

```text
+-------------------------------------------------------+
|                  ThermalOps.Desktop                   |
| Diagnosis | Preventive | Failure | Support | Reports  |
+--------------------------+----------------------------+
                           |
                           v
+-------------------------------------------------------+
|                ThermalOps.Application                 |
| Diagnose | Inspect | Assess | Remediate | Escalate    |
+--------------------------+----------------------------+
                           |
                           v
+-------------------------------------------------------+
|                   ThermalOps.Domain                   |
| Printer | Evidence | Finding | Maintenance | Service  |
| Snapshot | Policy | RepairPlan | Disposition          |
+------------+----------------------+-------------------+
             |                      |
             v                      v
+------------------------+   +--------------------------+
| Windows Infrastructure |   | Vendor Adapters          |
| WinSpool/SCM/PnP/Event |   | Zebra first              |
+------------------------+   +--------------------------+

Approved writes only:

Application -> strict IPC -> Temporary Privileged Helper -> Windows
```

## Estrutura de solution proposta

Criar projects apenas quando o milestone precisar deles.

```text
src/
├── ThermalOps.Domain/
├── ThermalOps.Application/
├── ThermalOps.Infrastructure.Windows/
├── ThermalOps.Adapters.Zebra/
├── ThermalOps.Desktop/
└── ThermalOps.PrivilegedHelper/

tests/
├── ThermalOps.Domain.Tests/
├── ThermalOps.Application.Tests/
├── ThermalOps.Infrastructure.Windows.Tests/
├── ThermalOps.Adapters.Zebra.Tests/
├── ThermalOps.Security.Tests/
└── ThermalOps.EndToEnd.Tests/
```

Não criar projects vazios apenas para deixar o repository “enterprise-looking”.

## Dependency Direction

```text
Desktop ---------------------> Application --------> Domain
Windows Infrastructure ------> Application/Domain ports
Vendor Adapters -------------> Application/Domain ports
Privileged Helper -----------> tiny typed privileged contract
```

`Domain` não referencia:

- WPF;
- P/Invoke implementation;
- filesystem implementation;
- network implementation;
- vendor SDK;
- database;
- AI SDK;
- installer technology.

## Composition Root

O entry point do Desktop é o composition root.

Ele compõe:

- policy source;
- localization resources;
- maintenance catalog;
- baseline provider;
- Windows implementations;
- vendor adapters;
- diagnostic rules;
- maintenance rules;
- report/ServiceCase generators;
- privileged-helper client;
- ViewModels.

Não usar hidden service locator dentro do Domain.

## Core Evidence Concepts

### PrinterIdentity

Identity normalizada construída de evidence disponível, não de friendly name.

Potential inputs:

- Windows queue identity;
- port identity;
- PnP device identity;
- vendor serial/device ID;
- network endpoint;
- USB instance data;
- explicitly managed Enterprise identity.

Identity resolution deve tolerar evidence parcial sem fundir devices incorretamente.

### PrinterSnapshot

Immutable point-in-time observation set.

Usado para:

- before/after;
- baseline compare;
- support bundle;
- preventive inspection;
- condition history.

### DiagnosticEvidence

Campos conceituais:

```text
EvidenceId
Source
Timestamp
TargetId
Category
NormalizedValue
SafeRawRepresentation?
CollectionOutcome
Error?
SchemaVersion
```

### TechnicianObservation

Human-entered evidence com:

- operator/session attribution;
- timestamp;
- observation type;
- value/result;
- note/attachment reference quando permitido.

Nunca deve ser apresentado como sensor/automatic evidence.

### DiagnosticFinding

Conclusão derivada de evidence IDs.

Inclui:

- type;
- severity;
- certainty semantics;
- explanation/resource key;
- evidence references;
- recommended next step;
- rule version.

Finding não reescreve evidence para caber na conclusão.

## PrintJob

`PrintJob` pertence a uma queue específica e preserva:

- canonical queue identity;
- job ID;
- state flags;
- timestamps quando disponíveis;
- age;
- policy-controlled document metadata;
- collection outcome.

Document name/content deve ser minimizado por privacy.

## Maintenance Concepts

### MaintenanceInspection

Workflow/session que combina:

- automatic evidence;
- applicable MaintenanceTaskDefinitions;
- TechnicianObservation/checklist;
- baseline/history comparison;
- MaintenanceDue;
- Findings;
- ServiceDisposition.

### MaintenanceTaskDefinition

Versioned task com:

- source/reference;
- applicability;
- trigger/interval;
- safety notes;
- result semantics;
- capability/policy requirements.

### MaintenanceTaskResult

Suggested states:

```text
Pass
Observation
Fail
NotPerformed
NotApplicable
Blocked
```

### MaintenanceBaseline

Versioned reference state com applicability scope.

### MaintenanceDue

Derived state:

```text
Unknown
NotApplicable
NotDue
DueSoon
Due
Overdue
Blocked
```

### HealthAssessment

Explainable aggregate de health components.

Se numeric score existir, cada `HealthContribution` precisa ser persistível/inspectable.

### ConditionTrend

Historical trend, não proven root cause.

## Service Concepts

### ServiceDisposition

Policy-aware outcome:

```text
ContinueInService
ContinueWithObservation
LocalRemediationAllowed
EscalateToAuthorizedService
RemoveFromService
InsufficientEvidence
```

### ServiceCase

Structured handoff com:

- target;
- evidence;
- Findings;
- TechnicianObservation;
- actions/results;
- Preventive Inspection;
- disposition;
- attachments;
- privacy level;
- manifest.

### EscalationPolicy

Mapeia evidence/findings + field authority para recommendations/allowed outcomes sem colocar company-specific workflow no core.

## Policy Model

Policy é input versionado e restritivo.

Invariants:

- policy pode disable capability;
- policy pode exigir stronger confirmation;
- policy pode restringir export/discovery;
- policy não cria executable capability;
- imported policy é untrusted até validation/trust handling;
- policy ID/version aparece em audit/report quando influencia decisão.

## RepairPlan / Local Remediation

`RepairAction` é strongly typed.

Examples:

```text
CancelPrintJob(queueId, jobId)
RestartSpooler(expectedInitialState)
RepairSelectedQueue(queueId, strategyId)
```

No free-form privileged command string.

`RepairPlan` inclui:

```text
PlanId
Targets[]
Impact
RationaleFindingIds[]
Preconditions[]
SnapshotSpec
Actions[]
ConfirmationRequirements
ValidationChecks[]
RecoverySteps[]
ExpectedPostConditions[]
PolicyDecision
RequiresElevation
```

Future action requer code change + review + tests + capability registration.

## Windows Boundaries

Prefer supported APIs em vez de shell parsing.

### WinSpool

Use para:

- printer enumeration;
- queue details;
- jobs;
- job control;
- supported queue operations.

### Service Control Manager

Use para:

- Spooler state;
- startup/config evidence;
- controlled service operations quando autorizado.

### PnP / SetupAPI

Use para device presence/identity/correlation quando apropriado.

### Event Log

Use Windows Event Log APIs para print-related evidence.

### Network

Use narrowly scoped APIs para known endpoints. Broad discovery é policy-gated.

### Shell/Process Invocation

Se uma future integration exigir external executable suportado:

- fixed executable path/identity;
- strongly structured arguments;
- no untrusted string concatenation;
- timeout;
- output size bounds;
- explicit ADR/security rationale.

Nunca usar shell como default integration layer.

## Vendor Adapter Boundary

Conceptual interface:

```text
IPrinterVendorAdapter
  CanHandle(evidence)
  GetCapabilitiesAsync(printer)
  DiscoverLocalAsync(policy)
  ReadIdentityAsync(printer)
  ReadStatusAsync(printer)
  ReadCountersAsync(printer)
  ReadConfigurationAsync(printer, requestedKeys)
  RunApprovedDiagnosticAsync(...)
```

Adapters:

- expõem capabilities/evidence;
- preservam vendor source;
- tratam device input como untrusted;
- não definem MaintenancePolicy;
- não definem ServiceDisposition;
- não definem UI;
- não definem AI behavior.

Read capability e write capability são distintas.

## Zebra Adapter Direction

Usar interfaces suportadas Zebra Link-OS / SGD / ZPL quando práticas e validadas.

Potential evidence:

- readiness;
- head state;
- media/ribbon;
- pause;
- thermal warning;
- device warning/errors;
- firmware;
- counters;
- selected read-only config.

Cada capability precisa de applicability por model/firmware/connection quando necessário.

## Connection Model

Represent transport independentemente do vendor:

```text
Usb
Dot4
TcpRaw
TcpTls
Lpr
WindowsShare
Bluetooth
Serial
Parallel
BrowserBridge
Unknown
```

Port number ou friendly port name é evidence, não identity suficiente do transport.

## Temporary Privileged Helper

Security properties obrigatórias:

- launched somente para approved Portable Pro action;
- UAC somente no helper;
- restrictive local IPC ACL;
- protocol version;
- session-bound nonce/token;
- caller validation onde prático;
- strongly typed request;
- capability allowlist;
- bounded input;
- timeout;
- canonical target revalidation;
- policy revalidation;
- structured response;
- no arbitrary process/shell/file/registry endpoint;
- cleanup/termination.

Veja ADR-0002.

## IPC Direction

Named pipes são preferred candidate, mas implementation detail final precisa de M2 review.

O protocol deve incluir:

- protocol version;
- session ID;
- request ID;
- nonce/token;
- action type;
- canonical target;
- action-specific payload;
- timeout/deadline;
- result/status;
- verification metadata.

## Portable vs Enterprise Boundary

Portable:

- no persistent DB;
- no agent/service;
- session-local;
- offline;
- explicit baseline import/export;
- central backend optional/nonexistent.

Enterprise pode reutilizar Domain/Application/Adapters, mas exige ADRs para:

- persistence;
- agent/service lifecycle;
- Central API;
- auth/RBAC;
- TLS/certificates;
- retention;
- backup/restore;
- update lifecycle;
- observability.

Não transformar Portable em thin client para Fleet.

## UI Architecture

WPF é initial UI.

Princípios:

- MVVM-compatible separation;
- no business rule em code-behind;
- user strings em localization resources;
- commands/capabilities vêm de Application state/policy;
- evidence drill-down disponível;
- destructive actions contextuais;
- async collection sem congelar UI;
- cancellation/timeouts visíveis.

### N1 / Field

Progressive disclosure e guided next step.

### N2/N3

Deep evidence, counters/config, Maintenance, actions, ServiceCase e timeline.

Home actions:

```text
Quick Diagnosis
Preventive Inspection
Analyze Failure
Collect Evidence
Prepare Escalation
Technical Reports
```

## Localization Boundary

UI labels podem ser pt-BR/en-US/etc., mas Domain enums/schema values permanecem canonical English identifiers.

Nunca use localized display text como key de business logic.

## Failure Handling

External boundary failure vira structured outcome:

```text
Success
Unavailable
Unsupported
AccessDenied
Timeout
MalformedResponse
Disconnected
Partial
Failed
```

Não lançar exception genérica até a UI sem semantic normalization quando o Domain/Application precisa distinguir estados.

## Observability

Application events podem ser estruturados como:

```text
SessionStarted
EvidenceCollectionStarted
EvidenceCollected
EvidenceCollectionFailed
MaintenanceInspectionStarted
RepairPlanRequested
RepairPlanExecuted
RepairPlanVerified
ServiceDispositionAssigned
ServiceCaseExported
SessionCleanupCompleted
```

Event type permanece locale-neutral.

## Architecture Evolution Rules

Antes de adicionar novo project/service:

1. identificar boundary real;
2. demonstrar por que existing module não é suficiente;
3. avaliar coupling/deployment/testing cost;
4. criar ADR quando decisão for significativa;
5. manter Domain independente;
6. incluir security/privacy impact;
7. definir validation strategy.

Complexidade só entra quando resolve problema real.
