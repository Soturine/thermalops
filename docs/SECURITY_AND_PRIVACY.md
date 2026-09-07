# Security and Privacy

## Security objectives

1. Read-only diagnosis/preventive workflows cannot accidentally become writes.
2. UI/device/imported data cannot turn the helper into arbitrary code execution.
3. A local remediation affects only declared scope unless a break-glass plan is explicitly confirmed.
4. Preventive policy/baseline data cannot expand executable capabilities.
5. Portable leaves no intentional persistence.
6. Customer data is not uploaded/exported silently.
7. Service-case exports make identity-bearing content visible before export.
8. Release artifacts are identifiable/signable/auditable.
9. Failure prefers a known/recoverable state over blind continuation.

## Trust boundaries

```text
Operator
  -> Desktop UI (standard user)
  -> Application / Domain
      -> Windows reads
      -> Vendor/device reads
      -> Imported maintenance policy/baseline (untrusted input)
      -> Technician observations

Only approved write:
Application -> IPC trust boundary -> Privileged Helper -> Windows

Future Enterprise:
Agent/API/database/dashboard are additional trust boundaries requiring ADR/threat-model updates.
```

## Privileged helper abuse

Controls:

- no generic command execution;
- typed/versioned messages;
- capability allowlist;
- restrictive IPC ACL;
- caller/session validation;
- nonce/token;
- bounded inputs/timeouts;
- canonical target IDs;
- helper revalidates policy/target;
- no arbitrary path/service/registry/process endpoint.

## Confused deputy / scope overreach

Controls:

- target identity revalidation;
- selected-job cancellation first;
- queue-scoped operations where possible;
- global reset separate break-glass capability;
- visible impact/scope;
- pre/post snapshots;
- stronger confirmation for broad impact.

## Service-state corruption

Record initial Spooler state/configuration, use bounded waits, preserve policy-required state, verify post-condition and attempt recovery. Never force `Running` merely because the tool wants it.

## Imported policy/baseline threats

Treat imported JSON/package as untrusted:

- schema/version validation;
- bounded file/field sizes;
- no embedded script/expression engine;
- no path/command execution;
- policy can reduce capability only;
- signature required before treating a package as organization-trusted when that feature exists;
- baseline mismatch does not automatically authorize changes.

## Customer-data leakage

Controls:

- session staging under `%TEMP%`;
- sanitized default export;
- full/service-case export explicit;
- redaction pipeline;
- no automatic USB save;
- no upload/telemetry by default;
- cleanup verification;
- minimize document/job names and environment identifiers.

## Attachments

Manual attachments are untrusted. Enforce explicit selection, file/size validation, safe archive/path handling, no execution, optional metadata stripping and privacy preview.

## Malformed device/network data

Use bounded reads, timeouts, strict parsing, encoding handling, output escaping and size limits. Never turn printer text into executable commands.

## Network discovery

Local/known endpoint first. Broader discovery requires explicit operator/policy authorization and bounded scope. No automatic scan in Customer Safe.

## Maintenance safety

- no invented maintenance intervals;
- source/applicability retained;
- no automatic firmware/config changes from preventive findings;
- no assumption that disassembly is allowed;
- no LLM authority for due/disposition;
- show manufacturer/model-specific safety notes rather than generalizing risky procedures.

## Privileged capability candidates

```text
CancelPrintJob(queueId, jobId)
RestartPrintSpooler(expectedInitialState)
RepairSelectedQueue(queueId, strategyId)
```

Explicitly forbidden generic capabilities:

```text
ExecuteCommand(string)
RunPowerShell(string)
RunCmd(string)
DeletePath(string)
WriteRegistry(path, value)
StartArbitraryService(name)
InstallArbitraryDriver(path)
```

## Temporary files

Use unpredictable OS-temp session paths, restrictive ACLs where practical, reparse-point/symlink safety at privilege boundaries, ownership/location checks and cleanup only of ThermalOps-owned resources.

## Logging

Structured/redactable. Do not log secrets, arbitrary spool content, full environment variables, document contents or unnecessary identities.

## AI/privacy

No external AI upload by default. Future cloud AI requires opt-in organization policy, redaction, provider/retention review, evidence citations and zero privileged/maintenance/disposition authority.

## Supply chain

Release gates grow to include dependency/license review, secret scanning, CodeQL/static analysis, vulnerability scanning, SBOM, signed artifacts, checksums and provenance/attestation where feasible.

## Code signing / endpoint controls

Production binaries should use Authenticode when available. ThermalOps cooperates with Defender, EDR/XDR, WDAC, AppLocker and removable-media/application controls rather than bypassing them.

## Secure updates

No automatic update without ADR covering signed manifests, rollback/downgrade, proxy/offline environments, enterprise deferral and signature verification.

## Vulnerability reporting

See root `SECURITY.md`.
