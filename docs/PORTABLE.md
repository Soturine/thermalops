# Portable Editions

Portable operation is a core product requirement.

## Goals

A technician should be able to:

1. receive an approved/signed ThermalOps artifact;
2. execute it on an authorized customer Windows endpoint;
3. diagnose without installation;
4. elevate only an explicitly chosen repair action when using Portable Pro;
5. export only the intended report/bundle;
6. exit;
7. leave no intentional persistent component.

## Packaging

Primary target:

```text
ThermalOps-Portable-<version>-win-x64.zip
├── ThermalOps.exe
├── checksums.sha256
├── SBOM.spdx.json
├── README.txt
└── SECURITY.txt
```

If signing/provenance produces separate metadata, include it without making runtime execution depend on the presence of the metadata files.

Daily technician use may expose only the signed executable through an approved internal software channel, while security teams retain the full release package.

## Runtime

Use .NET self-contained publishing so the target does not require a preinstalled .NET runtime.

Initial architecture targets:

- `win-x64` — primary;
- `win-arm64` — supported when test coverage exists;
- `win-x86` — only if a real customer/support requirement justifies it.

Single-file publishing is desirable, but not at the expense of runtime reliability, signing, native vendor SDK compatibility, startup time, or forensic clarity. If a small signed multi-file directory is safer, document the trade-off in an ADR.

## Session storage

Do **not** automatically write collected customer data to removable media.

Default session root:

```text
%TEMP%\ThermalOps\Sessions\<session-id>\
```

Session content may include normalized evidence, temporary logs, snapshots, and bundle staging.

At close:

- allow explicit export;
- attempt secure application-level cleanup of ThermalOps-created temporary files;
- stop/close helper and IPC;
- report cleanup failures;
- do not promise forensic secure erase on filesystems where the application cannot guarantee it.

## Read-only mode

`ThermalOps.exe --readonly`

Properties:

- no helper launch;
- no UAC;
- no job cancellation;
- no service control;
- no filesystem-based queue repair;
- no printer configuration write;
- no ZPL/SGD write;
- no diagnostic print;
- no driver install/remove;
- no firmware action.

This is enforced in application/domain policy, not only by disabling buttons.

## Customer Safe mode

Customer Safe is a stricter operational profile suitable for environments where even harmless discovery is sensitive.

Defaults:

- read-only;
- no telemetry;
- no upload;
- no automatic network scanning;
- no printer writes;
- no test print;
- local evidence only unless operator explicitly enables an allowed check.

Portable Lite can use Customer Safe semantics permanently.

## UAC and privileged helper

Portable Pro remains standard-user until a confirmed repair requires elevation.

```text
ThermalOps.exe (standard user)
        |
        | signed structured request
        v
ThermalOps.PrivilegedHelper.exe (temporary elevated process)
        |
        +-- allowlisted Windows operation
        |
        v
validate post-condition -> helper terminates
```

The helper must not expose a terminal, script engine, arbitrary executable launch, generic registry write, or generic file delete endpoint.

## Enterprise endpoint security

Assume customer endpoints may use:

- Microsoft Defender;
- EDR/XDR;
- AppLocker;
- WDAC;
- removable-media controls;
- application allowlisting;
- Controlled Folder Access;
- privilege-management products.

ThermalOps must **cooperate** with these controls, not attempt to bypass them.

Release identity should support publisher-based allowlisting when organizations choose to approve the tool:

```text
Product: ThermalOps Portable
Version: 1.x.y
Publisher: <future signing identity>
Signature: valid Authenticode
Commit: <sha>
Build: <build-id>
SHA-256: <artifact hash>
```

## Offline behavior

Core features must continue with:

```text
Internet: unavailable
Cloud/API: unavailable
Account/login: unavailable
```

Required offline capabilities:

- Windows diagnosis;
- local printer discovery;
- supported vendor-local status;
- policy-permitted repair;
- logs/session timeline;
- report generation.

Optional AI/cloud explanation must fail closed to deterministic diagnosis, never block support.

## No-persistence verification

Portable E2E tests should verify, before vs after clean exit:

- no ThermalOps service installed;
- no scheduled task created;
- no Run/Startup entry created;
- no helper process remains;
- no named pipe remains open;
- no expected temporary session directory remains after successful cleanup;
- no new application-managed registry persistence;
- no log file left in the executable directory or removable media unless explicitly exported.

## Export choices

At session end:

```text
[Discard session]
[Export sanitized report]
[Export full technical support bundle]
```

Full bundle must show a concise warning that it may contain environment identifiers and is intended for authorized support handling.
