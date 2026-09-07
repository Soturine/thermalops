# Diagnostics and Repair

## Principle

ThermalOps gathers evidence from multiple independent layers, derives findings, recommends the least-impact next action, and separates diagnosis from remediation.

```text
Windows APIs + Device APIs + Diagnostic Rules
                    |
                    v
               Evidence
                    |
                    v
                Findings
                    |
                    v
          Recommended Action
                    |
         (operator confirmation)
                    v
              Repair Plan
```

## Evidence layers

### Windows print subsystem

Collect where available/authorized:

- Print Spooler state;
- service configuration relevant to diagnosis;
- installed printers;
- selected queue details;
- print jobs and job states;
- driver name/version/package evidence;
- port/monitor evidence;
- print processor evidence in advanced mode;
- print-related Windows Event Log entries;
- errors/access-denied/timeouts as first-class evidence.

Prefer WinSpool/SCM/Event Log APIs over command parsing.

### PnP / USB

For locally attached devices:

- PnP presence;
- hardware/instance identity where policy allows;
- connection/disconnection evidence;
- mapped Windows queue/port relationships when determinable.

Do not claim USB physical presence solely because a queue name contains `USB`.

### Network

Only known/explicitly allowed endpoints by default.

Potential checks:

- endpoint resolution;
- TCP reachability to the configured printer service;
- connection timeout/error;
- TLS capability/certificate evidence where supported.

ICMP ping is not equivalent to printer health and must never be the sole reachability conclusion.

### Vendor-native printer

Zebra first. Normalize supported evidence such as:

- responding;
- ready to print;
- head open/closed;
- media out/present;
- ribbon out/present where applicable;
- paused;
- head too hot/temperature warnings;
- buffer/state conditions;
- firmware;
- counters/odometer where supported;
- selected read-only configuration.

Vendor status is evidence from the device. Windows queue status remains separate evidence.

## Status normalization

Do not use:

```text
status == 0 => ONLINE
else => ATTENTION
```

Windows printer status values may be bitmasks/flags and can represent multiple conditions. Preserve flags and translate them individually.

A normalized status model might expose:

```text
WindowsQueueState
TransportState
DeviceState
Readiness
ConsumablesState
MechanicalState
ThermalState
JobsState
```

## Connection classification

Classify from structured evidence where possible:

- USB;
- DOT4;
- TCP/IP RAW;
- TCP/TLS;
- LPR;
- Windows share;
- Bluetooth;
- serial;
- parallel;
- browser/local bridge;
- unknown.

Display raw port name separately from normalized transport.

## Quick Diagnosis rule examples

### Physical problem takes precedence over unnecessary Windows repair

Evidence:

```text
Spooler = Running
Queue jobs = 0
Transport = reachable
Device responding = true
HeadOpen = true
```

Finding:

```text
Windows print path appears operational; device reports head open.
Recommended: close/inspect printer head before any spooler repair.
```

### Stale job

Evidence:

```text
Spooler = Running
Selected queue job count > 0
One job age exceeds policy threshold
Job state indicates error/stall
Device otherwise ready
```

Recommended low-impact plan:

```text
Cancel selected job only -> re-query queue -> validate device/queue
```

### Insufficient evidence

If device-native status cannot be collected, say so. Do not infer `ready` from Windows only.

## Repair impact levels

### Low

Narrow scope, reversible/limited effect.

Example: cancel one selected job.

### Medium

Service-level impact but expected to be recoverable.

Example: controlled Print Spooler restart.

### High

May affect multiple jobs/queues or configuration.

Example: queue repair that must temporarily stop a shared subsystem.

### Break glass

Global reset with broad impact. Requires explicit warning and should be disabled by policy in many environments.

## RepairPlan schema concepts

```text
RepairPlan
  id
  title
  targetResources[]
  impact
  rationaleFindingIds[]
  preconditions[]
  snapshotSpec
  actions[]
  validationChecks[]
  recoverySteps[]
  expectedPostConditions[]
  policyDecision
  requiresElevation
  confirmationText
```

## Cancel selected job

Preferred queue cleanup path:

1. resolve target queue identity;
2. enumerate jobs;
3. revalidate selected job still exists and belongs to queue;
4. capture job snapshot;
5. request explicit operator confirmation if policy requires;
6. call supported job-control API;
7. re-enumerate queue;
8. report success only when target job is absent/cancelled as expected.

Do not delete all spool files to achieve this.

## Controlled spooler restart

Preflight:

- current service state;
- startup configuration/policy evidence where relevant;
- current queues/jobs snapshot;
- permission/elevation capability.

Execution:

- request stop;
- wait with timeout;
- if stop fails, do not continue to deletion/reset actions;
- perform only plan-declared intermediate action;
- request start only when consistent with original/policy state;
- wait with timeout.

Validation:

- verify expected final service state;
- re-enumerate target queue/jobs;
- check relevant events/errors;
- mark partial if service recovered but original fault persists.

Recovery:

- attempt to restore service state when an intermediate step fails;
- if recovery fails, present high-severity outcome and exact safe next step.

## Global spool reset

Never the default repair button.

Requirements before implementation:

- separate break-glass capability;
- clear warning that unrelated local print queues/jobs can be affected;
- snapshot of visible queues/jobs;
- explicit confirmation;
- safe path derivation internally;
- reparse-point/path safety analysis;
- service-state transaction logic;
- post-condition validation;
- audit record.

## Device configuration backup/diff

Read-only milestone:

- query allowlisted safe configuration keys;
- normalize values;
- export snapshot;
- compare snapshot/device A vs B;
- show differences with source/units.

Writing configuration requires a later dedicated design.

## Diagnostic print

A safe diagnostic label is useful for separating software/transport from physical print quality.

It is still a write operation and must have:

- target confirmation;
- policy permission;
- clear label dimensions/media assumptions;
- bounded content;
- no arbitrary user-provided ZPL in privileged workflows;
- validation that job reached the selected printer where possible.

## Evidence-driven UI

Each finding should expose a "Why?" or evidence view. A technician should be able to distinguish:

- observed fact;
- inferred conclusion;
- recommended action;
- action actually executed;
- verified result.
