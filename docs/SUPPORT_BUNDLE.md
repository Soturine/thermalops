# Support Bundle and Session Reporting

## Goals

Support output should let N2/N3 reason from evidence without requiring the field technician to manually transcribe the environment, while minimizing unnecessary customer data.

## Session ID

Every run gets a random session/correlation ID. Optional ticket reference is metadata, not identity/security authority.

## Default sanitized report

Human-readable summary plus machine-readable JSON where useful.

Sanitize by default:

- username;
- hostname;
- IP addresses unless essential to the selected endpoint diagnosis;
- print server names;
- non-target printer queues;
- document/job names;
- local paths containing identities.

Use stable per-bundle pseudonyms when correlation is needed, e.g. `HOST-01`, `PRINTSERVER-01`, `IP-01`.

## Full technical bundle

Explicit operator action only.

Planned archive:

```text
ThermalOps-SupportBundle-<session>.zip
├── summary.json
├── printers.json
├── drivers.json
├── jobs.json
├── windows-events.json
├── device-status.json
├── device-config.json
├── network.json
├── diagnostic.log
├── repair-history.json
└── manifest.json
```

Not every file is present if the collection was disabled/unavailable. The manifest records missing sections and reasons.

## Manifest

Example fields:

```json
{
  "schemaVersion": "1.0",
  "sessionId": "...",
  "thermalOpsVersion": "0.1.0",
  "commitSha": "...",
  "buildId": "...",
  "createdUtc": "...",
  "privacyLevel": "sanitized",
  "files": [
    {"path": "summary.json", "sha256": "...", "schemaVersion": "1.0"}
  ]
}
```

## Repair history

Must record intent and validation separately:

```text
Requested -> Confirmed -> Executed -> Verified/Partial/Failed -> Recovery outcome
```

Do not report a repair as successful solely from command return status.

## Storage behavior

Stage in:

```text
%TEMP%\ThermalOps\Sessions\<session-id>
```

Do not automatically save to the executable directory or removable media.

## Encryption

Do not invent home-grown encryption. If encrypted support bundles become necessary, create an ADR selecting a standard format/key-distribution model appropriate to enterprise support. Sanitization and approved secure transfer are the early default.

## Schemas

JSON documents should use versioned schemas once implementation begins. Structured schemas allow:

- backward-compatible support tooling;
- deterministic validation;
- safe redaction tests;
- future local analytics/AI without parsing free text.
