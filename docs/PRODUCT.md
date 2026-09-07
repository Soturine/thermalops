# Product Specification

## Mission

ThermalOps reduces time-to-diagnosis and risk during support of Windows-connected thermal printers by combining Windows print-subsystem evidence, transport evidence, vendor-native printer evidence, safe remediation plans, and support-quality reporting.

The product complements existing ERP/WMS/label-design/print-management ecosystems; it is not intended to replace them.

## Personas

### Field / N1 technician
Needs a fast, safe answer with minimal choices.

Primary workflow:

1. start approved Portable Lite/Pro;
2. run Quick Diagnosis;
3. select target thermal printer;
4. see evidence-backed conclusion;
5. perform only an authorized low-risk action or escalate;
6. export a sanitized report.

### N2/N3 support analyst
Needs raw evidence, protocol-level status, configuration comparison, job details, events, and controlled repair plans.

### Enterprise operator
Needs fleet inventory, history, policy enforcement, alerting, and centralized operational visibility without weakening endpoint security.

### Customer security/IT
Needs predictable behavior, publisher signing, no hidden persistence, no automatic upload, no arbitrary network scan, and a clear list of privileged capabilities.

## Editions

### Portable Lite

- single/self-contained Windows artifact or signed package;
- no installation;
- no required runtime installation;
- read-only by design;
- no UAC path;
- local diagnosis;
- sanitized report/export;
- customer-safe mode characteristics always enforced.

### Portable Pro

Everything in Lite plus:

- explicitly confirmed repair plans;
- temporary elevated helper;
- selected-job cancellation;
- controlled spooler restart;
- approved queue repair;
- vendor-native diagnostics/configuration reads;
- safe diagnostic print where allowed;
- N2/N3 support bundle.

### Enterprise

Planned capabilities:

- managed installation;
- inventory/history;
- policy profiles;
- role-based control if a central service is added;
- alerting/health trends;
- enterprise audit/retention;
- optional agent lifecycle.

Enterprise is not permission to reuse the portable helper as an unrestricted system service. Its security model requires its own review/ADR.

## Product modes

### Quick Diagnosis

Read-only one-click collection with progress by domain:

- Hardware/device;
- Driver;
- Connection;
- Spooler;
- Queue;
- Printer-native status.

Output:

- findings ordered by impact;
- evidence;
- likely layer of failure;
- least-impact recommended next action;
- explicit note when evidence is insufficient.

### Advanced Diagnostics

Expandable views for:

- Windows Print Subsystem;
- WinSpool details;
- print processors;
- drivers and driver store;
- ports;
- TCP/IP/USB/PnP;
- services;
- print-related Windows events;
- vendor-native status;
- SGD/ZPL or equivalent vendor diagnostics where applicable;
- firmware/counters;
- configuration.

### Read-only / `--readonly`

Hard guardrail. State-changing commands must be unreachable, not merely hidden. This mode remains read-only even when the caller is an administrator.

### Customer Safe

Enforces:

- no system writes;
- no printer configuration writes;
- no diagnostic print;
- no automatic network discovery/scan;
- no upload;
- no telemetry;
- local session-only processing.

## Field session

A session has a random ID and may optionally store operator-provided metadata such as a ticket reference. Customer/company fields are optional and should not be required for diagnosis.

Example timeline:

```text
14:31:12 Session started
14:31:13 Selected printer discovered
14:31:14 Spooler = Running
14:31:15 4 jobs observed
14:31:17 Device ready = false
14:31:17 Device evidence = RibbonOut
14:33:04 Operator requested CancelJob(job=918)
14:33:04 Repair plan confirmed
14:33:05 Job cancellation returned success
14:33:07 Post-condition: queue healthy, device still RibbonOut
```

The timeline distinguishes observations, operator intent, execution, and validation.

## Before/after

Every repair-capable workflow captures relevant snapshot A and B.

Example:

```text
                       BEFORE       AFTER
Spooler                Running      Running
Selected queue jobs    7            0
Device Ready           No           Yes
Head                    Closed       Closed
Ribbon                  OK           OK
```

A repair is reported `validated` only when its post-condition is actually observed.

## Printer status UX

Do not collapse all evidence into `ONLINE`/`ATTENTION`.

Show normalized fields and source:

```text
Windows
  Driver: installed
  Queue: 3 jobs
  Spooler: running

Transport
  Endpoint: reachable
  Channel: TCP/IP

Printer
  Responding: yes
  Ready: no
  Head: closed
  Media: present
  Ribbon: out
  Temperature: normal

Conclusion
  Windows and transport are healthy. Printer reports Ribbon Out.

Recommended action
  Replace/check ribbon before changing Windows state.
```

## Configuration snapshot/diff

For vendor adapters that support safe configuration reads, ThermalOps can compare two devices or before/after snapshots.

Candidate normalized fields:

- print darkness;
- speed;
- media mode;
- width;
- tear-off position;
- print language;
- firmware;
- selected connectivity settings.

Write-back/import is not part of the initial read-only milestone.

## Safe diagnostic label

A future approved test label can include:

- app/session ID;
- model/DPI;
- timestamp;
- barcode and QR test;
- line-width samples;
- alignment markers;
- darkness/calibration aids.

Printing is a write operation and must be disabled in read-only/customer-safe mode.

## Policy profiles

A policy file may constrain capabilities without changing code.

Conceptual example:

```json
{
  "allowNetworkDiscovery": false,
  "allowDiagnosticPrint": true,
  "allowSpoolerRestart": true,
  "allowDriverInstall": false,
  "allowFirmwareUpdate": false
}
```

Policy can only reduce capability relative to the build's maximum capability; it must never enable a feature that the executable does not support.

## Non-goals for early milestones

- replacing label-design software;
- ERP/WMS integration engine;
- remote-control platform;
- arbitrary script execution;
- general Windows repair utility;
- automatic firmware flashing;
- automatic driver replacement;
- mandatory cloud console;
- autonomous AI remediation;
- broad unattended network scanning.
