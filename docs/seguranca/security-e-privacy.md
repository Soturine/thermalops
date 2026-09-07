# Security e Privacy

ThermalOps interage com Windows printing, vendor devices, customer environments, imported policy/baseline data, support exports e future enterprise services. O security model deve assumir que inputs podem estar incorretos, malformados, stale ou maliciosos, e que uma action privilegiada errada pode afetar recursos não relacionados.

## Security Objectives

1. Read-only Diagnosis/Preventive workflows não viram writes por acidente.
2. UI, device data, imported files ou AI output não transformam o helper em arbitrary code execution.
3. Local Remediation afeta somente o declared target/scope, salvo explicit break-glass confirmation.
4. Imported policy/baseline não amplia executable capability.
5. Portable deixa no intentional persistence.
6. Customer data não é uploaded/exported silenciosamente.
7. Identity-bearing export é visível antes da confirmação.
8. Release artifacts são identifiable, auditable e signable.
9. Failure prefere known/recoverable state a blind continuation.
10. Automatic evidence não pode ser falsamente representada como TechnicianObservation nem vice-versa.
11. Fleet services, quando existirem, obedecem least privilege e explicit authentication/RBAC.

## Trust Boundaries

```text
Operator
  |
  v
Desktop UI (standard user)
  |
  v
Application / Domain
  |        |        |        |
  |        |        |        +--> TechnicianObservation
  |        |        +-----------> Imported policy/baseline/bundle
  |        +--------------------> Vendor/device reads
  +-----------------------------> Windows reads

Approved write only:
Application
  -> local IPC trust boundary
  -> Temporary Privileged Helper
  -> narrowly scoped Windows operation

Future Enterprise:
Agent/Collector -> Central API -> Database/Dashboard
cada boundary exige auth/TLS/RBAC/retention design próprio.
```

## Threat: Privileged Helper Abuse

Um helper que aceite arbitrary command vira local privilege-execution service.

Controls:

- no generic command execution;
- typed/versioned messages;
- capability allowlist;
- restrictive IPC ACL;
- caller/session validation;
- session-bound nonce/token;
- replay protection quando aplicável;
- bounded message sizes;
- per-action timeout;
- canonical target IDs;
- target/policy revalidation no helper;
- no arbitrary path/service/registry/process endpoint;
- helper terminates after intended use;
- binary/signature relationship validada quando implementation chegar.

Forbidden capabilities:

```text
ExecuteCommand(string)
RunPowerShell(string)
RunCmd(string)
DeletePath(string)
WriteRegistry(path, value)
StartArbitraryService(name)
InstallArbitraryDriver(path)
LaunchExecutable(path, args)
```

## Threat: Confused Deputy

Um standard-user process pode tentar fazer o elevated helper agir sobre recurso diferente do apresentado na UI.

Controls:

- display name não é resource identity;
- canonical queue/service target;
- helper re-resolve/revalidate;
- request contém session/plan identity;
- policy evaluated no execution boundary;
- high-impact action usa stronger confirmation;
- logs/audit vinculam plan, request e result.

## Threat: Queue Overreach

Objetivo: corrigir uma queue/job sem afetar outras.

Controls:

- selected-job cancellation via supported API primeiro;
- queue-scoped operations quando possível;
- no broad spool-directory deletion para targeted issue;
- global spool reset como separate break-glass capability;
- before snapshot de affected scope;
- UI lista impact;
- post-condition verification.

## Threat: Service-State Corruption

Remediation pode deixar Print Spooler em state diferente do apropriado.

Controls:

- capture initial state;
- capture relevant startup/policy evidence;
- bounded stop/start waits;
- no blind retry;
- recovery path;
- final state definido por original/policy intent, não por assumption `Running`;
- partial/recovery failure reportado explicitamente.

## Threat: Imported Policy/Baseline Abuse

Imported JSON/package é untrusted input.

Controls:

- schema/version validation;
- bounded file/field sizes;
- encoding validation;
- no embedded script/expression engine;
- no dynamic class loading;
- no arbitrary path/process references executadas;
- policy only reduces/constrains capability;
- signed/trusted package semantics somente após dedicated design;
- baseline compatibility check;
- mismatch não autoriza write;
- unknown field/version behavior definido.

## Threat: Customer-Data Leakage

Potential leakage paths:

- logs no USB;
- full bundle enviado sem review;
- document/job names;
- hostnames/IPs;
- serials;
- filesystem paths;
- screenshots/attachments;
- cloud AI;
- fleet telemetry excessiva.

Controls:

- `%TEMP%` session staging;
- sanitized export default;
- privacy preview;
- explicit FullTechnical/ServiceCase export;
- field-level redaction/pseudonymization;
- no automatic upload;
- no telemetry required;
- no automatic USB save;
- cleanup verification;
- collect only target-relevant data;
- document/label content excluded by default.

## Threat: Attachments / Archive Abuse

Manual attachments e imported bundles são untrusted.

Controls:

- explicit selection;
- type/size/file-count limits;
- safe filename normalization;
- reject absolute paths;
- reject `..` traversal;
- zip-bomb limits;
- no execution;
- no extraction to privileged/system location;
- metadata stripping quando policy exigir;
- hash in manifest;
- malware scanning pode complementar, mas não substituir safe parsing.

## Threat: Malformed Device Responses

Printer/device pode responder com malformed, oversized ou adversarial data.

Controls:

- bounded reads;
- timeout;
- strict parser;
- encoding handling;
- size limits;
- escaping em UI/log/report;
- no command construction a partir de device text;
- unsupported/unknown field handled safely;
- parser exceptions viram structured collection outcome.

## Threat: Unauthorized Network Discovery

Broad scan pode violar customer policy ou gerar security incident.

Controls:

- local/known endpoint first;
- explicit operator/policy permission;
- bounded range/subnet;
- no automatic scan em Customer Safe;
- discovery start auditável;
- rate limiting/timeouts;
- no assumption de unrestricted network access.

## Threat: Maintenance Advice Incorrecto

Unsafe recommendation pode causar downtime/dano.

Controls:

- maintenance tasks source-backed;
- vendor/model/context applicability;
- source/version visible;
- `Unknown` quando inputs faltarem;
- safety notes preservadas;
- no automatic firmware/config action derivada de finding;
- no assumption of disassembly authority;
- AI não define interval/lifetime/due authoritative;
- technician confirmation para manual checks.

## Threat: Evidence Integrity

Se UI/log confundir source, uma pessoa pode tomar decisão errada.

Controls:

- evidence IDs;
- source/timestamp/target;
- automatic vs human attribution;
- immutable point-in-time snapshots;
- Finding references evidence;
- rule version recorded;
- raw/normalized representation quando seguro;
- no silently rewriting evidence after conclusion.

## Threat: Network/Printer Command Injection

Device strings e imported data nunca devem entrar em shell/command context.

Controls:

- prefer native APIs;
- typed vendor commands;
- allowlisted configuration keys;
- no arbitrary ZPL/SGD privileged command interface;
- escaping/encoding;
- fixed executable/argument schema se external tool for inevitável.

## Temporary Files

Use:

```text
%TEMP%\ThermalOps\Sessions\<unpredictable-session-id>\
```

Controls:

- OS-provided temp base;
- unpredictable names;
- restrictive ACL quando practical;
- ownership/location validation;
- reparse-point/symlink safety em privileged paths;
- privileged helper derives sensitive paths internally;
- cleanup only ThermalOps-owned resources;
- report cleanup failure.

## Portable Persistence Threats

E2E deve verificar ausência de:

- ThermalOps service;
- scheduled task;
- Run/Startup entry;
- persistent helper;
- leftover IPC endpoint;
- unexpected registry persistence;
- log beside executable/USB;
- temporary executable copy;
- hidden cache/history no customer endpoint.

Explicit exported file é expected exception.

## Logging

Structured e redactable.

Não logar por default:

- credentials/tokens;
- document contents;
- spool file contents;
- full environment variables;
- unnecessary username/hostname/IP;
- raw network payload indiscriminado;
- proprietary attachment contents.

Errors devem manter diagnostic utility sem revelar secret.

## Privacy Classification

Potential data classes:

```text
PublicProductMetadata
OperationalMetadata
CustomerIdentifier
SensitiveOperationalData
SecretCredential
DocumentContent
```

`SecretCredential` e `DocumentContent` não entram em normal support bundle.

Classification final precisa ser refinada quando schemas reais existirem.

## Export Privacy Levels

### Sanitized

Default. Remove/pseudonymize unnecessary identities.

### FullTechnical

Explicit. Pode conter additional environment/device identity, ainda sem secrets/unrelated content.

### VendorServiceCase

Explicit. Inclui somente fields exigidos/úteis ao approved support workflow.

UI mostra fields/categories antes de export quando possível.

## AI / Privacy

No customer evidence sent to external AI by default.

Future cloud AI exige:

- explicit opt-in policy;
- provider configuration;
- data classification;
- redaction;
- retention/contract review;
- no secret transmission;
- evidence/source citations;
- no privileged authority;
- deterministic fallback.

Retrieved documents/device text são prompt-injection-capable untrusted content.

## Enterprise / Fleet Security

Antes de M6 implementation, ADR/threat model deve definir:

- service authentication;
- user authentication;
- RBAC;
- site/tenant boundaries;
- TLS/certificate lifecycle;
- secrets storage;
- least-privilege agent identity;
- API authorization;
- rate limiting;
- retention/deletion;
- audit log integrity;
- backup/restore;
- offline backlog;
- upgrade security;
- compromised credential/certificate response.

Central service não herda unrestricted local privileges.

## Code Signing

Production binaries devem usar Authenticode quando signing identity existir.

Signing ajuda:

- publisher identity;
- tamper detection;
- application control/allowlisting.

Não substitui secure design.

Private key nunca entra no repository.

## Supply Chain

Release gates devem incluir progressivamente:

- dependency review;
- license inventory;
- secret scanning;
- CodeQL/static analysis;
- vulnerability scanning;
- SBOM;
- signed artifacts;
- SHA-256;
- provenance/attestation quando practical;
- vendor SDK redistribution review.

CI action/dependency pinning/governance deve ser revisado conforme threat model amadurecer.

## Secure Updates

No automatic updater antes de dedicated ADR.

Future design precisa de:

- signed manifests;
- signature verification;
- channel policy;
- atomicity;
- rollback;
- downgrade rules;
- proxy/offline mirrors;
- enterprise deferral;
- compromised-key response;
- audit/logging.

## Endpoint Security Compatibility

Assumir:

- Defender;
- EDR/XDR;
- WDAC;
- AppLocker;
- Controlled Folder Access;
- removable-media policy;
- privilege-management tools.

ThermalOps coopera com controles; não sugere bypass.

## Threat Modeling Process

Atualizar threat model quando uma change adiciona:

- new privileged capability;
- persistent service;
- external API;
- cloud integration;
- new file import/export format;
- updater;
- driver/firmware write;
- direct vendor submission;
- multi-tenant Fleet;
- new credential/secret storage.

Para mudança relevante, documentar:

```text
Asset
Trust boundary
Threat
Preconditions
Impact
Controls
Residual risk
Tests
```

## Security Testing

Veja `../engenharia/testing.md`.

Required high-risk tests incluem:

- helper unauthorized caller;
- nonce/replay;
- target tampering;
- arbitrary action rejection;
- path traversal/reparse point;
- read-only bypass attempt;
- policy capability expansion attempt;
- malformed import;
- bundle/archive traversal;
- redaction failures;
- cleanup/persistence;
- blocked endpoint policy behavior.

## Vulnerability Reporting

Veja `../../SECURITY.md`.

Sensitive exploit details não devem ser abertos em public issue.
