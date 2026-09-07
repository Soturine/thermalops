# Architecture

## Style

ThermalOps starts as a **modular monolith** with a separately elevated helper as a security boundary.

```text
+--------------------------------------------------+
|                 ThermalOps.Desktop               |
| Dashboard | Diagnosis | Jobs | Plans | Support   |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              ThermalOps.Application              |
| DiagnosePrinter | DiagnoseSpooler | RepairQueue  |
| GenerateSupportBundle | RunSafePrintTest         |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|                 ThermalOps.Domain                |
| Printer | PrintJob | Finding | Evidence          |
| RepairPlan | RepairAction | Policy | Snapshot    |
+-----------+----------------+---------------------+
            |                |
            v                v
+-------------------+  +---------------------------+
| Windows Infra     |  | Vendor Adapters           |
| WinSpool / SCM    |  | Zebra first               |
| PnP / Event Log   |  | future Honeywell / TSC    |
+-------------------+  +---------------------------+
            |
            | read operations
            v
         Windows

Only when required:

Desktop/Application
      |
      | structured authenticated local request
      v
Temporary Privileged Helper
      |
      +-- CancelJob
      +-- RestartSpooler
      +-- RepairQueue
      +-- other explicitly approved future actions
```

## Proposed solution structure

```text
src/
├── ThermalOps.Domain/
├── ThermalOps.Application/
├── ThermalOps.Infrastructure.Windows/
├── ThermalOps.Adapters.Zebra/
├── ThermalOps.Desktop/
└── ThermalOps.PrivilegedHelper/

tests/
├── ThermalOps.Domain.Tests/
├── ThermalOps.Application.Tests/
├── ThermalOps.Infrastructure.Windows.Tests/
├── ThermalOps.Adapters.Zebra.Tests/
├── ThermalOps.Security.Tests/
└── ThermalOps.EndToEnd.Tests/
```

Add projects only when the milestone needs them; do not generate empty complexity for appearance.

## Dependency direction

```text
Desktop ------------> Application ------------> Domain
Windows Infrastructure ----implements--------> Domain/Application ports
Zebra Adapter --------------implements-------> Domain/Application ports
Privileged Helper ----------implements-------> a tiny privileged contract
```

`Domain` must not reference:

- WPF;
- Windows API P/Invoke;
- filesystem;
- network stack;
- vendor SDK;
- database;
- AI SDK.

## Core domain concepts

### PrinterIdentity

Stable normalized identity composed from available evidence, not only display name. Potential inputs:

- Windows queue identity;
- port identity;
- PnP device identity;
- vendor serial/device identifier;
- network endpoint.

Identity resolution must tolerate partial evidence and avoid merging two physical devices merely because their friendly names match.

### PrinterSnapshot

Immutable observation set at a point in time containing normalized evidence references.

### DiagnosticEvidence

Fields:

- source;
- timestamp;
- category;
- normalized value;
- optionally safe raw representation;
- target resource;
- collection outcome/error.

### DiagnosticFinding

A conclusion derived from one or more evidence records.

A finding contains severity, certainty semantics, explanation, evidence IDs, and recommended next step. It must not rewrite evidence.

### PrintJob

Represents a job in a specific queue with stable queue/job identifiers, state flags, timestamps where available, document name only when policy allows, and age.

### RepairPlan

Contains:

- plan ID;
- target(s);
- impact level;
- preconditions;
- actions;
- snapshot requirements;
- confirmation requirements;
- expected post-conditions;
- validation checks;
- recovery steps;
- policy decision.

### RepairAction

Strongly typed action. No free-form privileged command string.

Examples:

- `CancelPrintJob(queueId, jobId)`;
- `RestartSpooler(expectedInitialState)`;
- `RepairSelectedQueue(queueId)`.

A future action requires a code change, review, tests, and capability registration.

## Windows boundaries

Planned Windows implementations should prefer supported native APIs over shelling out:

- WinSpool for printer/job enumeration and manipulation;
- Service Control Manager APIs for Print Spooler status/control;
- PnP/SetupAPI or supported managed Windows interfaces for device evidence;
- Windows Event Log APIs for print-related events;
- Windows networking APIs for narrowly scoped endpoint checks.

Shell/process invocation, if ever unavoidable for a specific supported tool, must use fixed executable/argument structures and never untrusted string concatenation.

## Vendor adapter boundary

Conceptual interface:

```text
IPrinterVendorAdapter
  CanHandle(evidence)
  DiscoverLocalAsync(policy)
  ReadStatusAsync(printer)
  ReadConfigurationAsync(printer, requestedKeys)
  GetCapabilitiesAsync(printer)
  RunApprovedDiagnosticAsync(...)
```

Read and write capabilities are separate. An adapter that can read configuration does not automatically gain permission to change it.

## Zebra adapter direction

Use official/supported Zebra capabilities where practical:

- Link-OS SDK;
- SGD for supported configuration/status reads;
- ZPL status queries when appropriate;
- USB/network discovery mechanisms allowed by policy.

Normalize vendor-specific values into domain evidence while preserving the vendor-native source.

## Connection model

Represent transport independently from printer vendor:

```text
Usb
Dot4
TcpRaw9100
TcpTls9143
Lpr
WindowsShare
Bluetooth
Serial
Parallel
BrowserBridge
Unknown
```

The exact port number is evidence, not identity of the transport by itself.

## Privileged helper

The helper is a separate trust boundary, not a utility process with general command execution.

Required properties:

- launched only for a required operation in Portable Pro;
- UAC elevation only for the helper;
- local IPC with restrictive ACL;
- protocol versioning;
- session-bound nonce/token;
- caller identity/process validation where practical;
- strongly typed request schema;
- capability allowlist;
- bounded input sizes;
- explicit timeouts;
- structured result schema;
- terminates after the operation/session according to design;
- leaves no service/daemon in portable mode.

See ADR-0002.

## Enterprise evolution

Fleet capability can reuse domain/application/adapters but may add managed persistence and a service. Do not prematurely make portable code depend on an enterprise backend.

Potential enterprise components require separate ADRs for:

- local agent lifecycle;
- central API;
- authentication/RBAC;
- data retention;
- TLS/certificate management;
- rate limiting;
- health/readiness;
- metrics/tracing;
- update channel.

## UI

First UI direction is WPF on .NET 10 LTS. UI must display evidence and impact rather than hiding complexity behind a single status color.

N1: progressive disclosure and guided actions.

N2/N3: detailed evidence panels and export.

## Composition root

Desktop entry point composes:

- policy source;
- Windows implementations;
- available vendor adapters;
- diagnostic rule engine;
- report generator;
- privileged-helper client;
- UI view models.

No service locator hidden inside domain logic.
