# Field Service, Triage e Escalation

ThermalOps é desenhado para technicians/support analysts que podem diagnosticar, realizar Preventive Inspection, coletar evidence, executar remediation local limitada e autorizada e escalar o equipamento quando o problema ultrapassa field scope.

O produto **não presume** que todo operador pode abrir impressora, trocar hardware interno, flash firmware ou executar bench repair.

## Pergunta central

ThermalOps deve ajudar a responder:

> Qual é o estado desta impressora, o que pode ser tratado aqui com segurança e dentro da policy, e o que deve ser escalado?

Esse modelo continua válido mesmo quando o processo real varia por organização, contrato, site, vendor ou device family.

## Generic Field Workflow

```text
Start authorized session
  -> Identify device / queue / connection
  -> Preventive or corrective inspection
  -> Collect Windows + transport + vendor-native evidence
  -> Add TechnicianObservation
  -> Derive Findings
  -> Evaluate FieldServicePolicy / EscalationPolicy
  -> Local low-risk remediation if authorized
  -> Re-validate
  -> Determine ServiceDisposition
  -> Generate report / ServiceCase
```

Esse fluxo é generic model, não uma afirmação sobre processo interno de empresa específica.

## Work Categories

### Field-resolvable / Local Remediation

Examples possíveis, quando policy permitir:

- cancelar um selected blocked/stale job;
- controlled Print Spooler restart;
- corrigir explicitamente uma queue/software association aprovada;
- unpause queue/device por approved workflow;
- orientar media/ribbon checks;
- executar diagnostic label;
- re-run deterministic validation.

A capability list real é definida pelo build + policy.

### Requires Technical Assessment

Findings que podem justificar avaliação mais profunda:

- recurring print-quality degradation;
- repeated hardware-reported warning;
- possible sensor/mechanical issue;
- abnormal temperature condition;
- recurring transport failure com Windows saudável;
- configuration/firmware anomaly fora do field scope;
- physical symptom que software não consegue confirmar;
- issue que exige parts assessment.

ThermalOps descreve evidence e recommendation. Não inventa internal repair procedure.

### Vendor / Authorized-Service Escalation

Potential triggers:

- suspected internal hardware fault;
- device fails to initialize/respond após allowed checks;
- persistent device fault após permitted workflow;
- action requires disassembly;
- parts replacement fora da autorização local;
- warranty/service-contract process deve assumir;
- firmware/component procedure fora da authority do operador;
- safety risk;
- insufficient evidence com impacto alto.

Rules de escalation vêm de approved policy ou explicit operator decision. Não hard-code quem abre RMA, remove equipamento ou contata fabricante.

## FieldServicePolicy

`FieldServicePolicy` representa o que o operador/site/contrato está autorizado a fazer.

Conceptual fields:

```text
FieldServicePolicy
  policyId
  version
  allowedCapabilities[]
  forbiddenCapabilities[]
  dispositionAuthority[]
  escalationRules[]
  evidenceRequirements[]
  attachmentPolicy
  exportPolicy
  effectivePeriod
```

Policy pode restringir capability, mas não criar executable capability ausente do build.

## EscalationPolicy

`EscalationPolicy` traduz Findings + authority + context em allowed/recommended next steps.

Exemplo conceitual:

```text
Finding: PersistentDeviceFault
Field scope: no internal hardware service
Required evidence: device status + Windows state + technician checklist
Recommendation: EscalateToAuthorizedService
```

A rule deve preservar:

- rule ID/version;
- applicability;
- evidence prerequisites;
- recommended disposition;
- required operator confirmation;
- follow-up metadata;
- source quando derivada de procedimento aprovado.

## ServiceDisposition

Normaliza o outcome da sessão separadamente do device status.

Suggested values:

```text
ContinueInService
ContinueWithObservation
LocalRemediationAllowed
EscalateToAuthorizedService
RemoveFromService
InsufficientEvidence
```

`RemoveFromService` só existe se explicit policy conceder autoridade para essa recommendation.

Uma disposition registra:

- policy version;
- finding/evidence references;
- operator decision quando aplicável;
- timestamp;
- reason;
- follow-up/due date quando permitido;
- whether recommended automatically or manually selected;
- acknowledgement.

## Device status != ServiceDisposition

Exemplo:

```text
DeviceState: NotReady
Finding: PersistentHardwareReportedFault
ServiceDisposition: EscalateToAuthorizedService
```

São três camadas diferentes. Misturá-las prejudica auditability e pode gerar actions incorretas.

## TechnicianObservation

Manual observations são first-class evidence, mas claramente marcadas como human-entered.

Exemplo:

```text
Automatic evidence
- DeviceReady=false
- WindowsQueueState=Healthy
- TransportState=Reachable

TechnicianObservation
- visible damage: none
- abnormal noise: yes
- diagnostic print: missing vertical lines
```

Cada observation deve preservar:

- observation type;
- operator/session attribution;
- timestamp;
- value/result;
- optional note;
- optional attachment reference;
- privacy classification.

Nunca apresentar manual observation como sensor measurement.

## ServiceCase

`ServiceCase` empacota a sessão para N2/N3, authorized repair center ou vendor support workflow.

Suggested data model:

```text
ServiceCase
  caseId
  sessionId
  targetDevice
  caseType
  problemSummary
  evidenceIds[]
  findings[]
  technicianObservations[]
  actionsAttempted[]
  actionResults[]
  preventiveInspectionRef?
  disposition
  policyVersion
  attachments[]
  privacyLevel
  createdAt
  schemaVersion
```

## Case Types

Possible normalized case types:

```text
CorrectiveIncident
PreventiveFinding
RecurringIssue
ConfigurationDrift
PhysicalAssessmentRequired
VendorSupportRequest
PostRepairValidation
Unknown
```

Case type não substitui Findings.

## Escalation Package

Future export:

```text
ThermalOps-ServiceCase-<id>.zip
├── summary.json
├── device.json
├── windows-print.json
├── printer-status.json
├── configuration.json
├── counters.json
├── events.json
├── network.json
├── preventive-inspection.json
├── diagnostic-label-result.json
├── timeline.json
├── action-history.json
├── attachments/
└── manifest.json
```

Nem todo arquivo é obrigatório. O manifest registra:

```text
collected
skipped
blocked
unsupported
redacted
failed
```

## Handoff N1 -> N2/N3

Um handoff útil deve evitar retrabalho.

Ao invés de:

```text
“Impressora não funciona.”
```

O recipient recebe:

```text
Target identity
Symptoms
Windows state
Transport state
Vendor-native state
Technician observations
Findings
Actions attempted
Verified outcomes
Disposition
Missing evidence
```

Isso melhora continuity e reduz troubleshooting repetido.

## Vendor-Support Compatibility

Public vendor support flows podem separar technical support de repair request/RMA. ThermalOps deve preparar dados úteis, mas não deve assumir integração direta.

Initial direction:

```text
ThermalOps
  -> generate structured ServiceCase
  -> operator follows approved support/repair process
```

Future direct integration:

```text
ThermalOps
  -> approved connector
  -> official vendor/service API/workflow
```

Somente implementar direct submission quando houver:

- official supported interface;
- authentication design;
- authorization model;
- privacy review;
- error/retry/idempotency model;
- contract/licensing review;
- audit requirements.

## Warranty / Entitlement / RMA

ThermalOps não adivinha:

- warranty status;
- service entitlement;
- RMA requirement;
- repair center routing;
- SLA.

Esses dados precisam vir de trusted source ou operator input validado.

## Photos e Attachments

Future ServiceCase pode incluir manually selected photos/files.

Guardrails:

- nunca auto-capture screen/camera;
- explicit operator selection;
- privacy preview;
- file/type/size validation;
- treat as untrusted content;
- no execution;
- safe archive/path handling;
- optional metadata stripping;
- sanitized export excludes attachment by default;
- hash attachment no manifest quando incluído.

## Field Workflow UX

Home screen pode oferecer:

```text
[ Quick Diagnosis ]
[ Preventive Inspection ]
[ Analyze Failure ]
[ Collect Evidence ]
[ Prepare Escalation ]
[ Technical Report ]
```

Destructive/local-remediation actions são contextual/secondary.

Não colocar um giant “Repair Everything” button.

## Example Session

```text
09:14 SessionStarted
09:15 TargetSelected
09:16 Spooler=Running
09:16 QueueJobs=0
09:17 Transport=Reachable
09:18 DeviceResponding=true
09:18 DeviceReady=false
09:18 DeviceWarning=...
09:21 TechnicianObservation=abnormal noise
09:22 Finding=PersistentDeviceFault
09:22 LocalRemediationAllowed=false
09:23 ServiceDisposition=EscalateToAuthorizedService
09:24 ServiceCaseExported=sanitized
```

A timeline demonstra o que foi observado, inferido e decidido.

## Unknown Real-World Process

O repository não codifica workflow interno não verificado, incluindo:

- qual support level pode trocar qual componente;
- quem leva equipamento;
- quem abre chamado interno;
- quando RMA é obrigatório;
- quem chama Zebra/other OEM;
- customer-specific forms;
- contract SLA;
- entitlement rules;
- proprietary configuration templates.

Quando regras reais forem conhecidas e legítimas, mapear para abstractions genéricas:

```text
FieldServicePolicy
EscalationPolicy
ServiceDispositionRule
MaintenancePolicy
ReportTemplate
```

Confidential policy permanece fora do public core.

## Testing

Field-service implementation exige testes para:

- policy allows/denies action;
- ServiceDisposition authority;
- missing evidence;
- manual vs automatic attribution;
- escalation recommendation;
- ServiceCase redaction;
- attachment safety;
- schema compatibility;
- offline Portable export;
- no repair required before escalation;
- conflicting operator/policy decisions.
