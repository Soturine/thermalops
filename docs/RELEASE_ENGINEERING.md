# Release Engineering

## Versioning and status

Use Semantic Versioning once distributable builds begin. `dev`, `preview`, and `stable` represent validation channels, not marketing labels.

Never call an unsigned/unvalidated artifact stable because it downloads successfully.

## Portable artifacts

```text
ThermalOps-Portable-<version>-win-x64.zip
ThermalOps-Portable-<version>-win-arm64.zip
checksums.sha256
SBOM.spdx.json
release-notes.md
```

Single-file is optional. Reliability, signing and vendor-native dependency correctness outrank cosmetic packaging.

## Enterprise package

Packaging technology remains an ADR decision. It must support the lifecycle contract in `DEPLOYMENT_AND_LIFECYCLE.md`:

- interactive/silent install;
- silent uninstall;
- offline deployment;
- upgrade/migration;
- rollback/recovery;
- predictable exit codes/logs;
- clean uninstall;
- normal-path no-reboot goal.

## Build identity

Expose:

- semantic version;
- commit SHA;
- CI/build ID;
- build timestamp when policy allows;
- RID/architecture;
- edition;
- capability/schema versions where useful.

Support bundles/service cases also record applicable policy/baseline/schema versions.

## CI gates

As implementation arrives:

1. documentation validation;
2. formatting/lint;
3. build;
4. unit tests;
5. component/contract tests;
6. Windows integration tests;
7. preventive policy/baseline/schema tests;
8. security/static analysis;
9. dependency/license checks;
10. packaging/lifecycle smoke tests;
11. artifact integrity;
12. release-only signing/SBOM/provenance;
13. hardware-in-the-loop gate for claimed vendor-native capabilities.

## Signing

Use Authenticode when a production signing identity/service is available. Never store private signing keys in the repository. Verify signature after final signing/packaging.

## Checksums/SBOM

Generate SHA-256 for final distributed bytes. Produce an SBOM covering first-party and dependencies. SPDX JSON remains the preferred starting format unless an ADR changes it.

## Provenance/reproducibility

Aim for deterministic builds where practical. Do not claim byte-for-byte reproducibility until verified; signing timestamps/native packaging can alter bytes.

## Release sequence

```text
known-green source SHA
 -> release build
 -> tests/security/package validation
 -> sign
 -> verify signature
 -> checksums/SBOM/provenance
 -> publish
 -> tag/release points to validated source
```

## Enterprise allowlisting

Release documentation should give endpoint teams publisher, hashes, supported OS/architecture, required privileges, expected persistence/network behavior, update behavior and known limitations.

## Upgrade/uninstall gates

Before Enterprise stable:

- clean install test;
- silent install/uninstall;
- N-1 -> N upgrade;
- policy/baseline/history preservation;
- failed migration recovery;
- uninstall cleanup;
- offline install;
- blocked-by-policy behavior;
- no-reboot normal path validation.

## Update policy

No silent self-updater in early releases. A future updater requires signed manifests, signature verification, enterprise deferral, offline mirrors, proxy behavior, rollback/downgrade policy and compromised-key response.
