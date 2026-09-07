# Security and Privacy

## Security objectives

1. A read-only diagnosis cannot accidentally become a write.
2. A compromised/untrusted UI input cannot turn the privileged helper into arbitrary code execution.
3. A repair affects only the declared target/scope unless a clearly marked break-glass plan is confirmed.
4. Portable execution leaves no intentional persistence.
5. Customer information is not uploaded or exported silently.
6. Release artifacts are identifiable, auditable, and signable.
7. Failure should prefer a recoverable/known state over blind continuation.

## Trust boundaries

```text
Operator
   |
   v
Desktop UI (standard user)
   |
   v
Application/Domain
   |                    \
   v                     v
Windows/device reads   Vendor/device reads
   |
   | only when repair authorized
   v
IPC trust boundary
   v
Privileged Helper
   v
Windows privileged operations
```

Enterprise networking/cloud introduces additional boundaries and requires separate threat-model updates.

## Threats to design against

### Privilege escalation abuse

Threat: helper accepts attacker-controlled arbitrary commands.

Controls:

- no generic command execution;
- strongly typed messages;
- capability allowlist;
- IPC ACL restricted to intended local principal/session;
- caller/session validation;
- short-lived nonce/token;
- protocol version;
- bounded input sizes;
- canonical resource identifiers;
- no path supplied for operations that should derive safe paths internally.

### Confused deputy

Threat: a standard-user process tricks the elevated helper into modifying another queue/resource.

Controls:

- helper revalidates target identity and policy;
- request includes plan/session identity;
- helper does not trust UI-provided display names as resource identity;
- high-impact/global operations require stronger confirmation flow and capability.

### Queue overreach

Threat: clearing one printer removes jobs from unrelated printers.

Controls:

- selected-job cancellation through WinSpool first;
- queue-scoped operations where supported;
- global spool reset is a distinct break-glass action;
- explicit impact display listing affected scope;
- pre/post snapshots.

### Service-state corruption

Threat: repair leaves Print Spooler stopped or violates customer service policy.

Controls:

- record initial state/startup behavior;
- bounded stop/start waits;
- post-condition validation;
- recovery path;
- do not force `Running` when original/policy state requires otherwise;
- report partial recovery honestly.

### Customer-data leakage

Threat: portable logs remain on USB or are exported to a ticket without redaction.

Controls:

- `%TEMP%` session staging;
- sanitized report default;
- explicit full-bundle export;
- redaction pipeline;
- no telemetry/upload by default;
- cleanup validation.

### Malicious/malformed device responses

Threat: printer/network response causes parser crash, excessive allocation, or injection into logs/UI.

Controls:

- bounded reads/timeouts;
- strict parsers;
- encoding handling;
- output escaping;
- size limits;
- treat device data as untrusted;
- never convert device text into executable commands.

### Network scanning risk

Threat: tool triggers unauthorized broad discovery.

Controls:

- local evidence first;
- explicit operator/policy permission for discovery beyond known endpoints;
- bounded subnet/range if future discovery exists;
- no automatic scan in Customer Safe;
- audit discovery initiation.

## Privileged operation allowlist

Initial candidates, each requiring milestone implementation and tests:

```text
CancelPrintJob(queue-id, job-id)
RestartPrintSpooler(expected-initial-state)
RepairSelectedQueue(queue-id, strategy-id)
```

Not allowed:

```text
ExecuteCommand(string)
RunPowerShell(string)
RunCmd(string)
DeletePath(string)
WriteRegistry(path, value)
StartArbitraryService(name)
InstallArbitraryDriver(path)
```

A future privileged capability is a source-code/API change, not data-driven arbitrary execution.

## Temporary files

- generate unpredictable session directory names;
- use OS-provided temporary base;
- restrictive ACLs for sensitive staging where practical;
- avoid following untrusted reparse points/symlinks for privileged file operations;
- helper derives privileged paths internally;
- validate ownership/location before delete;
- cleanup only ThermalOps-owned session resources.

## Logging

Structured local events should support redaction and avoid secrets.

Do not log by default:

- credentials/tokens;
- full raw network payloads unless explicitly required and safe;
- document content;
- arbitrary spool file contents;
- full environment variables;
- unnecessary serial/user/hostname identifiers.

## Support-bundle privacy levels

### Sanitized (default)

Redact or pseudonymize:

- username;
- hostname;
- IP addresses where not essential;
- print server names;
- non-target printers;
- document/job names if not required;
- file paths containing user identity.

### Full technical (explicit)

May contain additional identifiers. UI must explain this and record that full export was chosen. Still exclude secrets and unrelated document content.

## AI/privacy

No customer evidence is sent to any external AI provider by default. If a future organization enables cloud AI:

- opt-in policy;
- explicit data classification;
- redaction before transmission;
- provider/retention agreement review;
- no privileged action authority;
- citations/evidence shown to the operator.

Offline/local documentation retrieval is preferred where feasible and licensing permits.

## Supply chain

Release gates should grow to include:

- dependency review;
- secret scanning;
- CodeQL/static analysis;
- SBOM generation;
- known-vulnerability scanning;
- license inventory;
- signed release artifacts;
- checksums;
- provenance/attestation where feasible.

Pin or otherwise govern CI actions/dependencies according to project policy. Avoid unreviewed installer scripts.

## Code signing

Production portable artifacts should use Authenticode when a signing identity is available. Signing is not a substitute for secure code, but it supports enterprise publisher verification/allowlisting and tamper detection.

## Secure updates

Do not implement automatic update until there is a dedicated design for:

- signed update manifests;
- channel policy;
- rollback;
- downgrade rules;
- proxy/offline environments;
- enterprise deferral;
- signature verification before execution.

Portable manual updates are safer for early releases.

## Vulnerability reporting

See root `SECURITY.md`. Until a private reporting channel is configured, do not request that reporters publish sensitive exploit details in a public issue.
