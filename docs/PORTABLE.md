# Portable Editions

Portable operation is a core product requirement for diagnosis, preventive inspection, triage, evidence collection and controlled field remediation.

## Goals

A technician should be able to:

1. receive an approved/signed artifact;
2. run it on an authorized supported Windows endpoint;
3. diagnose and perform preventive inspection without installation;
4. stay read-only unless a Pro action is explicitly chosen;
5. collect/prepare an escalation case without being forced to repair;
6. export only intended data;
7. exit and leave no intentional persistent component.

## Portable Lite

Permanently read-only. Intended for N1/field/preventive use.

Includes, as milestones mature:

- Quick Diagnosis;
- Advanced read-only diagnostics;
- Preventive Inspection;
- technician checklist;
- source-backed maintenance due calculation;
- baseline comparison/import/export;
- service disposition and escalation preparation;
- sanitized reporting.

No helper/UAC/write path exists.

## Portable Pro

Everything in Lite plus policy-authorized local remediation, diagnostic print and full service/support bundles. UAC is requested only for a specific action that truly requires elevation.

## Packaging

```text
ThermalOps-Portable-<version>-win-x64.zip
├── ThermalOps.exe
├── checksums.sha256
├── SBOM.spdx.json
├── release-notes.md
├── README.txt
└── SECURITY.txt
```

Single-file is desirable but not mandatory if it harms vendor-native SDK compatibility, signing, helper verification, reliability, endpoint-security compatibility or troubleshooting.

## Runtime

Self-contained .NET publish. Target machine should not require a preinstalled .NET runtime.

- `win-x64` primary;
- `win-arm64` after real testing;
- `win-x86` only if a demonstrated requirement exists.

## Session storage

Do not automatically write customer data to removable media.

```text
%TEMP%\ThermalOps\Sessions\<session-id>\
```

Session staging may contain normalized evidence, snapshots, checklist state, logs and bundle staging.

At close:

- explicit export choices;
- close helper/IPC;
- remove ThermalOps-created temporary session files where possible;
- report cleanup failure;
- do not promise forensic secure erase.

## Read-only mode

`ThermalOps.exe --readonly`

Enforced at application/domain capability level.

Impossible actions include:

- helper launch/UAC;
- job cancellation;
- service control;
- queue reset;
- printer setting write;
- arbitrary ZPL/SGD write;
- diagnostic print;
- driver install/remove;
- firmware action.

Preventive inspection, evidence collection and escalation-package preparation should remain useful.

## Customer Safe

Defaults:

- read-only;
- no telemetry/upload;
- no automatic network scanning;
- no printer/system writes;
- no diagnostic print;
- local evidence first.

## Baselines and previous inspections

Portable does not keep hidden customer history. The operator may explicitly import/export a sanitized baseline or previous-inspection artifact when policy permits.

Imported policy/baseline data can constrain or inform the workflow but can never unlock code capabilities absent from the executable.

## Privileged helper

```text
ThermalOps.exe (standard user)
        |
        | confirmed typed request
        v
Temporary Elevated Helper
        |
        +-- one allowlisted operation
        v
validate post-condition -> helper exits
```

No shell, script engine, arbitrary executable launch, generic registry write, arbitrary file delete, or general service-control endpoint.

## Endpoint controls

Assume Defender, EDR/XDR, AppLocker, WDAC, removable-media restrictions, Controlled Folder Access and privilege-management products.

ThermalOps cooperates with these controls. It never bypasses them.

Production release metadata should support security review and publisher allowlisting:

```text
Product / edition
Version
Publisher
Authenticode status
Commit SHA
Build ID
Architecture
SHA-256
SBOM
Known network/persistence behavior
```

## Offline behavior

Core functions remain available without internet/cloud/login:

- Windows diagnosis;
- local printer discovery;
- vendor-local status where supported;
- preventive inspection;
- baseline comparison from local approved file;
- local policy-permitted remediation;
- timeline/report/service-case generation.

Optional cloud/AI fails closed to deterministic functionality.

## Portable UX target

Normal usage should not require an installer, CLI, dependency setup or reboot.

A future measured target may be less than 60 seconds from launch to beginning first diagnosis on a supported normal endpoint. Do not advertise it until benchmarked.

## No-persistence E2E verification

Before/after clean exit verify:

- no ThermalOps service;
- no scheduled task;
- no startup/Run entry;
- no helper process;
- no open IPC endpoint;
- no unexpected session directory;
- no app-managed persistent registry state;
- no log beside executable/USB unless explicitly exported.

## Export choices

```text
[Discard session]
[Export sanitized diagnostic report]
[Export preventive report]
[Export full technical bundle]
[Export service-case/escalation package]
```

Full/identity-bearing exports require an explicit privacy warning.

See `DEPLOYMENT_AND_LIFECYCLE.md` for enterprise installation/upgrade/uninstall requirements.
