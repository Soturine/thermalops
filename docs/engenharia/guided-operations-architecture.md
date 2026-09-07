# Guided Operations Architecture

## Objetivo

Este documento define a arquitetura técnica para Guided Operations, Knowledge, Self-Service, Lifecycle/Health e future native diagnostic actions sem violar as boundaries do ThermalOps.

A intenção é evitar três anti-patterns:

1. colocar troubleshooting business logic na WPF;
2. transformar documentos/LLM em executable control plane;
3. acoplar o Domain diretamente ao Zebra SDK ou a um helpdesk específico.

## High-level architecture

```text
ThermalOps.Desktop
  |
  +-- ExperienceProfile Presenter
  +-- Guidance UI
  +-- Knowledge Center UI
  +-- Health/Lifecycle UI
  |
  v
ThermalOps.Application
  |
  +-- DiagnoseUseCase
  +-- RunGuidanceUseCase
  +-- GetKnowledgeUseCase
  +-- AssessHealthUseCase
  +-- CreateServiceCaseUseCase
  +-- CommissionPrinterUseCase (future)
  +-- ReturnToServiceUseCase (future)
  |
  v
ThermalOps.Domain
  |
  +-- Evidence / Findings
  +-- Guidance definitions/state
  +-- Health/Lifecycle semantics
  +-- Policy / ExperienceProfile
  +-- ServiceCase / RepairPlan
  |
  +-------------------------+
  |                         |
  v                         v
Knowledge Ports        Device/Windows Ports
  |                         |
  v                         v
Knowledge Infra        Windows Infra / Vendor Adapters
```

Writes continuam seguindo:

```text
Application -> typed action -> policy -> RepairPlan
            -> Temporary Privileged Helper when Windows elevation is required
            -> Vendor Adapter write boundary when device write is required
            -> Verify post-condition
```

## Modules inside the modular monolith

Não criar projects novos automaticamente. M1-M4 devem primeiro usar módulos/namespaces coesos dentro dos projects existentes.

Suggested logical modules:

```text
ThermalOps.Domain
  Diagnostics/
  Maintenance/
  Guidance/
  Health/
  Service/
  Policies/

ThermalOps.Application
  Diagnostics/
  Guidance/
  Knowledge/
  Health/
  SelfService/
  ServiceCases/
  Remediation/

ThermalOps.Infrastructure.Windows
  Printing/
  PnP/
  Services/
  Eventing/

ThermalOps.Adapters.Zebra
  Status/
  Settings/
  Counters/
  Diagnostics/
```

Um `ThermalOps.Knowledge` project separado só deve surgir se houver boundary/dependency concreta que justifique deployment/testing diferente.

## Domain model additions

### Guidance

```text
Runbook
RunbookStep
RunbookApplicability
GuidanceSession
GuidanceStepResult
GuidanceOutcome
ActionSafetyClass
CanonicalSymptom
SourceReference
```

### Health/Lifecycle

```text
AssetAge
UsageMetric
UsageMetricType
UsageUnit
ComponentCondition
ManufacturerWarning
HealthAssessment
HealthComponent
HealthContribution
MaintenanceCompliance
ConditionTrend
RemainingLifeEstimate
RemainingLifeStatus
ApplicabilityClass
```

### Experience / Self-Service

```text
ExperienceProfile
CapabilityPresentation
AssignedAssetScope
BlockedCapabilityReason
SupportRequest
```

Esses nomes são candidates; implementation pode refiná-los por ADR/code review sem perder as semantics definidas nos product docs.

## Ports

Suggested Application ports:

```text
IRunbookRepository
IKnowledgeSourceRepository
IKnowledgePackVerifier
IPrinterCapabilityProvider
IPrinterUsageReader
IPrinterDiagnosticActionProvider
IServiceDeskConnector
IAssetScopeProvider
IIdentityContext
```

### IRunbookRepository

Responsável por retornar structured runbooks aplicáveis.

Não retorna arbitrary code/script.

Conceptual API:

```text
FindApplicableAsync(targetContext, symptom, locale)
GetByIdAsync(runbookId, version)
```

### IKnowledgeSourceRepository

Resolve source metadata e content references permitidas.

Can support:

- local metadata/index;
- approved local pack;
- official URL reference;
- future online retrieval.

### IPrinterCapabilityProvider

Agrega capability evidence de Windows/vendor adapters sem deixar UI adivinhar feature support.

Conceptual output:

```text
CapabilitySet
  canReadStatus
  canReadCounters
  canReadSetting(key)
  canRunDiagnostic(action)
  canWriteSetting(key)
  capabilitySources[]
  limitations[]
```

`canWriteSetting` não equivale a `policyAllowsWrite`.

### IServiceDeskConnector

Opcional e configurado no Enterprise/integration boundary.

```text
CreateTicketAsync(ServiceCaseExport, SupportRequestContext)
GetSubmissionCapabilitiesAsync()
```

Connector não recebe arbitrary local filesystem access nem credentials em plain text.

## Guidance rule evaluation

Runbook branching deve usar uma deterministic rule model pequena e auditable.

Avoid:

```text
script: "if (...) { powershell ... }"
```

Prefer:

```text
Condition
  evidenceKey
  operator
  expectedValue

NextStepRule
  when ConditionSet
  nextStepId
```

Supported operators devem ser enumerados e bounded.

Examples:

```text
Equals
NotEquals
Exists
CollectionOutcomeIs
CapabilityAvailable
PolicyAllows
AllOf
AnyOf
```

Complex logic should move to compiled Domain/Application rules, not grow into a general expression engine.

## Action resolution

A runbook references an `ActionReference`, not arbitrary command text.

```text
ActionReference
  actionType = CalibrateMedia
  requiredCapability = Zebra.MediaCalibration
  safetyClass = AssistedWrite
```

Application resolves this to a typed action implementation after revalidating target, capability and policy.

No document or AI text can construct privileged method names dynamically.

## Action registry

Conceptual registry:

```text
ActionType
  ReadStatus
  ReadConfigurationReport
  RunPrintQualityReport
  RunSensorProfile
  CalibrateMedia
  PrintDiagnosticLabel
  CancelSelectedJob
  UnpauseQueue
  RestartSpooler
  FactoryReset
  FirmwareUpdate
```

Not all are implemented. Registry entry status can be:

```text
Planned
ImplementedNotValidated
Experimental
Validated
Disabled
```

Each action declares:

- read/write;
- target type;
- safety class;
- privilege requirement;
- policy key;
- capability requirement;
- verification strategy;
- rollback/recovery strategy where applicable.

## Knowledge pack architecture

A local pack should be data-only.

Example:

```text
ThermalOps.KnowledgePack.zip
├── manifest.json
├── sources.json
├── runbooks/
│   ├── zebra.zt4x1.media-calibration.v1.json
│   └── generic.windows.queue-stalled.v1.json
├── strings/
│   ├── pt-BR.json
│   └── en-US.json
└── indexes/
```

Pack must never contain executable DLL/script loaded automatically.

### Manifest

```text
schemaVersion
packId
packVersion
createdUtc
publisher
sources[]
files[] with sha256
supportedLocales[]
signatureMetadata?
```

When organization-trusted signed packs exist, trust changes *data provenance*, not executable capability.

## Knowledge pack validation

- archive size/file-count bounds;
- no traversal;
- UTF-8/schema validation;
- hash verification;
- signature verification when trusted mode exists;
- source inventory/license status;
- no unexpected binary/executable content;
- runbook IDs/version uniqueness;
- localization resource completeness;
- no unknown action references unless explicitly tolerated as unsupported.

## Online retrieval boundary

Future online retrieval should return text/source metadata only.

It must not return executable actions directly.

Flow:

```text
Query
 -> approved source allowlist
 -> retrieval
 -> sanitize/limit content
 -> source metadata
 -> optional AI explanation
 -> user-visible citation
```

Device/user data sent to search endpoints must be minimized.

## Zebra Adapter evolution

The current conceptual adapter can evolve from:

```text
ReadStatus
ReadCounters
ReadConfiguration
RunApprovedDiagnostic
```

to more explicit capability families:

```text
IPrinterStatusReader
IPrinterSettingsReader
IPrinterUsageReader
IPrinterDiagnosticActionProvider
IPrinterConfigurationWriter (future, narrow)
IFirmwareActionProvider (future, separate risk)
```

This can be logical interfaces in one adapter project; do not create interface explosion unless implementation benefits.

## Settings capability model

For vendor setting `X`:

```text
ReadCapability(X)
WriteCapability(X)
AllowedRange(X)
ReadOnlyFlag(X)
PolicyDecision(X)
```

All are distinct.

A setting may be writable by vendor API but denied by ThermalOps policy.

## Native diagnostic action semantics

Each self-test/diagnostic action should define:

```text
DiagnosticActionDefinition
  actionType
  vendor
  applicability
  stateChange
  mediaConsumption
  expectedDuration
  requiresIdlePrinter
  requiresMedia
  requiresRibbon?
  privilegeRequirement
  sourceReference
  verification
```

Example: a print quality report consumes media and changes printer activity, so it is not read-only even if it does not permanently alter configuration.

## Health engine

Health calculation belongs to Domain/Application rules, not adapters.

Adapters emit evidence:

```text
HeadTooHot = false
TotalPrintLength = X
HeadMaintenanceWarning = true
```

Health rules derive:

```text
PrintheadHealth = AttentionRecommended
```

and preserve evidence/rule version.

## RUL boundary

RUL estimator, if ever implemented, is a replaceable Application/Domain service with explicit model metadata:

```text
IRemainingLifeEstimator
  applicability
  modelVersion
  requiredFeatures
  validationMetadata
```

No estimator exists by default. `NotValidated` is a valid product outcome.

## ExperienceProfile architecture

`ExperienceProfile` is not authorization by itself.

Final capability presentation is intersection:

```text
ExecutableCapabilities
INTERSECT DeviceCapabilities
INTERSECT OrganizationPolicy
INTERSECT User/AssetScope
INTERSECT ExperienceProfile
INTERSECT RuntimeConstraints
```

This prevents UI profile from accidentally granting a capability.

## Self-Service authorization

For managed Enterprise:

```text
User identity
 -> RBAC/assignment policy
 -> allowed asset scope
 -> allowed use cases
```

For Portable Lite Self-Service:

```text
No central identity required
 -> only local/selected assets
 -> permanent read-only capability envelope
```

Self-Service should not depend on obscurity of hidden buttons.

## Helpdesk connector boundary

Connector receives a prepared export payload and explicit submission context.

Suggested flow:

```text
ServiceCaseDraft
 -> Redaction
 -> PrivacyPreview
 -> OperatorConfirmation
 -> Serialize connector payload
 -> Submit
 -> Capture external case ID/status
```

Do not allow connector adapters to trigger device remediation.

## Corporate deployment relationship

Managed Self-Service client follows Enterprise packaging/lifecycle rules.

It can be published via software distribution platforms. Microsoft Intune Company Portal is a useful deployment pattern: administrators make approved applications available and users can install/use those available apps. ThermalOps remains vendor-neutral toward deployment tooling.

## Security boundaries introduced

New boundaries requiring threat modeling:

- Knowledge Pack import;
- online source retrieval;
- ServiceDesk connector;
- user identity/asset assignment;
- native diagnostic writes;
- security assessment data;
- health/RUL derived output.

See the dedicated threat-model supplement.

## Observability

Suggested structured events:

```text
GuidanceSessionStarted
RunbookResolved
RunbookStepPresented
RunbookStepVerified
GuidanceActionRequested
GuidanceActionBlocked
GuidanceCompleted
KnowledgeSourceOpened
KnowledgePackValidated
KnowledgePackRejected
HealthAssessmentProduced
UsageMetricCollected
ServiceRequestPrepared
ServiceRequestSubmitted
```

No document text or personal data in event names.

## Versioning

Need independent versions for:

```text
Domain schema
Runbook schema
Knowledge pack
Maintenance catalog
Health rule set
Security baseline
ServiceCase schema
Connector schema
```

A product release may update one or more; reports must record versions that affected decisions.

## Failure model

Guidance/Knowledge collection outcomes:

```text
Success
Unsupported
Unavailable
BlockedByPolicy
SourceUnavailableOffline
SourceVersionUnsupported
KnowledgePackInvalid
CapabilityMissing
TargetChanged
Timeout
Cancelled
Failed
```

The UI should not collapse these into generic `Erro`.

## Testing

Dedicated matrix is in `validation-matrix-lifecycle-guidance-self-service.md`.

Key rules:

- same evidence => same Domain Finding across profiles;
- runbook cannot bypass policy;
- invalid pack cannot execute anything;
- AI output cannot select an ActionType directly without deterministic re-resolution;
- native actions require HIL before support claim;
- RUL remains unavailable until validation requirements exist.

## Migration strategy

Add these capabilities incrementally:

1. model the Domain semantics and data-only runbooks;
2. add read-only guidance using M1 evidence;
3. add Zebra read capabilities during M3;
4. add source-backed preventive guidance in M4;
5. add managed Self-Service deployment/integration in M5+;
6. add fleet history/health trends in M6;
7. add safe vendor-native writes only through explicitly approved action backlog;
8. add AI retrieval/explanation in M8;
9. RUL only in M9 research.

No need to delay all guidance until AI.
