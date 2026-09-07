# ThermalOps

ThermalOps is a Windows-first toolkit for **safe diagnosis, support, remediation, and observability of thermal printers**.

The first device adapter targets Zebra printers. The architecture is intentionally vendor-neutral so Honeywell, TSC, and other thermal-printer adapters can be added later without contaminating the core domain.

> Project status: **M0 — architecture, safety model, product specification, and engineering foundations.** No production repair feature should be considered ready until its milestone acceptance criteria and tests are green.

## Product family

| Edition | Primary use | Persistence | Write operations |
| --- | --- | --- | --- |
| **Portable Lite** | Field/N1 diagnosis | None | No — read-only |
| **Portable Pro** | N2/N3 field support | None | Yes, only explicit allowlisted repairs |
| **Enterprise** | Fleet inventory, history, policies, monitoring | Optional managed installation | Policy-controlled |

The portable editions are first-class products, not packaging afterthoughts. A technician should be able to run ThermalOps from approved removable media, diagnose a customer machine, export an authorized support bundle, close the session, and leave no permanent component behind.

## Core principles

- **Read-only by default.** Diagnosis must work without administrator rights whenever Windows allows it.
- **Least privilege.** The desktop UI never needs to stay elevated. Privileged work is delegated to a narrowly scoped helper only when explicitly requested.
- **Offline-first.** Core diagnosis and repair do not depend on cloud services, accounts, internet access, telemetry, or AI.
- **Deterministic truth first.** Windows APIs, device protocols, and explicit diagnostic rules are authoritative. AI may explain evidence but may never be the authority that executes a repair.
- **No broad destructive shortcuts.** Target a selected printer/job first. Global spool reset is a break-glass operation with clear impact warnings.
- **Preflight → Snapshot → Execute → Verify → Recovery → Post-condition.** A repair is not complete because a command returned success.
- **Privacy by design.** Customer data stays local by default. Reports are sanitized by default and full technical bundles require explicit export.
- **No arbitrary shell execution.** No generic PowerShell/cmd execution endpoint, no `shell=True`-style command construction, no remotely supplied command strings.
- **No silent persistence.** Portable mode must not install services, scheduled tasks, startup entries, or leave local logs behind after successful cleanup.
- **Production-quality delivery.** Signed artifacts, checksums, SBOM, version/build identity, CI gates, tests, and documented rollback expectations are part of the product.

## What ThermalOps diagnoses

The intended diagnostic surface includes:

- Windows Print Spooler status and configuration;
- installed printers and selected printer details;
- print jobs and blocked/stale jobs;
- print drivers and driver packages;
- printer ports and connection type;
- USB/PnP evidence;
- print-related Windows events;
- local/network reachability where explicitly allowed;
- vendor-native device status;
- firmware and selected read-only configuration data;
- before/after snapshots;
- evidence-backed findings and recommended actions.

For Zebra devices, the native adapter is intended to use supported Link-OS/SGD/ZPL capabilities where appropriate so ThermalOps can distinguish a Windows queue problem from physical states such as head open, media out, ribbon out, pause, overheating, or device-not-ready conditions.

## Connection model

ThermalOps models connection types explicitly instead of relying on a single string heuristic:

- USB / DOT4;
- TCP/IP RAW (commonly 9100);
- TLS printer channel where supported (commonly 9143 on applicable Zebra workflows);
- LPR;
- Windows shared printer;
- Bluetooth;
- serial;
- parallel;
- browser/local bridge scenarios;
- unknown/other.

## Repair model

Every write operation becomes a `RepairPlan` with impact, scope, preconditions, expected post-conditions, validation, and recovery behavior.

Example escalation:

1. **Low impact:** cancel one selected stale job.
2. **Medium impact:** restart the Print Spooler while preserving the original service state and validating recovery.
3. **High impact:** targeted queue repair with explicit affected-printer scope.
4. **Break glass:** global spool reset only when the operator explicitly confirms that all local print queues may be affected.

AI never changes this escalation order.

## Portable workflow

```text
Approved USB / local copy
        |
        v
ThermalOps.exe
        |
        +--> Quick Diagnosis (read-only)
        |
        +--> Advanced Diagnostics (N2/N3)
        |
        +--> Explicit Repair Plan --UAC--> Temporary Privileged Helper
        |
        +--> Validate before/after
        |
        +--> Export sanitized report or authorized support bundle
        |
        +--> Session cleanup / helper termination / no persistence
```

Portable defaults:

- self-contained executable;
- no preinstalled .NET runtime required on the target machine;
- no installer;
- no account/login;
- no required network access;
- session data under an OS temporary location, not the USB drive;
- sanitized export by default;
- `--readonly` mode that cannot perform writes even when the user is an administrator;
- customer-safe mode with no writes, no telemetry, no automatic network scan, and no printer configuration changes.

## Tech support UX

ThermalOps is designed for both fast N1 use and deeper N2/N3 analysis.

A quick diagnosis should answer questions such as:

- Is Windows printing healthy?
- Is the selected driver present and associated with the expected queue?
- Are there blocked jobs?
- Is the printer reachable?
- Is the problem in Windows, transport, or the physical printer?
- What evidence supports the conclusion?
- What is the least-impact next action?

Advanced mode exposes Windows print subsystem, WinSpool, print processors, drivers, driver store, ports, PnP, services, events, vendor protocol evidence, firmware, counters, and configuration snapshots.

## Support bundles

Default export is sanitized. A full technical bundle requires explicit operator choice.

Planned structure:

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

The manifest records hashes, schema versions, application version, build identity, and collection timestamps.

## Technology direction

Initial architecture decision:

- **C# / .NET 10 LTS**;
- **WPF** for the first Windows desktop UI;
- modular monolith;
- domain/application layers independent from Windows/UI concerns;
- Windows infrastructure adapters around supported APIs;
- separate vendor adapters;
- temporary privileged helper with a strict local IPC contract;
- self-contained portable publishing for Windows.

.NET 10 is an active LTS release and is the baseline unless an ADR changes it.

## Repository map

```text
.
├── AGENTS.md
├── ENGINEERING_CONSTITUTION.md
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
│   ├── PRODUCT.md
│   ├── ARCHITECTURE.md
│   ├── PORTABLE.md
│   ├── SECURITY_AND_PRIVACY.md
│   ├── DIAGNOSTICS_AND_REPAIR.md
│   ├── SUPPORT_BUNDLE.md
│   ├── AI.md
│   ├── TESTING.md
│   ├── RELEASE_ENGINEERING.md
│   ├── ROADMAP.md
│   └── adr/
└── tools/
    └── validate_docs.py
```

The future source tree is specified in `docs/ARCHITECTURE.md`; implementation starts only after M0 decisions are accepted.

## Roadmap

| Milestone | Outcome |
| --- | --- |
| **M0** | Constitution, threat model, ADRs, product boundaries, CI foundations |
| **M1** | Read-only WinSpool/PnP/driver/job/spooler diagnosis |
| **M2** | Safe targeted repair, transactional spooler restart, validation/recovery |
| **M3** | Zebra native adapter: Link-OS/SGD/ZPL status and configuration evidence |
| **M4** | Support suite: sanitized bundles, snapshots, diff, safe diagnostic labels |
| **M5** | Enterprise hardening: helper security, signing, policy controls, packaging |
| **M6** | Fleet inventory/history/alerts for managed deployments |
| **M7** | Additional thermal-printer vendor adapters |
| **M8** | Optional knowledge/AI explanation layer with evidence citations and guardrails |

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for acceptance criteria.

## Safety and authorization

ThermalOps is intended for systems and printers the operator is authorized to support. Customer security policy always takes precedence. Portable capability is not a mechanism to bypass EDR, WDAC, AppLocker, removable-media restrictions, least-privilege policy, or application allowlisting.

## References

Primary implementation work should prefer official platform/vendor documentation, including:

- Microsoft Win32 printing APIs (`OpenPrinter`, `EnumJobs`, `GetJob`, `SetJob`, `PRINTER_INFO_2`);
- Microsoft Service Control Manager and Windows security documentation;
- Zebra Link-OS SDK and Zebra printer protocol documentation;
- NIST Secure Software Development Framework (SSDF);
- OWASP ASVS and relevant OWASP guidance for any future service/API surface.

## License

A project license has **not yet been selected**. Do not add or copy third-party code into this repository unless its license is identified and compatible. License selection is tracked as an M0 governance task.
