# Visão do Produto

## Missão

ThermalOps reduz downtime, ambiguidade de suporte e risco operacional em ambientes Windows com impressoras térmicas ao combinar:

- Windows print-subsystem evidence;
- transport evidence;
- vendor-native evidence;
- Preventive Inspection e MaintenancePolicy;
- TechnicianObservation;
- safe local remediation;
- Support Bundle e ServiceCase;
- escalation assistance;
- futura Fleet/Condition Monitoring.

O produto complementa ERP/WMS, label-design/printing software, vendor management suites e authorized repair organizations. Ele não pretende substituir essas categorias.

## Problema que o produto resolve

Uma falha de impressão pode parecer simples na ponta, mas a causa pode estar em várias camadas:

```text
Application / ERP / WMS
        |
        v
Windows queue / job
        |
        v
Driver / port / print processor
        |
        v
Transport
        |
        v
Printer firmware / configuration / physical state
        |
        v
Consumables / maintenance / hardware condition
```

Sem coleta estruturada, é comum haver troubleshooting baseado em tentativa e erro, reinícios amplos, perda de contexto entre N1/N2/N3 e dificuldade de demonstrar por que uma ação foi tomada.

ThermalOps procura substituir esse comportamento por evidence-driven support.

## Jobs-to-be-done

### Antes da falha

O usuário deve conseguir:

- executar Preventive Inspection;
- coletar firmware, counters e configuration quando suportado;
- comparar contra MaintenanceBaseline aplicável;
- detectar maintenance due, configuration drift e warnings recorrentes;
- seguir checklist físico/manual apropriado;
- registrar TechnicianObservation separadamente de automatic evidence;
- gerar Preventive Report;
- decidir se a impressora continua em serviço, requer observação ou precisa de escalation.

### Durante um incident

O usuário deve conseguir:

- identificar se o problema está em Windows, queue/job, driver, port, transport, vendor-native state, configuration ou se há insufficient evidence;
- enxergar exatamente a evidence que sustenta uma Finding;
- receber least-impact recommended next step;
- executar apenas local remediation autorizada por policy;
- verificar o resultado por post-condition;
- evitar broad/reset actions quando uma ação narrow resolver o problema.

### Quando o escopo local termina

O usuário deve conseguir:

- registrar findings e actions attempted;
- registrar ServiceDisposition;
- preparar ServiceCase/escalation package;
- preservar evidence para N2/N3, authorized service ou vendor support;
- exportar somente o nível de dados autorizado;
- não ser forçado a executar repair antes de escalar.

### Depois da ação

O usuário deve conseguir:

- comparar before/after;
- confirmar se o post-condition realmente foi atingido;
- distinguir `Verified`, `Partial`, `Failed` e recovery outcome;
- gerar relatório técnico;
- preservar histórico na edição Enterprise conforme retention policy.

### Em uma fleet

O Enterprise deve futuramente permitir:

- inventory;
- maintenance scheduling/history;
- baselines;
- configuration drift;
- condition trends;
- recurring failure/service-case analysis;
- explainable alerting;
- maintenance by exception;
- policy enforcement;
- RBAC/audit/retention.

## Personas

### Field / N1 Technician

Precisa de workflow rápido, seguro e com pouca ambiguidade.

Principais necessidades:

- abrir o Portable sem instalação;
- selecionar ou descobrir o target autorizado;
- executar Quick Diagnosis;
- realizar Preventive Inspection;
- entender o provável fault layer;
- seguir guided checks;
- executar apenas ação local de baixo risco quando permitida;
- preparar escalation e relatório.

### N2/N3 Support Analyst

Precisa de detalhe técnico suficiente para investigação profunda:

- raw/normalized evidence;
- WinSpool details;
- Event Log;
- driver/port/print processor;
- vendor protocol status;
- configuration/counters;
- snapshot diff;
- RepairPlan;
- ServiceCase;
- support bundle;
- policy/rule versions;
- timeline completa.

### Preventive Maintenance Technician

Precisa de inspeção repetível e auditável:

- MaintenanceTaskCatalog aplicável;
- source-backed due rules;
- checklist manual;
- baseline comparison;
- usage/counter evidence;
- HealthAssessment explicável;
- Preventive Report;
- follow-up/disposition.

### Enterprise/Fleet Operator

Precisa saber onde agir, sem abrir centenas de dispositivos individualmente:

- inventory;
- attention queues;
- due/overdue maintenance;
- configuration drift;
- alert lifecycle;
- recurring failure patterns;
- baselines/policies;
- audit history.

### Customer Security / IT

Precisa de comportamento previsível:

- signed publisher;
- known hash/build identity;
- no hidden persistence;
- no automatic upload;
- no automatic broad scan;
- clear privilege model;
- exact list of privileged capabilities;
- offline operation;
- clean uninstall para Enterprise;
- compatibility com WDAC/AppLocker/EDR.

### Authorized Service / Vendor Support Recipient

Precisa receber um caso estruturado, não uma descrição vaga:

- model/device identity quando autorizado;
- firmware;
- status;
- counters/configuration;
- Windows/transport evidence;
- actions attempted;
- TechnicianObservation;
- preventive findings;
- ServiceDisposition;
- manifest/hash/schema metadata.

## Edições

### Portable Lite

Objetivo: field/N1/preventive read-only.

Características:

- self-contained Windows package;
- no installer;
- no preinstalled .NET runtime;
- no UAC/helper path;
- permanently read-only;
- Quick Diagnosis;
- Advanced Diagnostics read-only;
- Preventive Inspection;
- Technician checklist;
- MaintenanceBaseline import/compare/export quando permitido;
- sanitized reports;
- ServiceCase evidence collection;
- Customer Safe semantics.

### Portable Pro

Tudo do Lite, mais:

- explicit RepairPlan/local-remediation workflows;
- Temporary Privileged Helper;
- selected-job cancellation;
- controlled Spooler restart;
- approved queue remediation;
- diagnostic print quando permitido;
- full technical bundle;
- richer ServiceCase;
- additional vendor-native diagnostics quando capability/policy permitir.

Portable Pro continua sem persistent service/agent.

### Enterprise

Planned only after dedicated ADRs.

Capabilities candidatas:

- managed installation;
- persistent inventory/history;
- MaintenanceSchedule e history;
- configuration baselines/drift;
- HealthAssessment history;
- condition trends;
- alerting;
- ServiceCase history;
- fleet policies;
- RBAC/audit;
- retention;
- optional managed collector/agent;
- dashboard.

## Main workflows

### Quick Diagnosis

Read-only, one-click ou guided collection focada em:

- Windows print subsystem;
- driver;
- queue/jobs;
- transport;
- PnP/USB;
- vendor-native status quando disponível.

Output esperado:

- Findings priorizadas por relevância/impact;
- evidence view;
- likely fault layer;
- least-impact recommendation;
- explicit `InsufficientEvidence` quando não houver dados suficientes.

### Advanced Diagnostics

Expõe detalhes de:

- WinSpool;
- print processors;
- drivers/driver store;
- ports;
- PnP;
- SCM/Spooler;
- Event Log;
- known endpoint checks;
- Link-OS/SGD/ZPL ou equivalente;
- firmware;
- counters;
- selected configuration.

### Preventive Inspection

```text
Collect automatic evidence
+ apply source-backed MaintenancePolicy
+ load applicable MaintenanceBaseline/history
+ guide technician checklist
+ derive MaintenanceFinding
+ determine ServiceDisposition
+ generate Preventive Report
```

### Analyze Failure

Guided triage que mantém separado:

```text
Observation -> Finding -> Recommendation -> Action -> Verification
```

### Collect Evidence

Permite preparar relatório/support package sem alterar o endpoint.

### Prepare Escalation

Cria ServiceCase/escalation package quando o problema ultrapassa field scope.

### `--readonly`

Hard guardrail. Não é somente UI state.

State-changing methods devem ser unreachable por design, mesmo se o processo estiver sendo executado por administrador.

### Customer Safe

Profile com máxima previsibilidade:

- read-only;
- no diagnostic print;
- no automatic network discovery;
- no telemetry;
- no upload;
- no printer/system writes;
- local evidence first.

## Health UX

A apresentação principal deve ser component-based e explicável:

```text
Overall condition: ATTENTION RECOMMENDED

Device.................. OK
Windows................. OK
Transport............... Observation
Configuration........... Drift
Maintenance............. DueSoon
Evidence completeness... 91%
```

Se um numeric Health Score for introduzido:

- é secundário;
- é deterministic;
- é versioned;
- cada contribution é visível;
- missing evidence não recebe valor “bom” por default;
- scores de populations incompatíveis não são comparados cegamente;
- AI não calcula a autoridade final.

## Baselines e Configuration Drift

`MaintenanceBaseline` é uma reference/approved state, não a verdade universal.

Deve ter applicability suficiente, como:

- vendor;
- model/family;
- DPI;
- media/application context;
- firmware range;
- connection context;
- site/policy profile;
- schema version.

A UI mostra current vs baseline, source, difference, severity, acknowledgement e recommendation.

## Diagnostic Label

Quando permitido, uma test label pode ajudar a separar software/transport de print-quality issues.

Pode incluir:

- session ID;
- model/DPI;
- timestamp;
- barcode/QR samples;
- line-width patterns;
- alignment markers;
- darkness/calibration patterns.

É uma write operation e deve ser impossible em `--readonly`/Customer Safe.

A avaliação visual continua sendo TechnicianObservation.

## ServiceCase

Um `ServiceCase` pode incluir:

- target identity;
- case type;
- problem summary;
- evidence IDs;
- Findings;
- TechnicianObservation;
- actions attempted/results;
- Preventive Inspection reference;
- ServiceDisposition;
- policy version;
- attachments;
- privacy level;
- manifest/build/schema metadata.

Direct vendor/RMA submission não é early requirement.

## Policies

Policy pode **reduzir** ou **restringir** capability; não pode habilitar algo que o build não implementa.

Exemplo conceitual:

```json
{
  "allowNetworkDiscovery": false,
  "allowDiagnosticPrint": true,
  "allowSpoolerRestart": true,
  "allowQueueRepair": true,
  "allowDriverInstall": false,
  "allowFirmwareUpdate": false,
  "allowFullTechnicalExport": true,
  "allowRemoveFromServiceDisposition": false
}
```

Maintenance schedules/tasks são versionados separadamente e preservam source/applicability.

## Localization

A UI é pt-BR-first, mas localization-ready.

User-facing wording pode ser localizado. Domain names, schemas, internal event types e contracts permanecem em inglês para estabilidade técnica.

## Non-goals dos primeiros milestones

- substituir label-design/print automation suite;
- substituir ERP/WMS;
- virar general Windows repair utility;
- arbitrary script execution;
- physical printer disassembly workflow genérico;
- automatic parts replacement decision;
- automatic firmware flashing;
- automatic driver replacement;
- mandatory cloud/login;
- autonomous AI remediation;
- broad unattended network scan;
- automatic vendor/RMA submission;
- predictive failure claim sem dataset/validation.

## Critério de valor

ThermalOps deve ser melhor em **trustworthy diagnosis, preventive inspection, evidence quality, safe local remediation, deployment simplicity e escalation handoff** antes de tentar competir em breadth com grandes suites de gerenciamento.
