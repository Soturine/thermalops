# ADR-0002: Temporary Privileged Helper Separado

- **Status:** Accepted in principle; implementation details require M2 threat-model review
- **Date:** 2026-09-07

## Context

Algumas local-remediation actions podem exigir Administrator privilege. Manter todo o Desktop elevated aumenta attack surface, dificulta least privilege, piora compatibility com enterprise controls e conflita com o valor da Portable Lite/Pro.

A maioria das ações de Diagnosis e Preventive Inspection deve funcionar em standard-user context.

## Decision

Portable Pro mantém main UI/Application process em standard-user integrity e inicia um **Temporary Privileged Helper** somente quando um approved `RepairPlan` exige elevation.

O helper expõe um local IPC protocol pequeno, versionado, strongly typed e allowlisted.

## Core Invariant

```text
Standard-user UI
   |
   | Diagnosis / Preventive / Reporting
   | (no elevation)
   |
   +---- explicit approved RepairPlan ----> UAC
                                             |
                                             v
                                Temporary Privileged Helper
                                             |
                                     one allowlisted action
                                             |
                                             v
                                      verify / terminate
```

Privilege é temporário e orientado a capability, não ao aplicativo inteiro.

## Required Properties

- UAC somente quando necessário;
- no persistent service em Portable;
- no arbitrary shell/script/process execution;
- restrictive local IPC ACL;
- protocol version;
- session-bound nonce/token;
- request ID;
- caller/process/session validation quando practical;
- canonical target identity;
- strongly typed request/response;
- capability allowlist;
- bounded message/input sizes;
- per-action timeout;
- helper revalidates target e policy;
- action/result/audit correlation;
- clean termination;
- orphan cleanup/recovery strategy;
- signing/identity verification relationship entre UI/helper.

## Initial Capability Candidates

Apenas após implementation/tests:

```text
CancelPrintJob(queueId, jobId)
RestartPrintSpooler(expectedInitialState)
RepairSelectedQueue(queueId, strategyId)
```

Cada capability é específica e possui schema próprio.

## Explicitly Rejected Capability

```text
ExecuteCommand(string)
```

E equivalentes:

```text
RunPowerShell(string)
RunCmd(string)
LaunchExecutable(path, args)
DeletePath(string)
WriteRegistry(path, value)
StartArbitraryService(name)
```

Reason: transformariam narrow repair helper em generic local privilege execution surface.

## Rejected Design: Entire UI Elevated

Não executar ThermalOps inteiro como Administrator por default.

Reasons:

- unnecessary privilege para read-only workflows;
- maior blast radius de UI/parser/vendor data bugs;
- pior separation of duties;
- imported data passaria por elevated process desnecessariamente;
- maior dificuldade de demonstrar safe Portable behavior.

## IPC Candidate

Named pipe é preferred initial candidate, sujeito a M2 validation.

Reasons:

- local Windows primitive;
- ACL control;
- request/response model adequado;
- no need for localhost TCP listener.

Exact ACL/integrity/process validation ainda precisa de spike/test.

## Protocol Concepts

Conceptual request:

```text
ProtocolVersion
SessionId
RequestId
NonceOrToken
ActionType
PlanId
CanonicalTarget
ActionPayload
Deadline
```

Response:

```text
ProtocolVersion
RequestId
ExecutionOutcome
NativeError?
VerificationData?
Timing
AuditReference
```

UI message não deve transportar localized strings como command identity.

## Authentication / Session Binding

O protocol deve impedir que unrelated local process envie uma action ao helper.

Potential controls:

- named pipe ACL;
- current user/session binding;
- cryptographically random nonce/token entregue de forma segura;
- short lifetime;
- caller PID/process identity validation where reliable;
- helper executable identity;
- request replay detection.

A combinação final precisa de threat-model testing em M2.

## Target Revalidation

Helper não confia em display name enviado pela UI.

Para queue/job:

1. resolve canonical queue target;
2. re-enumerate/revalidate job;
3. verify relation to requested plan;
4. reject stale/conflicting target;
5. execute only if policy/preconditions remain true.

Isso reduz confused-deputy risk.

## Helper Location / Extraction

Se Portable for single-file, helper extraction precisa de design seguro.

M2 deve decidir:

- bundled separate signed helper vs extraction;
- temp path ownership/ACL;
- binary hash/signature verification;
- cleanup;
- race/replacement protection;
- endpoint security compatibility.

Não extrair executable em predictable writable path e simplesmente elevated-execute sem verification.

## Failure Behavior

### UAC Denied

- no action executed;
- UI reports cancellation/denial;
- no hidden retry;
- deterministic diagnosis remains available.

### Helper Crash

- UI times out;
- current Windows state re-collected;
- action marked Unknown/Partial until verified;
- recovery suggested/executed only through approved path;
- orphan resources cleaned when possible.

### IPC Disconnect

Execution outcome não é inferido automaticamente. Re-query target/post-condition.

### UI Crash

Helper must not become permanent daemon. Define action-specific behavior to finish safely or abort/recover, then terminate.

## Logging / Audit

Registrar sem secrets:

- session ID;
- plan ID;
- request ID;
- action type;
- canonical target;
- caller/session validation outcome;
- execution outcome;
- verification reference;
- duration;
- error category.

Não logar token/nonce reutilizável.

## Testing Requirements

Antes de M2 exit:

- unauthorized caller;
- wrong nonce/token;
- replay;
- unsupported protocol version;
- unknown capability;
- malformed/oversized payload;
- target spoofing;
- unrelated queue request;
- policy changed;
- UAC denied;
- helper crash;
- UI crash;
- IPC disconnect;
- timeout;
- path/reparse tampering se extraction existir;
- helper binary replacement/mismatch;
- no helper persistence after session.

## Consequences

### Positive

- least privilege;
- smaller elevated attack surface;
- Portable Lite remains cleanly read-only;
- privileged behavior auditable/testable;
- easier enterprise security review.

### Costs

- IPC complexity;
- helper lifecycle complexity;
- signing/extraction concerns;
- concurrency/crash recovery testing;
- more explicit schemas/action code.

Esses custos são aceitáveis porque privilege boundary é safety-critical.

## Revisit Triggers

Revisitar se:

- Enterprise precisar de persistent agent/service;
- Windows security model/tooling justificar mecanismo melhor;
- privilege-management product exigir integration específica;
- helper capability set crescer a ponto de indicar architecture smell.

Enterprise persistent service precisa de ADR próprio e não herda automaticamente este helper contract.
