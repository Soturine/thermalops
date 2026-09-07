# Portable

Portable operation é um requisito central do ThermalOps para diagnosis, Preventive Inspection, field triage, evidence collection, reporting e controlled local remediation.

A edição Portable não é “a versão instalada copiada para um pendrive”. Ela possui contrato próprio de lifecycle, privilege, storage, cleanup e privacy.

## Objetivos

Um técnico deve conseguir:

1. receber um artifact aprovado/assinado;
2. executá-lo em um supported Windows endpoint autorizado;
3. diagnosticar sem installer;
4. executar Preventive Inspection sem installer;
5. permanecer read-only no Lite;
6. elevar somente uma ação específica no Pro quando necessário;
7. preparar ServiceCase/escalation sem ser obrigado a reparar;
8. exportar somente os dados escolhidos;
9. sair e não deixar intentional persistence.

## Portable Lite

Portable Lite é permanentemente read-only.

Use cases planejados:

- Quick Diagnosis;
- Advanced Diagnostics read-only;
- Preventive Inspection;
- Technician checklist;
- source-backed MaintenanceDue;
- MaintenanceBaseline import/compare/export quando permitido;
- configuration drift view;
- ServiceDisposition;
- Prepare Escalation;
- sanitized diagnostic/preventive reports;
- ServiceCase evidence collection.

Não existe helper/UAC/write path no Lite.

Isso deve ser enforceado em Application/Domain capability policy, não apenas por esconder buttons.

## Portable Pro

Inclui tudo do Lite e adiciona capabilities de local remediation aprovadas:

- selected-job cancellation;
- controlled Spooler restart;
- approved queue remediation;
- diagnostic print;
- full technical Support Bundle;
- richer ServiceCase;
- additional vendor-native diagnostic operations quando permitidas.

O Pro continua standard-user durante diagnosis/inspection. UAC aparece somente quando a selected RepairAction realmente exigir elevation.

## Packaging

Layout de referência:

```text
ThermalOps-Portable-<version>-win-x64.zip
├── ThermalOps.exe
├── checksums.sha256
├── SBOM.spdx.json
├── release-notes.md
├── README.txt
└── SECURITY.txt
```

Um single-file executable é desejável somente se não piorar:

- runtime reliability;
- vendor-native SDK compatibility;
- native library loading;
- Authenticode;
- helper extraction/verification;
- endpoint-security compatibility;
- startup time;
- troubleshooting/forensic clarity.

Se um pequeno signed multi-file directory for mais seguro/confiável, esse trade-off deve ser documentado por ADR.

## Runtime

Use self-contained .NET publishing para que o target machine não precise de preinstalled .NET runtime.

Targets iniciais:

- `win-x64` — primary;
- `win-arm64` — somente após real compatibility/testing;
- `win-x86` — somente se existir demonstrated support requirement.

“Builda” não significa “supported”. Cada target precisa de test coverage e vendor/hardware validation relevante.

## Experiência de uso

Normal usage não deve exigir:

- installer;
- terminal/CLI;
- dependency setup;
- login;
- internet;
- reboot;
- manual environment variables;
- persistent service.

Target UX conceitual:

```text
Approved package / USB / local copy
  -> start ThermalOps
  -> select target / Quick Diagnosis
  -> inspect / diagnose / report
```

Uma meta futura pode ser menos de 60 segundos entre launch e início do primeiro diagnosis em um endpoint normal, mas isso só vira claim depois de benchmark real.

## Session storage

Nunca escrever customer data automaticamente no removable media.

Default session root:

```text
%TEMP%\ThermalOps\Sessions\<session-id>\
```

A sessão pode conter temporariamente:

- normalized evidence;
- snapshots;
- checklist state;
- maintenance calculation inputs;
- temporary logs;
- bundle staging;
- attachment staging explicitamente selecionado.

## Cleanup

No clean exit:

- encerrar helper;
- fechar IPC;
- remover session temp files criados pelo ThermalOps quando possível;
- remover temporary executable copies próprias quando aplicável;
- reportar cleanup failures;
- preservar explicit exports escolhidos pelo operador.

Não prometer forensic secure erase se NTFS/SSD/OS não permite garantia.

## `--readonly`

`ThermalOps.exe --readonly` é hard guardrail.

Ações impossíveis:

- helper launch/UAC;
- cancel job;
- service control;
- queue reset;
- printer config write;
- arbitrary ZPL/SGD write;
- diagnostic print;
- driver install/remove;
- firmware action;
- qualquer new write capability que não tenha explicit read-only exclusion test.

Mesmo se o usuário executar o app como Administrator, `--readonly` continua read-only.

## Customer Safe

Customer Safe é um profile operacional mais restritivo para ambientes sensíveis.

Defaults:

- read-only;
- no telemetry;
- no upload;
- no automatic network scan;
- no printer writes;
- no system writes;
- no diagnostic print;
- local evidence first;
- explicit operator enablement para checks adicionais permitidos.

Portable Lite pode adotar Customer Safe semantics como default permanente.

## Baselines e Previous Inspections

Portable não mantém hidden customer history.

O operador pode explicitamente:

- importar MaintenanceBaseline sanitizado;
- importar previous-inspection snapshot;
- exportar baseline/snapshot;
- comparar current vs baseline;
- descartar tudo ao final.

Imported data é untrusted:

- schema/version validation;
- file-size limits;
- compatibility/applicability check;
- no embedded code;
- nunca habilita executable capability ausente.

Uma future signed policy/baseline package pode ser usada em ambientes controlados após ADR/security design.

## Temporary Privileged Helper

Fluxo conceitual:

```text
ThermalOps.exe (standard user)
        |
        | operator selects RepairPlan
        | explicit confirmation
        v
UAC
        |
        v
Temporary Privileged Helper
        |
        +-- exactly one allowlisted capability
        |
        v
post-condition validation
        |
        v
helper exit / cleanup
```

O helper não oferece:

- terminal;
- script engine;
- arbitrary executable launch;
- generic registry write;
- arbitrary file delete;
- generic service control;
- `ExecuteCommand(string)`.

## Endpoint controls

Assumir que customer endpoints podem usar:

- Microsoft Defender;
- EDR/XDR;
- AppLocker;
- WDAC;
- Controlled Folder Access;
- removable-media controls;
- application allowlisting;
- privilege-management products.

ThermalOps deve cooperar com esses controles, nunca bypassá-los.

Se policy corporativa bloquear execução, o produto deve falhar de forma clara e não sugerir bypass.

## Signing e identity

Production artifacts devem expor quando disponível:

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
Known network behavior
Known persistence behavior
```

Publisher-based allowlisting é preferível a depender de novos unsigned hashes a cada release.

## Offline behavior

Core functionality deve permanecer disponível com:

```text
Internet: unavailable
Cloud API: unavailable
Account: unavailable
```

Inclui:

- Windows diagnosis;
- local printer discovery;
- supported vendor-local status;
- Preventive Inspection;
- local baseline compare;
- policy-permitted remediation;
- timeline;
- reports;
- ServiceCase generation.

Optional AI/cloud failure não pode bloquear deterministic workflows.

## Export choices

Ao encerrar uma sessão:

```text
[Descartar sessão]
[Exportar relatório sanitizado]
[Exportar Preventive Report]
[Exportar full technical bundle]
[Exportar ServiceCase / escalation package]
```

Full/identity-bearing export exige privacy preview/warning explícito.

## No-persistence E2E

Antes/depois de um clean exit, validar:

- nenhum ThermalOps service instalado;
- nenhuma scheduled task;
- nenhuma Run/Startup entry;
- nenhum helper process;
- nenhum IPC endpoint esperado;
- nenhuma unexpected session directory;
- nenhum app-owned persistent registry state;
- nenhum log ao lado do executable/USB sem explicit export.

## Failure scenarios

Portable deve tratar corretamente:

- temp directory unavailable;
- disk full;
- file locked during cleanup;
- UAC denied;
- helper crash;
- customer policy blocks executable;
- vendor SDK missing/incompatible;
- imported baseline corrupt;
- export target unavailable;
- USB removal during explicit export.

## Relação com Enterprise

Portable nunca depende do backend Enterprise para executar core field workflows.

Enterprise pode reutilizar Domain/Application/adapters, mas persistence/agent/API/authentication são boundaries adicionais definidos separadamente.

Veja `../engenharia/deployment-e-lifecycle.md` para install/upgrade/uninstall da edição gerenciada.
