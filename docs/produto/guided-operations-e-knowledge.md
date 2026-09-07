# Guided Operations e Knowledge

## Objetivo

Guided Operations é a camada que transforma evidence e documentação aprovada em **passos verificáveis, model-aware e policy-aware**. O objetivo é ajudar técnico e usuário final a chegar da pergunta “o que está acontecendo?” até uma próxima ação segura, sem reduzir o ThermalOps a um PDF viewer e sem entregar autoridade operacional a AI.

Ela atravessa Diagnosis, Preventive Maintenance, Self-Service, Commissioning, Local Remediation, Security Assessment e Return-to-Service.

## Problema que resolve

Um manual tradicional pode dizer:

```text
Faça A
Depois B
Depois C
```

O ThermalOps pode fazer:

```text
Collect evidence
  -> skip steps already proven
  -> show only applicable step
  -> explain why
  -> execute/read/guide according to ActionSafetyClass
  -> verify outcome
  -> branch to next step
  -> preserve timeline
```

A guidance session nunca substitui the Domain evidence model. Ela é um workflow sobre facts, capabilities, approved sources e policy.

## Princípios

- source-backed;
- capability-aware;
- model/firmware/context-aware;
- read-only-first;
- policy-gated;
- progressive disclosure;
- each automated conclusion references evidence;
- each write action uses the Local Remediation lifecycle;
- AI may interpret natural language and explain, but does not authorize actions;
- offline-first when an approved local knowledge pack exists;
- vendor documentation/licensing respected;
- no hard-coded employer/customer proprietary procedure in public core.

## Main capabilities

### Guided Troubleshooting

O usuário escolhe um symptom, ou descreve em natural language, e o ThermalOps resolve para canonical symptom candidates.

Exemplo:

```text
User input:
“imprime duas etiquetas e pula uma”

Candidate symptom:
LabelGapOrCalibrationIssue

Deterministic collection:
- Media state
- Label length/config
- Sensor/calibration evidence
- Queue/transport state
- Applicable runbooks
```

AI pode ajudar a mapear texto -> candidate symptom, mas o next step final vem de rules/runbook applicability e evidence.

### Model-aware Manuals

A `Knowledge Center` deve resolver documentação por:

```text
Vendor
Model / Family
Firmware range
Printer language
Connection type
Feature/capability
Topic
Locale
Source version
```

Nunca assumir que um procedimento de uma ZD411 se aplica automaticamente a ZT411 ou a todos os Link-OS printers.

### Commissioning / Setup

Future workflow para novo equipamento:

```text
Identify hardware
  -> resolve vendor/model/capabilities
  -> check Windows driver/queue/transport
  -> load approved baseline/policy
  -> guide media/ribbon setup
  -> configure only approved settings
  -> calibration if applicable
  -> diagnostic/configuration report
  -> validate
  -> create commissioning snapshot/report
```

Driver installation, network configuration e printer-setting writes são actions separadas e exigem policy/privilege design próprio.

### Return-to-Service

Após manutenção externa, replacement ou reset:

```text
Identify returned device
  -> compare identity/firmware/config with expected baseline
  -> validate Windows queue/driver/transport
  -> run approved self-tests/calibration
  -> compare print quality where allowed
  -> record differences
  -> create ReturnToServiceReport
```

Não restaurar configuration automaticamente só porque existe baseline. Drift primeiro gera evidence/finding; write-back precisa de explicit plan.

### Preventive Procedures

A guidance layer pode apresentar `MaintenanceTaskDefinition` passo a passo, mantendo:

- source/reference;
- model applicability;
- safety notes;
- required power state;
- expected result;
- TechnicianObservation requirements;
- post-check.

Ela não reescreve manufacturer instructions como uma universal recipe.

### Native Diagnostics / Self-Tests

Quando o Adapter e o model suportarem, o catálogo pode expor native diagnostic actions como:

```text
ConfigurationReport
NetworkConfigurationReport
PrintQualityReport
CommunicationDiagnosticsTest
SensorProfileReport
SmartCalMediaCalibration
ManualMediaCalibration
```

Cada action possui support matrix e safety class. Uma feature existir no manual de um model não significa que o SDK permita dispará-la programaticamente da mesma forma; implementation deve validar a interface oficial disponível.

### Security Assessment

Future Printer Security Assessment pode comparar settings observáveis com um `SecurityBaseline` aprovado.

Potential evidence:

- enabled services/protocols quando suportado;
- open TCP ports quando suportado;
- TLS/certificate state quando suportado;
- security-related settings;
- firmware/security policy context.

Resultado é `SecurityFinding`, não automatic reconfiguration.

## ActionSafetyClass

Toda operation apresentada por guidance deve cair em uma classe explícita.

### `Informational`

Sem state change.

Exemplos:

- abrir instrução;
- explicar evidence;
- mostrar diagram;
- comparar config;
- mostrar status.

### `GuidedManual`

Usuário executa uma ação física/manual; ThermalOps não modifica device/system.

Exemplos:

- verificar mídia;
- fechar printhead;
- inspecionar platen roller;
- seguir procedimento de cleaning aprovado.

O sistema pode recheck evidence após a ação.

### `AssistedWrite`

ThermalOps prepara e executa uma write action após preview/confirmation/policy.

Exemplos possíveis:

- media calibration;
- diagnostic print;
- selected configuration change;
- unpause queue.

Action entra no RepairPlan/typed action lifecycle quando muda state.

### `AutomatedLowRisk`

Somente future policy-approved deterministic actions com narrow impact e robust verification.

Exemplo potencial:

- cancel selected stale job em context seguro.

Default é disabled até explicit policy e validation.

### `HighImpact`

Exige stronger confirmation, explicit policy e dedicated design.

Examples:

- network reset;
- factory reset;
- firmware update;
- broad configuration restore.

Não pode ser disfarçado como “passo do assistente”.

### `ForbiddenInProfile`

Action implementada no product, mas indisponível naquele ExperienceProfile/Policy.

Self-Service deve cair frequentemente nessa classe para writes administrativos.

## Guidance Session

Suggested Domain/Application representation:

```text
GuidanceSession
  sessionId
  targetId
  symptomIds[]
  runbookId
  runbookVersion
  sourceRefs[]
  activeStepId
  completedSteps[]
  skippedSteps[]
  evidenceRefs[]
  actions[]
  operatorInputs[]
  outcome
  startedAt
  endedAt?
```

A session deve ser resumível no ServiceCase para evitar retrabalho do próximo support level.

## Runbook

Um runbook é structured data, não free-form markdown executável.

```text
Runbook
  runbookId
  version
  titleResourceKey
  purpose
  applicability
  sourceReferences[]
  prerequisites[]
  steps[]
  completionRules[]
  escalationRules[]
  safetyClassification
```

### RunbookStep

Potential fields:

```text
stepId
stepType
instructionResourceKey
evidenceRequirements[]
preconditions[]
capabilityRequirements[]
policyRequirements[]
actionReference?
manualObservationType?
verificationChecks[]
nextStepRules[]
sourceReference?
```

No embedded arbitrary scripting/expression engine. Conditions devem usar a pequena rule model aprovada pelo Domain/Application.

## Evidence-driven branching

Example:

```text
Symptom: DoesNotPrint

Step 1: Check Windows queue
Result: OK
-> skip queue-reset guidance

Step 2: Check transport
Result: OK

Step 3: Read vendor-native state
Result: HeadOpen

Guidance:
Follow approved model-specific head-close check.

Recheck:
HeadOpen=false
ReadyToPrint=true

Outcome:
ResolvedByGuidedManualAction
```

O workflow registra que nenhuma Windows remediation foi executada.

## Knowledge Center

UI concept:

```text
CENTRAL TÉCNICA

Zebra ZT411

[ Guia rápido ]
[ Setup / Commissioning ]
[ Preventiva ]
[ Troubleshooting ]
[ Calibration ]
[ Print Quality ]
[ Network ]
[ Configuration ]
[ Security ]
[ Firmware guidance ]
[ Support / Service ]
```

Search deve considerar canonical topics/symptoms, aliases localizados e model applicability.

## Source hierarchy

Suggested trust order:

1. approved organization policy/procedure, quando aplicável e autorizado;
2. official vendor documentation para o exact model/family;
3. official platform documentation;
4. ThermalOps authored generic runbooks baseados em evidence e references;
5. community reference apenas se explicitamente reviewed/approved.

Um higher-trust source não pode silenciosamente ser substituído por uma forum answer.

## KnowledgeSource

```text
KnowledgeSource
  sourceId
  publisher
  title
  canonicalUrl
  documentVersion?
  publishedDate?
  retrievedDate
  locale
  license/redistributionStatus
  trustClass
  applicability
  hash?
```

A UI deve mostrar source/version quando uma instruction depende dele.

## Online links versus local Knowledge Pack

### Official link mode

ThermalOps abre/referencia documentação oficial.

Pros:

- source atual;
- no redistribution copy.

Cons:

- internet required;
- site may change;
- availability not guaranteed.

### Local Knowledge Pack

Para ambientes offline, o product pode distribuir/indexar conteúdo permitido.

Um pack deve conter apenas material que possa ser legalmente redistributed ou authored metadata/summaries.

Potential structure:

```text
knowledge-pack/
  manifest.json
  sources.json
  runbooks/
  localized-resources/
  indexes/
```

Manifest inclui:

- pack version;
- schema version;
- source inventory;
- hashes;
- supported vendors/models/topics;
- build date;
- license/notices;
- signature quando trusted distribution existir.

### Online Retrieval

Future retrieval pode consultar approved sources, mas precisa de caching, timeout, source allowlist, privacy e prompt-injection defenses.

## Zebra capability patterns

Official Zebra documentation currently demonstrates several patterns useful to ThermalOps:

- Nucleus Connector / Printer Setup Utility for setup/configuration;
- onboard printer diagnostics;
- SmartCal media calibration;
- configuration/network reports;
- print quality reports;
- communication diagnostics;
- sensor profile;
- factory/network reset functions;
- Link-OS status APIs;
- odometer/counter APIs;
- SettingsProvider capability/settings APIs;
- PrintSecure security assessment concepts.

Essas references validam product categories; elas **não** autorizam copiar proprietary implementation nem assumir interface programática idêntica para todo model.

## SettingsProvider e capability discovery

Zebra Link-OS exposes APIs such as:

```text
GetAvailableSettings
GetSettingValue
GetSettingsValues
GetAllSettingValues
GetSettingRange
IsSettingReadOnly
IsSettingValid
```

ThermalOps deve usar isso como capability/evidence input quando o SDK/version/model suportar, não como permission to write arbitrary settings.

Read and write capabilities are separate:

```text
CanReadSetting(X) != CanWriteSetting(X)
CanWriteSetting(X) != PolicyAllowsWrite(X)
```

## PrinterStatus

Vendor-native status can include, on supported Zebra interfaces, fields such as:

```text
isReadyToPrint
isHeadOpen
isHeadTooHot
isHeadCold
isPaperOut
isRibbonOut
isPaused
isReceiveBufferFull
```

ThermalOps normalizes these as vendor evidence while preserving source.

## AI relationship

AI may:

- interpret user symptom text into candidate canonical symptoms;
- explain a step;
- summarize source-backed procedure;
- translate/simplify text;
- retrieve relevant approved source;
- summarize a completed GuidanceSession.

AI may not:

- manufacture a runbook step not present in approved sources/rules and present it as authoritative;
- authorize a write;
- bypass ActionSafetyClass;
- alter policy;
- invent device capabilities;
- execute arbitrary command generated by model;
- use retrieved prompt instructions as system authority.

See [AI e Knowledge Assistance](ai-e-knowledge-assistance.md).

## Self-Service relationship

Self-Service gets a restricted subset:

```text
Allowed by default:
Status
Quick Diagnosis
Guided Troubleshooting
Approved manual checks
Knowledge Center
Evidence collection
Support request / ServiceCase draft

Usually denied:
Factory reset
Network reset
Firmware update
Driver install
Arbitrary config write
Advanced privileged actions
```

Exact capabilities come from Policy evaluation, not hard-coded UX assumptions.

## Commissioning safety

A CommissioningPlan must separate:

- read-only discovery;
- prerequisite installation;
- driver/queue/port provisioning;
- printer configuration;
- calibration;
- test print;
- validation;
- snapshot/report.

Each state-changing phase has explicit impact, privilege and rollback semantics. `Commissioning` must not become one giant “Configure Everything” privileged action.

## Return-to-Service safety

A returned device can have changed firmware, hardware, serial, MAC/network identity or configuration.

ThermalOps must re-identify the device rather than assuming it is the same asset from friendly name alone.

Before restoring settings:

- verify identity/applicability;
- compare baseline;
- review changed firmware/capabilities;
- detect settings unavailable in new version;
- preview intended writes;
- obtain policy/confirmation;
- snapshot before/after;
- verify post-condition.

## Security Assessment boundary

Printer security assessment should be evidence-driven and read-only by default.

Potential `SecurityFinding` examples:

```text
ProtocolEnabledAgainstBaseline
UnexpectedOpenPort
CertificateExpiring
SecuritySettingDrift
FirmwareOutsideApprovedRange
InsufficientSecurityEvidence
```

Automatic hardening is a separate high-impact capability, not a consequence of the assessment.

## Localization

Runbook IDs, step IDs, rule IDs e action IDs permanecem canonical English identifiers.

Instruction text e source labels podem ser localized.

Safety-critical translations devem ser reviewed; não depender somente de machine translation.

## Offline behavior

Guided diagnosis must degrade gracefully:

```text
Local evidence available
Local runbook available
Internet unavailable
AI unavailable

=> deterministic guided workflow continues
```

Se o required source não estiver presente offline:

```text
SourceUnavailableOffline
```

Não inventar instruction para preencher o vazio.

## Status taxonomy

Suggested outcomes:

```text
Resolved
ResolvedWithObservation
NotResolved
EscalationRecommended
BlockedByPolicy
BlockedByMissingCapability
BlockedByMissingSource
InsufficientEvidence
Cancelled
```

## Metrics

Future product analytics, quando policy/privacy permitirem, podem medir apenas aggregate/non-sensitive workflow effectiveness:

- guidance completion rate;
- resolved without escalation;
- escalation after guidance;
- average steps to resolution;
- runbook step failure frequency;
- source coverage gaps.

No customer document content needed.

## Non-goals

- universal repair bot;
- LLM-controlled printer administration;
- auto factory reset;
- unreviewed community instructions;
- copying vendor manuals without licensing rights;
- executing arbitrary commands embedded in documents;
- hiding technician authority boundaries;
- replacing authorized repair organization.

## Relação com outros documentos

- [Guided Operations Architecture](../engenharia/guided-operations-architecture.md)
- [Self-Service](self-service.md)
- [Lifecycle e Health](lifecycle-e-health.md)
- [Preventive Maintenance](manutencao-preventiva.md)
- [AI e Knowledge Assistance](ai-e-knowledge-assistance.md)
- [Security Threat Model complementar](../seguranca/self-service-e-guided-operations-threat-model.md)
- [ADR-0006](../adr/0006-guided-operations-and-knowledge.md)
