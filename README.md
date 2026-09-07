# ThermalOps

ThermalOps is a Windows-first platform for **safe diagnosis, preventive maintenance, field triage, local remediation, support evidence, escalation assistance, and future fleet/condition monitoring of thermal printers**.

The first vendor adapter targets Zebra printers. The architecture is vendor-neutral so Honeywell, TSC, SATO, and other adapters can be added later without leaking vendor-specific rules into the core domain.

> Status: **M0 — product/architecture/security foundations.** The repository is not yet production-ready. No printer, repair, preventive, or fleet capability is considered validated until its milestone acceptance criteria and required tests are green.

## Product purpose

ThermalOps is not intended to replace label-design/printing platforms, vendor management suites, ERP/WMS systems, or authorized repair processes. It focuses on the operational gap around the printer lifecycle:

```text
BEFORE a failure
  -> preventive inspection / maintenance / baseline checks

DURING a problem
  -> diagnosis / triage / safe local remediation

WHEN field scope ends
  -> evidence / service case / escalation

AFTER an action
  -> validation / report / history

BETWEEN incidents (Enterprise)
  -> fleet visibility / condition trends / maintenance by exception
```

## Product pillars

```text
                         THERMALOPS
                              |
  +------------+--------------+--------------+-------------+
  |            |              |              |             |
  v            v              v              v             v
Diagnosis  Preventive     Local          Support       Observability
           Maintenance    Remediation    / Evidence    / Fleet
  |            |              |              |             |
  +------------+--------------+--------------+-------------+
                              |
                    Field Service / Escalation
```

The core question for field support is:

> What is the state of this printer, what can be safely handled here under policy, and what should be escalated?

## Product family

| Edition | Primary use | Persistence | Write operations |
| --- | --- | --- | --- |
| **Portable Lite** | N1/field diagnosis + preventive inspection + reporting | None | No — structurally read-only |
| **Portable Pro** | N2/N3 field support + controlled local remediation + service cases | None | Explicit allowlisted operations only |
| **Enterprise** | Fleet, history, condition monitoring, policies, preventive schedules | Managed | Policy/RBAC controlled |

Portable is a first-class product. A technician should be able to run an approved signed package, diagnose/inspect an authorized endpoint without installation, export only the intended evidence, close the session, and leave no intentional persistent component behind.

## Core engineering principles

- **Read-only by default.** Diagnosis and preventive inspection should work without administrator rights whenever Windows/device APIs allow it.
- **Least privilege.** The UI does not stay elevated. A temporary helper is used only for an approved privileged action.
- **Field scope is explicit.** ThermalOps does not assume the operator can disassemble or repair internal printer hardware.
- **Offline-first.** Core diagnosis, preventive inspection, report generation, and approved local remediation do not require cloud, login, internet, telemetry, or AI.
- **Evidence before conclusion.** Windows, transport, vendor-native and technician observations remain traceable and separately attributable.
- **Deterministic authority.** AI may explain evidence but never authorizes or executes repair, maintenance, escalation, or policy decisions.
- **Maintenance is sourced.** No invented service intervals, component lifetimes, or replacement thresholds.
- **Targeted remediation first.** Never perform broad spool cleanup when a specific queue/job action is available.
- **Repair discipline.** `Preflight -> Snapshot -> Execute -> Verify -> Recovery -> Post-condition`.
- **Privacy by design.** Session-local processing; sanitized export by default; full technical export is explicit.
- **No arbitrary privileged shell.** No generic PowerShell/cmd/execute endpoint.
- **Portable purity.** No hidden service, scheduled task, startup entry, daemon, or automatic USB logging.
- **Production delivery matters.** Signing, SHA-256, SBOM, build identity, CI gates, tests, hardware validation and known-limitations documentation are product requirements.

## What ThermalOps can eventually observe

### Windows print path

- Print Spooler state/configuration;
- installed printers and target queue;
- print jobs and stale/blocked jobs;
- drivers/packages;
- ports/print processors;
- USB/PnP evidence;
- print-related Windows events;
- access denied/timeouts as first-class evidence.

### Transport

- USB/DOT4;
- TCP/IP RAW;
- TLS-capable printer channel where supported;
- LPR;
- Windows shared printer;
- Bluetooth;
- serial/parallel;
- known-endpoint reachability under policy.

### Vendor-native

For Zebra, use supported Link-OS / SGD / ZPL mechanisms where appropriate and validated. Potential evidence includes readiness, head/media/ribbon states, pause, temperature warnings, firmware, counters/odometer, selected read-only configuration and device-reported warnings/errors.

Windows queue status is not equivalent to physical printer health.

## Preventive maintenance

Preventive maintenance is a first-class module, not a side effect of diagnostics.

A preventive inspection combines:

```text
Automatic evidence
+ approved manufacturer/organization maintenance policy
+ applicable baseline
+ technician-verified physical checklist
+ history/counters when available
= explainable maintenance findings + disposition
```

It can detect/report:

- maintenance due/soon/overdue/unknown;
- configuration drift;
- recurring communication or print-path issues;
- recurring device warnings;
- usage/counter thresholds from approved policy;
- missing/incomplete preventive checks;
- technician observations such as print-quality issues.

The software does **not** invent intervals and does not treat a numeric health score as magic truth. See [`docs/PREVENTIVE_MAINTENANCE.md`](docs/PREVENTIVE_MAINTENANCE.md).

## Field service and escalation

ThermalOps distinguishes:

- local field-resolvable issues;
- findings that require deeper technical assessment;
- cases that should be escalated to an authorized service/vendor process.

The exact rules are policy-driven. The public core does not hard-code any employer/customer workflow or assume who opens an RMA, removes equipment, or contacts a vendor.

A future `ServiceCase` can package model/serial (when authorized), firmware, device status, configuration, counters, Windows evidence, events, technician observations, preventive checklist, actions attempted, disposition and attachments into a structured support package.

See [`docs/FIELD_SERVICE_AND_ESCALATION.md`](docs/FIELD_SERVICE_AND_ESCALATION.md).

## Portable workflow

```text
Approved USB / local copy
        |
        v
ThermalOps.exe
        |
        +--> Quick Diagnosis
        +--> Preventive Inspection
        +--> Advanced Diagnostics
        +--> Analyze Failure
        +--> Collect Evidence
        +--> Prepare Escalation
        |
        +--> explicit local remediation --UAC--> temporary helper
        |
        +--> validate before/after
        +--> sanitized report / full bundle / service case
        +--> cleanup / no persistence
```

Portable goals:

- self-contained .NET publish;
- no preinstalled runtime required;
- no installer;
- no reboot;
- no account;
- no required internet;
- normal UX does not require CLI;
- session staging under `%TEMP%`, not removable media;
- `--readonly` hard guardrail;
- Customer Safe profile;
- production Authenticode signing when a signing identity exists.

See [`docs/PORTABLE.md`](docs/PORTABLE.md) and [`docs/DEPLOYMENT_AND_LIFECYCLE.md`](docs/DEPLOYMENT_AND_LIFECYCLE.md).

## Local remediation model

`Repair` in ThermalOps means **local, policy-authorized remediation**, not bench repair or internal hardware service.

Examples of planned local remediation:

1. cancel one selected stale job;
2. controlled Print Spooler restart preserving original/policy state;
3. selected queue remediation using approved strategies;
4. diagnostic print when explicitly allowed.

A global spool reset is a separate break-glass action and must clearly state that unrelated queues/jobs may be affected.

## Service disposition

A field/preventive session may produce:

```text
ContinueInService
ContinueWithObservation
LocalRemediationAllowed
EscalateToAuthorizedService
RemoveFromService        # only if policy grants this authority
InsufficientEvidence
```

Disposition is a policy/conclusion layer, not raw device state.

## Support outputs

Planned outputs include:

- sanitized diagnostic report;
- full technical support bundle;
- preventive maintenance report;
- before/after report;
- configuration/baseline diff;
- service-case / escalation package;
- hash manifest and versioned schemas.

See [`docs/SUPPORT_BUNDLE.md`](docs/SUPPORT_BUNDLE.md).

## Enterprise / fleet direction

Enterprise may add:

- managed inventory;
- maintenance schedule/history;
- condition trends;
- configuration drift;
- recurring-failure analysis;
- proactive explainable alerts;
- maintenance by exception;
- service cases/history;
- policy/baseline management;
- RBAC/audit/retention;
- optional managed collector/agent after ADR review.

Portable never depends on Enterprise to perform core field work.

See [`docs/FLEET_AND_CONDITION_MONITORING.md`](docs/FLEET_AND_CONDITION_MONITORING.md).

## Technology direction

- **C# / .NET 10 LTS** baseline;
- **WPF** first Windows UI;
- modular monolith;
- Domain/Application isolated from Windows/vendor/UI details;
- Windows adapters around supported APIs;
- vendor adapters, Zebra first;
- temporary privileged helper with strict IPC;
- self-contained Windows portable publishing.

## Repository documentation

```text
docs/
├── PRODUCT.md
├── ARCHITECTURE.md
├── PORTABLE.md
├── DEPLOYMENT_AND_LIFECYCLE.md
├── PREVENTIVE_MAINTENANCE.md
├── FIELD_SERVICE_AND_ESCALATION.md
├── FLEET_AND_CONDITION_MONITORING.md
├── DIAGNOSTICS_AND_REPAIR.md
├── SUPPORT_BUNDLE.md
├── SECURITY_AND_PRIVACY.md
├── TESTING.md
├── RELEASE_ENGINEERING.md
├── AI.md
├── RESEARCH.md
├── ROADMAP.md
└── adr/
```

## Roadmap

| Milestone | Outcome |
| --- | --- |
| **M0** | Constitution, threat model, field/preventive scope, ADRs, CI, license decision |
| **M1** | Read-only Windows diagnosis foundation |
| **M2** | Safe local remediation + privileged helper |
| **M3** | Zebra native adapter / capability-aware status and read-only config |
| **M4** | Support + preventive suite / service cases / snapshots / diagnostic label |
| **M5** | Enterprise hardening / signing / packaging / deployment lifecycle |
| **M6** | Fleet + condition monitoring / maintenance by exception |
| **M7** | Additional vendor adapters based on real demand/hardware |
| **M8** | Optional knowledge/AI explanation with evidence citations |
| **M9** | Predictive-maintenance research only after sufficient validated data |

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Public research references

Product direction is informed by official/public material including Zebra Link-OS and ZT411/ZT421 maintenance documentation, Zebra support/repair flows, Zebra Printer Profile Manager Enterprise, SOTI Connect, and TSC Console/Web. These references validate patterns such as vendor-aware maintenance schedules, centralized fleet visibility, proactive alerts, protocol adapters, configuration profiles, support-case workflows and preventive-maintenance tooling.

ThermalOps uses those patterns as research input and does not copy proprietary implementation or claim vendor certification/partnership.

See [`docs/RESEARCH.md`](docs/RESEARCH.md).

## Safety and authorization

ThermalOps is for systems and printers the operator is authorized to support. Customer security policy and approved service scope take precedence. The tool must cooperate with EDR, Defender, WDAC, AppLocker, removable-media controls and application allowlisting rather than bypass them.

## License

A project license has not yet been selected. Do not copy third-party implementation code into this repository until license compatibility and attribution requirements are reviewed. License selection remains an M0 governance task.
