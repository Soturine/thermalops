# Preventive Maintenance

Preventive maintenance is a first-class ThermalOps capability. The goal is not to wait for a printer to fail and then guess; it is to collect evidence, guide an authorized inspection, detect drift or recurring warning signs, and produce a defensible recommendation before an avoidable interruption occurs.

ThermalOps must not pretend that software can see every physical condition, and it must not invent maintenance intervals, component lifetimes, or replacement thresholds.

## Position in the product

```text
                         THERMALOPS
                              |
      +-----------------------+-----------------------+
      |                       |                       |
      v                       v                       v
  DIAGNOSIS             PREVENTIVE              LOCAL REMEDIATION
                        MAINTENANCE
      |                       |                       |
      +-----------------------+-----------------------+
                              |
                              v
                     SUPPORT / EVIDENCE
                              |
                  +-----------+-----------+
                  v                       v
              PORTABLE                ENTERPRISE
```

The three disciplines answer different questions:

- **diagnosis:** what is happening now?
- **preventive maintenance:** what should be inspected, cleaned, compared, monitored, or scheduled before it becomes a failure?
- **local remediation:** what narrow, authorized action can safely be performed now?

Predictive maintenance is a later and separate maturity level. It must not be marketed as available merely because historical data exists.

## Preventive inspection workflow

The normal workflow is observation-first and primarily read-only:

```text
Identify target
  -> Collect automatic evidence
  -> Load applicable maintenance policy/baseline
  -> Guide technician inspection
  -> Compare current state vs baseline/history
  -> Derive maintenance findings
  -> Determine service disposition
  -> Generate preventive report
  -> Optional authorized follow-up action
```

The inspection must remain useful in Portable Lite without administrator rights.

## Automatic evidence

Where supported and authorized, a preventive inspection may collect:

### Windows

- Print Spooler state and relevant configuration;
- selected print queue state;
- print jobs and repeated/stale-job evidence;
- driver identity/version/package evidence;
- port and transport evidence;
- PnP/USB evidence;
- relevant Windows Event Log entries;
- access-denied and unavailable-data outcomes.

### Transport

- USB/PnP presence where applicable;
- configured endpoint;
- narrowly scoped TCP reachability when policy allows it;
- timeouts and repeated connection failures;
- protocol/channel evidence;
- TLS/certificate evidence only where supported and explicitly designed.

### Device-native

Capabilities differ by model, firmware, print language, connection type, and vendor. The adapter must ask what is supported instead of assuming every device exposes the same data.

Possible Zebra evidence includes:

- responding / communication result;
- ready-to-print state;
- printhead open/closed;
- media state;
- ribbon state where applicable;
- pause state;
- printhead thermal warning state;
- receive-buffer/state conditions;
- firmware / Link-OS information;
- counters or odometer values where supported;
- selected safe, read-only settings;
- device system errors/warnings.

Windows queue state and physical-printer state are separate evidence sources.

## Technician-verified inspection

Software cannot reliably determine visual wear, cleanliness, physical damage, abnormal noise, cable condition, or all media-path problems. ThermalOps therefore models technician observations separately from automatic evidence.

A checklist may contain tasks such as:

```text
Physical inspection
[ ] External condition inspected
[ ] Power/data connections inspected
[ ] Media path inspected/cleaned as applicable
[ ] Sensors inspected/cleaned as applicable
[ ] Printhead condition/cleanliness inspected
[ ] Platen roller inspected
[ ] Ribbon/media installation checked
[ ] Unusual mechanical noise checked
[ ] Diagnostic label inspected, if allowed
[ ] Visible damage recorded
```

These are generic categories, not permission to disassemble equipment.

A checklist task must carry:

- task ID;
- applicable device family/model/capability;
- source/reference;
- safety notes;
- whether it is automatic or technician-verified;
- whether it requires the device to be powered off;
- whether it is permitted by the active policy;
- result (`Pass`, `Observation`, `Fail`, `NotPerformed`, `NotApplicable`, `Blocked`);
- optional sanitized note/evidence reference.

Internal repair/disassembly instructions are out of scope unless a separately approved procedure explicitly authorizes them.

## Source-backed maintenance schedules

ThermalOps must never invent an interval such as “replace component X after N labels”. Maintenance timing can come only from an approved source, for example:

- manufacturer documentation for the exact model/family;
- an organization-approved maintenance plan;
- a service-contract policy;
- an approved site/application-specific procedure;
- a validated usage-based threshold.

Every schedule rule should preserve its source/version.

A maintenance task can be triggered by:

```text
Calendar interval
Usage counter threshold
Condition/event threshold
Configuration drift
Manual inspection result
Service-case follow-up
```

Suggested due states:

```text
Unknown
NotApplicable
NotDue
DueSoon
Due
Overdue
Blocked
```

Unknown data must not silently become “healthy” or “not due”.

## Zebra example: cleaning schedule is model-specific

The Zebra ZT411/ZT421 user guide explicitly treats routine preventive maintenance as important to normal operation and provides cleaning schedules for the printhead, platen, media/ribbon sensors, paths, cutter options, and other parts. For example, the published schedule ties some cleaning to each roll of media or ribbon and gives other periodic intervals.

This is precisely why ThermalOps should use a versioned `MaintenanceTaskCatalog` rather than a universal hard-coded schedule.

Manufacturer instructions also include safety/technique constraints. For example, cleaning methods differ for standard and linerless platen rollers, and Zebra warns against inappropriate solvents/lubrication for some parts. ThermalOps should cite the approved instruction rather than paraphrase a dangerous maintenance step into an unverified generic recipe.

## Baselines

A baseline represents an expected or approved state. It is evidence for comparison, not proof that a different configuration is wrong.

Possible baseline sources:

- explicitly approved configuration profile;
- a known-good device of the same applicable class;
- a previous approved inspection snapshot;
- organization policy;
- vendor-recommended secure/configuration profile.

A baseline must be scoped. Useful dimensions include:

- vendor/model/family;
- DPI;
- print mode/application;
- media/ribbon context if relevant;
- connection type;
- firmware range;
- site or policy profile;
- baseline schema version.

Do not compare unrelated device variants as if all settings should match.

### Configuration drift

Example:

```text
Approved baseline
Darkness: 15
Speed: 6

Current device
Darkness: 28
Speed: 12

Result
Configuration drift detected.
This does not by itself prove a hardware fault.
```

The UI must show:

- baseline value;
- current value;
- difference;
- evidence source;
- severity according to policy;
- recommended verification;
- whether the drift is acknowledged/approved.

## Portable baseline workflow

Portable must remain non-persistent by default. A technician may explicitly import/export a sanitized baseline or previous-inspection snapshot.

Example:

```text
ThermalOps-Baseline-v1.json
```

A future signed policy/baseline package may be preferable in controlled environments. Signature validation is required before an imported policy can grant trust; imported data must never expand executable capabilities beyond those compiled into the application.

## Health assessment

A health assessment is an explainable summary over evidence. It must not collapse uncertainty into a magic number.

Preferred primary presentation:

```text
Overall condition: ATTENTION RECOMMENDED

Device................. OK
Windows................ OK
Transport.............. Observation
Configuration.......... Drift detected
Maintenance............ Due soon
Evidence completeness.. 91%
```

An optional numeric score may exist only as a secondary view if every contribution is transparent and tested.

Example:

```text
Health score: 82/100

-5 repeated transport failures
-5 configuration drift
-4 thermal warnings
-4 maintenance task due
```

Rules for any score:

- deterministic and versioned;
- weights visible;
- unknown values do not become zero;
- not directly comparable across incompatible policy/model classes;
- never generated by an LLM;
- score is not a warranty or failure prediction;
- operator can inspect the underlying evidence.

## Maintenance findings

Preventive findings are separate from diagnostic facts and repair actions.

Examples:

- cleaning due according to approved schedule;
- configuration drift;
- repeated communication instability;
- recurring thermal warnings;
- preventive checklist incomplete;
- counter threshold reached;
- diagnostic-label quality observation;
- firmware differs from approved baseline;
- maintenance history missing/unknown.

A maintenance recommendation may be:

```text
Inspect
Clean according to approved procedure
Monitor
Schedule follow-up
Escalate for authorized assessment
No preventive action required
```

It must not silently perform the action.

## Service disposition

A preventive inspection may conclude with a policy-controlled `ServiceDisposition`.

Suggested normalized values:

- `ContinueInService`;
- `ContinueWithObservation`;
- `LocalRemediationAllowed`;
- `EscalateToAuthorizedService`;
- `RemoveFromService` — only when an explicit policy gives ThermalOps authority to recommend this state;
- `InsufficientEvidence`.

Disposition is a recommendation/decision layer, not a raw device status.

## Preventive report

A preventive report should separate automatic evidence from technician verification.

Example structure:

```text
PREVENTIVE MAINTENANCE REPORT

Target
Inspection date/session
Policy/baseline version

Automatic checks
- Windows
- Transport
- Device-native
- Firmware/counters
- Configuration

Technician inspection
- checklist and results

Findings
- evidence-backed observations

Maintenance due
- due/soon/overdue/unknown

Local actions
- none, or explicitly recorded action

Disposition
- continue / observe / remediate / escalate

Next inspection
- derived only from approved policy/source
```

## Diagnostic print quality check

A policy-permitted diagnostic label can help separate software/communication issues from physical print quality.

It may include:

- session ID;
- model/DPI;
- timestamp;
- barcode/QR samples;
- line-width samples;
- alignment markers;
- darkness/calibration patterns.

Printing is a write operation. It is disabled in `--readonly` and Customer Safe modes.

Technician observations such as `Good`, `Light`, `Dark`, `MissingLines`, `AlignmentProblem`, or `BarcodeUnreadable` are manual inspection data and must remain distinct from automatically measured evidence.

## Maintenance history

Enterprise can retain a policy-controlled history of:

- inspections;
- maintenance tasks performed;
- findings;
- acknowledgements;
- approved configuration changes;
- service dispositions;
- service cases;
- counters over time;
- recurring warnings/errors;
- next-due calculation inputs.

Portable does not create a hidden local history on the customer endpoint.

## Condition-based maintenance

Condition monitoring is the next maturity step after deterministic preventive maintenance.

Examples:

- rising communication-error frequency;
- repeated head-temperature warnings;
- increasing stalled-job recurrence;
- persistent configuration drift;
- repeated service cases;
- usage counters approaching an approved service threshold.

A trend is not a proven failure cause. The UI must say what was observed and what is inferred.

## Predictive maintenance

Predictive maintenance is deferred until ThermalOps has sufficient real, labeled, representative historical data and a validation strategy.

Do not ship claims such as:

```text
“Printhead will fail in 3 days.”
```

merely because an ML/AI model can produce a number.

Before predictive maintenance can be supported, require:

- a defined prediction target;
- representative historical dataset;
- labels/ground truth;
- train/validation/test separation;
- false-positive/false-negative cost analysis;
- calibration and confidence analysis;
- drift monitoring;
- device/model applicability matrix;
- human review and policy controls;
- explicit statement that prediction does not replace manufacturer guidance.

## Domain concepts

Planned domain concepts:

```text
MaintenanceInspection
MaintenanceTaskDefinition
MaintenanceTaskResult
MaintenanceFinding
MaintenanceRecommendation
MaintenancePolicy
MaintenanceBaseline
MaintenanceRecord
MaintenanceSchedule
MaintenanceDue
HealthAssessment
HealthContribution
ConditionTrend
TechnicianObservation
ServiceDisposition
```

These belong in the domain/application layers, not in the WPF UI or vendor adapter.

## Safety boundaries

Preventive mode must not:

- automatically change firmware;
- automatically install/remove drivers;
- automatically alter printer configuration;
- assume physical disassembly is authorized;
- invent manufacturer intervals;
- upload customer data automatically;
- broaden network discovery without permission;
- use AI output as maintenance authority.

The default sequence is:

```text
Observe -> Analyze -> Compare -> Recommend
```

not:

```text
Observe -> Automatically change everything
```
