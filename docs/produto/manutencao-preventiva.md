# Preventive Maintenance

Preventive Maintenance é uma capability de primeira classe no ThermalOps. O objetivo não é esperar a impressora falhar para então tentar descobrir o motivo, mas coletar evidence, orientar uma inspeção autorizada, detectar drift ou sinais recorrentes e produzir uma recommendation defensável antes de uma parada evitável.

ThermalOps não deve fingir que software enxerga toda condição física. Também não deve inventar maintenance intervals, component lifetime ou replacement thresholds.

## Posição no produto

```text
                         THERMALOPS
                              |
      +-----------------------+-----------------------+
      |                       |                       |
      v                       v                       v
  DIAGNOSIS             PREVENTIVE              LOCAL REMEDIATION
                        MAINTENANCE
      |                       |                       |
      +-----------------------+-----------------------+
                              |
                              v
                     SUPPORT / EVIDENCE
                              |
                  +-----------+-----------+
                  v                       v
              PORTABLE                ENTERPRISE
```

Cada disciplina responde a uma pergunta diferente:

- **Diagnosis:** o que está acontecendo agora?
- **Preventive Maintenance:** o que deve ser inspecionado, limpo, comparado, monitorado ou agendado antes de virar falha?
- **Local Remediation:** qual ação estreita e autorizada pode ser executada agora com segurança?

Predictive Maintenance é um nível posterior de maturidade e não pode ser anunciado apenas porque existe histórico.

## Preventive Inspection workflow

Fluxo normal, observation-first e read-only-first:

```text
Identify target
  -> Collect automatic evidence
  -> Load applicable MaintenancePolicy / MaintenanceBaseline
  -> Guide Technician Inspection
  -> Compare current state vs baseline/history
  -> Derive MaintenanceFinding
  -> Determine ServiceDisposition
  -> Generate Preventive Report
  -> Optional authorized follow-up action
```

Portable Lite deve continuar útil para esse workflow sem Administrator rights.

## Automatic evidence

Quando suportado e autorizado, uma Preventive Inspection pode coletar:

### Windows

- Print Spooler state;
- configuração relevante do serviço;
- selected print queue state;
- jobs e repeated/stale-job evidence;
- driver identity/version/package;
- port/transport evidence;
- PnP/USB evidence;
- relevant Event Log entries;
- access denied, timeout e unavailable-data outcomes.

### Transport

- USB/PnP presence quando aplicável;
- configured endpoint;
- narrowly scoped TCP reachability quando permitido;
- timeout/repeated connection failure;
- protocol/channel evidence;
- TLS/certificate evidence somente quando suportado e desenhado explicitamente.

### Vendor-native

Capabilities variam por model, firmware, print language, connection type e vendor. O Adapter deve perguntar o que o dispositivo suporta em vez de presumir um universal feature set.

Possible Zebra evidence:

- communication result;
- ready-to-print state;
- printhead open/closed;
- media state;
- ribbon state quando aplicável;
- pause state;
- printhead thermal warnings;
- receive-buffer/state conditions;
- firmware/Link-OS information;
- counters/odometer quando suportado;
- selected safe read-only settings;
- device-reported errors/warnings.

Windows queue state e physical-printer state permanecem evidence sources separadas.

## Technician-verified inspection

Software não consegue determinar com confiabilidade:

- visual wear;
- cleanliness;
- physical damage;
- abnormal noise;
- cable condition;
- todas as condições do media path;
- aparência real da impressão.

Esses itens entram como `TechnicianObservation`, nunca como automatic sensor evidence.

Exemplo de checklist genérico:

```text
Physical inspection
[ ] External condition inspected
[ ] Power/data connections inspected
[ ] Media path inspected/cleaned as applicable
[ ] Sensors inspected/cleaned as applicable
[ ] Printhead condition/cleanliness inspected
[ ] Platen roller inspected
[ ] Ribbon/media installation checked
[ ] Unusual mechanical noise checked
[ ] Diagnostic label inspected, if allowed
[ ] Visible damage recorded
```

Isso **não** é autorização para desmontar equipamento.

Cada task deve carregar:

- task ID;
- version;
- applicable vendor/device family/model/capability;
- source/reference;
- source version/date quando conhecida;
- safety notes;
- whether automatic or technician-verified;
- whether power-off is required;
- required policy/capability;
- result semantics;
- optional sanitized note/evidence reference.

Suggested task results:

```text
Pass
Observation
Fail
NotPerformed
NotApplicable
Blocked
```

## Source-backed maintenance schedules

ThermalOps nunca deve inventar uma regra como:

```text
“Troque o componente X depois de N labels.”
```

Maintenance timing só pode vir de source aprovado, por exemplo:

- manufacturer documentation para model/family correto;
- organization-approved MaintenancePolicy;
- service-contract policy;
- approved site/application procedure;
- validated usage threshold.

Cada schedule rule preserva source/version/applicability.

Potential triggers:

```text
CalendarInterval
UsageCounterThreshold
ConditionEventThreshold
ConfigurationDrift
ManualInspectionResult
ServiceCaseFollowUp
```

Suggested `MaintenanceDue` states:

```text
Unknown
NotApplicable
NotDue
DueSoon
Due
Overdue
Blocked
```

Missing input nunca vira silenciosamente `NotDue`.

## Zebra como exemplo de schedule específico

A documentação pública da Zebra para ZT411/ZT421 possui seção de routine maintenance e cleaning schedules por parte/uso. Ela trata printhead, platen, media/ribbon sensors, paths, cutter options e outros componentes de forma específica.

A lição para o produto não é copiar um único schedule para toda impressora Zebra. A lição é usar um catálogo versionado e aplicável:

```text
MaintenanceTaskCatalog
  -> vendor/family/model applicability
  -> source/version
  -> trigger/interval
  -> safety notes
  -> task definition
```

Manufacturer procedures também podem possuir restrições de técnica e segurança. ThermalOps deve referenciar a instrução correta em vez de resumir um procedimento potencialmente arriscado em uma frase genérica.

## MaintenanceTaskCatalog

O catálogo futuro pode ser estruturado por packages/version sets.

Conceitualmente:

```text
MaintenanceTaskDefinition
  taskId
  schemaVersion
  titleResourceKey
  vendor
  modelFamilies[]
  capabilityRequirements[]
  contextRules[]
  sourceReference
  sourceVersion
  trigger
  safetyNotes[]
  expectedResultType
```

O Domain não deve depender de texto localizado da task para aplicar a regra.

## MaintenanceBaseline

Baseline representa expected/approved reference state. Uma diferença não significa automaticamente defeito.

Possible baseline sources:

- explicitly approved config profile;
- known-good compatible device;
- previous approved inspection snapshot;
- organization policy;
- vendor-recommended profile.

Applicability pode considerar:

- vendor/model/family;
- DPI;
- print mode/application;
- media/ribbon context;
- connection type;
- firmware range;
- site/policy profile;
- baseline schema version.

Não comparar device variants incompatíveis como se toda configuração devesse ser idêntica.

## Configuration Drift

Exemplo:

```text
Approved baseline
Darkness: 15
Speed: 6

Current device
Darkness: 28
Speed: 12

Result
Configuration drift detected.
This does not by itself prove a hardware fault.
```

A UI deve apresentar:

- baseline value;
- current value;
- difference;
- evidence source;
- policy severity;
- acknowledgement state;
- recommended verification;
- applicability context.

## Portable baseline workflow

Portable permanece non-persistent por default.

Operator pode explicitamente importar/exportar:

```text
ThermalOps-Baseline-v1.json
ThermalOps-InspectionSnapshot-v1.json
```

Imported data exige:

- schema validation;
- size bounds;
- compatibility/applicability validation;
- safe parsing;
- no code/script execution;
- trust/signature handling quando implementado.

Mesmo um signed policy package não pode habilitar code capability ausente do executable.

## HealthAssessment

HealthAssessment é um resumo explicável sobre evidence; não um magic number.

Preferred primary presentation:

```text
Overall condition: ATTENTION RECOMMENDED

Device.................. OK
Windows................. OK
Transport............... Observation
Configuration........... Drift detected
Maintenance............. DueSoon
Evidence completeness... 91%
```

### Numeric Health Score

Pode existir como secondary view, se houver justificativa.

Exemplo:

```text
Health Score: 82/100

-5 repeated transport failures
-5 configuration drift
-4 thermal warnings
-4 maintenance task due
```

Regras:

- deterministic;
- versioned;
- weights/contributions visíveis;
- missing evidence não vira zero penalty automaticamente;
- compatibility class clara;
- não comparar contexts incompatíveis sem normalização definida;
- never generated as authority by LLM;
- não é warranty nem failure prediction;
- user consegue abrir o “Why?”.

## MaintenanceFinding

Examples:

- cleaning due according to approved schedule;
- configuration drift;
- repeated communication instability;
- recurring thermal warning;
- preventive checklist incomplete;
- usage counter threshold reached;
- diagnostic-label quality observation;
- firmware outside approved baseline;
- maintenance history missing/unknown;
- source data unavailable.

Finding deve referenciar evidence/rules que a produziram.

## MaintenanceRecommendation

Possible normalized recommendations:

```text
Inspect
CleanAccordingToApprovedProcedure
Monitor
ScheduleFollowUp
EscalateForAuthorizedAssessment
NoPreventiveActionRequired
InsufficientEvidence
```

Recommendation não executa automaticamente action.

## ServiceDisposition

Uma Preventive Inspection pode resultar em policy-controlled `ServiceDisposition`:

```text
ContinueInService
ContinueWithObservation
LocalRemediationAllowed
EscalateToAuthorizedService
RemoveFromService
InsufficientEvidence
```

`RemoveFromService` só é available se policy explícita conceder essa authority.

Disposition é conclusion/decision layer, nunca raw status.

## Preventive Report

O relatório deve separar automatic evidence de TechnicianObservation.

Suggested structure:

```text
PREVENTIVE MAINTENANCE REPORT

Target / session
Policy version
Maintenance catalog version
Baseline version

Automatic checks
- Windows
- Transport
- Device-native
- Firmware/counters
- Configuration

Technician Inspection
- checklist/results

MaintenanceDue
- due/soon/overdue/unknown

Findings
Recommendations
Local actions, if any
ServiceDisposition
Next inspection, only if source-backed
```

## Diagnostic print quality check

Uma policy-permitted diagnostic label pode ajudar a separar software/transport de print-quality issue.

Pode incluir:

- session ID;
- model/DPI;
- barcode/QR;
- line-width samples;
- alignment markers;
- darkness/calibration patterns.

É write operation, portanto disabled em `--readonly` e Customer Safe.

Technician observations como:

```text
Good
Light
Dark
MissingLines
AlignmentProblem
BarcodeUnreadable
```

são manual evidence.

## Maintenance History

Enterprise pode reter, por policy:

- inspections;
- tasks performed;
- findings;
- acknowledgements;
- approved config changes;
- ServiceDisposition;
- ServiceCases;
- counters over time;
- recurring warnings/errors;
- due calculation inputs;
- policy/catalog/baseline versions.

Portable não cria hidden local history no customer endpoint.

## Condition-based Maintenance

É a etapa seguinte depois de deterministic Preventive Maintenance.

Examples:

- communication errors crescendo;
- repeated temperature warnings;
- stalled-job recurrence;
- persistent configuration drift;
- repeated ServiceCases;
- usage counter approaching approved threshold.

Uma trend não é proven cause.

UI deve separar:

```text
Observed trend
Derived interpretation
Recommendation
What is NOT claimed
```

## Predictive Maintenance

Predictive Maintenance fica deferred até existir dado histórico representativo e validation strategy.

Não publicar claims como:

```text
“Printhead will fail in 3 days.”
```

apenas porque um model consegue gerar uma probabilidade.

Antes de qualquer predictive claim, exigir:

- defined prediction target;
- ground truth;
- representative historical dataset;
- train/validation/test separation;
- false-positive/false-negative cost analysis;
- calibration;
- confidence analysis;
- drift monitoring;
- model/device applicability matrix;
- human/policy review;
- benchmark contra deterministic baseline;
- rollback/disable strategy se performance degradar.

## Domain concepts

Planned concepts:

```text
MaintenanceInspection
MaintenanceTaskDefinition
MaintenanceTaskResult
MaintenanceFinding
MaintenanceRecommendation
MaintenancePolicy
MaintenanceBaseline
MaintenanceRecord
MaintenanceSchedule
MaintenanceDue
HealthAssessment
HealthContribution
ConditionTrend
TechnicianObservation
ServiceDisposition
```

Esses concepts pertencem ao Domain/Application, não à WPF UI ou Vendor Adapter.

## Safety boundaries

Preventive mode não deve:

- automatically change firmware;
- automatically install/remove driver;
- automatically alter printer config;
- assumir hardware-disassembly authority;
- invent manufacturer interval;
- upload customer data automaticamente;
- ampliar network discovery sem permission;
- usar AI como maintenance authority.

Default sequence:

```text
Observe -> Analyze -> Compare -> Recommend
```

Nunca:

```text
Observe -> Automatically change everything
```

## Testing implications

A implementação deve cobrir:

- task applies / not applies / unknown;
- due boundary conditions;
- missing source inputs;
- baseline compatibility;
- drift acknowledgement;
- technician checklist incomplete;
- automatic vs manual evidence attribution;
- HealthAssessment explainability;
- report localization sem alterar machine schema;
- read-only/no-persistence E2E;
- hardware validation para vendor-native claims.
