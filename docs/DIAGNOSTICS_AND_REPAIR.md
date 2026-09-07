# Diagnostics and Local Remediation

## Principle

ThermalOps gathers evidence from multiple independent layers, derives findings, recommends the least-impact next step, and separates diagnosis from preventive maintenance, local remediation, and escalation.

```text
Windows APIs + Vendor APIs + Technician observations + Approved policy
                             |
                             v
                          Evidence
                             |
                             v
                          Findings
             +---------------+---------------+
             |               |               |
             v               v               v
      Preventive         Local            Escalation
      recommendation     remediation      recommendation
                         plan
```

A technician is not assumed to be authorized to perform internal hardware repair.

## Evidence layers

### Windows print subsystem

Collect where available/authorized:

- Print Spooler state and relevant configuration;
- installed printers and selected queue details;
- print jobs and job states;
- driver identity/version/package evidence;
- port/monitor evidence;
- print processor evidence in advanced mode;
- print-related Windows Event Log entries;
- access denied/timeouts/errors as first-class evidence.

Prefer supported WinSpool/SCM/Event Log APIs over command-output parsing.

### PnP / USB

- physical/PnP presence where observable;
- hardware/instance identity when policy allows;
- connect/disconnect evidence;
- queue/port mapping when determinable.

Never infer USB presence solely from a friendly string.

### Network / transport

Only known or explicitly authorized endpoints by default.

Potential checks:

- endpoint resolution;
- TCP reachability to configured service;
- timeout/error behavior;
- TLS capability/certificate evidence where supported.

ICMP alone is not printer health.

### Vendor-native printer

Zebra first. Normalize supported evidence such as:

- communication result;
- ready-to-print;
- head state;
- media/ribbon state;
- pause state;
- temperature warning;
- buffer/state conditions;
- firmware;
- counters/odometer where supported;
- selected safe read-only configuration;
- device-reported warnings/errors.

Vendor-native state and Windows queue state remain separate.

### Technician observations

Manual evidence can include visual condition, cable condition, unusual noise, print quality or checklist results. It must carry human/session attribution and never be presented as automatically measured.

## Status normalization

Do not use:

```text
status == 0 => ONLINE/HEALTHY
```

Preserve Windows bit flags and vendor-native fields individually.

Suggested normalized components:

```text
WindowsQueueState
TransportState
DeviceState
Readiness
ConsumablesState
MechanicalState
ThermalState
JobsState
EvidenceCompleteness
```

## Quick Diagnosis examples

### Device condition outranks unnecessary Windows repair

Evidence:

```text
Spooler=Running
QueueJobs=0
Transport=Reachable
DeviceResponding=true
HeadOpen=true
```

Finding:

```text
Windows/transport appear operational. Device reports head open.
```

Recommendation:

```text
Follow approved physical/check procedure before changing Windows state.
```

### Stale job

Evidence:

```text
Spooler=Running
Selected queue contains old failed job
Device otherwise ready
```

Recommended low-impact plan:

```text
Cancel selected job -> re-enumerate -> validate
```

### Possible hardware issue / field-scope boundary

Evidence:

```text
Windows queue healthy
Transport healthy
Device repeatedly reports fault
Allowed field checks completed
Fault persists
```

Recommendation:

```text
Prepare ServiceCase / escalate according to policy.
```

Do not fabricate a disassembly/parts-replacement instruction.

### Insufficient evidence

If device-native status cannot be collected, say so. Do not infer readiness or healthy hardware from Windows only.

## Local remediation impact levels

### Low

Narrow scope, e.g. cancel one selected job.

### Medium

Service-level effect with controlled recovery, e.g. restart Print Spooler.

### High

May affect multiple jobs/queues or configuration.

### Break glass

Broad/global reset. Explicit warning, stronger confirmation, policy may disable it entirely.

## RepairPlan

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

1. resolve canonical queue identity;
2. enumerate jobs;
3. revalidate job still belongs to queue;
4. snapshot target;
5. confirm if policy requires;
6. call supported job-control API;
7. re-enumerate;
8. report success only after post-condition is observed.

Do not delete all spool files for this.

## Controlled Spooler restart

Preflight captures current service state, relevant startup/policy evidence, visible queue/job snapshot and permission capability.

Execution uses bounded stop/start waits and only plan-declared intermediate actions.

Validation checks expected final service state, target queue/jobs and relevant events/errors.

Recovery attempts to restore the appropriate original/policy state. Partial recovery is reported honestly.

## Global spool reset

Never the default repair button. Before implementation require separate capability, broad-impact warning, visible affected scope, snapshot, explicit confirmation, safe path handling, service transaction logic and validation.

## Configuration backup/diff

Read-only early scope:

- query allowlisted safe keys;
- preserve source/units;
- normalize;
- export snapshot;
- compare current vs approved baseline/device;
- distinguish drift from confirmed fault.

Write-back/import requires separate design and policy.

## Diagnostic print

Useful for separating software/transport from print quality, but it is a write operation.

Require:

- target confirmation;
- policy permission;
- bounded known content;
- clear media/dimension assumptions;
- no arbitrary user ZPL in privileged workflows;
- validation where possible;
- technician print-quality observation stored separately.

## Escalation

If the problem lies outside local authorized scope, the correct action may be **no local repair**.

ThermalOps should help create a `ServiceCase` containing the evidence, actions already performed, technician observations and `ServiceDisposition`.

See `FIELD_SERVICE_AND_ESCALATION.md`.

## Preventive relationship

Preventive findings may recommend cleaning/inspection/monitoring/scheduling, but source-backed maintenance tasks live in `PREVENTIVE_MAINTENANCE.md`. Preventive mode must not silently call local remediation.

## Evidence-driven UI

A technician must be able to distinguish:

- observed fact;
- technician observation;
- inferred finding;
- preventive recommendation;
- local remediation option;
- escalation recommendation;
- action executed;
- verified outcome.
