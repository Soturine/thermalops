# Diagnóstico e Local Remediation

## Princípio

ThermalOps coleta evidence de camadas independentes, deriva Findings, recomenda o next step de menor impacto e separa explicitamente:

- Diagnosis;
- Preventive Maintenance;
- Local Remediation;
- Escalation.

```text
Windows APIs + Vendor APIs + TechnicianObservation + Approved Policy
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
      Recommendation     Remediation      Recommendation
                         / RepairPlan
```

O operador não é presumido como bench-repair technician.

## Evidence Layers

### Windows Print Subsystem

Coletar quando available/authorized:

- Print Spooler state;
- relevant service configuration;
- installed printers;
- selected queue details;
- jobs e job state flags;
- driver identity/version/package;
- port/monitor evidence;
- print processor evidence em Advanced Diagnostics;
- relevant Event Log entries;
- access denied/timeouts/errors como first-class evidence.

Preferir WinSpool, SCM e Event Log APIs em vez de command-output parsing.

### PnP / USB

Potential evidence:

- PnP presence;
- hardware/instance identity quando permitido;
- connect/disconnect evidence;
- queue/port/device correlation quando determinável.

Nunca inferir USB physical presence apenas porque friendly name/port contém `USB`.

### Network / Transport

Default: known endpoint ou explicitly authorized scope.

Potential checks:

- endpoint resolution;
- TCP reachability ao configured printer service;
- timeout/refused/unreachable outcome;
- TLS capability/certificate evidence quando suportado;
- protocol-level response quando vendor adapter permitir.

ICMP ping não equivale a printer health.

### Vendor-native Printer

Zebra first.

Normalize supported evidence como:

- communication result;
- ready-to-print;
- head state;
- media/ribbon state;
- pause state;
- thermal warning;
- buffer/state conditions;
- firmware;
- counters/odometer;
- selected safe read-only configuration;
- device-reported errors/warnings.

Vendor-native state e Windows queue state ficam separados.

### TechnicianObservation

Manual evidence pode incluir:

- visual condition;
- cable condition;
- abnormal noise;
- print quality;
- checklist results;
- visible damage;
- consumable installation observation.

Deve carregar human/session attribution e nunca aparecer como automatically measured.

## Status Normalization

Não usar:

```text
status == 0 => ONLINE/HEALTHY
```

Windows printer status pode representar bit flags/multiple conditions. Vendor status também pode conter múltiplos fields.

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

Cada component preserva source.

## Evidence Completeness

É importante distinguir:

```text
No issue observed
```

de:

```text
Could not collect enough evidence
```

`EvidenceCompleteness` pode indicar o quanto do expected inspection set foi coletado, mas não deve ser usado como health score.

## Finding Model

Uma Finding precisa de:

- finding type;
- severity;
- certainty/qualification;
- evidence IDs;
- rule version;
- explanation resource key;
- recommended next step;
- missing evidence quando relevante.

Example:

```text
FindingType: DeviceReportsHeadOpen
Severity: Warning
Evidence: ZebraNative.HeadState=Open
Windows: Spooler=Running
Recommendation: FollowApprovedDeviceCheck
```

## Quick Diagnosis

Quick Diagnosis deve ser low-friction e read-only.

Flow:

```text
Select/resolve target
 -> collect minimum useful evidence set
 -> normalize
 -> evaluate deterministic rules
 -> show Findings
 -> show Why?
 -> recommend least-impact next step
```

### Example: Device Condition Before Windows Repair

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
Follow approved physical check before changing Windows state.
```

### Example: Stale Job

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

### Example: Possible Hardware Issue / Field Boundary

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

Não inventar disassembly/parts instruction.

### Example: Insufficient Evidence

Se native status não puder ser coletado:

```text
WindowsQueueState=Healthy
DeviceState=Unknown
```

Não concluir `DeviceHealthy=true`.

## Advanced Diagnostics

Advanced mode expõe detalhes que ajudam N2/N3:

- raw Windows flags;
- queue/job detail;
- driver/package detail;
- port/monitor;
- print processors;
- PnP correlation;
- Event Log;
- network outcomes;
- vendor-native raw/normalized fields;
- firmware;
- counters;
- config snapshot;
- timeline;
- collection failures.

Raw data deve ser sanitized quando necessário e tratada como untrusted display content.

## Local Remediation Impact Levels

### Low

Narrow scope, limitado e normalmente reversível.

Example:

- cancel one selected job.

### Medium

Service-level impact com recovery esperado.

Example:

- controlled Print Spooler restart.

### High

Pode afetar múltiplos jobs/queues/configuration.

Examples:

- selected queue repair com temporary shared-subsystem impact;
- config write futuramente aprovado.

### Break Glass

Broad/global action.

Example:

- global spool reset.

Break-glass deve ser distinct capability, normalmente disabled por default/policy.

## RepairPlan

Schema conceitual:

```text
RepairPlan
  id
  titleResourceKey
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
  confirmationResourceKey
```

## Preflight

Antes de write:

- re-resolve target identity;
- verify capability;
- verify policy;
- collect current state;
- detect conflicting changes;
- confirm required permissions;
- calculate impact scope;
- ensure recovery path prerequisites quando aplicável.

## Snapshot

Capture somente o que é necessário para:

- verification;
- recovery;
- audit;
- before/after.

Snapshot não significa dump indiscriminado de customer data.

## Cancel Selected Job

Preferred queue cleanup:

1. resolve canonical queue identity;
2. enumerate jobs;
3. revalidate selected job belongs to target queue;
4. capture target job snapshot;
5. present plan/impact;
6. explicit confirmation se policy exigir;
7. call supported job-control API;
8. re-enumerate queue;
9. report success somente se expected post-condition for observado.

Não usar deletion global de spool files para conseguir o mesmo efeito.

## Controlled Spooler Restart

### Preflight

Capturar:

- current service state;
- startup/config policy evidence relevante;
- visible queues/jobs snapshot;
- target fault context;
- elevation capability.

### Execute

- request stop;
- wait bounded timeout;
- se stop falhar, não continuar para unrelated deletion/reset;
- perform somente plan-declared steps;
- request start somente quando consistente com original/policy state;
- wait bounded timeout.

### Verify

- expected service state;
- target queue/job re-enumeration;
- relevant Event Log/error evidence;
- original issue state.

Se Spooler voltar mas problema original persistir:

```text
Repair outcome = Partial
```

### Recovery

Se intermediate step falhar:

- attempt safe restore;
- preserve/report current actual state;
- do not blindly loop;
- present exact residual risk.

## Global Spool Reset

Nunca default repair button.

Antes de implementar, exigir:

- separate break-glass capability;
- broad impact warning;
- visible affected scope;
- queues/jobs snapshot;
- explicit confirmation;
- internally derived safe paths;
- reparse-point/path safety analysis;
- transactional service-state handling;
- post-condition validation;
- audit event;
- dedicated destructive test environment.

## Queue Repair Strategies

Uma future `RepairSelectedQueue(queueId, strategyId)` não pode aceitar arbitrary scripts.

Cada `strategyId` deve apontar para implementation allowlisted/versioned com:

- applicability;
- impact;
- preconditions;
- actions;
- validation;
- recovery.

## Configuration Backup / Diff

Read-only early scope:

- query allowlisted safe keys;
- preserve source/units;
- normalize values;
- export snapshot;
- compare current vs baseline/device;
- mark incompatible comparison;
- distinguish drift from fault.

Write-back/import requires dedicated design/policy.

## Diagnostic Print

Useful para separar software/transport de print quality, mas é write.

Requirements:

- target confirmation;
- policy permission;
- known/bounded label content;
- media/dimension assumptions claras;
- no arbitrary user-supplied ZPL em privileged workflow;
- validation de job/target quando possível;
- TechnicianObservation da qualidade armazenada separadamente.

## Firmware / Driver Actions

Não fazem parte do early remediation scope.

Qualquer future firmware update/driver install exige:

- dedicated ADR;
- vendor-supported method;
- package authenticity;
- compatibility validation;
- power-loss/failure behavior;
- rollback/recovery quando possível;
- maintenance window impact;
- explicit policy;
- hardware validation.

## Escalation

A ação correta pode ser **não reparar localmente**.

Quando outside field scope:

```text
Collect evidence
 -> derive Finding
 -> assign ServiceDisposition
 -> prepare ServiceCase
 -> export under approved privacy level
```

Veja `../produto/field-service-e-escalation.md`.

## Preventive Relationship

Preventive Findings podem recomendar inspection/cleaning/monitoring/scheduling, mas não chamam local remediation silenciosamente.

Veja `../produto/manutencao-preventiva.md`.

## Evidence-driven UI

A UI precisa permitir distinguir:

- observed fact;
- TechnicianObservation;
- inferred Finding;
- Preventive Recommendation;
- Local Remediation option;
- Escalation Recommendation;
- action requested;
- action executed;
- verification outcome.

Toda Finding importante deve possuir `Why?`/evidence drill-down.

## Concurrency e State Change

O environment pode mudar entre diagnosis e action.

Exemplos:

- job some antes do cancel;
- device disconnects;
- service state changes externally;
- queue removed;
- policy file updated.

Por isso, actions revalidam target/preconditions no execution boundary.

## Timeouts e Retry

- external reads: bounded retry/backoff quando seguro;
- writes: não retry cegamente;
- helper request: explicit timeout;
- device query: bounded response size/time;
- UI: cancellation disponível quando seguro.

## Failure Injection Requirements

Testar:

- Spooler already stopped;
- cannot stop;
- stops but cannot start;
- state changes externally;
- job disappears;
- access denied;
- UAC denied;
- printer disconnects;
- malformed vendor response;
- network timeout;
- helper crash;
- cleanup fails;
- verification differs from expected.

## Definition of Validated

Diagnosis rule não é validated somente porque unit test passou.

Examples:

- Windows evidence -> Windows integration test;
- privileged action -> negative/security tests;
- Zebra native claim -> real compatible hardware;
- Portable behavior -> no-persistence E2E;
- config write/firmware -> dedicated milestone validation.
