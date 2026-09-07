# Field Service, Triage, and Escalation

ThermalOps is designed for technicians and support analysts who may diagnose, inspect, perform preventive maintenance, execute limited authorized software-side remediation, and escalate a device when the issue is outside field scope.

The product must **not** assume that a field technician is authorized to open the printer, replace internal hardware, flash firmware, or perform bench repair.

## Core question

ThermalOps should help answer:

> What is the state of this printer, what can be safely handled here under policy, and what should be escalated?

This keeps the tool useful even when the real service process differs by organization, contract, site, vendor, or device family.

## Generic field workflow

```text
Start authorized session
  -> Identify device / queue / connection
  -> Preventive or corrective inspection
  -> Collect Windows + transport + device-native evidence
  -> Classify findings
  -> Check policy and field scope
  -> Local low-risk remediation if authorized
  -> Re-validate
  -> Continue in service / observe / escalate
  -> Generate report or service-case package
```

This is a generic model, not a claim about any particular company process.

## Work categories

ThermalOps separates at least these categories:

### Field-resolvable / local remediation

Examples may include, when policy allows:

- canceling one selected blocked print job;
- controlled Print Spooler restart;
- correcting an explicitly approved software/queue association;
- unpausing a queue/device through an approved workflow;
- guiding media/ribbon checks;
- running an approved diagnostic label;
- re-running deterministic validation.

The actual capability list is policy-controlled.

### Requires technical assessment

Examples of findings that may justify a deeper technical assessment:

- recurring print-quality degradation;
- repeated hardware-reported warnings;
- possible sensor/mechanical problem;
- abnormal temperature condition;
- recurring transport failures with Windows otherwise healthy;
- firmware/configuration anomaly outside field policy.

ThermalOps should describe evidence and recommend escalation rather than invent an internal repair procedure.

### Vendor / authorized-service escalation

Potential triggers include:

- suspected internal hardware fault;
- device cannot initialize/respond after allowed checks;
- persistent device fault after permitted field workflow;
- action would require disassembly or parts replacement;
- warranty/service-contract process should take over;
- firmware or component procedure is outside local authorization.

Rules that map a finding to escalation must come from an approved service policy or explicit operator decision. Do not hard-code assumptions about who opens an RMA, who removes the printer, or who contacts the manufacturer.

## ServiceDisposition

Normalize the outcome of a field session separately from device status:

```text
ContinueInService
ContinueWithObservation
LocalRemediationAllowed
EscalateToAuthorizedService
RemoveFromService
InsufficientEvidence
```

`RemoveFromService` must only be available when an explicit policy grants authority for that recommendation.

A disposition records:

- policy version;
- findings/evidence references;
- operator decision where applicable;
- timestamp;
- optional follow-up/due date;
- reason;
- whether it was automatically recommended or manually selected.

## Technician observations

Manual observations are first-class evidence but must be clearly marked as human-entered.

Examples:

```text
Automatic evidence
- device Ready=false
- Windows queue healthy
- transport reachable

Technician observation
- visible physical damage: none
- abnormal noise: yes
- diagnostic print: missing vertical lines
```

Never merge these into a single untraceable status.

## Service case

A `ServiceCase` packages the field session for N2/N3, an authorized repair center, or a vendor support workflow.

Suggested data model:

```text
ServiceCase
  caseId
  sessionId
  targetDevice
  caseType
  problemSummary
  evidenceIds[]
  findings[]
  technicianObservations[]
  actionsAttempted[]
  actionResults[]
  preventiveInspectionRef?
  disposition
  policyVersion
  attachments[]
  privacyLevel
  createdAt
```

## Escalation package

A future export may contain:

```text
ThermalOps-ServiceCase-<id>.zip
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

Not every file is mandatory. The manifest states what was collected, skipped, blocked, unsupported, or redacted.

## Vendor-support compatibility

Zebra's public support flow exposes separate technical-support and repair-request paths, and its repair resources may use device serial numbers, warranty/service state, problem categories, and RMA workflows. ThermalOps should therefore make these data available **when authorized**, but it should not automatically submit a case or RMA until a dedicated integration and privacy/security review exists.

Initial direction:

```text
ThermalOps
  -> produce a clean, structured case package
  -> operator follows the approved support/repair process
```

Possible future integration:

```text
ThermalOps
  -> approved connector
  -> vendor/service portal API or workflow
```

Only implement direct integration when an official supported interface and authorization model are available.

## Photos and attachments

A future service case may allow manually selected photos or files. Guardrails:

- never capture screen/camera automatically;
- operator explicitly selects attachment;
- show privacy warning;
- strip metadata where policy requires;
- scan/validate file type and size;
- never execute attachments;
- sanitized export excludes attachments unless selected.

## Field workflow UX

A technician-oriented home screen can expose:

```text
[ Quick Diagnosis ]
[ Preventive Inspection ]
[ Analyze Failure ]
[ Collect Evidence ]
[ Prepare Escalation ]
[ Technical Report ]
```

The UI must prioritize evidence and disposition over a large generic “Repair” button.

## Unknown real-world process

The repository intentionally does not encode unverified internal workflow such as:

- which support level can perform a given hardware action;
- who physically removes a printer;
- who opens an internal ticket;
- whether a vendor RMA is required;
- who contacts Zebra or another OEM;
- contract-specific SLA/entitlement rules.

When a real organization provides these rules, map them into generic `FieldServicePolicy`, `EscalationPolicy`, `ServiceDispositionRule`, and report templates. Keep confidential/customer-specific policy outside the public core.
