# Support Bundles, Preventive Reports e Service Cases

## Objetivo

Outputs do ThermalOps devem permitir que outro support level, analyst ou authorized service recipient raciocine a partir de evidence sem obrigar o field technician a transcrever manualmente todo o ambiente.

Ao mesmo tempo, export deve minimizar customer data e tornar claro o que será incluído.

## Princípios

- sanitized por default;
- full technical somente por explicit operator choice;
- ServiceCase separado de Diagnostic Report;
- machine-readable data usa versioned schemas;
- human-readable report pode ser localized;
- manifest registra collection status;
- missing/blocked/unsupported evidence não some silenciosamente;
- hashes verificam integridade do bundle;
- attachment é untrusted content;
- nenhum bundle é uploaded automaticamente.

## Session Identity

Cada run possui random session/correlation ID.

Optional metadata pode incluir:

- ticket reference;
- operator-provided customer/site label;
- operator ID quando política permitir;
- purpose/category.

Esses fields são metadata, não authentication/authorization authority.

## Output Classes

### Sanitized Diagnostic Report

Default output para field support.

Inclui:

- target pseudonym/approved identity;
- Windows/transport/device evidence summary;
- Findings;
- missing evidence;
- recommended next step;
- actions attempted;
- verification result;
- ServiceDisposition se aplicável;
- application version/build ID;
- schema version.

Redact/pseudonymize quando não necessário:

- username;
- hostname;
- IP address;
- print server;
- non-target queue;
- document/job name;
- filesystem path;
- customer/site identifiers.

### Preventive Report

Inclui:

- target/session;
- inspection time;
- MaintenancePolicy version;
- MaintenanceTaskCatalog version;
- MaintenanceBaseline version;
- automatic checks;
- TechnicianObservation/checklist;
- MaintenanceDue states;
- configuration drift;
- Findings;
- recommendations;
- local actions, if any;
- ServiceDisposition;
- next inspection somente quando source-backed;
- incomplete/blocked tasks.

Automatic evidence e TechnicianObservation ficam em sections distintas.

### Before/After Report

Para local remediation:

```text
BEFORE
  evidence snapshot A
  target state
  queue/jobs
  service state

ACTION
  RepairPlan
  operator confirmation
  execution result

AFTER
  evidence snapshot B
  validation checks
  post-condition
  recovery outcome
```

A report nunca transforma “command returned success” em `Verified` sem post-condition.

### Full Technical Support Bundle

Explicit operator action only.

Proposed layout:

```text
ThermalOps-SupportBundle-<session>.zip
├── summary.json
├── printers.json
├── drivers.json
├── jobs.json
├── windows-events.json
├── device-status.json
├── device-counters.json
├── device-config.json
├── network.json
├── maintenance-inspection.json
├── diagnostic-label-result.json
├── diagnostic.log
├── action-history.json
├── timeline.json
└── manifest.json
```

Nem todo arquivo existirá em toda sessão.

Manifest deve indicar para cada section:

```text
Collected
SkippedByPolicy
Unsupported
AccessDenied
Timeout
CollectionFailed
Redacted
NotApplicable
```

### ServiceCase / Escalation Package

```text
ThermalOps-ServiceCase-<case>.zip
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

Intended recipients:

- N2/N3;
- internal support team;
- authorized repair center;
- vendor support workflow.

Não há automatic upload.

## Manifest

Candidate schema:

```json
{
  "schemaVersion": "1.0",
  "sessionId": "...",
  "caseId": "...",
  "thermalOpsVersion": "...",
  "commitSha": "...",
  "buildId": "...",
  "createdUtc": "...",
  "locale": "pt-BR",
  "privacyLevel": "sanitized",
  "policyVersion": "...",
  "baselineVersion": "...",
  "maintenanceCatalogVersion": "...",
  "files": [
    {
      "path": "summary.json",
      "sha256": "...",
      "schemaVersion": "1.0",
      "status": "Collected"
    }
  ]
}
```

## Machine-readable vs Human-readable

Schemas internos permanecem locale-neutral.

Exemplo:

```json
{
  "serviceDisposition": "ContinueWithObservation",
  "maintenanceDue": "DueSoon"
}
```

Human report pt-BR:

```text
Disposição: Continuar com observação
Manutenção: Vence em breve
```

Localization nunca altera canonical machine values.

## Summary Model

`summary.json` deve conter overview suficiente sem duplicar arbitrariamente todo bundle.

Potential fields:

- target reference;
- session purpose;
- overall findings;
- evidence completeness;
- action count;
- disposition;
- maintenance summary;
- privacy level;
- generated-at;
- app/build version.

## Timeline

Timeline separa intent, observation, execution e validation.

Suggested events:

```text
Observed
FindingDerived
Recommended
OperatorRequested
Confirmed
ExecutionStarted
Executed
VerificationStarted
Verified
Partial
Failed
RecoveryStarted
RecoveryCompleted
ServiceDispositionAssigned
Exported
```

## Action History

Cada state-changing action registra:

- RepairPlan ID;
- target;
- policy decision;
- impact;
- confirmation;
- action results;
- validation;
- recovery;
- before/after refs;
- timestamps.

## Redaction

### Goals

Remover unnecessary identity sem destruir diagnostic correlation.

Pode usar stable per-bundle pseudonyms:

```text
HOST-01
PRINTSERVER-01
IP-01
QUEUE-01
```

Se o mesmo hostname aparecer em vários files do mesmo bundle, o pseudonym deve ser consistente dentro daquele bundle quando correlation for necessária.

### Fields para atenção

- usernames;
- hostnames;
- IPs;
- UNC paths;
- print server names;
- document names;
- file paths;
- serial numbers;
- customer labels;
- ticket IDs;
- device descriptions com site info.

Nem todo field precisa sempre ser redacted; o privacy policy define necessity. Default é minimizar.

## Privacy Levels

### Sanitized

Default.

Objetivo: preservar diagnostic usefulness com mínimo de identifiers.

### FullTechnical

Explicit choice.

Pode incluir identifiers adicionais necessários para authorized support. Ainda exclui:

- secrets;
- credentials;
- unrelated document content;
- arbitrary spool file contents;
- unrelated customer devices.

### VendorServiceCase

Explicit choice.

Pode exigir model/serial/firmware/problem classification dependendo do workflow aprovado.

UI precisa mostrar privacy preview antes do export.

## Privacy Preview

Antes de full/service-case export, mostrar algo como:

```text
Este pacote incluirá:
- printer model
- serial number
- firmware
- selected configuration
- Windows events
- target endpoint address

Não incluirá:
- document contents
- credentials
- unrelated printer data
```

A lista real é dynamic conforme collected data/policy.

## Attachments

Future manual attachments:

- explicit selection;
- no auto-capture;
- type allowlist ou safe generic handling;
- file size limits;
- total archive size limits;
- no execution;
- safe filename normalization;
- archive path traversal prevention;
- metadata stripping quando policy exigir;
- hash no manifest;
- malware scan integration quando environment disponibilizar, sem depender disso como única defesa.

## Archive Safety

Ao gerar/ler ZIP:

- derive archive paths internally;
- normalize separators;
- reject `..` traversal;
- reject absolute paths;
- bound file count/size;
- defend against zip bombs;
- no automatic extraction of untrusted bundle into privileged location;
- extraction, se existir, usa safe session directory.

## Storage

Staging default:

```text
%TEMP%\ThermalOps\Sessions\<session-id>
```

Não salvar automaticamente no executable directory ou USB.

Export destination é explicit operator choice.

## Cleanup

Após export/discard:

- close streams;
- delete owned temp staging;
- report failures;
- preserve explicit exported file;
- no deletion outside session ownership.

## Encryption

Não criar home-grown encryption.

Se encrypted bundle for necessário:

- ADR;
- standard format;
- key distribution;
- recovery;
- enterprise compatibility;
- recipient workflow;
- metadata visibility;
- cryptographic library review.

Sanitization + approved secure transfer é early default.

## Schema Versioning

Machine outputs usam versioned schemas.

Requisitos:

- explicit `schemaVersion`;
- backwards-compatible reading strategy quando possível;
- migration/conversion tooling se necessário;
- tests com old fixtures;
- unknown fields tolerated conforme design;
- required fields claramente definidos;
- validation antes de AI/analytics processing.

## Support Bundle as Input

Se future ThermalOps puder reabrir bundle:

- treat entire archive as untrusted;
- verify schema;
- verify hashes quando manifest existir;
- do not trust publisher/customer identity automaticamente;
- no execution;
- no privileged action derivada diretamente do bundle;
- mark stale historical evidence claramente.

## AI Use

AI pode summarize/explain bundle após redaction/policy, mas:

- no external upload by default;
- source/evidence citations;
- output não altera evidence;
- output não autoriza action;
- bundle parsing robusto contra prompt injection em text fields.

## Testing

Required tests incluem:

- sanitized vs full;
- pseudonym consistency;
- serial/IP/path redaction;
- missing/unsupported section no manifest;
- hash consistency;
- corrupt archive;
- zip traversal;
- zip bomb limits;
- attachment opt-in;
- metadata policy;
- disk full;
- destination unavailable;
- cleanup locked file;
- schema compatibility;
- localized human report com invariant machine JSON;
- privacy preview correctness.
