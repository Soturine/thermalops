# Support Bundles, Preventive Reports, and Service Cases

## Goal

ThermalOps outputs should allow another support level or authorized service recipient to reason from evidence without forcing the field technician to manually transcribe the environment, while minimizing unnecessary customer data.

## Session identity

Every run has a random session/correlation ID. Ticket/customer/operator fields are optional metadata and are not security authority.

## Output classes

### Sanitized diagnostic report

Default human-readable/machine-readable summary. Redact/pseudonymize unnecessary username, hostname, IP, print-server, non-target queue, document/job name and identity-bearing path data.

### Preventive maintenance report

Contains:

- target and inspection time;
- policy/baseline/catalog versions;
- automatic checks;
- technician checklist results;
- maintenance due states;
- configuration drift;
- findings/recommendations;
- local actions, if any;
- service disposition;
- next inspection only if source-backed.

Automatic evidence and technician-entered observations are clearly separated.

### Full technical bundle

Explicit operator action only.

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
└── manifest.json
```

Missing/blocked/unsupported sections are represented in the manifest rather than silently absent.

### Service-case / escalation package

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

Intended for N2/N3 or an authorized support/repair/vendor workflow. It is not automatically uploaded.

## Manifest

Candidate fields:

```json
{
  "schemaVersion": "1.0",
  "sessionId": "...",
  "caseId": "...",
  "thermalOpsVersion": "...",
  "commitSha": "...",
  "buildId": "...",
  "createdUtc": "...",
  "privacyLevel": "sanitized",
  "policyVersion": "...",
  "baselineVersion": "...",
  "files": [
    {"path": "summary.json", "sha256": "...", "schemaVersion": "1.0"}
  ]
}
```

## Timeline/action history

Record intent separately from execution and validation:

```text
Observed
Recommended
Requested
Confirmed
Executed
Verified / Partial / Failed
Recovery outcome
Disposition
```

Never equate command return success with verified repair success.

## Attachments

Future manual attachments/photos:

- explicitly selected;
- never auto-captured;
- size/type bounded;
- treated as untrusted content;
- metadata stripped when policy requires;
- excluded from sanitized export unless selected;
- never executed.

## Storage

Stage under:

```text
%TEMP%\ThermalOps\Sessions\<session-id>
```

No automatic USB/executable-directory save.

## Export privacy levels

### Sanitized — default

Minimize identities while preserving diagnostic correlation.

### Full technical — explicit

May include additional device/environment identifiers needed for authorized support. Still exclude secrets and unrelated document content.

### Vendor/service case — explicit

May require model/serial/firmware/problem classification depending on authorized workflow. The UI must show what will be included before export.

## Encryption

No home-grown encryption. If required, select a standard enterprise-appropriate format/key-distribution model through ADR.

## Schemas

All machine-readable outputs use versioned schemas for validation, redaction tests, backwards compatibility, analytics and future knowledge/AI processing.
