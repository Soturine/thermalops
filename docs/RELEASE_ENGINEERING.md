# Release Engineering

## Versioning

Use Semantic Versioning once distributable builds begin.

Before 1.0, minor versions may introduce capability while patch versions remain backward-compatible fixes within the documented experimental surface.

## Channels

Potential channels:

- `dev` — CI artifacts, not for customer use;
- `preview` — signed/controlled evaluation once signing exists;
- `stable` — release gates complete.

Do not call an unsigned/unvalidated artifact stable merely because it is downloadable.

## Release artifacts

Portable example:

```text
ThermalOps-Portable-0.3.0-win-x64.zip
ThermalOps-Portable-0.3.0-win-arm64.zip
checksums.sha256
SBOM.spdx.json
release-notes.md
```

Installed/enterprise packaging (MSI/MSIX or another strategy) requires an ADR when that milestone begins.

## Build identity

Application/About and support bundle should expose:

- semantic version;
- commit SHA;
- build ID/run ID;
- build timestamp when reproducibility policy allows;
- target RID/architecture;
- edition/mode.

## CI gates

As implementation arrives:

1. formatting/lint;
2. build;
3. unit tests;
4. component tests;
5. Windows integration tests appropriate for standard runners;
6. static/security analysis;
7. dependency/license checks;
8. packaging smoke tests;
9. artifact integrity checks;
10. release-only signing/SBOM/provenance gates.

Hardware-in-the-loop may run on a dedicated protected runner and can be a required gate for releases that claim vendor-native hardware support.

## Signing

Use Authenticode for Windows binaries when a signing certificate/service is available. Protect signing credentials in an approved CI secret/signing service; never store private keys in the repository.

Verify signature after packaging and before publishing.

## Checksums

Generate SHA-256 for final distributed bytes after signing/packaging. The checksum file itself should be included in the release metadata and may be signed/attested depending on the release system.

## SBOM

Generate an SBOM for production distributions covering first-party components and dependencies. SPDX JSON is the initial preferred interchange format unless tooling constraints justify CycloneDX via ADR.

## Reproducibility

Aim for deterministic builds where practical, but do not claim byte-for-byte reproducibility until verified. Signing timestamps and native packaging can affect bytes.

## Release rule

```text
CI green SHA -> release build -> security/package verification -> tag/release
```

Tag must identify the validated source SHA. Never tag first and hope CI becomes green later.

## Enterprise allowlisting

Stable publisher identity is more useful to enterprise application-control teams than an ever-changing unsigned executable. Release notes should include publisher, hashes, supported OS/architecture, and known behavior that endpoint security teams can review.
