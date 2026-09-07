# Deployment and Application Lifecycle

ThermalOps has two fundamentally different deployment models:

- **Portable:** no installation, no persistent agent, field/support use.
- **Enterprise:** managed installation with policy-controlled persistence for fleet/history features.

Deployment simplicity is a product requirement, not a late packaging task.

## Portable experience target

From an approved package to first read-only diagnosis should require no manual dependency installation.

Target experience:

```text
Approved package / USB / local copy
  -> start ThermalOps
  -> select target or Quick Diagnosis
```

Goals:

- no installer;
- self-contained runtime;
- no account required;
- no internet required;
- no CLI required for normal use;
- no reboot;
- no service/daemon installation;
- no permanent registry/startup/task persistence;
- no automatic writes to removable media;
- signed publisher identity when production signing exists.

A target such as **under 60 seconds from launch to starting the first diagnosis on a normal supported endpoint** may be used as a UX performance goal once measured on real hardware. It is not a release claim until benchmarked.

## Portable package

Preferred release layout:

```text
ThermalOps-Portable-<version>-win-x64.zip
├── ThermalOps.exe                 # or minimal signed app directory
├── checksums.sha256
├── SBOM.spdx.json
├── release-notes.md
├── README.txt
└── SECURITY.txt
```

Single-file publishing is preferred only if it remains compatible with vendor SDK/native libraries, Authenticode, startup reliability, helper extraction/verification, endpoint controls, and troubleshooting.

## Architecture targets

- `win-x64` primary;
- `win-arm64` after real compatibility/testing exists;
- `win-x86` only for a demonstrated support requirement.

Do not claim a target is supported because it builds; it needs test coverage and any required hardware/vendor validation.

## Enterprise deployment requirements

Enterprise packaging technology is intentionally undecided until a dedicated ADR, but the product contract should support:

- one managed package or clearly defined package set;
- interactive install;
- silent/unattended install;
- silent/unattended uninstall;
- offline deployment;
- upgrade in place;
- rollback/recovery strategy;
- clean uninstall;
- configuration/policy preservation rules;
- install log suitable for support;
- signed binaries/package;
- deterministic return/exit codes for software distribution;
- no reboot for a normal ThermalOps application install/upgrade where technically possible.

Potential enterprise distribution systems include Microsoft Intune, Configuration Manager/SCCM, endpoint software distribution, or manual deployment. ThermalOps should provide standards-compatible packages/command-line behavior rather than embedding vendor-specific deployment logic in the application.

## No-reboot goal

The core application should not require a Windows reboot for normal install, upgrade, or uninstall.

If a future third-party driver, vendor SDK component, low-level service, or Windows prerequisite creates a reboot requirement:

- detect it before/after the action where possible;
- state the reason;
- never restart automatically without policy/confirmation;
- distinguish ThermalOps requirement from external component requirement.

## Upgrade behavior

An enterprise upgrade should preserve only documented persistent state, such as:

- policies;
- approved baselines;
- maintenance history;
- device inventory/history;
- audit metadata;
- service configuration that remains compatible.

Versioned migrations must be:

- forward tested;
- failure safe;
- logged;
- backup-aware for durable state;
- reversible where practical, or explicitly declare irreversible schema changes.

Do not update binaries first and hope migrations work later.

## Uninstall

A clean uninstall should remove ThermalOps-owned:

- application binaries;
- services/agents installed by ThermalOps Enterprise;
- scheduled tasks/startup registrations;
- machine/user configuration owned by ThermalOps;
- temporary files;
- update components.

Retention of history/database/report exports must be an explicit installer/administrator choice, especially when required for audit. Uninstall must not delete unrelated customer files.

## Repair installation

If the selected Windows packaging technology supports an installer repair mode, use it only to repair ThermalOps installation state. Do not conflate “installer repair” with printer remediation.

## Offline networks

Enterprise installation and Portable operation should both support disconnected or restricted environments.

Core package installation must not require downloading:

```text
.NET runtime
vendor dependency
application files
license manager bootstrap
cloud agent
```

unless a specific optional feature is clearly documented as requiring it.

## Signing and allowlisting

Production releases should use Authenticode when a signing identity exists.

Endpoint/security teams should be able to verify:

- publisher;
- product name;
- semantic version;
- source commit/build ID;
- architecture;
- SHA-256;
- signature status;
- SBOM;
- known network/persistence behavior.

Publisher-based allowlisting is generally more maintainable than approving a new unsigned hash for every release.

ThermalOps must cooperate with Defender, EDR/XDR, WDAC, AppLocker and removable-media controls. It must not attempt bypasses.

## Update strategy

Do not implement silent self-update in early versions.

A future updater requires an ADR covering:

- signed update manifests;
- signature verification;
- channel selection;
- enterprise deferral;
- offline mirrors;
- proxy behavior;
- rollback;
- downgrade policy;
- compromised-key response;
- atomicity/recovery.

Portable manual replacement and managed enterprise deployment are safer early defaults.

## Lifecycle tests

Release qualification should eventually include:

- portable launch on clean supported Windows VM;
- no-runtime-preinstalled scenario;
- portable no-persistence before/after diff;
- install from clean VM;
- silent install/uninstall;
- upgrade N-1 -> N;
- failed migration rollback/recovery;
- uninstall cleanup;
- policy/baseline preservation;
- package/signature verification;
- blocked-by-policy behavior;
- offline install/use;
- no-reboot verification for normal paths.
