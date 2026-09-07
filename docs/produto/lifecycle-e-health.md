# Lifecycle e Health

## Objetivo

Este documento define como o ThermalOps representa **uso, idade, condição atual, manutenção, histórico e estimativas de vida útil** sem misturar conceitos nem inventar precisão que a evidence não suporta.

`Health`, `AssetAge`, `UsageMetrics`, `ComponentCondition`, `MaintenanceCompliance`, `ConditionTrend` e `RemainingLifeEstimate` são conceitos diferentes. Uma impressora antiga pode estar saudável; uma impressora nova pode estar crítica. Muito uso não significa automaticamente falha iminente, e ausência de um contador não significa zero uso.

O objetivo inicial é oferecer **Lifecycle Indicators defensáveis**. `Remaining Useful Life` (RUL) é uma capability futura e só pode existir quando houver source/model/dataset e validation apropriados.

## Princípios não negociáveis

```text
Unknown != Zero
Unknown != Healthy
Age != Health
Usage != Wear proof
Warning != Failure prediction
Configuration drift != Hardware fault
Health Score != Remaining life
LLM output != RUL
```

Toda informação precisa preservar source, timestamp, applicability, units, collection outcome e, quando derivada, rule/model version.

## Modelo conceitual

```text
PrinterSnapshot
   |
   +-- CurrentDeviceState
   +-- UsageMetrics
   +-- ManufacturerWarnings
   +-- ComponentEvidence
   +-- MaintenanceCompliance
   +-- ConfigurationState
   +-- Transport/Windows evidence
   +-- TechnicianObservation
             |
             v
      HealthAssessment
             |
             +--> ConditionTrend (quando history existir)
             +--> MaintenanceRecommendation
             +--> ServiceDisposition

RemainingLifeEstimate
   somente quando uma capability validada existir
```

## Current Health

`CurrentHealth` responde: **qual é a condição observável agora?**

A apresentação principal é component-based:

```text
Overall condition: ATTENTION RECOMMENDED

Device.................. OK
Printhead............... OK
Windows................. OK
Transport............... Observation
Configuration........... Drift
Maintenance............. DueSoon
Evidence completeness... 88%
```

O usuário deve poder abrir cada componente e chegar às evidence que produziram a avaliação.

## HealthAssessment

Suggested model:

```text
HealthAssessment
  assessmentId
  targetId
  observedAt
  overallState
  components[]
  evidenceCompleteness
  ruleSetId
  ruleSetVersion
  applicabilityClass
  unknownReasons[]
```

`overallState` pode usar uma taxonomia simples e não numérica:

```text
Good
GoodWithObservations
AttentionRecommended
Critical
InsufficientEvidence
NotApplicable
```

### Health components

Potential components:

```text
DeviceHealth
PrintheadHealth
ConsumablesHealth
MechanicalCondition
MaintenanceHealth
UsageContext
TransportHealth
WindowsPrintHealth
ConfigurationHealth
SecurityPosture
EvidenceCompleteness
```

Nem todo model expõe todos os componentes. Ausência de capability gera `Unsupported` ou `Unknown`, não score positivo fictício.

## Numeric Health Score

Um numeric score pode existir apenas como **secondary visualization**.

Requisitos:

- deterministic;
- versioned;
- contributions inspectable;
- no hidden ML/LLM weighting;
- missing evidence explicit;
- applicability class explícita;
- comparações somente entre populations compatíveis;
- weights cobertos por tests;
- score não é garantia, warranty nem prediction.

Exemplo:

```text
Health Score: 82 / 100

Device................. 100
Printhead................90
Maintenance..............70
Transport................85
Configuration............75
Evidence completeness....88
```

A UI precisa oferecer `Por que 82?` e mostrar cada `HealthContribution`.

## Asset Age

`AssetAge` é metadata de lifecycle, não health.

Potential evidence:

- manufacturing date quando oficialmente exposta;
- purchase/commissioning date fornecida por asset management;
- first-seen date do ThermalOps Enterprise;
- manually approved asset record.

Suggested representation:

```text
AssetAge
  source
  startDate?
  age?
  confidence/applicability
```

Se a data real de entrada em operação não existir, não inferir a idade a partir de firmware, driver ou first-seen sem deixar a semântica clara.

## UsageMetrics

Usage deve ser capability-driven.

Potential normalized metrics:

```text
TotalPrintLength
PrintLengthSinceService
LabelCount
LabelDotLength
HeadCleanCounter
LatchOpenCounter
UserResettableCounter1
UserResettableCounter2
OperatingHours
PowerOnHours
PrintCycles
CutterCycles
```

Esses nomes são Domain candidates; um Adapter só popula métricas que o dispositivo realmente expõe e que foram validadas.

### Zebra Link-OS

A documentação oficial do Link-OS `PrinterUtil.GetOdometerStatus` informa que printers compatíveis podem fornecer total print length, head clean counter, label dot length, head new, latch open counter e user-resettable counters.

Isso justifica `UsageMetrics`, mas **não** justifica afirmar que todas as Zebra fornecem `OperatingHours` ou `PowerOnHours`. Esses fields permanecem capability-dependent.

Representação correta:

```text
OperatingHours
  collectionOutcome = Unsupported
```

ou:

```text
OperatingHours
  collectionOutcome = Unknown
  reason = AdapterCouldNotDetermineCapability
```

Nunca:

```text
OperatingHours = 0
```

quando o dado não existe.

## Units e normalization

Usage precisa preservar units originais e normalized units quando converter.

Exemplo:

```text
rawValue = 12500000
rawUnit = dots
normalizedValue = 15.87
normalizedUnit = km
conversionContext = 203dpi
```

Conversão depende de DPI/semântica corretos. Não converter sem contexto suficiente.

## ComponentCondition

`ComponentCondition` agrega evidence referente a uma peça/subsystem, sem prometer lifetime remaining.

Candidate model:

```text
ComponentCondition
  componentType
  observedState
  automaticEvidenceIds[]
  technicianObservationIds[]
  manufacturerWarningIds[]
  usageMetrics[]
  maintenanceDueRefs[]
  assessmentRuleVersion
  limitations[]
```

Potential component types:

```text
Printhead
PlatenRoller
Cutter
MediaSensors
RibbonSensors
PowerSubsystem
ConnectivityModule
Other
```

### Printhead

A cabeça de impressão pode ter evidence mais rica, dependendo do modelo:

- head open/closed;
- head thermal warning;
- manufacturer maintenance/replacement warning;
- usage/odometer counters;
- print-quality TechnicianObservation;
- diagnostic/self-test result;
- maintenance cleaning due.

Isso permite `PrintheadHealth`, mas não uma porcentagem de vida restante sem modelo validado.

### Platen roller, sensors e cutter

Muitos componentes não possuem electronic wear sensor universal. Nesses casos a condição pode depender de:

```text
manufacturer schedule
+ usage evidence
+ TechnicianObservation
+ service history
```

A UI deve mostrar claramente quando o estado é manual, estimado por rule, ou não observável eletronicamente.

## ManufacturerWarnings

Warnings do firmware/device têm alto valor de evidence, mas devem manter significado original e applicability.

Exemplos possíveis:

```text
HeadTooHot
HeadOpen
PaperOut
RibbonOut
Paused
ReceiveBufferFull
HeadMaintenanceNeeded
ReplacePrinthead
```

A taxonomia precisa ser confirmada por Adapter/model/firmware. Um warning não deve ser generalizado para todos os vendors.

## MaintenanceCompliance

Responde se tarefas aplicáveis estão em dia segundo a `MaintenancePolicy` e o `MaintenanceTaskCatalog`.

```text
MaintenanceCompliance
  applicableTasks
  completedTasks
  dueSoonTasks
  dueTasks
  overdueTasks
  blockedTasks
  unknownTasks
```

`MaintenanceCompliance` influencia health, mas não substitui device state.

Uma printer pode estar `Ready` e ter maintenance overdue.

## Current Health versus Lifecycle

Exemplo:

```text
Printer A
Age................... 8 years
Usage................ High
Current Health........ Good
Maintenance........... Current

Printer B
Age................... 1 year
Usage................ Low
Current Health........ Critical
Maintenance........... Current
```

Age e usage servem para contexto/planning, não como shortcut de health.

## History e ConditionTrend

Enterprise pode persistir snapshots versionados e produzir trends.

Potential trends:

```text
PrintLengthTrend
HeadCleanCounterTrend
ThermalWarningTrend
CommunicationFailureTrend
MaintenanceComplianceTrend
ServiceCaseRecurrenceTrend
ConfigurationDriftTrend
```

Exemplo:

```text
Observed:
Communication timeouts/week = 1, 2, 5, 11

Derived:
Increasing trend

Recommendation:
Inspect transport/network path

Not claimed:
Hardware failure confirmed
```

## Peer comparison

Comparar usage/health entre devices pode ajudar maintenance by exception, mas exige compatible peer group.

Possible dimensions:

- vendor/model/family;
- DPI;
- firmware range;
- connection type;
- site/application;
- media/ribbon context;
- maintenance policy;
- operating environment.

`+42% above peer usage` é evidence de workload, não diagnosis de falha.

## RemainingLifeEstimate / RUL

`RemainingLifeEstimate` fica unavailable por default.

Suggested status:

```text
Unavailable
NotSupported
NotValidated
Experimental
ValidatedForApplicabilityClass
```

Antes de produzir RUL exigir:

- prediction target definido;
- component/failure semantics definidos;
- representative historical data;
- ground truth;
- censoring/maintenance replacement treatment;
- train/validation/test separation temporal;
- calibration;
- false-positive/false-negative cost analysis;
- applicability matrix;
- drift monitoring;
- benchmark contra deterministic maintenance rules;
- human/policy review;
- rollback/disable mechanism.

Nunca gerar RUL a partir de idade + usage com fórmula arbitrária.

## Self-Service presentation

O ExperienceProfile `SelfService` pode mostrar health de forma simples:

```text
Estado geral
Bom, com uma observação

Impressora............ OK
Comunicação............ OK
Fila de impressão...... OK
Manutenção............. Atenção
```

Detalhes como raw counters, rule versions e low-level warnings podem permanecer escondidos por progressive disclosure/policy.

O mesmo `HealthAssessment` alimenta Technician/AdvancedSupport; não existem dois motores de health.

## Technician presentation

Technician pode visualizar:

- current state;
- usage metrics;
- source/capability;
- component condition;
- maintenance due;
- previous inspection;
- configuration drift;
- manufacturer warnings;
- limitations/unsupported metrics.

## Enterprise presentation

Enterprise pode adicionar:

- history charts;
- maintenance by exception;
- peer comparison;
- due scheduling;
- service-case recurrence;
- condition trends;
- asset lifecycle metadata.

Aggregate sempre deve permitir drill-down até evidence.

## Reporting

Preventive Report e ServiceCase podem incluir, conforme privacy policy:

```text
LifecycleSummary
CurrentHealth
UsageMetrics
ComponentCondition
ManufacturerWarnings
MaintenanceCompliance
ConditionTrend
EvidenceCompleteness
RulStatus
```

`RulStatus=NotValidated` deve ser permitido e preferível a omitir silenciosamente a limitation.

## Privacy

Usage/counters e serial/asset metadata podem revelar intensidade operacional. Enterprise retention e exports devem respeitar data classification e purpose limitation.

Não coletar document/label contents para calcular usage quando printer counters são suficientes.

## Domain candidates

```text
AssetAge
UsageMetric
UsageMetricType
UsageUnit
ComponentCondition
ComponentType
ManufacturerWarning
HealthAssessment
HealthComponent
HealthContribution
EvidenceCompleteness
MaintenanceCompliance
ConditionTrend
RemainingLifeEstimate
RemainingLifeStatus
ApplicabilityClass
```

Names finais devem ser refinados quando M1-M4 implementarem os primitives necessários.

## Validation

Antes de afirmar suporte a uma metric/capability:

- official source/protocol review;
- parser/units tests;
- unsupported/unknown behavior;
- real hardware validation quando vendor-native;
- firmware/model matrix;
- regression fixture;
- documentation of limitations.

## Relação com outros documentos

- [Preventive Maintenance](manutencao-preventiva.md) define tasks, due e inspection.
- [Fleet e Condition Monitoring](fleet-e-condition-monitoring.md) define history/trends.
- [Self-Service](self-service.md) define o que end users podem visualizar/acionar.
- [Arquitetura](../engenharia/arquitetura.md) define boundaries.
- [Validation Matrix](../engenharia/validation-matrix-lifecycle-guidance-self-service.md) define testes específicos.
- [ADR-0008](../adr/0008-lifecycle-health-and-rul-semantics.md) registra as decisões semânticas.
