# ThermalOps

ThermalOps é uma plataforma Windows-first para **diagnóstico seguro, manutenção preventiva, field service, triagem, local remediation, Guided Operations, Lifecycle & Health, Self-Service, coleta de evidências, escalation assistance e futura gestão de fleet/condition monitoring de impressoras térmicas**.

O primeiro Vendor Adapter será Zebra. A arquitetura permanece intencionalmente vendor-neutral para permitir Honeywell, TSC, SATO e outros fabricantes sem espalhar vendor-specific rules pelo Domain.

> **Status do projeto:** M0 — fundações de produto, arquitetura, segurança, manutenção preventiva, field service, Lifecycle/Health, Guided Operations e Self-Service. Nenhuma capability física, native diagnostic action, remediation, preventive, Self-Service gerenciado, Fleet ou predictive feature deve ser considerada validada até cumprir os acceptance criteria, testes, source review e hardware validation previstos no roadmap.

![Visão conceitual do ThermalOps](docs/assets/thermalops-concept-overview.png)

> **Imagem conceitual.** A interface, versões, fabricantes, números, Health Score e textos mostrados são ilustrações da direção do produto, não evidência de funcionalidades já implementadas. A arte também pode conter termos promocionais ilustrativos que não representam status jurídico, de licenciamento, parceria ou certificação atual do projeto.

## Por que o ThermalOps existe

Em operações que dependem de impressoras térmicas, uma falha raramente pertence a uma única camada. O problema pode estar no Windows Print Subsystem, queue, job, driver, port, USB/PnP, network transport, configuração, consumível, firmware, estado físico reportado pelo equipamento, maintenance condition ou em algo que software sozinho não consegue observar.

Além de responder a incidentes, a operação precisa saber:

- o que está saudável agora;
- o que não pôde ser verificado;
- quanto o equipamento vem sendo usado quando counters existem;
- quais maintenance tasks estão due;
- quais componentes possuem warnings/observations;
- o que mudou em relação a baseline/history;
- qual próximo passo é seguro e aplicável ao modelo;
- quando o próprio end user pode resolver algo simples;
- quando o caso precisa virar ServiceCase e escalation.

O ThermalOps organiza essas evidências para responder, com rastreabilidade:

> **Qual é o estado desta impressora, o que pode ser tratado localmente com segurança e dentro da policy, o que deve ser apenas orientado, e o que precisa ser escalado?**

## Ciclo operacional

```text
ANTES DA FALHA
  -> Preventive Inspection
  -> MaintenancePolicy / MaintenanceTaskCatalog
  -> Lifecycle indicators / usage / baseline
  -> checklist / TechnicianObservation

DURANTE A FALHA
  -> Quick Diagnosis
  -> Advanced Diagnostics
  -> Guided Troubleshooting
  -> triage / least-impact Local Remediation

QUANDO O ESCOPO LOCAL TERMINA
  -> evidence
  -> ServiceCase
  -> escalation package
  -> optional Helpdesk connector

DEPOIS DA AÇÃO / MANUTENÇÃO
  -> verify
  -> before/after
  -> Return-to-Service checks
  -> report / history

ENTRE OCORRÊNCIAS (Enterprise)
  -> Fleet
  -> Health history
  -> ConditionTrend
  -> drift / alerts
  -> maintenance by exception
```

## Pilares do produto

```text
                              THERMALOPS
                                   |
      +------------+---------------+---------------+-------------+
      |            |               |               |             |
      v            v               v               v             v
 Diagnosis    Preventive        Guided          Support      Observability
              Maintenance       Operations      / Evidence   / Fleet
      |            |               |               |             |
      +------------+---------------+---------------+-------------+
                                   |
                         Lifecycle & Health
                                   |
                    +--------------+--------------+
                    |                             |
                    v                             v
              Self-Service                 Field Service
                                           / Escalation
```

### Diagnosis

Combina Windows, transport, vendor-native evidence e observações humanas sem reduzir tudo a `ONLINE/OFFLINE`.

### Preventive Maintenance

Usa tasks source-backed, baseline, counters quando suportados, configuration drift, maintenance history e TechnicianObservation. O ThermalOps não inventa intervals, replacement thresholds ou component lifetime.

### Guided Operations

Transforma evidence + capabilities + approved sources em troubleshooting guiado e verificável. Um `Runbook` pode pular passos já comprovados, solicitar verificação manual, recheckar o equipamento e encaminhar para typed actions seguras quando apropriado.

Runbooks são **data**, não scripts. Documentos, AI ou Knowledge Packs nunca podem criar arbitrary executable capability.

### Lifecycle & Health

Separa explicitamente:

```text
AssetAge
UsageMetrics
ComponentCondition
MaintenanceCompliance
CurrentHealth
ConditionTrend
RemainingLifeEstimate
```

`CurrentHealth` representa condição observável agora. `RemainingLifeEstimate`/RUL é prediction futura e permanece `Unavailable`/`NotValidated` até existir modelo validado para uma applicability class explícita.

### Local Remediation

`Repair` no projeto significa remediation local, restrita e autorizada — por exemplo, cancelar um job selecionado ou executar um controlled Spooler restart. Não significa assumir que todo técnico pode desmontar ou fazer bench repair.

### Support / Evidence

Cada Finding e recommendation relevante deve apontar para evidence. Diagnostic Report, Preventive Report, Support Bundle, GuidanceSession summary e ServiceCase preservam contexto para N1/N2/N3, assistência autorizada ou fabricante.

### Self-Service

Self-Service é um `ExperienceProfile`, não uma nova edição. O objetivo é permitir que um end user, em ambiente aprovado pela organização, veja status/Health, rode Quick Diagnosis, siga guided checks e prepare support evidence como standard user.

O objetivo **não** é contornar TI. Em ambientes com WDAC/App Control, AppLocker, EDR, firewall, proxy ou software catalog, ThermalOps deve ser aprovado/distribuído conforme a política da organização e depois operar dentro desse envelope.

### Observability / Fleet

A edição Enterprise poderá adicionar inventory, health/history, maintenance schedules, ConditionTrend, configuration drift, alerting, ServiceCase recurrence e maintenance by exception depois de ADRs específicos de persistence, authentication/RBAC, agent lifecycle e retention.

## Edições e Experience Profiles

| Edição | Uso principal | Persistência | Writes |
| --- | --- | --- | --- |
| **Portable Lite** | Field/N1/Self-Service read-only, diagnosis e preventive | Nenhuma intencional | Não; read-only por design |
| **Portable Pro** | Technician/N2/N3, field support e controlled remediation | Nenhuma intencional | Somente operations allowlisted, policy-gated e confirmadas |
| **Enterprise** | Managed Self-Service, Fleet, history, policies, schedules, integrations | Gerenciada | Controlado por policy/RBAC/capability |

Experience Profiles previstos:

```text
SelfService
Technician
AdvancedSupport
```

Eles compartilham o mesmo Domain/diagnostic engine. Muda progressive disclosure e effective capability surface; não existe um “diagnóstico simplificado” que possa contradizer o técnico.

## Portable Lite

Deve funcionar sem installer, sem .NET previamente instalado, sem login, sem internet obrigatória e sem UAC. Continua útil para:

- Quick Diagnosis;
- Advanced Diagnostics read-only;
- Guided Troubleshooting read-only;
- Knowledge Center offline quando pack aprovado existir;
- Preventive Inspection;
- Lifecycle/Health summary;
- baseline comparison;
- checklist;
- reports;
- evidence collection;
- ServiceCase preparation.

## Portable Pro

Adiciona Local Remediation e native diagnostic actions aprovadas. A UI permanece standard-user e eleva somente o **Temporary Privileged Helper** para a operation allowlisted específica que realmente exigir Windows elevation.

Printer-side writes também precisam de typed action, capability resolution, policy, impact preview e verification; não ficam automaticamente seguras só porque não exigem UAC.

## Enterprise

Pode adicionar:

- managed installation;
- managed Self-Service client;
- asset/user scope;
- optional SSO/organization identity;
- Fleet inventory/history;
- MaintenanceSchedule/history;
- HealthAssessment history;
- baselines/drift;
- alerting;
- ServiceDesk connectors;
- RBAC/audit/retention;
- optional least-privilege collector/agent.

Enterprise não pode transformar o Temporary Privileged Helper em um serviço irrestrito persistente.

## Evidence sources

### Windows print path

- Print Spooler state e configuração relevante;
- installed printers e target queue;
- jobs e estados de erro/stall;
- driver identity/version/package;
- ports e print processors;
- USB/PnP evidence;
- Windows Event Log;
- access denied, timeout, blocked e unavailable como first-class outcomes.

### Transport

Potential transport model:

```text
USB / DOT4
TCP/IP RAW
TCP/TLS
LPR
Windows Share
Bluetooth
Serial
Parallel
Browser/local bridge
Unknown
```

Known-endpoint reachability pode ser verificada quando policy permitir. ICMP nunca é prova de printer health.

### Vendor-native

No adapter Zebra, Link-OS, SGD, ZPL e outras interfaces suportadas podem fornecer, dependendo de model/firmware/connection:

- readiness;
- head state;
- media/ribbon state;
- pause;
- thermal warnings;
- device warnings/errors;
- firmware;
- counters/odometer;
- selected read-only configuration;
- diagnostic/self-test capabilities.

Windows queue status e physical-device status permanecem fontes distintas.

## Lifecycle, uso e vida útil

O ThermalOps pode coletar `UsageMetrics` quando a printer expõe counters oficialmente suportados. No ecossistema Zebra Link-OS, por exemplo, há APIs de odometer/counters que podem expor métricas como total print length e outros counters em printers compatíveis.

Isso **não** significa que todas as Zebra fornecem `OperatingHours`, `PowerOnHours`, vida útil da cabeça ou porcentagem de vida restante.

Correct representation:

```text
OperatingHours
collectionOutcome = Unsupported
```

em vez de:

```text
OperatingHours = 0
```

A vida útil restante só pode aparecer por `RemainingLifeEstimate` quando validada. Até lá, o produto mostra indicators defensáveis: CurrentHealth, Usage, MaintenanceDue, ComponentCondition, ManufacturerWarnings e ConditionTrend.

Detalhes: [Lifecycle e Health](docs/produto/lifecycle-e-health.md).

## Preventive Maintenance

A preventiva é uma capability de primeira classe:

```text
Automatic evidence
+ source-backed MaintenancePolicy
+ applicable MaintenanceBaseline
+ UsageMetrics quando suportados
+ TechnicianObservation / checklist
+ history
= MaintenanceFinding + recommendation + ServiceDisposition
```

`Unknown` não vira `NotDue`. Configuration drift é Finding, não proof de hardware fault. Numeric Health Score, se existir, é secondary, deterministic, versioned e explainable.

Detalhes: [Preventive Maintenance](docs/produto/manutencao-preventiva.md).

## Guided Troubleshooting e Knowledge Center

A Guidance layer resolve runbooks por:

```text
Vendor
Model/family
Firmware
Capability
Transport
Symptom/topic
Policy
Locale
Source/version
```

Example:

```text
Não imprime
  -> Windows queue = OK
  -> transport = OK
  -> Zebra native status = HeadOpen
  -> apresentar approved model-aware check
  -> recheck
  -> ReadyToPrint=true
  -> outcome Resolved
```

Nenhum reset/restart de Windows é executado se evidence já localizou uma condição física simples.

Knowledge pode vir de official links, local approved Knowledge Packs ou future online retrieval. Redistribution de vendor manuals depende de licensing; o repository não assume permissão para copiar PDFs inteiros.

Detalhes: [Guided Operations e Knowledge](docs/produto/guided-operations-e-knowledge.md).

## Native diagnostics e setup

Future Zebra Adapter pode mapear capabilities como configuration report, network report, print-quality report, communication diagnostics, sensor profile e calibration **somente onde a interface/model realmente suportar e depois de validation**.

Uma ação aparecer no painel/manual da printer não significa automaticamente que existe API programática equivalente para todos os models.

Cada action recebe `ActionSafetyClass`:

```text
Informational
GuidedManual
AssistedWrite
AutomatedLowRisk
HighImpact
ForbiddenInProfile
```

Calibration/test printing são write/state-change operations, mesmo quando não exigem administrator rights no Windows.

## Commissioning e Return-to-Service

Guided Operations prevê workflows futuros para:

```text
Commission new printer
  -> identify
  -> driver/queue/transport checks
  -> approved config/baseline
  -> calibration/test
  -> validate
  -> commissioning snapshot

Return from service
  -> re-identify physical device
  -> compare firmware/config/identity
  -> validate print path
  -> approved self-tests
  -> report differences
  -> ReturnToServiceReport
```

Nenhum baseline é automaticamente escrito de volta sem explicit plan/policy/verification.

## Self-Service

Self-Service default:

```text
Allowed:
Status
Quick Diagnosis
Health summary
Guided Troubleshooting
Knowledge Center
Preventive status
Sanitized evidence/report
ServiceCase draft

Denied by default:
Spooler restart
Driver install
Firmware update
Factory/network reset
Arbitrary config write
Advanced privileged actions
```

Em empresas com managed software distribution, ThermalOps pode ser aprovado uma vez e disponibilizado para standard users. Isso reduz fricção sem virar bypass de segurança.

Detalhes: [Self-Service / End-User Experience](docs/produto/self-service.md).

## ServiceCase e Helpdesk

Quando guidance não resolve:

```text
Diagnosis
 -> GuidanceSession
 -> NotResolved / EscalationRecommended
 -> sanitized ServiceCase draft
 -> privacy preview
 -> export or optional configured Helpdesk connector
```

Future connectors podem integrar com ServiceNow, Jira Service Management, Movidesk, Freshservice, Zendesk ou private organization APIs, mas o public core usa `IServiceDeskConnector` e não hard-code de URL, ticket schema, SLA, credentials ou employer rules.

## Segurança

ThermalOps é safety-sensitive support software. Guardrails centrais:

- read-only by default;
- least privilege;
- Self-Service standard-user-first;
- no arbitrary PowerShell/cmd/shell;
- no executable runbook scripts;
- no broad spool-folder deletion para selected job;
- no automatic broad network scan;
- no automatic customer-data upload;
- imported policy/baseline/knowledge pack é untrusted data;
- policy pode reduzir capability, nunca criar capability ausente;
- AI não autoriza action, maintenance due, ServiceDisposition ou RUL;
- writes seguem typed lifecycle + verification;
- Portable no intentional persistence;
- corporate controls são respeitados, nunca bypassados.

Veja [Security e Privacy](docs/seguranca/security-e-privacy.md) e o [Threat Model de Self-Service/Guided Operations](docs/seguranca/self-service-e-guided-operations-threat-model.md).

## Idioma e terminologia

Documentation e user-facing product são pt-BR-first, localization-ready. Código, schemas, Domain types, APIs e consolidated technical terms permanecem em inglês quando isso mantém precisão.

Examples:

```text
Domain
Application
Infrastructure
Adapter
Policy
Baseline
ServiceCase
ServiceDisposition
RepairPlan
HealthAssessment
GuidanceSession
Runbook
ExperienceProfile
Quick Diagnosis
Preventive Inspection
Spooler
WinSpool
PnP
Link-OS
SGD
ZPL
CI/CD
SBOM
RBAC
```

## Stack e arquitetura

Initial direction:

- C#;
- .NET 10 LTS;
- WPF;
- modular monolith;
- Domain/Application independentes de UI, Windows implementation, vendor SDK e AI;
- Windows Infrastructure com supported APIs;
- Vendor Adapters separados;
- Temporary Privileged Helper com IPC estrito;
- self-contained publishing para Portable;
- data-only Knowledge Packs;
- ExperienceProfile não usado como standalone authorization.

Veja [Arquitetura](docs/engenharia/arquitetura.md), [Guided Operations Architecture](docs/engenharia/guided-operations-architecture.md) e [ADRs](docs/adr/).

## Estrutura da documentação

```text
docs/
├── README.md
├── produto/
│   ├── visao-do-produto.md
│   ├── portable.md
│   ├── manutencao-preventiva.md
│   ├── lifecycle-e-health.md
│   ├── guided-operations-e-knowledge.md
│   ├── self-service.md
│   ├── field-service-e-escalation.md
│   ├── fleet-e-condition-monitoring.md
│   ├── ai-e-knowledge-assistance.md
│   └── localizacao-e-terminologia.md
├── engenharia/
│   ├── arquitetura.md
│   ├── guided-operations-architecture.md
│   ├── validation-matrix-lifecycle-guidance-self-service.md
│   ├── diagnostico-e-remediacao-local.md
│   ├── deployment-e-lifecycle.md
│   ├── support-bundles-e-service-cases.md
│   ├── testing.md
│   └── release-engineering.md
├── seguranca/
│   ├── security-e-privacy.md
│   └── self-service-e-guided-operations-threat-model.md
├── pesquisa/
│   └── referencias-e-padroes.md
├── planejamento/
│   └── roadmap.md
├── adr/
└── assets/
```

## Roadmap

| Milestone | Resultado principal |
| --- | --- |
| **M0** | Product/security/preventive/field-service/lifecycle/guidance/self-service foundations |
| **M1** | Read-only Windows Diagnosis + guidance primitives |
| **M2** | Safe Local Remediation |
| **M3** | Zebra native evidence/capability adapter |
| **M4** | Support + Preventive + Guided Operations suite |
| **M5** | Enterprise hardening + managed Self-Service/deployment integrations |
| **M6** | Fleet + Condition Monitoring + Health history |
| **M7** | Multi-vendor adapters |
| **M8** | Knowledge / AI assistance |
| **M9** | Predictive-maintenance/RUL research, não promised feature |

Veja o [Roadmap completo](docs/planejamento/roadmap.md).

## Engineering Constitution

Toda implementação segue [ENGINEERING_CONSTITUTION.md](ENGINEERING_CONSTITUTION.md). A Constitution define business/domain correctness, safety/security, authorization/privacy, reliability, maintainability, testing, observability, UX/accessibility, supply chain, documentation governance e honest status.

## Licença

A licença do projeto ainda não foi selecionada. Source publicamente visível não é automaticamente reusable. Não copiar third-party implementation nem redistribuir vendor documentation/SDK sem license/redistribution review explícita.
