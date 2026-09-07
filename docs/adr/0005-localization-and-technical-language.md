# ADR-0005: Localization pt-BR-first com Technical Language e Code em Inglês

- **Status:** Accepted for product design and initial implementation
- **Date:** 2026-09-07

## Context

O público inicial do ThermalOps inclui technicians/support analysts no Brasil. Uma UI totalmente em inglês aumenta friction desnecessário no field workflow, principalmente para warnings, confirmations, preventive checklists e reports.

Ao mesmo tempo, o ecosystem técnico do produto é majoritariamente expresso em inglês:

- .NET/C#;
- Windows APIs;
- WinSpool;
- PnP;
- Event Log;
- Link-OS/SGD/ZPL;
- common architecture terms;
- security/release tooling;
- vendor SDK documentation.

Traduzir literalmente todos os terms e code identifiers reduziria precisão e aumentaria manutenção.

## Decision

ThermalOps será:

- **pt-BR-first** para user-facing UI, human-readable reports e repository documentation;
- **localization-ready** desde a primeira UI implementation;
- **English canonical** para code identifiers, Domain type names, schema fields, protocol/internal contracts e structured event types;
- natural/bilingual na documentação técnica, preservando established technical terms em inglês quando a tradução literal não melhora compreensão.

## User-Facing Language

Locale inicial de referência:

```text
pt-BR
```

Future candidates:

```text
en-US
es
```

Adicionar locale não pode duplicar business logic.

## Canonical Technical Identifiers

Examples que permanecem em inglês:

```text
MaintenanceInspection
MaintenanceBaseline
DiagnosticEvidence
DiagnosticFinding
TechnicianObservation
ServiceDisposition
ServiceCase
RepairPlan
HealthAssessment
ConditionTrend
```

Não criar duplicate translated types.

## Technical Terms na Documentação

Terms consolidados podem permanecer em inglês dentro de frases pt-BR:

```text
Domain
Application
Infrastructure
Adapter
Policy
Baseline
Spooler
WinSpool
PnP
Event Log
Link-OS
SGD
ZPL
CI/CD
SBOM
RBAC
TLS
IPC
UAC
```

A meta é precisão/naturalidade, não pureza linguística.

## UI Labels

Canonical Domain value e localized label são distintos.

Example:

```text
Domain: ContinueInService
pt-BR: Continuar em serviço
en-US: Continue in service
```

Business logic nunca compara localized display text.

## Resource Architecture

WPF deve usar resource mechanism, não hard-coded strings espalhadas em code-behind/ViewModel.

Potential direction:

```text
Resources/
  Strings.resx
  Strings.pt-BR.resx
  Strings.en-US.resx
```

Exact tooling pode ser refinado durante M1, desde que preserve invariants:

- stable semantic resource keys;
- deterministic fallback;
- no business rule em translated string;
- no localized identifier em schema;
- testability.

## Resource Keys

Prefer semantic keys:

```text
Diagnosis.Quick.Title
Maintenance.Preventive.Title
ServiceDisposition.ContinueInService
RepairPlan.Confirmation.Title
Export.Privacy.FullTechnical.Warning
```

Evitar usar a frase em português como key.

## Machine-readable Data

Schemas permanecem locale-neutral.

Example:

```json
{
  "serviceDisposition": "ContinueWithObservation",
  "maintenanceDue": "DueSoon",
  "evidenceSource": "ZebraNative"
}
```

Human report pode traduzir labels sem alterar os valores persistidos.

## Structured Logs

Event types permanecem estáveis:

```text
SessionStarted
EvidenceCollectionFailed
MaintenanceInspectionCompleted
RepairPlanVerified
ServiceCaseExported
```

User-visible message pode ser localized.

## Error Model

Usar stable code/type + localized message quando apropriado.

Example:

```text
PORTABLE_TEMP_UNAVAILABLE
```

pt-BR:

```text
Não foi possível criar a área temporária segura para esta sessão.
```

Isso facilita support cross-locale.

## Dates, Numbers e Units

Presentation respeita locale para:

- date/time;
- number formatting;
- decimal separator;
- user-facing units.

Machine-readable data usa canonical formats/documented units.

Não serializar numeric Domain value como localized string.

## Reports

Human-readable report deve poder ser localized independentemente de JSON schemas.

Bundle manifest registra locale do human report, mas canonical fields permanecem estáveis.

## Safety-Critical Warnings

Warnings de high-impact action, privacy export ou maintenance safety precisam de reviewed translation.

AI/machine translation pode auxiliar drafting, mas não deve ser única revisão para safety-critical wording.

## Documentation

Repository docs usam pt-BR-first com technical terms preservados em inglês.

Structure por responsibility é definida na Engineering Constitution.

Isso facilita leitura local sem distanciar o texto de official Microsoft/Zebra/.NET vocabulary.

## Source Code

Code permanece em inglês:

- namespaces;
- type names;
- method names;
- property names;
- enum names/values;
- interfaces;
- tests ligados diretamente ao code/domain;
- JSON field names;
- protocol messages.

Comments podem usar inglês ou pt-BR conforme contexto, mas devem ser raros e úteis; naming/documentation deve tornar code self-explanatory.

## Alternatives Considered

### Everything in English

Simplifica code/docs consistency, mas piora initial field UX para público brasileiro.

Rejected para user-facing product.

### Everything Literally Translated to Portuguese

Rejected porque:

- perde correspondência com vendor/platform docs;
- cria awkward architecture terms;
- piora code naming;
- dificulta contribuição/manutenção;
- não ajuda internacionalização futura.

### Separate Full Repository per Language

Rejected initially por duplication/maintenance cost.

Pode existir translated docs set no futuro se demand justificar e existir governance sustentável.

## Testing Requirements

- missing resource keys;
- fallback locale;
- long-string layout;
- DPI/scaling;
- screen reader semantics;
- date/number formatting;
- report localization;
- canonical schema invariance;
- same Domain decision em locales diferentes;
- safety warning resource coverage.

## Consequences

### Positive

- natural Brazilian technician UX;
- stable English code/contracts;
- future locales sem business logic duplication;
- technical docs próximas da vocabulary oficial;
- better supportability cross-locale.

### Costs

- resource governance;
- localization tests;
- terminology review;
- layout must handle variable text length;
- reports precisam de presentation/machine separation.

## Revisit Triggers

Revisitar se:

- significant international adoption justificar default locale change;
- docs precisarem de full multilingual publishing pipeline;
- WPF localization tooling escolhido se mostrar inadequado;
- legal/compliance require specific language behavior.

A mudança de locale default não altera canonical Domain/schema identifiers.
