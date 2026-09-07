# Release Engineering

Release Engineering faz parte da qualidade do produto. Um executable que “abre” não é automaticamente um artifact confiável para field support ou ambiente corporativo.

## Versioning

Use Semantic Versioning quando distributable builds começarem.

Antes de `1.0.0`, minor versions podem adicionar capabilities ainda em evolução, mas cada release deve declarar claramente validation status e known limitations.

Possible channels:

```text
dev
preview
stable
```

Esses channels representam validation level, não marketing.

- `dev` — CI artifacts / developer use;
- `preview` — controlled evaluation, preferencialmente signed quando signing estiver disponível;
- `stable` — required release gates completos para o scope anunciado.

Nunca chamar artifact unsigned/unvalidated de stable apenas porque foi publicado.

## Build Identity

Application/About, logs e support outputs devem conseguir expor:

- Semantic Version;
- source commit SHA;
- CI/build/run ID;
- target RID/architecture;
- edition (`PortableLite`, `PortablePro`, `Enterprise`);
- build timestamp quando policy/reproducibility strategy permitir;
- schema versions relevantes;
- adapter versions;
- policy/baseline/catalog versions quando influenciam output.

Essa identity permite correlacionar issue com source exato.

## Portable Artifacts

Exemplo:

```text
ThermalOps-Portable-0.3.0-win-x64.zip
ThermalOps-Portable-0.3.0-win-arm64.zip
checksums.sha256
SBOM.spdx.json
release-notes.md
```

Single-file é optional. Reliability, signature correctness e native dependency compatibility têm prioridade sobre estética de “um único EXE”.

## Enterprise Package

Packaging technology é decision de ADR no M5.

O selected package deve cumprir `deployment-e-lifecycle.md`:

- interactive install;
- silent install/uninstall;
- offline deployment;
- upgrade/migration;
- rollback/recovery;
- predictable logs/exit codes;
- clean uninstall;
- no-reboot normal path quando possível.

## CI Gates

A pipeline deve crescer incrementalmente conforme código aparece.

### Foundation / M0

- documentation validation;
- internal-link validation;
- repository-structure validation.

### M1+

Adicionar:

- format/lint;
- `dotnet restore` com dependency governance;
- build;
- Domain tests;
- Application tests;
- Windows integration tests relevantes.

### M2+

Adicionar:

- helper/security tests;
- negative paths;
- privileged contract validation.

### M3+

Adicionar:

- adapter contract tests;
- HIL protected runner/manual gate para capabilities anunciadas.

### M4+

Adicionar:

- maintenance policy/catalog validation;
- schemas;
- baseline compatibility fixtures;
- bundle/redaction/archive tests.

### M5+

Adicionar:

- CodeQL/static analysis;
- dependency/vulnerability scan;
- license inventory/check;
- packaging smoke tests;
- lifecycle tests;
- signing verification;
- SBOM;
- provenance/attestation quando viável.

## Known-Green Discipline

Canonical flow:

```text
logical change
 -> commit
 -> push
 -> CI
 -> next logical change
```

Preservar last-known-green.

Não criar release tag em red CI.

Release tag identifica validated source SHA; não deve apontar para commit que ainda “espera ficar verde”.

## Restore e Dependencies

Dependency handling deve ser previsível.

Regras:

- package source explícito/confiável;
- lock/version governance quando apropriado;
- dependency purpose documentado;
- license review;
- vulnerability review;
- avoid transient installer scripts;
- não baixar executable arbitrary em build script;
- native dependencies recebem atenção especial.

## Signing

Production Windows binaries devem usar Authenticode quando signing identity/service estiver disponível.

Signing credentials:

- nunca no repository;
- nunca em artifact público;
- usar approved secret/signing service;
- least-privilege access;
- audit de signing events quando provider suportar.

Sequence:

```text
build
 -> test
 -> package/stage
 -> sign final binaries/package
 -> verify signature
 -> produce final hashes
 -> publish
```

Se package process modificar bytes depois do signing, revisar ordem conforme tecnologia escolhida.

## Signature Verification

Release pipeline precisa verificar:

- signature present;
- expected subject/publisher;
- cryptographic validity;
- timestamp behavior;
- signed file é o mesmo que será publicado.

Não confiar apenas porque signing command returned success.

## SHA-256 Checksums

Generate checksums sobre final distributed bytes.

Exemplo:

```text
<sha256>  ThermalOps-Portable-0.3.0-win-x64.zip
```

O checksum file deve fazer parte do release metadata. Pode receber assinatura/attestation quando sistema de release permitir.

## SBOM

Production distributions devem possuir Software Bill of Materials.

Initial preferred interchange:

```text
SPDX JSON
```

CycloneDX pode ser adotado via ADR/tooling rationale se se tornar melhor fit.

SBOM deve cobrir:

- first-party components;
- NuGet dependencies;
- native libraries;
- bundled vendor components quando license/distribution permitir;
- versions;
- identifiers suficientes para vulnerability management.

## Provenance / Attestation

Quando tooling permitir, registrar provenance de build:

- source repository/ref;
- source SHA;
- workflow identity;
- build environment;
- artifact digest.

Não alegar SLSA level ou equivalent sem cumprir formalmente os requisitos correspondentes.

## Reproducibility

Buscar deterministic builds quando prático.

Mas não afirmar byte-for-byte reproducibility até medir.

Potential sources de diferença:

- signing timestamp;
- native packaging;
- generated metadata;
- archive ordering/timestamps;
- toolchain version.

Documentar toolchain versions importantes.

## Release Sequence

Canonical production sequence:

```text
known-green source SHA
 -> release build
 -> unit/component/integration validation
 -> security/package validation
 -> sign
 -> verify signatures
 -> generate checksums/SBOM/provenance
 -> artifact integrity smoke test
 -> publish
 -> release/tag references validated source SHA
```

## Release Notes

Release notes devem informar:

- version;
- source SHA;
- supported editions/RIDs;
- new capabilities;
- fixes;
- security changes quando divulgáveis;
- behavior changes;
- migration notes;
- known limitations;
- validation status;
- hardware support matrix reference quando relevante;
- breaking schema/policy changes.

Não usar linguagem que transforme `experimental` em “fully supported”.

## Supported Platform Matrix

Manter uma matrix versionada, futuramente semelhante a:

| OS | Arch | Edition | Status | Notes |
| --- | --- | --- | --- | --- |
| Windows 11 | x64 | Portable Lite | validated/preview | conforme testes |
| Windows 11 | arm64 | Portable | not validated | exemplo |

Não preencher support por inferência; somente após validation.

## Hardware Capability Matrix

Para vendor-native release, publicar internamente/externamente conforme adequado:

```text
Vendor
Model
DPI
Firmware range tested
Connection tested
Capabilities
Adapter version
Validation status
Known limitations
```

“Zebra supported” sem model/capability context é amplo demais.

## Enterprise Allowlisting Information

Stable release docs devem ajudar endpoint/security teams com:

- publisher identity;
- hashes;
- OS/architecture;
- install path;
- required privileges;
- service/agent identity se existir;
- expected network destinations;
- persistence behavior;
- update behavior;
- uninstall behavior;
- temp/storage behavior;
- known security controls interactions.

## WDAC / AppLocker / EDR

ThermalOps não deve buscar bypass.

Release validation deve considerar:

- signed publisher rule scenarios;
- hash-based approval quando necessário;
- Portable from removable media policies;
- helper elevation visibility;
- Controlled Folder Access;
- EDR false-positive troubleshooting com behavior documentation.

## Packaging Smoke Test

Após packaging/signing, testar final artifact, não só build output.

Portable:

- extract/run;
- signature valid;
- starts offline;
- expected files present;
- no missing native dependency;
- read-only workflow;
- cleanup.

Enterprise:

- install;
- launch;
- service health quando existir;
- upgrade/uninstall test subset;
- signature/package identity.

## Upgrade / Uninstall Gates

Antes de Enterprise stable:

- clean install;
- silent install;
- silent uninstall;
- N-1 -> N upgrade;
- policy/baseline/history preservation;
- failed migration recovery;
- uninstall cleanup;
- offline install;
- blocked-by-policy behavior;
- no-reboot normal path validation.

## Update Policy

No silent self-updater early.

Future updater requer:

- signed update manifest;
- signature verification;
- channel policy;
- enterprise deferral;
- offline mirror support;
- proxy behavior;
- atomic switch;
- rollback;
- downgrade rules;
- compromised-key response;
- logging/audit;
- update failure recovery.

## Security Release

Security-sensitive fix deve:

- preservar/expandir regression test;
- não reduzir security gate;
- documentar impact quando disclosure permitir;
- considerar vulnerable-version downgrade;
- atualizar known limitations se residual risk persistir.

## Rollback de Release

Se production release for problemática:

- disable/remove distribution channel quando apropriado;
- identificar affected SHA/version;
- publish corrected guidance;
- preserve evidence/artifacts para investigation;
- avoid force-moving published tags se isso prejudicar audit trail;
- produzir new version para correction quando possível.

## Licensing Gate

Antes de production/open distribution:

- project license decidida;
- dependency licenses inventariadas;
- vendor SDK redistribution reviewed;
- notices/attributions included;
- incompatible licenses blocked.

## Definition of Release-Ready

Um artifact só pode ser considerado release-ready para seu declared scope quando:

- source SHA conhecido e green;
- required tests green;
- security gates adequados ao milestone;
- package final smoke-tested;
- signature/checksum/SBOM disponíveis quando exigidos;
- docs/status/known limitations atualizados;
- hardware claims validados;
- no open blocker contradiz safety model.
