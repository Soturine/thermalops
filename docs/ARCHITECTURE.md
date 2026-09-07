# Architecture

## Style

ThermalOps starts as a **modular monolith** with a separately elevated helper as a security boundary.

```text
+-------------------------------------------------------+
|                  ThermalOps.Desktop                   |
| Diagnose | Preventive | Failure | Support | Reports   |
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

Only when an approved write requires it:

Application -> strict local IPC -> Temporary Privileged Helper -> Windows
```

## Proposed solution structure

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

Do not create extra projects merely to make the architecture look sophisticated.

## Dependency direction

```text
Desktop ---------------------> Application --------> Domain
Windows Infrastructure ------> application/domain ports
Vendor Adapters -------------> application/domain ports
Privileged Helper -----------> tiny typed privileged contract
```

Domain must not reference WPF, P/Invoke, filesystem, network implementation, vendor SDK, database, AI SDK or installer technology.

## Core evidence concepts

### PrinterIdentity

Normalized identity assembled from available queue, port, PnP, vendor identifier/serial and endpoint evidence. Friendly name alone is insufficient.

### PrinterSnapshot

Immutable point-in-time observation set.

### DiagnosticEvidence

Contains source, timestamp, category, normalized value, safe raw representation when needed, target, and collection outcome.

### TechnicianObservation

Human-entered evidence with operator/session/time attribution. Never presented as automatically measured data.

### DiagnosticFinding

Conclusion derived from evidence IDs, with severity, certainty semantics, explanation and recommended next step.

## Maintenance concepts

### MaintenanceInspection

A session/workflow that combines automatic evidence, applicable maintenance tasks, technician checks, baseline/history comparison and disposition.

### MaintenanceTaskDefinition

Versioned task with applicability, source/reference, interval/trigger rule, safety notes and policy requirements.

### MaintenanceTaskResult

Result for one inspection: `Pass`, `Observation`, `Fail`, `NotPerformed`, `NotApplicable`, or `Blocked`.

### MaintenanceBaseline

Versioned approved/reference state with applicability scope.

### MaintenanceDue

Derived due state (`Unknown`, `NotDue`, `DueSoon`, `Due`, `Overdue`, etc.) with rule/source reference.

### HealthAssessment

Explainable aggregate of evidence/components. Optional numeric score stores every deterministic contribution and rule version.

### ConditionTrend

Historical observation/trend, not a proven failure cause.

## Service concepts

### ServiceDisposition

Policy-aware field outcome such as continue, observe, local remediation, escalate, remove-from-service (only if allowed), or insufficient evidence.

### ServiceCase

Structured handoff containing target, evidence, findings, technician observations, actions/results, preventive inspection, disposition, attachments, privacy level and manifest.

### EscalationPolicy

Maps evidence/findings and operator authority to allowed/recommended next steps without embedding company/vendor-specific process into the public core.

## Print job

A `PrintJob` belongs to a specific queue and preserves stable queue/job identity, state flags, timestamps where available and policy-controlled document metadata.

## Local remediation / RepairPlan

`RepairAction` is strongly typed. Examples:

```text
CancelPrintJob(queueId, jobId)
RestartSpooler(expectedInitialState)
RepairSelectedQueue(queueId, strategyId)
```

No free-form privileged command string.

Every `RepairPlan` includes targets, impact, rationale finding IDs, preconditions, snapshot, actions, confirmation, expected post-conditions, validation, recovery and policy decision.

## Windows boundaries

Prefer supported APIs:

- WinSpool for printer/job enumeration/control;
- Service Control Manager for spooler state/control;
- PnP/SetupAPI or supported managed interfaces for device evidence;
- Event Log APIs;
- narrowly scoped network APIs for known endpoints.

Shell/process invocation, if unavoidable for a specific supported tool, uses a fixed executable/argument schema and never arbitrary user/device strings.

## Vendor adapter

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

Adapters expose capabilities/evidence. They do **not** own business maintenance policy, field disposition, escalation policy, UI or AI decisions.

Read and write capabilities are separate.

## Zebra adapter direction

Use supported Zebra Link-OS / SGD / ZPL mechanisms where practical and validated. Preserve vendor-native source and capability/firmware applicability.

Potential evidence includes readiness, head/media/ribbon/pause/temperature conditions, device warnings/errors, firmware, counters and selected read-only settings.

## Connection model

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

Port number/name is evidence, not sufficient transport identity by itself.

## Privileged helper

Required properties:

- launched only for an approved Portable Pro action;
- UAC applies to helper, not UI;
- restrictive local IPC ACL;
- protocol version;
- session binding/nonce;
- caller validation where practical;
- strongly typed request;
- capability allowlist;
- bounded inputs/timeouts;
- helper revalidates target/policy;
- structured result;
- no arbitrary process/shell/script/file/registry endpoint;
- terminates and cleans up in portable mode.

See ADR-0002.

## Portable vs Enterprise boundary

Portable:

- no persistent database/agent;
- session-local processing;
- optional explicit baseline import/export;
- works offline;
- no dependency on central services.

Enterprise may reuse Domain/Application/adapters but requires ADRs for persistence, agent/service, API, authentication/RBAC, TLS, retention, backup/restore, update lifecycle and observability.

Do not turn Portable into a thin client for Fleet.

## UI

N1/field: progressive disclosure and guided disposition.

N2/N3: detailed evidence, configuration/counters, maintenance, actions and service-case export.

Primary home actions:

```text
Quick Diagnosis
Preventive Inspection
Analyze Failure
Collect Evidence
Prepare Escalation
Technical Reports
```

Destructive controls are secondary/contextual, never the visual center of the product.

## Composition root

Desktop composes policy source, maintenance catalog/baseline provider, Windows implementations, vendor adapters, diagnostic/maintenance rules, support/service-case generator, privileged-helper client and view models.

No hidden service locator in domain logic.
