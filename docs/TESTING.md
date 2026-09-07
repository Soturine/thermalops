# Test Strategy

ThermalOps combines domain logic, Windows integration, privileged execution, networking, and physical printers. Testing must match those risks.

## Layers

### Domain unit tests

High volume and fast.

Cover:

- status-flag normalization;
- connection classification from structured evidence;
- finding rules;
- severity/impact;
- repair-plan preconditions;
- policy capability reduction;
- redaction;
- snapshot diff;
- status terminology (`validated`, `partial`, etc.).

### Application tests

Cover orchestration with controlled adapters:

- evidence collection order/parallelism;
- cancellation/timeouts;
- finding aggregation;
- repair-plan lifecycle;
- support-bundle generation;
- no write path in read-only mode;
- AI failure does not block deterministic results.

### Windows integration tests

Run on Windows runners/VMs where safe.

Cover:

- WinSpool enumeration;
- job enumeration on controlled test queues;
- SCM read behavior;
- Event Log query;
- PnP read APIs;
- access-denied behavior;
- helper IPC without granting arbitrary capability.

Destructive spooler tests should use dedicated CI/test machines, not shared general runners.

### Vendor adapter contract tests

Fixtures and parser tests for:

- valid responses;
- multiple simultaneous flags;
- unknown firmware fields;
- malformed/truncated response;
- oversized response;
- timeout/disconnect;
- unsupported capability.

### Hardware-in-the-loop

Required before claiming supported real-device behavior.

Initial matrix should prioritize devices physically available to the project. Record:

- model;
- DPI;
- firmware;
- connection type;
- driver;
- adapter version;
- tested capabilities.

A feature can be `experimental` until hardware validation exists.

### Security tests

Privileged helper:

- unauthorized caller;
- wrong session token/nonce;
- unsupported protocol version;
- unknown action;
- oversized message;
- path/resource tampering;
- replay attempt;
- helper crash;
- UAC denied;
- timeout;
- UI terminates mid-operation.

Portable:

- no persistence after clean exit;
- cleanup failure reporting;
- no log written beside executable by default;
- read-only mode cannot reach write methods.

### Failure injection

Mandatory cases for repair logic:

- spooler already stopped;
- spooler cannot stop;
- spooler stops but cannot start;
- service changes state externally mid-plan;
- job disappears between plan and execution;
- access denied;
- selected printer disconnects;
- device returns stale/malformed data;
- network timeout;
- support-bundle write fails;
- disk full;
- cleanup file locked;
- helper exits unexpectedly.

## E2E scenarios

Keep a small meaningful set:

1. Quick Diagnosis read-only with no printers.
2. Quick Diagnosis with one controlled Windows print queue.
3. Portable read-only complete session and cleanup.
4. Selected-job cancellation on dedicated test environment.
5. Controlled spooler restart with before/after validation on dedicated environment.
6. Zebra native status with real test printer when available.
7. Sanitized support-bundle export and redaction assertions.

## Definition of validated

A feature is not `validated` merely because unit tests pass.

Examples:

- Windows integration feature: needs Windows integration test.
- privileged repair: needs negative/security path coverage.
- Zebra hardware status: needs compatible real-hardware validation for the claimed model/capability set.
- portable cleanup: needs before/after persistence checks.

## Performance

Measure rather than guess. Useful budgets may include:

- app startup;
- Quick Diagnosis completion without network/vendor timeout;
- bounded per-device timeout;
- UI responsiveness during collection;
- support-bundle size;
- memory usage on typical enterprise endpoints.

Never trade safety for a superficial benchmark.
