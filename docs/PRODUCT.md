# Product Specification

## Mission

ThermalOps reduces downtime, support ambiguity, and operational risk around Windows-connected thermal printers by combining:

- Windows print-subsystem evidence;
- transport evidence;
- vendor-native evidence;
- preventive inspection and maintenance policy;
- technician observations;
- safe local remediation;
- support/escalation packaging;
- future fleet/condition monitoring.

The product complements ERP/WMS, label-design/printing software, vendor management suites, and authorized repair organizations. It does not replace them.

## Primary jobs-to-be-done

### Before a failure

- run a preventive inspection;
- collect firmware/counters/configuration where supported;
- compare with an approved baseline;
- detect maintenance due/drift/recurring warnings;
- guide a technician checklist;
- produce a preventive report.

### During an incident

- identify whether the fault is Windows, queue/job, transport, device-native, configuration, or insufficient evidence;
- recommend the least-impact next step;
- perform only policy-authorized local remediation;
- verify the result.

### When local scope ends

- record findings/actions;
- determine/record service disposition;
- generate a service-case/escalation package;
- preserve evidence for N2/N3 or authorized vendor/service workflows.

### Across a fleet

- inventory devices;
- monitor health components/trends;
- track maintenance due;
- detect configuration drift;
- surface recurring failures;
- alert by exception.

## Personas

### Field / N1 technician

Needs fast, safe, low-friction workflows and clear next actions. May perform preventive inspection, diagnosis, evidence collection, simple policy-authorized field actions, and escalation.

### N2/N3 analyst

Needs raw evidence, correlation, logs/events, configuration diff, native protocol status, before/after views, service-case details, and tightly controlled remediation.

### Preventive-maintenance technician

Needs a repeatable inspection workflow that separates automatic evidence from physical/manual checks and produces sourced maintenance recommendations.

### Enterprise/fleet operator

Needs inventory, history, baselines, maintenance scheduling, condition trends, alerts, policy enforcement and auditability.

### Customer security / IT

Needs predictable execution, code signing, no hidden persistence, no automatic upload, no automatic broad network scan, and an exact privileged capability list.

### Authorized service / vendor support recipient

Needs a structured case with model/device identity where allowed, firmware, status, configuration, counters, relevant Windows/transport evidence, actions attempted, technician observations and disposition.

## Editions

### Portable Lite

- self-contained Windows package;
- no installation/runtime installation;
- permanently read-only;
- no UAC/helper path;
- Quick/Advanced diagnosis reads;
- preventive inspection;
- technician checklist;
- baseline comparison/import/export where policy allows;
- sanitized reports;
- service-case evidence collection without local remediation;
- Customer Safe semantics.

### Portable Pro

Everything in Lite plus:

- explicit RepairPlan/local-remediation workflows;
- temporary elevated helper;
- selected-job cancellation;
- controlled spooler restart;
- approved queue remediation;
- safe diagnostic print;
- full N2/N3 bundles/service cases;
- additional device-native diagnostics as capability/policy permit.

### Enterprise

Planned, after dedicated ADRs:

- managed installation;
- inventory/history;
- preventive schedules/history;
- configuration baselines/drift;
- health components/trends;
- explainable alerts;
- service-case history;
- fleet policy;
- RBAC/audit/retention;
- optional collector/agent lifecycle;
- centralized dashboard.

## Main modes

### Quick Diagnosis

Read-only collection focused on:

- Windows print subsystem;
- driver;
- connection;
- queue/jobs;
- device-native status when available.

Output:

- findings ordered by relevance/impact;
- evidence;
- likely fault layer;
- least-impact next step;
- explicit insufficient-evidence state.

### Advanced Diagnostics

Expandable evidence for WinSpool, print processors, drivers/store, ports, PnP, services, Event Log, network endpoint checks, vendor-native status, firmware, counters and selected configuration.

### Preventive Inspection

Read-only-first workflow:

```text
Collect automatic evidence
+ apply source-backed maintenance policy
+ load applicable baseline/history
+ guide technician checklist
+ derive maintenance findings
+ determine service disposition
+ generate preventive report
```

### Analyze Failure

Guided triage that keeps observation, inference, recommendation and action separate.

### Collect Evidence / Prepare Escalation

Produces a support/service case without requiring the operator to perform a repair.

### `--readonly`

Hard guardrail: state-changing methods are unreachable, not just hidden.

### Customer Safe

- no system/printer writes;
- no diagnostic print;
- no automatic network scan;
- no upload/telemetry;
- local session processing only.

## Preventive maintenance domain

See `PREVENTIVE_MAINTENANCE.md`.

Key concepts:

```text
MaintenanceInspection
MaintenanceTaskDefinition
MaintenanceTaskResult
MaintenancePolicy
MaintenanceBaseline
MaintenanceFinding
MaintenanceRecommendation
MaintenanceDue
MaintenanceRecord
HealthAssessment
HealthContribution
ConditionTrend
TechnicianObservation
ServiceDisposition
```

Maintenance intervals must be source-backed. Unknown applicability remains unknown.

## Field service scope

See `FIELD_SERVICE_AND_ESCALATION.md`.

ThermalOps does not assume the operator is a bench-repair technician. Generic field outcomes include:

- continue in service;
- continue with observation;
- local remediation allowed;
- escalate to authorized service;
- remove from service only under explicit policy;
- insufficient evidence.

Company/customer/vendor-specific workflows are policy/configuration, not public-core assumptions.

## Health UX

Primary health display is explainable and component-based:

```text
Overall: ATTENTION RECOMMENDED
Device................ OK
Windows............... OK
Transport............. Observation
Configuration......... Drift
Maintenance........... Due soon
Evidence completeness. 91%
```

A numeric score is optional and secondary; every contribution must be deterministic, visible and versioned. AI does not generate the score.

## Baselines and drift

A baseline is an approved/reference state, not proof that every difference is wrong.

Scope baselines by applicable dimensions such as model/family, DPI, media/application, firmware range, connection and policy/site profile.

Show current vs baseline, evidence source, difference, severity, acknowledgement and recommendation.

## Diagnostic label

A policy-permitted test may include session ID, model/DPI, barcode/QR, line widths, alignment and darkness/calibration patterns. Printing is a write operation and impossible in read-only/Customer Safe mode.

Technician print-quality observations remain human-entered evidence.

## Service cases

A service case can include:

- target identity;
- problem summary;
- evidence/findings;
- technician observations;
- actions attempted/results;
- preventive inspection;
- disposition;
- policy version;
- attachments selected by operator;
- privacy level;
- hash/version manifest.

Direct vendor/RMA submission is not an early requirement.

## Policies

Policy can only reduce or constrain capability; it cannot enable a capability absent from the build.

Candidate policy fields include:

```json
{
  "allowNetworkDiscovery": false,
  "allowDiagnosticPrint": true,
  "allowSpoolerRestart": true,
  "allowQueueRepair": true,
  "allowDriverInstall": false,
  "allowFirmwareUpdate": false,
  "allowFullTechnicalExport": true,
  "allowRemoveFromServiceDisposition": false
}
```

Maintenance tasks/schedules are versioned separately and preserve source/applicability.

## Non-goals for early milestones

- replacing label design/print automation suites;
- general Windows repair;
- arbitrary script execution;
- physical printer disassembly workflow;
- automatic parts replacement decisions;
- autonomous firmware flashing;
- automatic driver replacement;
- mandatory cloud/login;
- autonomous AI remediation;
- broad unattended network scanning;
- automatic vendor/RMA submission;
- predictive failure claims without validated data.
