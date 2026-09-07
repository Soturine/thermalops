# Test Strategy

ThermalOps combines domain rules, Windows integration, vendor protocols, preventive maintenance, technician-entered observations, privileged execution, support exports and future fleet services. Test depth follows risk.

## Domain tests

Cover:

- status flag normalization;
- connection classification;
- evidence vs finding separation;
- diagnostic rules;
- MaintenanceDue calculations;
- maintenance task applicability/source/versioning;
- baseline scope and drift;
- HealthAssessment contributions and unknown handling;
- ServiceDisposition policy rules;
- RepairPlan preconditions/impact;
- policy capability reduction;
- redaction/pseudonymization;
- snapshot diff;
- status terminology.

## Application tests

Cover orchestration:

- evidence collection cancellation/timeouts;
- diagnosis/inspection sequencing;
- preventive workflow with blocked/unsupported tasks;
- technician observation attribution;
- baseline import validation;
- service-case generation;
- repair lifecycle;
- no write path in read-only mode;
- AI outage does not block deterministic workflows.

## Windows integration

On controlled Windows runners/VMs:

- WinSpool enumeration;
- jobs on test queues;
- SCM reads;
- Event Log reads;
- PnP reads;
- access denied;
- helper IPC security boundary.

Destructive Spooler tests run only on dedicated environments.

## Vendor adapter contract tests

Fixtures/parsers for:

- valid/multiple flags;
- unsupported fields/capabilities;
- unknown firmware;
- malformed/truncated/oversized reply;
- timeout/disconnect;
- encoding issues;
- counter/config value boundaries.

## Hardware-in-the-loop

Required before claiming model/capability support. Record model, DPI, firmware, connection, driver, adapter version, capabilities tested and test date.

A feature remains `experimental`/`not validated` until required physical validation exists.

## Preventive maintenance tests

Mandatory cases:

- manufacturer task applies vs does not apply;
- model/firmware/media applicability unknown;
- due/soon/due/overdue boundaries;
- no invented due date when source data missing;
- baseline compatible vs incompatible;
- configuration drift acknowledged vs unacknowledged;
- technician checklist incomplete;
- automatic evidence never impersonates technician observation;
- numeric health score (if implemented) explains every contribution;
- unknown evidence does not become healthy;
- predictive claim path remains unavailable before M9 criteria.

## Service-case tests

- sanitized vs full export;
- identity-bearing fields redacted correctly;
- missing/unsupported data represented in manifest;
- attachments opt-in only;
- path traversal/archive safety;
- hash manifest consistency;
- timeline separates request/execution/verification;
- ServiceDisposition requires policy authority for `RemoveFromService`.

## Security tests

Privileged helper:

- unauthorized caller;
- wrong nonce/token;
- unsupported protocol/action;
- oversized request;
- target tampering;
- replay;
- helper crash;
- UAC denied;
- timeout;
- UI exits mid-operation.

Portable:

- no persistence after clean exit;
- cleanup-failure reporting;
- no USB/executable-directory log by default;
- read-only cannot reach write methods;
- imported baseline/policy cannot add executable capability.

## Failure injection

Include Spooler stop/start failures, external state changes, job disappearing, access denied, device disconnect, malformed device data, network timeout, export write failure, disk full, file lock, helper crash, corrupted baseline and migration failure in Enterprise when implemented.

## E2E scenarios

1. Quick Diagnosis with no printers.
2. Quick Diagnosis with controlled Windows queue.
3. Portable Lite full read-only session and cleanup.
4. Preventive inspection with synthetic policy/baseline and technician checklist.
5. Sanitized preventive report.
6. Service-case generation with redaction.
7. Selected-job cancellation on dedicated machine.
8. Controlled Spooler restart with recovery validation.
9. Zebra native status with real test printer.
10. Portable baseline import/compare/export without hidden persistence.
11. Enterprise install/upgrade/uninstall when M5 exists.

## Definition of validated

- Windows feature -> Windows integration test;
- privileged write -> failure/security tests;
- Zebra/native claim -> compatible real hardware;
- preventive schedule claim -> source/applicability tests;
- Portable claim -> no-persistence E2E;
- Enterprise lifecycle claim -> install/upgrade/uninstall tests;
- predictive claim -> M9 validation program.

## Performance/UX budgets

Measure startup, first-diagnosis latency, device timeouts, UI responsiveness, preventive inspection duration, support bundle size, memory and fleet polling/alert throughput when relevant.

Do not advertise targets until measured and do not trade safety for benchmark appearance.
