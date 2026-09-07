# Deployment e Application Lifecycle

ThermalOps possui dois deployment models fundamentalmente diferentes:

- **Portable** — sem installer e sem persistent agent;
- **Enterprise** — managed installation com persistence controlada para fleet/history.

Deployment simplicity é product requirement, não packaging cleanup de última hora.

## Portable Experience Contract

Do approved package até o primeiro read-only diagnosis, o técnico não deve precisar instalar dependencies manualmente.

Target flow:

```text
Approved package / USB / local copy
  -> start ThermalOps
  -> select target / Quick Diagnosis
  -> inspect / diagnose / report
```

Goals:

- no installer;
- self-contained runtime;
- no account required;
- no internet required;
- no CLI required for normal use;
- no reboot;
- no persistent service/daemon;
- no permanent registry/startup/task persistence;
- no automatic write to removable media;
- signed publisher identity quando production signing existir.

Uma future performance target como menos de 60 segundos entre launch e começo do primeiro diagnosis pode ser usada internamente, mas não deve virar claim sem benchmark real.

## Portable Package

Preferred layout:

```text
ThermalOps-Portable-<version>-win-x64.zip
├── ThermalOps.exe
├── checksums.sha256
├── SBOM.spdx.json
├── release-notes.md
├── README.txt
└── SECURITY.txt
```

Single-file é optional, não um requirement absoluto.

Decision factors:

- native dependency loading;
- vendor SDK compatibility;
- helper extraction/verification;
- Authenticode behavior;
- endpoint security;
- startup performance;
- diagnostics/troubleshooting;
- forensic clarity.

## Target Architectures

Initial direction:

- `win-x64` primary;
- `win-arm64` after real validation;
- `win-x86` only for demonstrated requirement.

Support claim exige:

- build success;
- automated tests;
- runtime smoke test;
- vendor/native compatibility quando aplicável;
- known limitations documented.

## Enterprise Packaging Decision

Packaging technology é deliberadamente undecided até M5 ADR.

Candidates podem incluir MSI, MSIX ou outra abordagem adequada, mas a seleção deve avaliar requirement real em vez de preferência estética.

O ADR precisa comparar pelo menos:

- enterprise manageability;
- silent install/uninstall;
- repair/upgrade semantics;
- Windows service support se necessário;
- offline deployment;
- signing;
- rollback/recovery;
- app data retention;
- compatibility com Intune/Configuration Manager;
- endpoint-security behavior;
- installer logs/exit codes;
- complexity/maintenance.

## Enterprise Deployment Contract

Independentemente da tecnologia escolhida, o produto deve suportar:

- interactive install;
- silent/unattended install;
- silent/unattended uninstall;
- offline deployment;
- predictable exit codes;
- support-quality install logs;
- upgrade in place;
- migration strategy;
- rollback/recovery strategy;
- clean uninstall;
- explicit configuration/history retention behavior;
- signed binaries/package;
- no-reboot normal path quando tecnicamente possível.

## Corporate Distribution

ThermalOps não precisa implementar lógica específica dentro do app para cada deployment platform.

O package deve ser standards-compatible o suficiente para distribuição por:

- Microsoft Intune;
- Microsoft Configuration Manager/SCCM;
- enterprise software distribution;
- offline software repositories;
- manual authorized installation.

Documentation futura deve fornecer:

- install command;
- silent flags;
- uninstall command;
- detection rule guidance;
- expected exit codes;
- required privileges;
- disk requirements;
- network behavior;
- persistence behavior;
- reboot semantics.

## No-Reboot Goal

Core ThermalOps install/upgrade/uninstall não deve exigir reboot em normal path.

Se future third-party component criar reboot requirement:

- detectar/reportar;
- explicar origem;
- nunca restart automaticamente sem explicit policy/confirmation;
- distinguir ThermalOps requirement de external dependency requirement;
- definir exit code indicando reboot pending quando necessário.

## Install Privileges

Portable:

- standard-user para read-only usage;
- UAC somente para Pro remediation action específica.

Enterprise installer:

- pode exigir admin para machine-wide installation;
- installed app não deve operar permanentemente elevated;
- service/agent identity, se existir, usa least privilege;
- installer privilege não justifica runtime unrestricted privilege.

## Directory Layout

Final layout depende do packaging ADR, mas principles incluem:

- binaries em standard application location;
- machine config separada de user/session temp;
- logs com retention/security definidos;
- no customer data misturada com executable files;
- signed binaries não são modificados em runtime;
- update staging separado e validado.

## Configuration Ownership

Documentar claramente quais artifacts pertencem ao ThermalOps:

- app configuration;
- policy cache;
- baseline cache;
- agent config;
- database;
- logs;
- update metadata;
- user preferences.

Uninstall só remove owned resources conforme retention choice.

## Upgrade Behavior

Enterprise upgrade deve preservar somente persistent state documentado, como:

- policies;
- approved baselines;
- maintenance history;
- device inventory/history;
- audit metadata;
- compatible service configuration;
- user preferences quando apropriado.

## Schema Migrations

Persistent schema migration precisa ser:

- versioned;
- forward-tested;
- logged;
- failure-safe;
- backup-aware;
- idempotent quando apropriado;
- reversible quando prático;
- explicitamente irreversible quando não houver rollback.

Não atualizar binaries primeiro e “torcer” para migration funcionar.

Safer sequence conceitual:

```text
Preflight
 -> verify package/signature
 -> backup durable state if needed
 -> stop owned service safely
 -> migrate/stage
 -> switch version
 -> start
 -> verify health
 -> cleanup old version
```

Exact sequence depende do package/architecture ADR.

## Rollback

Rollback strategy deve definir:

- quais versions suportam downgrade;
- schema compatibility;
- backup location;
- service binary rollback;
- config version handling;
- operator messaging;
- what happens after partial upgrade;
- when manual intervention is required.

Não declarar rollback support sem testá-lo.

## Uninstall

Clean uninstall remove ThermalOps-owned:

- app binaries;
- installed services/agents;
- scheduled tasks;
- startup registrations;
- machine/user config definida como disposable;
- update components;
- temp/staging files.

History/database/report retention deve ser explicit installer/admin choice quando legal/operational requirements exigirem.

Uninstall não remove:

- unrelated customer files;
- arbitrary report folders;
- printer drivers que não foram explicitamente instalados/owned pelo ThermalOps;
- vendor software alheio;
- customer documents.

## Installer Repair Mode

Se packaging technology suportar “repair installation”, o termo significa reparar a instalação do ThermalOps.

Não confundir com printer repair/local remediation.

## Offline Networks

Core package installation não depende de download externo para funcionar.

Não exigir on-demand download de:

```text
.NET runtime
vendor dependency
application files
license bootstrap
cloud agent
```

Se optional feature exigir external download/service, isso deve ser separável e claramente documentado.

## Proxy e Restricted Networks

Future Enterprise network features devem respeitar:

- proxy config;
- firewall rules;
- no direct internet assumption;
- offline mode;
- certificate inspection environments quando suportável;
- explicit endpoints documentation.

Core field operation continua offline.

## Signing e Allowlisting

Production releases usam Authenticode quando signing identity estiver disponível.

Security teams devem conseguir verificar:

- publisher;
- product name;
- version;
- source commit/build ID;
- architecture;
- SHA-256;
- signature status;
- SBOM;
- expected network behavior;
- expected persistence;
- privileges;
- update mechanism.

ThermalOps coopera com Defender, EDR/XDR, WDAC, AppLocker e application/removable-media controls.

## Update Strategy

No silent self-update nas early versions.

Future updater exige ADR cobrindo:

- signed update manifests;
- signature verification;
- trusted root/key rotation;
- channel selection;
- enterprise deferral;
- offline mirrors;
- proxy behavior;
- atomicity;
- rollback;
- downgrade policy;
- compromised signing key response;
- failure recovery;
- audit.

Early defaults:

- Portable: manual artifact replacement;
- Enterprise: managed deployment.

## Update Channels

Possible future channels:

```text
dev
preview
stable
```

Channel label representa validation level, não marketing.

Enterprise policy pode pin/deferral version quando updater existir.

## Install/Upgrade Observability

Install lifecycle deve produzir logs úteis sem customer secrets.

Potential events:

```text
InstallStarted
PrerequisiteCheckFailed
PackageSignatureVerified
ServiceInstalled
MigrationStarted
MigrationCompleted
UpgradeVerificationFailed
RollbackStarted
UninstallCompleted
RebootRequired
```

Exit codes devem ser documentados.

## Lifecycle Security

Threats incluem:

- package tampering;
- DLL/native dependency hijack;
- untrusted upgrade source;
- path traversal in extracted package;
- unsafe temp permissions;
- privileged custom action abuse;
- downgrade to vulnerable version;
- unsigned helper replacement;
- service binary replacement;
- malicious config migration input.

Controls entram no packaging ADR/security review.

## Lifecycle Tests

Release qualification futura inclui:

### Portable

- launch em clean supported Windows VM;
- no-runtime-preinstalled;
- offline launch;
- no-persistence before/after;
- blocked-by-policy behavior;
- signature verification;
- export/cleanup failure.

### Enterprise

- clean install;
- silent install;
- silent uninstall;
- install from offline source;
- N-1 -> N upgrade;
- failed migration;
- rollback/recovery;
- policy/baseline/history preservation;
- uninstall cleanup;
- corrupted package;
- invalid signature;
- blocked by WDAC/AppLocker scenario quando test environment permitir;
- no-reboot normal path.

## Definition of Done para M5 Packaging

Não considerar packaging “feito” apenas porque setup abre.

Precisa existir:

- ADR aceito;
- automated/smoke lifecycle tests;
- security review;
- signing flow;
- install/uninstall docs;
- offline behavior;
- upgrade/recovery behavior;
- known limitations;
- enterprise deployment guidance;
- clean rollback/cleanup evidence.
